#!/usr/bin/env python3
"""Generate sync/manifest.json from this machine plus the repository catalog.

The manifest is a snapshot of what is installed here, described so that another
Windows machine can reproduce it: each skill's upstream source, its install
root, and the directory junctions that mirror it into other agents' folders.

Sources of truth
    skills/original/<name>            -> source.type "repo"
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
import re
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
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "manifest.json"

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


def frontmatter_author(path: Path) -> str:
    """Best-effort read of the frontmatter fields used for the authorship guard."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:2000]
    except OSError:
        return ""
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    block = m.group(1).replace("\r", "")
    for key in ("author", "authorship"):
        match = re.search(rf"^{key}\s*:\s*(.+)$", block, re.M)
        if match:
            value = match.group(1).strip().strip('"\'')
            if key == "author":
                return value
    return ""


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
        folder = path[: -len("/SKILL.md")] if path.endswith("/SKILL.md") else ""
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
            elif name in catalog:
                source = dict(catalog[name])
            else:
                source = {"type": "unresolved", "repo": None, "ref": None, "path": None}
            if source["type"] == "repo":
                authorship = "original"
            elif source["type"] == "github":
                authorship = "third-party"
            else:
                authorship = "unknown"
            author = frontmatter_author(entry / "SKILL.md")
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

    manifest = {
        "version": 1,
        "generatedAt": "2026-11-18",
        "sourceMachine": "DracieVajko (Windows, Cindy 0.1.139, Pi 1.5.2)",
        "roots": {k: tilde(v) for k, v in ROOTS.items()},
        "notes": [
            "Each skill is installed once, under roots[<root>].",
            "mirrors[] lists Windows directory junctions that expose those folders "
            "under other agents' skill directories; create them, never copy.",
            "source.type=repo installs from this repository, source.type=github uses "
            "git sparse-checkout, source.type=unresolved has no identified upstream "
            "and must be copied by hand.",
            "authorship=original only for the owner's own skills (installed from "
            "skills/original/); authorship=third-party and unknown skills are never "
            "promoted into skills/original/ and keep their upstream author.",
            "node_modules is never copied; run npm install in skills with "
            "needsNodeModules=true.",
            "cindyManagedSkills ship inside Cindy itself and are never copied between "
            "machines.",
        ],
        "cindyManagedSkills": managed,
        "mirrors": mirrors,
        "skills": skills,
    }
    text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        if current != text:
            print("manifest.json is stale; run python sync/generate-manifest.py")
            return 1
        print("manifest.json is up to date")
        return 0

    OUT.write_text(text, encoding="utf-8")
    counts: dict[str, int] = {}
    for s in skills:
        key = s["source"]["type"]
        counts[key] = counts.get(key, 0) + 1
    print(f"wrote {OUT}")
    print(f"  {len(skills)} skills {counts}")
    print(f"  {len(mirrors)} mirror rules, {len(managed)} cindy-managed skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
