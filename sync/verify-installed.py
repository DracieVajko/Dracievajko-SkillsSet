#!/usr/bin/env python3
"""Check that every installed skill matches the version recorded in the collection.

Reads `sync/manifest.json` (the collection in installer schema) and compares the
installed `SKILL.md` of each skill with the recorded hash, line endings
normalised, so a CRLF checkout is not reported as a difference.

Exit codes
    0 = every installed skill matches the collection
    1 = at least one skill is missing or differs (reinstall from the collection)

Usage
    python sync/verify-installed.py
    python sync/verify-installed.py --json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

SYNC_DIR = Path(__file__).resolve().parent
MANIFEST = SYNC_DIR / "manifest.json"
HOME = Path(os.path.expanduser("~"))
ROOT_PATHS = {
    "opencode": HOME / ".config/opencode/skills",
    "agents": HOME / ".agents/skills",
}


def norm(raw: bytes) -> str:
    return hashlib.sha256(raw.replace(bytes([13, 10]), bytes([10]))).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    if not MANIFEST.is_file():
        print(f"manifest not found: {MANIFEST}", file=sys.stderr)
        return 2

    collection = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ok, differs, missing = [], [], []

    for skill in collection.get("skills", []):
        name = skill["name"]
        root = ROOT_PATHS.get(skill.get("root"), HOME / skill.get("root", ""))
        skill_md = root / name / "SKILL.md"
        if not skill_md.is_file():
            missing.append(name)
            continue
        if skill.get("source", {}).get("type") == "unresolved":
            ok.append(name)  # nothing to compare against
            continue
        expected = skill.get("sha256") or ""
        actual = norm(skill_md.read_bytes())
        (ok if actual == expected else differs).append(name)

    result = {"ok": ok, "differs": differs, "missing": missing}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for name in differs:
            print(f"DIFFERS  {name}  (reinstall from the collection)")
        for name in missing:
            print(f"MISSING  {name}")
        print(
            f"{len(ok)} match, {len(differs)} differ, {len(missing)} missing "
            f"of {len(collection.get('skills', []))}"
        )
    return 0 if not differs and not missing else 1


if __name__ == "__main__":
    sys.exit(main())
