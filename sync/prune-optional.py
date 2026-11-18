#!/usr/bin/env python3
"""Move disabled skills out of every agent root.

Reads `sync/optional.json` and, for each disabled skill:

* a directory junction is removed as a link (the canonical copy is untouched);
* a real skill folder is moved to `~/.config/opencode/skills-disabled/<name>`.

Nothing is deleted. Remove the name from `sync/optional.json` and run
`scripts/sync-skills.ps1` to install it again.

Usage
    python sync/prune-optional.py
    python sync/prune-optional.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

SYNC_DIR = Path(__file__).resolve().parent
OPTIONAL = SYNC_DIR / "optional.json"
HOME = Path(os.path.expanduser("~"))
ROOTS = [
    HOME / ".config/opencode/skills",
    HOME / ".agents/skills",
    HOME / ".claude/skills",
    HOME / ".qwen/skills",
    HOME / ".pi/agent/skills",
]
DISABLED = HOME / ".config/opencode/skills-disabled"


def load_disabled() -> list[str]:
    if not OPTIONAL.is_file():
        return []
    data = json.loads(OPTIONAL.read_text(encoding="utf-8"))
    return [entry["name"] for entry in data.get("disabled", []) if entry.get("name")]


def is_link(path: Path) -> bool:
    return os.path.realpath(path) != os.path.abspath(path)


def remove_link(path: Path) -> None:
    # os.rmdir removes a Windows directory junction or a POSIX directory
    # symlink without touching the target.
    os.rmdir(path)


def move_to_disabled(path: Path, name: str) -> Path:
    DISABLED.mkdir(parents=True, exist_ok=True)
    destination = DISABLED / name
    if destination.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        destination = DISABLED / f"{name}-{stamp}"
    shutil.move(str(path), str(destination))
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="report without moving anything")
    args = parser.parse_args()

    names = load_disabled()
    if not names:
        print("No disabled skills in sync/optional.json")
        return 0

    links = 0
    moved = 0
    missing = 0
    for name in names:
        found = False
        for root in ROOTS:
            path = root / name
            if not path.exists():
                continue
            found = True
            if args.dry_run:
                kind = "unlink" if is_link(path) else "move"
                print(f"would {kind:6} {path}")
                continue
            if is_link(path):
                remove_link(path)
                print(f"unlinked {path}")
                links += 1
            else:
                destination = move_to_disabled(path, name)
                print(f"moved    {path} -> {destination}")
                moved += 1
        if not found:
            missing += 1

    if args.dry_run:
        print("Dry run: nothing changed")
    else:
        print(
            f"Done: {links} junction(s) removed, {moved} folder(s) moved, "
            f"{missing} not installed"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
