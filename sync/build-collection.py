#!/usr/bin/env python3
"""Build one unified collection from every machine snapshot.

Reads `sync/machines/*.json` (one snapshot per computer, written by
`generate-manifest.py`) plus `sync/cindy-plugins.json`, and writes
`sync/collection.json`: a single inventory of every skill and plugin that any
of these computers has, tagged with where it installs, who wrote it and which
computers already have it.

The collection is deliberately machine-neutral. Machine snapshots stay as
evidence; this file is the one big collection.

Usage
    python sync/build-collection.py
    python sync/build-collection.py --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SYNC_DIR = Path(__file__).resolve().parent
MACHINES_DIR = SYNC_DIR / "machines"
OUT = SYNC_DIR / "collection.json"
UNION_MANIFEST = SYNC_DIR / "manifest-union.json"
PLUGINS = SYNC_DIR / "cindy-plugins.json"

# A skill installed in one of these roots is visible to these harnesses.
VISIBILITY = {
    "opencode": ["opencode", "agents", "cindy", "claude", "pi"],
    "agents": ["agents", "cindy", "claude", "pi", "continue", "qwen", "roo"],
}

INSTALL_TARGETS = {
    "opencode": "~/.config/opencode/skills",
    "agents": "~/.agents/skills",
    "claude": "~/.claude/skills",
    "pi": "~/.pi/agent/skills",
    "cindy": "Cindy app: skills from ~/.agents/skills, plugins from sync/cindy-plugins.json",
}

AUTHORSHIP_RANK = {"original": 3, "third-party": 2, "unknown": 1}
TYPE_RANK = {"repo": 3, "github": 2, "unresolved": 1}


def load_machines() -> dict[str, dict]:
    """Return {machineId: snapshot} for every stored machine snapshot."""
    machines = {}
    if not MACHINES_DIR.is_dir():
        return machines
    for path in sorted(MACHINES_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        machine_id = data.get("machineId") or path.stem
        machines[machine_id] = data
    return machines


def build() -> dict:
    machines = load_machines()
    if not machines:
        raise SystemExit("no machine snapshots in sync/machines/")

    skills: dict[str, dict] = {}
    for machine_id, snapshot in machines.items():
        for entry in snapshot.get("skills", []):
            name = entry["name"]
            item = skills.setdefault(
                name,
                {
                    "name": name,
                    "authorship": entry.get("authorship", "unknown"),
                    "installRoot": entry.get("root", "opencode"),
                    "source": entry.get("source", {}),
                    "machines": {},
                    "needsNodeModules": False,
                },
            )
            item["machines"][machine_id] = entry.get("sha256")
            item["needsNodeModules"] = item["needsNodeModules"] or entry.get("needsNodeModules", False)
            # Keep the strongest provenance seen anywhere.
            if AUTHORSHIP_RANK.get(entry.get("authorship", ""), 0) > AUTHORSHIP_RANK.get(item["authorship"], 0):
                item["authorship"] = entry["authorship"]
            if TYPE_RANK.get(item["source"].get("type", ""), 0) < TYPE_RANK.get(entry["source"]["type"], 0):
                item["source"] = entry["source"]
                item["installRoot"] = entry.get("root", item["installRoot"])

    out_skills = []
    for name in sorted(skills):
        item = skills[name]
        hashes = {m: h for m, h in item["machines"].items() if h}
        drift = len(set(hashes.values())) > 1
        out_skills.append(
            {
                "name": name,
                "authorship": item["authorship"],
                "source": item["source"],
                "install": {
                    "method": {
                        "repo": "repository-copy",
                        "github": "git-sparse-checkout",
                        "unresolved": "manual",
                    }.get(item["source"].get("type"), "manual"),
                    "root": item["installRoot"],
                    "target": INSTALL_TARGETS.get(item["installRoot"], item["installRoot"]),
                },
                "harnesses": VISIBILITY.get(item["installRoot"], [item["installRoot"]]),
                "machines": sorted(item["machines"]),
                "sha256": hashes,
                "drift": drift,
                "needsNodeModules": item["needsNodeModules"],
            }
        )

    machine_ids = sorted(machines)
    gaps = {
        m: [s["name"] for s in out_skills if m not in s["machines"]]
        for m in machine_ids
    }

    plugins = json.loads(PLUGINS.read_text(encoding="utf-8")) if PLUGINS.is_file() else {"plugins": []}
    cindy_plugins = []
    for plugin in plugins.get("plugins", []):
        cindy_plugins.append(
            {
                "id": plugin["id"],
                "namespace": plugin.get("namespace"),
                "purpose": plugin.get("purpose", ""),
                "requiresAuthorization": bool(plugin.get("credentials") and plugin["credentials"] != "none"),
                "install": {"method": "cindy-marketplace", "onTarget": "cindy"},
                "cindyOnly": True,
            }
        )

    app_managed = {}
    for machine_id, snapshot in machines.items():
        for managed in snapshot.get("cindyManagedSkills", []):
            app_managed.setdefault("cindy", set()).add(managed)
        for managed in snapshot.get("codexManagedSkills", []):
            app_managed.setdefault("codex", set()).add(managed)
    codex_plugins = sorted(app_managed.pop("codex", set()))
    cindy_managed = sorted(app_managed.pop("cindy", set()))

    return {
        "version": 1,
        "generatedBy": "sync/build-collection.py",
        "machines": machine_ids,
        "targets": INSTALL_TARGETS,
        "notes": [
            "One collection for every computer. Machine snapshots in sync/machines/ are evidence, "
            "not separate collections.",
            "install.method tells how a skill reaches a computer: repository-copy, git-sparse-checkout, "
            "or manual when the upstream is not verified.",
            "harnesses lists every agent that sees the skill once it is installed in install.root.",
            "cindyPlugins install from the Cindy marketplace on each machine and are then authorized "
            "there; sync/CINDY-INSTALL.md contains a ready-to-paste prompt that does it.",
            "appManaged entries ship inside Cindy or Codex and are never copied between computers.",
        ],
        "cindyPlugins": cindy_plugins,
        "appManaged": {
            "cindySkills": cindy_managed,
            "codexSkills": codex_plugins,
        },
        "gaps": gaps,
        "skills": out_skills,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if collection.json is stale")
    args = parser.parse_args()

    text = json.dumps(build(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        if current != text:
            print("collection.json is stale; run python sync/build-collection.py")
            return 1
        print("collection.json is up to date")
        return 0

    OUT.write_text(text, encoding="utf-8")
    data = json.loads(text)

    # The same collection in the schema scripts/sync-skills.ps1 consumes, so a
    # single command can put every skill on a computer.
    union_skills = []
    for skill in data["skills"]:
        machines = [m for m in data["machines"] if m in skill["machines"]]
        entry = {
            "name": skill["name"],
            "root": skill["install"]["root"],
            "authorship": skill["authorship"],
            "source": skill["source"],
            "sizeKB": 0,
            "needsNodeModules": skill["needsNodeModules"],
            "sha256": next(iter(skill["sha256"].values()), ""),
            "machines": machines,
        }
        union_skills.append(entry)

    names_by_root: dict[str, list[str]] = {}
    for skill in union_skills:
        names_by_root.setdefault(skill["root"], []).append(skill["name"])

    union = {
        "version": 1,
        "generatedAt": data.get("generatedAt", ""),
        "machineId": "union",
        "sourceMachine": "union of " + ", ".join(data["machines"]),
        "roots": {k: v for k, v in INSTALL_TARGETS.items() if k in ("opencode", "agents")},
        "notes": [
            "Union manifest: every skill any known computer has. Installs from repository copies "
            "or git sparse-checkout; unresolved skills are reported, never guessed.",
            "Mirrors list every name so each agent sees the same set after install.",
        ],
        "mirrors": [
            {"dir": INSTALL_TARGETS["agents"], "only": names_by_root.get("opencode", [])},
            {"dir": INSTALL_TARGETS["claude"], "only": [s["name"] for s in union_skills]},
            {"dir": INSTALL_TARGETS["pi"], "only": [s["name"] for s in union_skills]},
        ],
        "cindyManagedSkills": data["appManaged"]["cindySkills"],
        "skills": union_skills,
    }
    UNION_MANIFEST.write_text(json.dumps(union, indent=2, ensure_ascii=False) + chr(10), encoding="utf-8")
    print(f"wrote {UNION_MANIFEST}")
    print(f"wrote {OUT}")
    print(f"  machines: {', '.join(data['machines'])}")
    print(f"  skills: {len(data['skills'])}  cindy plugins: {len(data['cindyPlugins'])}")
    for machine, missing in data["gaps"].items():
        print(f"  missing on {machine}: {len(missing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
