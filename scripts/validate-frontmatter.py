#!/usr/bin/env python3
"""
Validate frontmatter in all SKILL.md files.
Checks for required fields, valid YAML, and category consistency.
"""

import os
import sys
import yaml
from pathlib import Path

REQUIRED_FIELDS = ['name', 'description', 'version', 'author', 'category']
VALID_CATEGORIES = [
    'core', 'development', 'design', 'ai-ml', '3d-blender',
    'productivity', 'web-automation', 'thinking-frameworks', 'writing-docs',
    'third-party', 'custom'
]

def validate_skill(skill_path):
    """Validate a single skill's SKILL.md file."""
    errors = []
    warnings = []

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        errors.append(f"Missing SKILL.md in {skill_path}")
        return errors, warnings

    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        errors.append(f"Cannot read {skill_md}: {e}")
        return errors, warnings

    # Extract frontmatter
    if not content.startswith('---'):
        errors.append(f"No frontmatter found in {skill_md}")
        return errors, warnings

    try:
        _, fm_content, _ = content.split('---', 2)
        frontmatter = yaml.safe_load(fm_content)
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in {skill_md}: {e}")
        return errors, warnings
    except ValueError:
        errors.append(f"Malformed frontmatter in {skill_md}")
        return errors, warnings

    if frontmatter is None:
        errors.append(f"Empty frontmatter in {skill_md}")
        return errors, warnings

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field '{field}' in {skill_md}")
        elif not frontmatter[field]:
            errors.append(f"Empty required field '{field}' in {skill_md}")

    # Validate category
    category = frontmatter.get('category')
    if category and category not in VALID_CATEGORIES:
        warnings.append(f"Unknown category '{category}' in {skill_md} (valid: {VALID_CATEGORIES})")

    # Check name matches folder
    folder_name = skill_path.name
    skill_name = frontmatter.get('name')
    if skill_name and skill_name != folder_name:
        errors.append(f"Skill name '{skill_name}' != folder name '{folder_name}' in {skill_md}")

    # Check description length
    desc = frontmatter.get('description', '')
    if len(desc) > 160:
        warnings.append(f"Description too long ({len(desc)} chars, max 160) in {skill_md}")

    # Validate version format (basic semver)
    version = frontmatter.get('version', '')
    if version:
        parts = version.split('.')
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            warnings.append(f"Version '{version}' not semantic (MAJOR.MINOR.PATCH) in {skill_md}")

    return errors, warnings


def main():
    skills_dir = Path(__file__).parent.parent / 'skills'
    if not skills_dir.exists():
        print(f"Skills directory not found: {skills_dir}")
        sys.exit(1)

    all_errors = []
    all_warnings = []
    skill_count = 0

    for category_dir in skills_dir.iterdir():
        if not category_dir.is_dir():
            continue
        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_count += 1
            errors, warnings = validate_skill(skill_dir)
            all_errors.extend(errors)
            all_warnings.extend(warnings)

    print(f"Validated {skill_count} skills")
    print()

    if all_warnings:
        print("WARNINGS:")
        for w in all_warnings:
            print(f"  ⚠ {w}")
        print()

    if all_errors:
        print("ERRORS:")
        for e in all_errors:
            print(f"  ✗ {e}")
        print()
        print(f"Total: {len(all_errors)} errors, {len(all_warnings)} warnings")
        sys.exit(1)
    else:
        print("✓ All skills valid")
        if all_warnings:
            print(f"  ({len(all_warnings)} warnings)")
        sys.exit(0)


if __name__ == '__main__':
    main()