#!/usr/bin/env python3
"""
Validate SKILL.md frontmatter across the collection's skill roots.

Discovery root (recursive, deterministic):
    skills/original/

Field classification (per creating-skills/SKILL.md: "YAML frontmatter
(name, description required)"):

    Required platform fields   -> name, description          (errors if absent/empty)
    Optional metadata          -> version, author, category, license,
                                  status, tags, compatibility
    Repository style advisories-> missing optional metadata, unknown category,
                                  non-semver version, long description,
                                  long SKILL.md                      (warnings)

Name collisions are errors when they occur inside the same discovery scope
(one skill bucket under skills/) and warnings when they occur across scopes,
where the same name may be a deliberate variant for a separate interface.

This script validates frontmatter structure only. It does NOT verify
provenance, licenses, upstream sources, URLs, or runtime behaviour.

Exit code 0 = no errors (warnings allowed).
Exit code 1 = at least one validation error.
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml

# --- configuration ---------------------------------------------------------

SKILL_ROOTS = [
    'skills/original',
]

# Directories that must never be part of skill discovery.
EXCLUDE_DIR_NAMES = {
    '_backups',
    '_source-backups',
    '_private-review',
    '.git',
    'node_modules',
}

REQUIRED_FIELDS = ('name', 'description')

# Reasonable superset of categories used by SKILL.md files and the catalog.
KNOWN_CATEGORIES = {
    'core', 'development', 'design', 'ai-ml', '3d-blender',
    'productivity', 'web-automation', 'thinking-frameworks', 'writing-docs',
    'third-party', 'custom', 'investing', 'research', 'local-ai-infra',
}

DESCRIPTION_STYLE_ADVISORY = 160   # repository style
DESCRIPTION_DOC_LIMIT = 500        # documented authoring guidance ("under 500 characters")
SKILL_LINES_DOC_LIMIT = 500        # documented guidance ("Keep SKILL.md under 500 lines")


# --- discovery -------------------------------------------------------------

def resolve_root(cli_root):
    """Resolve the repository root, independent of the current directory."""
    if cli_root:
        return Path(cli_root).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def iter_skill_files(root):
    """Yield SKILL.md files under the configured roots, deterministically.

    Skips excluded directories and symlinks so discovery cannot escape the
    intended roots. Returns (skill_files, missing_roots).
    """
    found = []
    missing = []
    for root_name in SKILL_ROOTS:
        root_dir = root / root_name
        if not root_dir.is_dir():
            missing.append(root_name)
            continue
        for path in root_dir.rglob('SKILL.md'):
            if path.is_symlink():
                continue
            rel_parts = path.relative_to(root).parts
            if EXCLUDE_DIR_NAMES.intersection(rel_parts[:-1]):
                continue
            found.append(path)
    return sorted(found), missing


# --- validation ------------------------------------------------------------

def parse_frontmatter(skill_md):
    """Read a SKILL.md and return (frontmatter, content, error_message)."""
    try:
        content = skill_md.read_text(encoding='utf-8')
    except OSError as exc:
        return None, '', f"Cannot read {skill_md}: {exc}"

    if not content.startswith('---'):
        return None, content, f"No YAML frontmatter found in {skill_md}"

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content, f"Malformed frontmatter (missing closing '---') in {skill_md}"

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        return None, content, f"Invalid YAML in {skill_md}: {exc}"

    if not isinstance(frontmatter, dict):
        return None, content, f"Frontmatter is not a mapping in {skill_md}"
    return frontmatter, content, None


def validate_skill(skill_md, frontmatter, text):
    """Return (errors, warnings) for one skill."""
    errors = []
    warnings = []

    for field in REQUIRED_FIELDS:
        value = frontmatter.get(field)
        if field not in frontmatter:
            errors.append(f"Missing required field '{field}' in {skill_md}")
        elif value is None or str(value).strip() == '':
            errors.append(f"Empty required field '{field}' in {skill_md}")

    name = frontmatter.get('name')
    if name and name != skill_md.parent.name:
        errors.append(
            f"Skill name '{name}' does not match folder "
            f"'{skill_md.parent.name}' in {skill_md}"
        )

    for field in ('version', 'author', 'category'):
        if not frontmatter.get(field):
            warnings.append(f"Optional field '{field}' not set in {skill_md}")

    category = frontmatter.get('category')
    if category and category not in KNOWN_CATEGORIES:
        warnings.append(f"Unknown category '{category}' in {skill_md}")

    version = frontmatter.get('version')
    if version is not None:
        parts = str(version).split('.')
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            warnings.append(f"Version '{version}' is not MAJOR.MINOR.PATCH in {skill_md}")

    description = frontmatter.get('description') or ''
    if len(description) > DESCRIPTION_DOC_LIMIT:
        warnings.append(
            f"Description is {len(description)} chars, above the documented "
            f"{DESCRIPTION_DOC_LIMIT}-char guidance, in {skill_md}"
        )
    elif len(description) > DESCRIPTION_STYLE_ADVISORY:
        warnings.append(
            f"Description is {len(description)} chars, above the repository "
            f"{DESCRIPTION_STYLE_ADVISORY}-char style advisory, in {skill_md}"
        )

    line_count = len(text.splitlines())
    if line_count >= SKILL_LINES_DOC_LIMIT:
        warnings.append(
            f"SKILL.md is {line_count} lines, at or above the documented "
            f"{SKILL_LINES_DOC_LIMIT}-line guidance, in {skill_md}"
        )

    return errors, warnings


def check_name_collisions(records):
    """Return (errors, warnings) for duplicate skill names.

    A record is a dict with keys: name, scope, path.
    """
    errors = []
    warnings = []
    by_name = defaultdict(list)
    for record in records:
        by_name[record['name']].append(record)

    for name, recs in sorted(by_name.items()):
        if len(recs) < 2:
            continue
        by_scope = defaultdict(list)
        for rec in recs:
            by_scope[rec['scope']].append(rec)
        for scope, scoped in sorted(by_scope.items()):
            if len(scoped) > 1:
                paths = ', '.join(str(r['path']) for r in scoped)
                errors.append(
                    f"Duplicate skill name '{name}' in scope '{scope}': {paths}"
                )
        if len(by_scope) > 1:
            scopes = ', '.join(sorted(by_scope))
            warnings.append(
                f"Name '{name}' appears in multiple scopes ({scopes}); "
                "treat as a deliberate variant unless unintended"
            )
    return errors, warnings


# --- entry point -----------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--root', default=None,
        help='Repository root (defaults to the parent of this script).',
    )
    args = parser.parse_args(argv)

    root = resolve_root(args.root)
    if not root.is_dir():
        print(f"Repository root not found: {root}")
        return 1

    skill_files, missing_roots = iter_skill_files(root)

    errors = []
    warnings = []
    records = []

    for root_name in missing_roots:
        errors.append(f"Missing required skill root '{root_name}/' under {root}")

    for skill_md in skill_files:
        frontmatter, text, error = parse_frontmatter(skill_md)
        if error:
            errors.append(error)
            continue
        skill_errors, skill_warnings = validate_skill(skill_md, frontmatter, text)
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)
        records.append({
            'name': frontmatter.get('name'),
            'scope': _scope(root, skill_md),
            'path': skill_md.relative_to(root),
        })

    collision_errors, collision_warnings = check_name_collisions(records)
    errors.extend(collision_errors)
    warnings.extend(collision_warnings)

    print(f"Validated {len(skill_files)} skills under {root}")
    print(f"  roots: {', '.join(SKILL_ROOTS)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} errors, {len(warnings)} warnings")
        return 1
    print(f"OK: 0 errors, {len(warnings)} warnings")
    return 0


def _scope(root, skill_md):
    """Discovery scope = skill bucket under the repo root (e.g. skills/third-party)."""
    rel = skill_md.relative_to(root)
    root_name = rel.parts[0] if rel.parts else ''
    branch = rel.parts[1] if len(rel.parts) > 3 else ''
    return f"{root_name}/{branch}" if branch else root_name


if __name__ == '__main__':
    sys.exit(main())
