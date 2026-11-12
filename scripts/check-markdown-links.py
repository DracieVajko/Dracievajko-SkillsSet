#!/usr/bin/env python3
"""
Check that relative Markdown links in the repository point to existing files.

External links (http, https, mailto) and pure anchors are not checked here -
external availability is verified by scripts/check-links.py.

Usage
    python scripts/check-markdown-links.py
    python scripts/check-markdown-links.py --root <repository-root>

Exit codes
    0 = every relative link resolves
    1 = at least one relative link points to a missing file or directory
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

LINK_PATTERN = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
EXTERNAL_SCHEMES = ('http://', 'https://', 'mailto:', 'ftp://', 'tel:')
SKIP_DIRS = {'.git', '.desloppify', 'node_modules', '__pycache__'}

# Vendored upstream skills keep their original relative links. Some point at
# sibling skills that are not vendored here, so they are reported as warnings
# instead of failures - the upstream repository remains the source for them.
VENDORED_PREFIXES = ('skills/third-party/',)


def iter_markdown_files(root: Path):
    """Yield every Markdown file in the repository, skipping tool directories."""
    for path in sorted(root.rglob('*.md')):
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(root)
        if SKIP_DIRS.intersection(relative.parts):
            continue
        yield path


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks so example links are not treated as real ones."""
    lines = text.splitlines()
    kept: list[str] = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept.append(line)
    return '\n'.join(kept)


def check_file(path: Path, root: Path) -> tuple[list[str], list[str]]:
    """Return (problems, warnings) for one Markdown file."""
    text = path.read_text(encoding='utf-8')
    problems: list[str] = []
    warnings: list[str] = []
    relative = path.relative_to(root).as_posix()
    vendored = relative.startswith(VENDORED_PREFIXES)
    for target in LINK_PATTERN.findall(strip_code_blocks(text)):
        if target.startswith('#') or target.startswith(EXTERNAL_SCHEMES):
            continue
        target_path = unquote(target.split('#', 1)[0].split('?', 1)[0]).strip()
        if not target_path:
            continue
        if target_path.startswith('/'):
            resolved = root / target_path.lstrip('/')
        else:
            resolved = (path.parent / target_path).resolve()
        if resolved.exists():
            continue
        message = f"{relative}: link target not found: {target}"
        if vendored:
            warnings.append(f"{message} (vendored upstream link, not bundled)")
        else:
            problems.append(message)
    return problems, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--root', default=None,
        help='Repository root (defaults to the parent of this script).',
    )
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve() if args.root else Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print(f"Repository root not found: {root}")
        return 1

    files = list(iter_markdown_files(root))
    problems: list[str] = []
    warnings: list[str] = []
    for path in files:
        try:
            file_problems, file_warnings = check_file(path, root)
        except (OSError, UnicodeError) as exc:
            print(f"ERROR: {exc}")
            return 1
        problems.extend(file_problems)
        warnings.extend(file_warnings)

    for problem in problems:
        print(f"BROKEN: {problem}")
    for warning in warnings:
        print(f"WARN: {warning}")
    print(
        f"Checked {len(files)} Markdown file(s): {len(problems)} broken relative link(s), "
        f"{len(warnings)} vendored link(s) not bundled"
    )
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
