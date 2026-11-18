#!/usr/bin/env python3
"""Record this computer's installed skills as evidence for the collection.

Writes only sync/machines/<machineId>.json. It never writes sync/manifest.json,
sync/collection.json or sync/unresolved.md: those are built once from every
machine snapshot by sync/build-collection.py, so two computers cannot overwrite
each other's inventory.

Sources of truth
    skills/original/<name>            -> source.type "repo", authorship "original"
    skills/third-party/<name>         -> source.type "repo", authorship "third-party"
    catalog/items.json                -> source.type "github"
    OVERRIDES below                   -> source.type "github" (not in the catalog)
    anything else installed locally   -> source.type "unresolved"

Usage
    python sync/generate-manifest.py
    python sync/generate-manifest.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import socket
import sys
from pathlib import Path

REPO_NAME = "DracieVajko/Dracievajko-SkillsSet"
REPO_AUTHOR = "DracieVajko"
HOME = Path(os.path.expanduser("~"))

# Install roots: real skill folders only; mirrors are detected, never scanned.
ROOTS = {
    "opencode": HOME / ".config/opencode/skills",
    "agents": HOME / ".agents/skills",
}
MIRROR_DIRS = {
    "claude": HOME / ".claude/skills",
    "pi": HOME / ".pi/agent/skills",
}
MANAGED_ROOT = HOME / "AppData/Roaming/CindyGlobal/managed-agent-skills/cindy/skills"
CODEX_MANAGED_ROOT = HOME / ".codex/skills/.system"
# Roots that belong to another agent and are neither installed nor mirrored by
# this repository. They are inventoried so no skill silently falls out of scope.
EXTRA_ROOTS = {
    "qwen": HOME / ".qwen/skills",
}
REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = Path(__file__).resolve().parent
MACHINES = MANIFEST_DIR / "machines"


def machine_slug() -> str:
    """Stable, filesystem-safe id for this computer."""
    host = re.sub(r"[^a-z0-9]+", "-", socket.gethostname().lower()).strip("-")
    return host or "unknown-machine"


def machine_label() -> str:
    host = socket.gethostname()
    return f"{host} ({platform.system()} {platform.release()})"

# Upstreams verified by hashing SKILL.md against the upstream file on 2026-11-18.
OVERRIDES = {
    "rea-analysis-optimization": {
        "type": "github", "repo": "morluto/rea", "ref": "main",
        "path": ".agents/skills/rea-analysis-optimization",
    },
    "rea-changelog-update": {
        "type": "github", "repo": "morluto/rea", "ref": "main",
        "path": ".agents/skills/rea-changelog-update",
    },
    "rea-ci-tests-audit": {
        "type": "github", "repo": "morluto/rea", "ref": "main",
        "path": ".agents/skills/rea-ci-tests-audit",
    },
    "rea-tool-design": {
        "type": "github", "repo": "morluto/rea", "ref": "main",
        "path": ".agents/skills/rea-tool-design",
    },
    "deep-agents-memory": {
        "type": "github", "repo": "langchain-ai/design-agent", "ref": "main",
        "path": ".agents/skills/deep-agents-memory",
    },
}


def tilde(path: Path) -> str:
    return str(path).replace(str(HOME), "~")


def sha256(path: Path) -> str:
    """Hash the file with line endings normalised, so CRLF and LF copies match."""
    raw = path.read_bytes().replace(bytes([13, 10]), bytes([10]))
    return hashlib.sha256(raw).hexdigest()


def frontmatter_fields(path: Path) -> dict[str, str]:
    """Best-effort read of the frontmatter fields used for provenance and guard."""
    fields: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:2000]
    except OSError:
        return fields
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return fields
    block = m.group(1).replace("\r", "")
    for key in ("author", "authorship", "license"):
        match = re.search(rf"^{key}\s*:\s*(.+)$", block, re.M)
        if match:
            fields[key] = match.group(1).strip().strip('"\'')
    return fields


def dir_size_kb(path: Path) -> int:
    total = 0
    for dp, dns, fns in os.walk(path):
        dns[:] = [d for d in dns if d != "node_modules"]
        for fn in fns:
            try:
                total += (Path(dp) / fn).stat().st_size
            except OSError:
                pass
    return round(total / 1024)


def is_mirror(path: Path) -> bool:
    return os.path.realpath(path) != os.path.abspath(path)


def load_catalog() -> dict[str, dict]:
    catalog_path = REPO_ROOT / "catalog" / "items.json"
    if not catalog_path.is_file():
        return {}
    items = json.loads(catalog_path.read_text(encoding="utf-8"))
    by_name: dict[str, dict] = {}
    for item in items:
        name = item.get("name")
        repo_url = item.get("repository") or ""
        if not name or not repo_url:
            continue
        m = re.search(r"github\.com/([^/]+/[^/#?]+)", repo_url)
        if not m:
            continue
        path = item.get("path") or ""
        if path == "SKILL.md":
            folder = "."
        elif path.endswith("/SKILL.md"):
            folder = path[: -len("/SKILL.md")]
        else:
            folder = ""
        by_name.setdefault(
            name,
            {
                "type": "github",
                "repo": m.group(1),
                "ref": item.get("branch") or "main",
                "path": folder,
            },
        )
    return by_name


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if manifest.json is stale")
    args = ap.parse_args()

    for root in ROOTS.values():
        if not root.is_dir():
            print(f"skill root not found: {root}", file=sys.stderr)
            return 2

    catalog = load_catalog()
    originals = {p.name for p in (REPO_ROOT / "skills" / "original").iterdir() if p.is_dir()}
    bundled = {
        p.name
        for p in (REPO_ROOT / "skills" / "third-party").iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    }

    skills = []
    root_of: dict[str, str] = {}
    for root_key, root in ROOTS.items():
        for entry in sorted(root.iterdir()):
            if not entry.is_dir() or is_mirror(entry) or not (entry / "SKILL.md").is_file():
                continue
            name = entry.name
            if name in root_of:
                print(f"warning: {name} installed in both roots", file=sys.stderr)
                continue
            root_of[name] = root_key
            if name in OVERRIDES:
                source = dict(OVERRIDES[name])
            elif name in originals:
                source = {"type": "repo", "repo": REPO_NAME,
                          "ref": "master", "path": f"skills/original/{name}"}
            elif name in bundled:
                source = {"type": "repo", "repo": REPO_NAME,
                          "ref": "master", "path": f"skills/third-party/{name}"}
            elif name in catalog:
                source = dict(catalog[name])
            else:
                source = {"type": "unresolved", "repo": None, "ref": None, "path": None}
            if source["type"] == "repo":
                authorship = "original" if name in originals else "third-party"
            elif source["type"] == "github":
                authorship = "third-party"
            else:
                authorship = "unknown"
            fields = frontmatter_fields(entry / "SKILL.md")
            author = fields.get("author", "")
            if authorship != "original" and author == REPO_AUTHOR:
                print(
                    f"warning: {name} records author {REPO_AUTHOR} but its source is "
                    f"{authorship}; keep it out of skills/original unless it is "
                    f"the owner's own work",
                    file=sys.stderr,
                )
            skills.append(
                {
                    "name": name,
                    "root": root_key,
                    "authorship": authorship,
                    "source": source,
                    "author": fields.get("author", ""),
                    "license": fields.get("license", ""),
                    "sizeKB": dir_size_kb(entry),
                    "needsNodeModules": (entry / "package.json").is_file(),
                    "sha256": sha256(entry / "SKILL.md"),
                }
            )

    mirrors = []
    for mirror_key, mirror_dir in MIRROR_DIRS.items():
        if not mirror_dir.is_dir():
            continue
        names = []
        for entry in sorted(mirror_dir.iterdir()):
            if not entry.is_dir() or not (entry / "SKILL.md").is_file():
                continue
            target = Path(os.path.realpath(entry))
            # A mirror may point directly at an install root or through another
            # mirror; either way, record the name and let the installer resolve
            # the real source folder from its root.
            if any(Path(os.path.realpath(r)) in (target, target.parent)
                   for r in ROOTS.values()):
                names.append(entry.name)
        if names:
            mirrors.append({"dir": tilde(mirror_dir), "only": names})

    # Junctions inside an install root that point at the other root.
    for root_key, root in ROOTS.items():
        names = [
            e.name for e in sorted(root.iterdir())
            if e.is_dir() and is_mirror(e) and (e / "SKILL.md").is_file()
        ]
        if names:
            mirrors.append({"dir": tilde(root), "only": names})

    managed = []
    if MANAGED_ROOT.is_dir():
        managed = sorted(
            e.name for e in MANAGED_ROOT.iterdir() if (e / "SKILL.md").is_file()
        )

    codex_managed = []
    if CODEX_MANAGED_ROOT.is_dir():
        codex_managed = sorted(
            e.name
            for e in CODEX_MANAGED_ROOT.iterdir()
            if (e / "SKILL.md").is_file()
        )

    manifest_roots = {k: tilde(v) for k, v in ROOTS.items()}
    canonical = {s["name"]: s for s in skills}
    drift = []
    for extra_key, extra_root in {**MIRROR_DIRS, **EXTRA_ROOTS}.items():
        if not extra_root.is_dir():
            continue
        for entry in sorted(extra_root.iterdir()):
            skill_md = entry / "SKILL.md"
            if not entry.is_dir() or not skill_md.is_file():
                continue
            original = canonical.get(entry.name)
            if original is None:
                continue
            digest = sha256(skill_md)
            if digest != original["sha256"]:
                drift.append(
                    {
                        "name": entry.name,
                        "root": tilde(extra_root),
                        "link": is_mirror(entry),
                        "sha256": digest,
                        "canonicalRoot": manifest_roots[original["root"]],
                        "canonicalSha256": original["sha256"],
                    }
                )

    harness_roots = []

    def add_harness_root(root_id: str, path: Path, role: str) -> None:
        if not path.is_dir():
            return
        harness_roots.append(
            {
                "id": root_id,
                "dir": tilde(path),
                "role": role,
                "skills": sum(
                    1
                    for e in path.iterdir()
                    if e.is_dir() and (e / "SKILL.md").is_file()
                ),
            }
        )

    for root_key, root in ROOTS.items():
        add_harness_root(root_key, root, "install")
    for mirror_key, mirror_root in MIRROR_DIRS.items():
        add_harness_root(mirror_key, mirror_root, "mirror")
    for extra_key, extra_root in EXTRA_ROOTS.items():
        add_harness_root(extra_key, extra_root, "harness")
    add_harness_root("cindy-managed", MANAGED_ROOT, "managed")
    add_harness_root("codex-managed", CODEX_MANAGED_ROOT, "managed")

    manifest = {
        "version": 1,
        "generatedAt": "2026-11-18",
        "machineId": machine_slug(),
        "sourceMachine": machine_label(),
        "roots": manifest_roots,
        "notes": [
            "Each skill is installed once, under roots[<root>].",
            "harnessRoots[] inventories every skill root on this machine: role=install "
            "roots hold the canonical copy, role=mirror roots are junctions, role=harness "
            "roots belong to another agent and role=managed roots ship inside an app.",
            "mirrors[] lists Windows directory junctions that expose those folders "
            "under other agents' skill directories; create them, never copy.",
            "drift[] lists same-named copies whose SKILL.md hash differs from the "
            "canonical install; link=true means a junction into another root, "
            "link=false means a separate copy, so compare before trusting one.",
            "source.type=repo installs from this repository (skills/original or the "
            "approved bundled copies in skills/third-party), source.type=github uses "
            "git sparse-checkout, source.type=unresolved has no identified upstream "
            "and must be copied by hand.",
            "authorship=original only for the owner's own skills (installed from "
            "skills/original/); bundled third-party skills stay third-party even "
            "though they install from this repository, and unknown skills are never "
            "promoted into skills/original/ and keep their upstream author.",
            "node_modules is never copied; run npm install in skills with "
            "needsNodeModules=true.",
            "cindyManagedSkills and codexManagedSkills ship inside their app and are "
            "never copied between machines.",
        ],
        "cindyManagedSkills": managed,
        "codexManagedSkills": codex_managed,
        "harnessRoots": harness_roots,
        "drift": drift,
        "mirrors": mirrors,
        "skills": skills,
    }
    text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    machine_out = MACHINES / f"{manifest['machineId']}.json"

    if args.check:
        machine_current = machine_out.read_text(encoding="utf-8") if machine_out.is_file() else ""
        if machine_current != text:
            print(
                f"{machine_out.name} is stale; run python sync/generate-manifest.py"
            )
            return 1
        print(f"{machine_out.name} is up to date")
        return 0

    MACHINES.mkdir(exist_ok=True)
    machine_out.write_text(text, encoding="utf-8")

    counts: dict[str, int] = {}
    for s in skills:
        key = s["source"]["type"]
        counts[key] = counts.get(key, 0) + 1
    print(f"wrote {machine_out}")
    print(f"  {len(skills)} skills {counts}")
    print(f"  {len(mirrors)} mirror rules, {len(managed)} cindy-managed skills")
    print(
        f"  {len(harness_roots)} harness roots, {len(codex_managed)} codex-managed "
        f"skills, {len(drift)} drifted copies"
    )
    print("run python sync/build-collection.py to refresh the shared collection")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
