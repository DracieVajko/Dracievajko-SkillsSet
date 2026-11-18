#!/usr/bin/env python3
"""
Regenerate docs/CATEGORY_INDEX.md from the local original skill tree and the
catalog link files.

Authoritative inputs (exactly one source of truth per generated section)

    Section                     Authoritative source
    --------------------------  ---------------------------------------------
    Original local skills       filesystem: skills/original/**/SKILL.md
    External skills (links)     catalog/links/skill-links.txt
                                plus catalog/links/pinned-links.txt
    External descriptions       catalog/items.json (optional metadata)

No third-party skill code is read or copied. External skills are reported as
upstream URLs only; descriptions are shown only when the catalog already
contains curated metadata for that URL.

The same script also maintains the generated repository-count blocks in
README.md, catalog/README.md, ATTRIBUTION.md and skills/third-party/README.md.
Those counts are derived from catalog/items.json and the filesystem, so the
numbers are never maintained by hand in several places.

Usage
    python scripts/update-category-index.py            # write the index and count blocks
    python scripts/update-category-index.py --check    # exit 1 if stale, no writes

Exit codes
    0 = index written, or (--check) committed index and count blocks are up to date
    1 = error, or (--check) the committed index or a count block is stale/missing
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterator
from pathlib import Path

import yaml

SKILL_ROOTS = {
    'skills/original': 'Original Local Skills',
}

EXCLUDE_DIR_NAMES = {
    '_backups',
    '_source-backups',
    '_private-review',
    '.git',
    'node_modules',
}

LINK_DIR = ('catalog', 'links')
LINK_FILES = ('skill-links.txt', 'pinned-links.txt')
ITEMS_RELPATH = ('catalog', 'items.json')
INDEX_RELPATH = ('docs', 'CATEGORY_INDEX.md')
VERIFIED_DATE = '2026-11-12'


# --- helpers ---------------------------------------------------------------

def resolve_root(cli_root: str | None) -> Path:
    if cli_root:
        return Path(cli_root).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def iter_local_skills(root: Path, root_name: str) -> Iterator[tuple[Path, dict | None]]:
    """Yield (skill_md, frontmatter_or_None) for one root, deterministically."""
    base = root / root_name
    if not base.is_dir():
        return
    for skill_md in sorted(base.rglob('SKILL.md')):
        if skill_md.is_symlink():
            continue
        rel_parts = skill_md.relative_to(root).parts
        if EXCLUDE_DIR_NAMES.intersection(rel_parts[:-1]):
            continue
        yield skill_md, _read_frontmatter(skill_md)


def _read_frontmatter(skill_md: Path) -> dict | None:
    try:
        content = skill_md.read_text(encoding='utf-8')
    except OSError:
        return None
    if not content.startswith('---'):
        return None
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    return frontmatter if isinstance(frontmatter, dict) else None


def parse_link_files(root: Path) -> list[dict]:
    """Return sorted [{repo, name, url, source_file}] from catalog/links/.

    Both link files are authoritative for the external section, so a missing
    file is an error rather than an empty reference list.
    """
    links_dir = root.joinpath(*LINK_DIR)
    references = []
    missing = []
    for filename in LINK_FILES:
        path = links_dir / filename
        if not path.is_file():
            missing.append(str(path))
            continue
        for raw in path.read_text(encoding='utf-8-sig').splitlines():
            url = raw.strip()
            if not url or url.startswith('#'):
                continue
            references.append({
                'repo': _repo_from_url(url),
                'name': _name_from_url(url),
                'url': url,
                'source_file': filename,
            })
    if missing:
        raise FileNotFoundError(
            "Missing authoritative link file(s): " + ', '.join(missing)
        )
    references.sort(key=lambda r: (r['repo'], r['name'], r['url']))
    return references


def load_external_descriptions(root: Path) -> dict[str, str]:
    """Return {raw_url: description} from catalog/items.json.

    Descriptions are optional enrichment. A missing or malformed catalog does
    not break link rendering; the index simply falls back to name + URL.
    """
    path = root.joinpath(*ITEMS_RELPATH)
    if not path.is_file():
        return {}
    try:
        items = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(items, list):
        return {}
    descriptions = {}
    for item in items:
        if not isinstance(item, dict) or item.get('authorship') != 'link-only':
            continue
        url = item.get('raw_url')
        description = item.get('description')
        if not url or not description:
            continue
        descriptions[url] = ' '.join(str(description).split())
    return descriptions


def _repo_from_url(url: str) -> str:
    parts = url.split('/')
    if 'raw.githubusercontent.com' in url and len(parts) >= 5:
        return f"{parts[3]}/{parts[4]}"
    return 'unknown'


def _name_from_url(url: str) -> str:
    parts = [p for p in url.split('/') if p]
    if len(parts) >= 2 and parts[-1].lower() == 'skill.md':
        return parts[-2]
    return parts[-1] if parts else url


def _link_from_docs(target_rel_path: str) -> str:
    """Relative Markdown link from docs/CATEGORY_INDEX.md to a repo-relative path."""
    return f"../{target_rel_path.replace('\\', '/')}"


def _cell(text: str) -> str:
    """Escape a value for a Markdown table cell."""
    return str(text if text is not None else '').replace('|', '\\|')


# --- generation ------------------------------------------------------------

def generate(root: Path) -> str:
    """Return the full CATEGORY_INDEX.md content as a string."""
    lines = []
    lines.append("# Category Index")
    lines.append("")
    lines.append("Auto-generated by `scripts/update-category-index.py`. Do not edit by hand.")
    lines.append("Validate the tree with `python scripts/validate-frontmatter.py`.")
    lines.append("Check duplicated rule copies with `python scripts/check-sync.py`.")
    lines.append("")
    lines.append("Original skills are discovered on disk. External link skills are reported as upstream URLs only;")
    lines.append("bundled third-party skills are tracked under skills/third-party/. Link availability was verified on")
    lines.append(f"{VERIFIED_DATE} - see `catalog/links/README.md`.")
    lines.append("")
    lines.append("Authoritative source per section:")
    lines.append("")
    lines.append("| Section | Authoritative source |")
    lines.append("|---------|----------------------|")
    lines.append("| Original local skills | `skills/original/**/SKILL.md` |")
    lines.append("| External skills (links only) | `catalog/links/skill-links.txt` + `pinned-links.txt` |")
    lines.append("| External descriptions (optional) | `catalog/items.json` |")
    lines.append("")

    for root_name in SKILL_ROOTS:
        lines.extend(_render_local_section(root, root_name))

    lines.extend(_render_external_section(root))

    lines.append("---")
    lines.append("")
    lines.append("*Generated from the original skill tree and `catalog/links/`. "
                 "Regenerate with `python scripts/update-category-index.py`.*")
    return '\n'.join(lines) + '\n'


def _render_local_section(root: Path, root_name: str) -> list[str]:
    title = SKILL_ROOTS[root_name]
    rows = []
    for skill_md, frontmatter in iter_local_skills(root, root_name):
        rel = skill_md.relative_to(root).as_posix()
        folder = skill_md.parent.name
        if frontmatter is None:
            name = folder
            category = '-'
            version = '-'
            purpose = '-'
        else:
            name = frontmatter.get('name', folder)
            category = frontmatter.get('category', '-')
            version = frontmatter.get('version', '-')
            purpose = str(frontmatter.get('description') or '-').replace('\n', ' ').strip() or '-'
        rows.append((name, category, version, purpose, rel))

    rows.sort(key=lambda r: (str(r[0]), r[4]))

    out = [f"## {title}", "", f"Discovered under `{root_name}/`.", ""]
    if not rows:
        out.append("*None.*")
        out.append("")
        return out
    out.append("| Skill | Category | Version | What it is for | Path |")
    out.append("|-------|----------|---------|----------------|------|")
    for name, category, version, purpose, rel in rows:
        link = _link_from_docs(rel)
        out.append(
            f"| `{_cell(name)}` | {_cell(category)} | {_cell(version)} | "
            f"{_cell(purpose)} | [SKILL.md]({link}) |"
        )
    out.append("")
    return out


def _render_external_section(root: Path) -> list[str]:
    references = parse_link_files(root)
    descriptions = load_external_descriptions(root)
    out = ["## External Skills (Links Only)", ""]
    out.append(
        "Third-party skills referenced by upstream URL only; no local copy is "
        "bundled. Source: `catalog/links/skill-links.txt` (stable branches) and "
        "`catalog/links/pinned-links.txt` (pinned commits or release branches)."
    )
    out.append("")
    out.append(
        "Entries with a short description have curated metadata in "
        "`catalog/items.json`; entries without one are link-only."
    )
    out.append("")
    if not references:
        out.append("*None found.*")
        out.append("")
        return out

    total = len(references)
    out.append(f"Total: **{total}** references.")
    out.append("")

    by_repo = {}
    for ref in references:
        by_repo.setdefault(ref['repo'], []).append(ref)

    for repo in sorted(by_repo):
        refs = by_repo[repo]
        out.append(f"### {repo} ({len(refs)})")
        out.append("")
        for ref in refs:
            description = descriptions.get(ref['url'])
            suffix = f" — {_cell(description)}" if description else ""
            out.append(f"- [`{ref['name']}`]({ref['url']}){suffix}")
        out.append("")
    return out


# --- repository counts -----------------------------------------------------

COUNTS_BLOCK_START = '<!-- counts:start -->'
COUNTS_BLOCK_END = '<!-- counts:end -->'

# Each target file lists the count keys it shows. The block between the two
# markers is generated; the surrounding prose stays hand written. The counts
# are derived from catalog/items.json and the filesystem - never typed twice.
COUNT_TARGETS = {
    'README.md': (
        'original_skills', 'bundled_third_party', 'external_link_only',
        'stable_links', 'pinned_links', 'catalog_records',
        'system_prompts', 'personas', 'image_prompts', 'modules', 'profiles',
    ),
    'catalog/README.md': (
        'catalog_records', 'catalog_original', 'catalog_link_only',
        'stable_links', 'pinned_links', 'bundled_third_party',
    ),
    'ATTRIBUTION.md': (
        'catalog_original', 'catalog_link_only', 'catalog_records',
        'bundled_third_party',
    ),
    'skills/third-party/README.md': (
        'external_link_only', 'bundled_third_party',
    ),
}

COUNT_LABELS = {
    'original_skills': ('Original skills', '`skills/original/` - authored and maintained here'),
    'bundled_third_party': ('Bundled third-party skills', '`skills/third-party/` - local copies of upstream `SKILL.md` files'),
    'external_link_only': ('External link-only skills', 'referenced by URL; no content copied'),
    'stable_links': ('Stable-branch links', '`catalog/links/skill-links.txt`'),
    'pinned_links': ('Pinned links', '`catalog/links/pinned-links.txt`'),
    'catalog_records': ('Catalog records', '`catalog/items.json`'),
    'catalog_original': ('Catalog records with `authorship: original`', ''),
    'catalog_link_only': ('Catalog records with `authorship: link-only`', ''),
    'system_prompts': ('System prompts', '`prompts/system/`'),
    'personas': ('Personas', '`prompts/personas/`'),
    'image_prompts': ('Image prompts', '`prompts/image/`'),
    'modules': ('Instruction modules', '`instructions/modules/`'),
    'profiles': ('Agent profiles', '`instructions/profiles/`'),
}


def _count_skill_files(base: Path) -> int:
    """Count SKILL.md files under a directory, honouring the exclusion list."""
    if not base.is_dir():
        return 0
    return sum(
        1
        for path in base.rglob('SKILL.md')
        if path.is_file()
        and not path.is_symlink()
        and not EXCLUDE_DIR_NAMES.intersection(path.relative_to(base).parts[:-1])
    )


def _count_markdown_files(base: Path) -> int:
    """Count the Markdown files in a directory."""
    if not base.is_dir():
        return 0
    return sum(1 for path in base.glob('*.md') if path.is_file())


def compute_counts(root: Path) -> dict[str, int]:
    """Return the repository counts derived from the catalog and the filesystem."""
    counts: dict[str, int] = {}
    counts['original_skills'] = sum(1 for _ in iter_local_skills(root, 'skills/original'))
    counts['bundled_third_party'] = _count_skill_files(root / 'skills' / 'third-party')

    links_dir = root.joinpath(*LINK_DIR)
    per_file: list[int] = []
    for filename in LINK_FILES:
        path = links_dir / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing authoritative link file: {path}")
        urls = [line.strip() for line in path.read_text(encoding='utf-8-sig').splitlines()]
        per_file.append(sum(1 for url in urls if url and not url.startswith('#')))
    counts['stable_links'] = per_file[0]
    counts['pinned_links'] = per_file[1]
    counts['external_link_only'] = sum(per_file)

    items_path = root.joinpath(*ITEMS_RELPATH)
    records = []
    if items_path.is_file():
        try:
            loaded = json.loads(items_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            loaded = []
        if isinstance(loaded, list):
            records = loaded
    counts['catalog_records'] = len(records)
    counts['catalog_original'] = sum(
        1 for record in records
        if isinstance(record, dict) and record.get('authorship') == 'original')
    counts['catalog_link_only'] = sum(
        1 for record in records
        if isinstance(record, dict) and record.get('authorship') == 'link-only')

    counts['system_prompts'] = _count_markdown_files(root / 'prompts' / 'system')
    counts['personas'] = _count_markdown_files(root / 'prompts' / 'personas')
    counts['image_prompts'] = _count_markdown_files(root / 'prompts' / 'image')
    counts['modules'] = _count_markdown_files(root / 'instructions' / 'modules')
    counts['profiles'] = _count_markdown_files(root / 'instructions' / 'profiles')
    return counts


def render_counts_block(counts: dict[str, int], keys: tuple[str, ...]) -> str:
    """Render the generated count table for one file."""
    lines = ['| What | Count | Where |', '|------|------:|-------|']
    for key in keys:
        label, where = COUNT_LABELS[key]
        lines.append(f'| {label} | {counts[key]} | {where} |')
    return '\n'.join(lines)


def update_counts_blocks(root: Path, write: bool) -> list[str]:
    """Update (or verify) the generated count blocks in the target files.

    A target file that does not exist is skipped - the counts blocks are an
    optional integration, not a reason to fail the index generation. A target
    file that exists without the markers is a problem, because the numbers
    would silently go stale.
    """
    counts = compute_counts(root)
    problems: list[str] = []
    for rel_path, keys in COUNT_TARGETS.items():
        path = root / rel_path
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        if COUNTS_BLOCK_START not in text or COUNTS_BLOCK_END not in text:
            problems.append(f"counts markers are missing: {rel_path}")
            continue
        start = text.index(COUNTS_BLOCK_START)
        end = text.index(COUNTS_BLOCK_END)
        block = render_counts_block(counts, keys)
        updated = text[:start] + COUNTS_BLOCK_START + '\n\n' + block + '\n\n' + text[end:]
        if updated == text:
            continue
        if write:
            path.write_text(updated, encoding='utf-8', newline='\n')
        else:
            problems.append(f"counts block is stale: {rel_path}")
    return problems


# --- entry point -----------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--root', default=None,
        help='Repository root (defaults to the parent of this script).',
    )
    parser.add_argument(
        '--check', action='store_true',
        help='Do not write; exit 1 if the generated index or count blocks are stale.',
    )
    args = parser.parse_args(argv)

    root = resolve_root(args.root)
    if not root.is_dir():
        print(f"Repository root not found: {root}")
        return 1

    output_path = root.joinpath(*INDEX_RELPATH)
    try:
        content = generate(root)
        counts_problems = update_counts_blocks(root, write=not args.check)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    for problem in counts_problems:
        print(f"ERROR: {problem}")

    if args.check:
        if not output_path.is_file():
            print(f"STALE: {output_path} does not exist")
            return 1
        existing = output_path.read_text(encoding='utf-8')
        if existing.replace('\r\n', '\n') != content:
            print(f"STALE: {output_path} does not match the generated index")
            return 1
        if counts_problems:
            return 1
        print(f"OK: {output_path} is up to date")
        return 0

    output_path.write_text(content, encoding='utf-8', newline='\n')
    print(f"Wrote {output_path}")
    if counts_problems:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
