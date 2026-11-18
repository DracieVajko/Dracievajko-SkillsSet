#!/usr/bin/env python3
"""Build the one shared collection from every machine snapshot.

Reads `sync/machines/*.json` (raw evidence written by `generate-manifest.py`)
and `sync/cindy-plugins.json`, then writes three files that are identical on
every computer:

    sync/collection.json   the collection: every skill and plugin, how it
                           installs, which agents see it, where it was seen
    sync/manifest.json     the same collection in the schema
                           `scripts/sync-skills.ps1` installs from
    sync/unresolved.md     skills without a verified upstream

The merge is monotonic: a skill already in `collection.json` is never dropped
just because one machine snapshot is missing or older. A computer therefore
only adds its own evidence file and cannot overwrite the shared collection.

Usage
    python sync/build-collection.py
    python sync/build-collection.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

SYNC_DIR = Path(__file__).resolve().parent
MACHINES_DIR = SYNC_DIR / "machines"
COLLECTION = SYNC_DIR / "collection.json"
MANIFEST = SYNC_DIR / "manifest.json"
UNRESOLVED = SYNC_DIR / "unresolved.md"
PLUGINS = SYNC_DIR / "cindy-plugins.json"
GENERATED_AT = "2026-11-18"

# A skill installed in one of these roots is visible to these harnesses.
VISIBILITY = {
    "opencode": ["opencode", "agents", "cindy", "claude", "pi", "qwen"],
    "agents": ["agents", "cindy", "claude", "pi", "qwen", "continue", "roo"],
}

INSTALL_TARGETS = {
    "opencode": "~/.config/opencode/skills",
    "agents": "~/.agents/skills",
    "claude": "~/.claude/skills",
    "pi": "~/.pi/agent/skills",
    "qwen": "~/.qwen/skills",
    "cindy": "Cindy app: skills from ~/.agents/skills, plugins from sync/cindy-plugins.json",
    "opendesign": "OpenDesign: the opendesign-trial Cindy plugin plus prompts/system/opendesign-ui-code-audit.md",
}

AUTHORSHIP_RANK = {"original": 3, "third-party": 2, "unknown": 1}
TYPE_RANK = {"repo": 3, "github": 2, "unresolved": 1}
METHOD = {
    "repo": "repository-copy",
    "github": "git-sparse-checkout",
    "unresolved": "manual",
}


def load_machines() -> dict[str, dict]:
    """Return {machineId: snapshot} for every stored machine snapshot."""
    machines: dict[str, dict] = {}
    if not MACHINES_DIR.is_dir():
        return machines
    for path in sorted(MACHINES_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        machine_id = data.get("machineId") or path.stem
        machines[machine_id] = data
    return machines


def load_existing() -> dict:
    if not COLLECTION.is_file():
        return {}
    try:
        return json.loads(COLLECTION.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def repo_hash(source: dict) -> str:
    """Hash a repository copy, so repo skills never report false upstream drift."""
    path = source.get("path")
    if source.get("type") != "repo" or not path:
        return ""
    skill_md = SYNC_DIR.parent / path / "SKILL.md"
    if not skill_md.is_file():
        return ""
    raw = skill_md.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def load_catalog_sources() -> dict[str, dict]:
    """name -> upstream source for every link-only catalog record."""
    path = SYNC_DIR.parent / "catalog" / "items.json"
    if not path.is_file():
        return {}
    sources = {}
    for item in json.loads(path.read_text(encoding="utf-8")):
        if item.get("authorship") != "link-only" or not item.get("repository"):
            continue
        repo = item["repository"].rstrip("/").split("github.com/")[-1]
        folder = item.get("path") or ""
        if folder == "SKILL.md":
            folder = "."
        elif folder.endswith("/SKILL.md"):
            folder = folder[: -len("/SKILL.md")]
        sources.setdefault(
            item["name"],
            {
                "type": "github",
                "repo": repo,
                "ref": item.get("branch") or "main",
                "path": folder,
            },
        )
    return sources


def merge() -> tuple[dict[str, dict], set[str], dict[str, set[str]]]:
    """Merge existing collection and every snapshot without losing anything."""
    machines = load_machines()
    existing = load_existing()
    skills: dict[str, dict] = {}
    known_machines: set[str] = set(existing.get("machines", []))
    app_managed: dict[str, set[str]] = {
        key: set(value) for key, value in (existing.get("appManaged") or {}).items()
    }

    def slot(name: str) -> dict:
        return skills.setdefault(
            name,
            {
                "authorship": "unknown",
                "source": {"type": "unresolved", "repo": None, "ref": None, "path": None},
                "installRoot": "opencode",
                "author": "",
                "license": "",
                "needsNodeModules": False,
                "hashes": {},
                "machines": set(),
            },
        )

    for entry in existing.get("skills", []):
        item = slot(entry["name"])
        item["authorship"] = entry.get("authorship", item["authorship"])
        item["source"] = entry.get("source") or item["source"]
        item["installRoot"] = (entry.get("install") or {}).get(
            "root", item["installRoot"]
        )
        item["author"] = entry.get("author", item["author"])
        item["license"] = entry.get("license", item["license"])
        item["needsNodeModules"] = entry.get(
            "needsNodeModules", item["needsNodeModules"]
        )
        hashes = entry.get("sha256") or {}
        if isinstance(hashes, str):
            hashes = {}
        item["hashes"].update({k: v for k, v in hashes.items() if v})
        item["machines"].update(entry.get("machines", []))

    for machine_id in sorted(machines):
        snapshot = machines[machine_id]
        known_machines.add(machine_id)
        for entry in snapshot.get("skills", []):
            name = entry["name"]
            item = slot(name)
            item["machines"].add(machine_id)
            if entry.get("sha256"):
                item["hashes"][machine_id] = entry["sha256"]
            item["needsNodeModules"] = item["needsNodeModules"] or entry.get(
                "needsNodeModules", False
            )
            item["author"] = entry.get("author") or item["author"]
            item["license"] = entry.get("license") or item["license"]
            # Keep the strongest provenance seen anywhere.
            if AUTHORSHIP_RANK.get(entry.get("authorship", ""), 0) > AUTHORSHIP_RANK.get(
                item["authorship"], 0
            ):
                item["authorship"] = entry["authorship"]
            source = entry.get("source") or {}
            if TYPE_RANK.get(source.get("type", ""), 0) > TYPE_RANK.get(
                item["source"].get("type", ""), 0
            ):
                item["source"] = source
                item["installRoot"] = entry.get("root", item["installRoot"])
        for managed in snapshot.get("cindyManagedSkills", []):
            app_managed.setdefault("cindySkills", set()).add(managed)
        for managed in snapshot.get("codexManagedSkills", []):
            app_managed.setdefault("codexSkills", set()).add(managed)

    return skills, known_machines, app_managed


def build() -> dict:
    skills, known_machines, app_managed = merge()
    if not skills:
        raise SystemExit("no collection and no machine snapshots in sync/machines/")

    # The catalog is the authority for github sources. A skill recorded as
    # unresolved may have gained a catalog record since the snapshot was taken;
    # an already-resolved github skill may have had its branch or path corrected.
    catalog_sources = load_catalog_sources()
    for name, item in skills.items():
        catalog_source = catalog_sources.get(name)
        if catalog_source is None:
            continue
        if item["source"].get("type") == "unresolved":
            item["source"] = catalog_source
            if item.get("authorship") != "original":
                item["authorship"] = "third-party"
        elif item["source"].get("type") == "github":
            item["source"] = catalog_source

    out_skills = []
    for name in sorted(skills):
        item = skills[name]
        source = item["source"]
        hashes = {m: h for m, h in item["hashes"].items() if h}
        out_skills.append(
            {
                "name": name,
                "authorship": item["authorship"],
                "source": source,
                "author": item["author"],
                "license": item["license"],
                "install": {
                    "method": METHOD.get(source.get("type"), "manual"),
                    "root": item["installRoot"],
                    "target": INSTALL_TARGETS.get(item["installRoot"], item["installRoot"]),
                },
                "harnesses": VISIBILITY.get(
                    item["installRoot"], [item["installRoot"]]
                ),
                "machines": sorted(item["machines"]),
                "sha256": hashes,
                "drift": len(set(hashes.values())) > 1,
                "needsNodeModules": item["needsNodeModules"],
            }
        )

    machine_ids = sorted(known_machines)
    gaps = {
        machine: [s["name"] for s in out_skills if machine not in s["machines"]]
        for machine in machine_ids
    }

    plugin_doc = (
        json.loads(PLUGINS.read_text(encoding="utf-8"))
        if PLUGINS.is_file()
        else {"plugins": []}
    )
    cindy_plugins = []
    for plugin in plugin_doc.get("plugins", []):
        cindy_plugins.append(
            {
                "id": plugin["id"],
                "namespace": plugin.get("namespace"),
                "purpose": plugin.get("purpose", ""),
                "setup": plugin.get("setup", ""),
                "credentials": plugin.get("credentials", ""),
                "requiresAuthorization": bool(
                    plugin.get("credentials") and plugin["credentials"] != "none"
                ),
                "install": {"method": "cindy-marketplace", "onTarget": "cindy"},
                "cindyOnly": True,
            }
        )
    opencode_plugins = list(plugin_doc.get("opencodePlugins", []))
    opendesign_plugins = [
        plugin["id"] for plugin in cindy_plugins if "opendesign" in plugin["id"]
    ]

    return {
        "version": 2,
        "generatedAt": GENERATED_AT,
        "generatedBy": "sync/build-collection.py",
        "machines": machine_ids,
        "targets": INSTALL_TARGETS,
        "notes": [
            "One collection for every computer. A skill is installed from its source on "
            "each computer; foreign content is never copied into this repository.",
            "install.method tells how a skill reaches a computer: repository-copy, "
            "git-sparse-checkout, or manual when the upstream is not verified.",
            "harnesses lists every agent that sees the skill once it is installed in "
            "install.root.",
            "machines and gaps are coverage evidence: what was seen where and what a "
            "computer still needs. They are not separate collections.",
            "cindyPlugins install from the Cindy marketplace on each computer and are "
            "authorized there; sync/cindy-plugins.json lists what each one needs.",
            "opendesign-trial is the OpenDesign plugin; OpenDesign also uses "
            "prompts/system/opendesign-ui-code-audit.md.",
            "appManaged entries ship inside Cindy or Codex and are never copied.",
        ],
        "cindyPlugins": cindy_plugins,
        "opencodePlugins": opencode_plugins,
        "opendesignPlugins": opendesign_plugins,
        "appManaged": {
            "cindySkills": sorted(app_managed.get("cindySkills", set())),
            "codexSkills": sorted(app_managed.get("codexSkills", set())),
        },
        "gaps": gaps,
        "skills": out_skills,
    }


HASH_CACHE = SYNC_DIR / "source-hashes.json"


def load_hash_cache() -> dict[str, str]:
    if HASH_CACHE.is_file():
        try:
            return json.loads(HASH_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def upstream_skill_hash(source: dict, cache: dict[str, str]) -> str:
    """Hash of the upstream SKILL.md at the recorded ref, cached on disk."""
    repo = source.get("repo") or ""
    ref = source.get("ref") or "main"
    path = source.get("path") or ""
    if not repo:
        return ""
    file_path = "SKILL.md" if path in ("", ".") else f"{path}/SKILL.md"
    key = f"{repo}@{ref}:{file_path}"
    if key in cache:
        return cache[key]
    raw = subprocess.run(
        ["gh", "api", "-H", "Accept: application/vnd.github.raw",
         f"repos/{repo}/contents/{file_path}?ref={ref}"],
        capture_output=True,
    )
    if raw.returncode != 0:
        return ""
    digest = hashlib.sha256(raw.stdout.replace(b"\r\n", b"\n")).hexdigest()
    cache[key] = digest
    HASH_CACHE.write_text(
        json.dumps(cache, indent=2, sort_keys=True) + chr(10), encoding="utf-8"
    )
    return digest


def install_manifest(collection: dict) -> dict:
    """The collection in the schema scripts/sync-skills.ps1 already understands."""
    names_by_root: dict[str, list[str]] = {}
    union_skills = []
    hash_cache = load_hash_cache()
    for skill in collection["skills"]:
        hashes = skill.get("sha256") or {}
        canonical = repo_hash(skill["source"])
        if not canonical and skill["source"].get("type") == "github":
            canonical = upstream_skill_hash(skill["source"], hash_cache)
        if not canonical and hashes:
            counts = Counter(hashes.values())
            canonical = sorted(counts, key=lambda h: (-counts[h], h))[0]
        union_skills.append(
            {
                "name": skill["name"],
                "root": skill["install"]["root"],
                "authorship": skill["authorship"],
                "source": skill["source"],
                "author": skill.get("author", ""),
                "license": skill.get("license", ""),
                "sizeKB": 0,
                "needsNodeModules": skill.get("needsNodeModules", False),
                "sha256": canonical,
                "machines": skill.get("machines", []),
            }
        )
        names_by_root.setdefault(skill["install"]["root"], []).append(skill["name"])

    all_names = [skill["name"] for skill in union_skills]
    return {
        "version": 2,
        "generatedAt": collection["generatedAt"],
        "generatedBy": "sync/build-collection.py",
        "machineId": "collection",
        "sourceMachine": "unified collection of " + ", ".join(collection["machines"]),
        "roots": {
            "opencode": INSTALL_TARGETS["opencode"],
            "agents": INSTALL_TARGETS["agents"],
        },
        "notes": [
            "This is the one install manifest. Do not generate it per computer; run "
            "generate-manifest.py (evidence) and then build-collection.py (this file).",
            "Every resolvable skill installs once in its root, then mirrors into the "
            "other roots as directory junctions.",
            "source.type=repo copies from this repository, github uses git "
            "sparse-checkout, unresolved is reported and copied by hand.",
            "authorship=original only for skills/original/; bundled third-party skills "
            "stay third-party; unknown skills are never promoted.",
            "cindyManagedSkills and codexManagedSkills ship inside their app and are "
            "never copied.",
        ],
        "mirrors": [
            {"dir": INSTALL_TARGETS["agents"], "only": names_by_root.get("opencode", [])},
            {"dir": INSTALL_TARGETS["opencode"], "only": names_by_root.get("agents", [])},
            {"dir": INSTALL_TARGETS["claude"], "only": all_names},
            {"dir": INSTALL_TARGETS["pi"], "only": all_names},
            {"dir": INSTALL_TARGETS["qwen"], "only": all_names},
        ],
        "cindyManagedSkills": collection["appManaged"]["cindySkills"],
        "codexManagedSkills": collection["appManaged"]["codexSkills"],
        "cindyPlugins": [plugin["id"] for plugin in collection["cindyPlugins"]],
        "opencodePlugins": collection["opencodePlugins"],
        "opendesignPlugins": collection["opendesignPlugins"],
        "skills": union_skills,
    }


def unresolved_markdown(collection: dict) -> str:
    unresolved = [
        skill
        for skill in collection["skills"]
        if skill["source"].get("type") == "unresolved"
    ]
    lines = [
        "# Unresolved skills",
        "",
        "Skills in the collection whose upstream could not be verified. They are",
        "**not** in `catalog/items.json`, no content is copied into this repository,",
        "and they are never moved into `skills/original/`.",
        "",
        "Resolve one by finding the exact upstream repository, branch and `SKILL.md`",
        "path, then add a link-only catalog record and rebuild the collection.",
        "",
        f"Collection snapshot: {len(unresolved)} skills. Generated from",
        "`sync/collection.json` by `sync/build-collection.py`.",
        "",
        "| Skill | Install root | SHA-256 of SKILL.md | Why unresolved |",
        "|-------|--------------|---------------------|----------------|",
    ]
    for skill in unresolved:
        hashes = sorted(set((skill.get("sha256") or {}).values()))
        digest = hashes[0] if hashes else ""
        target = collection["targets"].get(
            skill["install"]["root"], skill["install"]["root"]
        )
        facts = []
        if skill.get("author"):
            facts.append(f"author `{skill['author']}`")
        if skill.get("license"):
            facts.append(f"license `{skill['license']}`")
        reason = (
            ", ".join(facts) + "; no exact repository, branch and path verified"
            if facts
            else "no upstream repository/path; hash match not verified"
        )
        if len(hashes) > 1:
            reason += "; copies differ between computers"
        lines.append(f"| `{skill['name']}` | `{target}/{skill['name']}` | `{digest}` | {reason} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if a shared file is stale")
    args = parser.parse_args()

    collection = build()
    collection_text = json.dumps(collection, indent=2, ensure_ascii=False) + "\n"
    manifest_text = (
        json.dumps(install_manifest(collection), indent=2, ensure_ascii=False) + "\n"
    )
    unresolved_text = unresolved_markdown(collection)

    outputs = {
        COLLECTION: collection_text,
        MANIFEST: manifest_text,
        UNRESOLVED: unresolved_text,
    }
    if args.check:
        stale = [
            path.name
            for path, text in outputs.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != text
        ]
        if stale:
            print(
                "stale: " + ", ".join(stale) + "; run python sync/build-collection.py"
            )
            return 1
        print("collection.json, manifest.json and unresolved.md are up to date")
        return 0

    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")

    print(f"wrote {COLLECTION}")
    print(f"wrote {MANIFEST}")
    print(f"wrote {UNRESOLVED}")
    print(f"  computers: {', '.join(collection['machines'])}")
    print(f"  skills: {len(collection['skills'])}")
    print(
        f"  plugins: {len(collection['cindyPlugins'])} Cindy, "
        f"{len(collection['opencodePlugins'])} OpenCode, "
        f"{len(collection['opendesignPlugins'])} OpenDesign"
    )
    for machine, missing in collection["gaps"].items():
        print(f"  missing on {machine}: {len(missing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
