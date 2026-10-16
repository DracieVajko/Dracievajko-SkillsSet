#!/usr/bin/env python3
"""
Regenerate docs/CATEGORY_INDEX.md from the catalog and the real local tree.

Authoritative inputs (exactly one source of truth per generated section)

    Section                       Authoritative source
    ----------------------------  ---------------------------------------------
    Original local skills         filesystem: 01-my-skills/**/SKILL.md
    Modified local skills         filesystem: 02-my-modified-skills/**/SKILL.md
    Third-party local skills      filesystem: 03-third-party-skills/**/SKILL.md
    Link-only references          03-third-party-skills/odysseus/skill-links.txt
                                  plus .../unverified-links.txt
    Unresolved inventory entries  catalog/items.json (authorship == "unresolved")
    Notes (catalog/local drift)   catalog/items.json (local_skill_path column)

catalog/items.json is the only structured catalog this generator trusts. A
missing or malformed authoritative input is a hard error (exit 1); it is never
silently treated as an empty collection.

Historical / derived catalog files that are deliberately NOT read here and never
override the sources above: custom-skills.json, custom-or-unresolved.json,
unresolved-sources.json, unresolved.md, items.csv, catalog-reconciliation.csv,
provenance-tracking.json, skills-catalog.json, categories/, presets/.
See catalog/README.md for the authority map and documented scope differences.

Groups produced
    Original local skills
    Modified local skills
    Third-party local skills
    Link-only references
    Unresolved inventory entries

The output is deterministic (no timestamps): identical inputs produce an
identical index. Link-only references are reported as upstream URLs, never as
missing local files.

Usage
    python scripts/update-category-index.py            # write the index
    python scripts/update-category-index.py --check    # exit 1 if stale, no writes

Exit codes
    0 = index written, or (--check) committed index is up to date
    1 = error, or (--check) the committed index is stale/missing
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

SKILL_ROOTS = {
    '01-my-skills': 'Original local skills',
    '02-my-modified-skills': 'Modified local skills',
    '03-third-party-skills': 'Third-party local skills',
}

EXCLUDE_DIR_NAMES = {
    '_backups',
    '_source-backups',
    '_private-review',
    'SystemPrompts',
    'ultimate-agent-library',
    'Dracievajko-AI-Agent-Collection-Public',
    'Dracievajko-Skills-Unified',
    'Dracievajko-SkillsSet',
    '.git',
    'node_modules',
}

CATALOG_PATH = ('catalog', 'items.json')
INDEX_RELPATH = ('docs', 'CATEGORY_INDEX.md')
ODYSSEUS_DIR = ('03-third-party-skills', 'odysseus')
LINK_FILES = ('skill-links.txt', 'unverified-links.txt')


# --- helpers ---------------------------------------------------------------

def resolve_root(cli_root):
    if cli_root:
        return Path(cli_root).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def read_catalog(root):
    """Return the parsed catalog records, raising on missing/invalid input."""
    catalog_path = root / 'catalog' / 'items.json'
    if not catalog_path.is_file():
        raise FileNotFoundError(f"Catalog file not found: {catalog_path}")
    try:
        data = json.loads(catalog_path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot parse {catalog_path}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError(f"{catalog_path} must contain a JSON array")
    return data


def iter_local_skills(root, root_name):
    """Yield (skill_md, frontmatter_or_None) for one skill root, deterministically."""
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


def _read_frontmatter(skill_md):
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


def parse_link_files(root):
    """Return sorted [{repo, name, url, source_file}] from the odysseus link files.

    Both link files are authoritative for the link-only section, so a missing
    file is an error rather than an empty reference list.
    """
    ody = root / '03-third-party-skills' / 'odysseus'
    references = []
    missing = []
    for filename in LINK_FILES:
        path = ody / filename
        if not path.is_file():
            missing.append(str(path))
            continue
        for raw in path.read_text(encoding='utf-8').splitlines():
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


def _repo_from_url(url):
    parts = url.split('/')
    if 'raw.githubusercontent.com' in url and len(parts) >= 5:
        return f"{parts[3]}/{parts[4]}"
    return 'unknown'


def _name_from_url(url):
    parts = [p for p in url.split('/') if p]
    if len(parts) >= 2 and parts[-1] == 'SKILL.md':
        return parts[-2]
    return parts[-1] if parts else url


def _link_from_docs(target_rel_path):
    """Relative Markdown link from docs/CATEGORY_INDEX.md to a repo-relative path."""
    return f"../{target_rel_path.replace('\\', '/')}"


def _cell(text):
    """Escape a value for a Markdown table cell."""
    return str(text if text is not None else '').replace('|', '\\|')


# --- generation ------------------------------------------------------------

def generate(root):
    """Return the full CATEGORY_INDEX.md content as a string."""
    catalog = read_catalog(root)
    notes = []

    lines = []
    lines.append("# Category Index")
    lines.append("")
    lines.append("Auto-generated by `scripts/update-category-index.py`. Do not edit by hand.")
    lines.append("Validate the tree with `python scripts/validate-frontmatter.py`.")
    lines.append("")
    lines.append("Local skills are discovered on disk; link-only references come from the")
    lines.append("`03-third-party-skills/odysseus/` link files and unresolved entries from")
    lines.append("`catalog/items.json`. Link-only references have no local copy.")
    lines.append("")
    lines.append("Authoritative source per section:")
    lines.append("")
    lines.append("| Section | Authoritative source |")
    lines.append("|---------|----------------------|")
    lines.append("| Original / Modified / Third-party local skills | the local tree under that root |")
    lines.append("| Link-only references | `03-third-party-skills/odysseus/skill-links.txt` + `unverified-links.txt` |")
    lines.append("| Unresolved inventory entries | `catalog/items.json` (`authorship: unresolved`) |")
    lines.append("")

    disk_paths = set()
    for root_name in SKILL_ROOTS:
        lines.extend(_render_local_section(root, root_name, disk_paths, notes))

    lines.extend(_render_link_only_section(root, notes))
    lines.extend(_render_unresolved_section(catalog))
    lines.extend(_render_notes_section(catalog, disk_paths, notes))

    lines.append("---")
    lines.append("")
    lines.append("*Generated from `catalog/items.json`, the Odysseus link files, and the "
                 "local tree. Regenerate with `python scripts/update-category-index.py`.*")
    return '\n'.join(lines) + '\n'


def _render_local_section(root, root_name, disk_paths, notes):
    title = SKILL_ROOTS[root_name]
    rows = []
    for skill_md, frontmatter in iter_local_skills(root, root_name):
        rel = skill_md.relative_to(root).as_posix()
        disk_paths.add(rel)
        folder = skill_md.parent.name
        if frontmatter is None:
            name = folder
            category = '—'
            version = '—'
            notes.append(f"Unreadable or malformed frontmatter: `{rel}`")
        else:
            name = frontmatter.get('name', folder)
            category = frontmatter.get('category', '—')
            version = frontmatter.get('version', '—')
            if name != folder:
                notes.append(
                    f"Frontmatter name '{name}' does not match folder '{folder}': `{rel}`"
                )
        rows.append((name, category, version, rel))

    rows.sort(key=lambda r: (str(r[0]), r[3]))

    out = [f"## {title}", "", f"Discovered under `{root_name}/`.", ""]
    if not rows:
        out.append("*None.*")
        out.append("")
        return out
    out.append("| Skill | Category | Version | Path |")
    out.append("|-------|----------|---------|------|")
    for name, category, version, rel in rows:
        link = _link_from_docs(rel)
        out.append(f"| `{_cell(name)}` | {_cell(category)} | {_cell(version)} | [SKILL.md]({link}) |")
    out.append("")
    return out


def _render_link_only_section(root, notes):
    references = parse_link_files(root)
    out = ["## Link-Only References", ""]
    out.append(
        "Third-party skills referenced by upstream URL only; no local copy is "
        "bundled. Source: `03-third-party-skills/odysseus/skill-links.txt` "
        "(stable branches) and `unverified-links.txt` (pinned release branch)."
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
            out.append(f"- [`{ref['name']}`]({ref['url']})")
        out.append("")
    return out


def _render_unresolved_section(catalog):
    unresolved = [item for item in catalog if item.get('authorship') == 'unresolved']
    out = ["## Unresolved Inventory Entries", ""]
    out.append(
        "Catalog records with no confirmed upstream source and no local content "
        "(authorship `unresolved` in `catalog/items.json`)."
    )
    out.append("")
    if not unresolved:
        out.append("*None.*")
        out.append("")
        return out
    rows = sorted(
        ((item.get('name', ''), item.get('category', '—'), item.get('verification', '—'))
         for item in unresolved),
        key=lambda r: str(r[0]),
    )
    out.append(f"Total: **{len(rows)}** records.")
    out.append("")
    out.append("| Name | Category | Status |")
    out.append("|------|----------|--------|")
    for name, category, status in rows:
        out.append(f"| `{_cell(name)}` | {_cell(category)} | {_cell(status)} |")
    out.append("")
    return out


def _render_notes_section(catalog, disk_paths, notes):
    by_path = {}
    for item in catalog:
        local_path = item.get('local_skill_path') or ''
        if not local_path:
            continue
        rel = Path(local_path).as_posix()
        by_path.setdefault(rel, []).append(item)
        if rel not in disk_paths:
            notes.append(f"Catalog lists a local copy that is missing on disk: `{local_path}`")

    for path, records in sorted(by_path.items()):
        if len(records) > 1:
            ids = ', '.join(f"`{record.get('id', '?')}`" for record in records)
            notes.append(
                f"Catalog lists {len(records)} records for the same local path `{path}` "
                f"(distinct upstream references, not confirmed origins): {ids}"
            )

    catalog_path_set = set(by_path)
    for rel in sorted(disk_paths - catalog_path_set):
        notes.append(f"Local skill not present in the catalog: `{rel}`")

    out = ["## Notes", ""]
    if not notes:
        out.append("No discrepancies found between the catalog and the local tree.")
        out.append("")
        return out
    out.append("Catalog/local-tree discrepancies (deterministic, sorted):")
    out.append("")
    for note in sorted(set(notes)):
        out.append(f"- {note}")
    out.append("")
    return out


# --- entry point -----------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--root', default=None,
        help='Repository root (defaults to the parent of this script).',
    )
    parser.add_argument(
        '--check', action='store_true',
        help='Do not write; exit 1 if docs/CATEGORY_INDEX.md is stale or missing.',
    )
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve() if args.root else Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print(f"Repository root not found: {root}")
        return 1

    output_path = root / 'docs' / 'CATEGORY_INDEX.md'
    try:
        content = generate(root)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.check:
        if not output_path.is_file():
            print(f"STALE: {output_path} does not exist")
            return 1
        existing = output_path.read_text(encoding='utf-8')
        if existing.replace('\r\n', '\n') != content:
            print(f"STALE: {output_path} does not match the generated index")
            return 1
        print(f"OK: {output_path} is up to date")
        return 0

    output_path.write_text(content, encoding='utf-8', newline='\n')
    print(f"Wrote {output_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
