#!/usr/bin/env python3
"""
Auto-generate CATEGORY_INDEX.md from skills directory.
Run after adding/removing skills to keep index in sync.
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

CATEGORIES = [
    ('core', 'Core Skills', 'Essential workflow skills that should be available in every agent session.'),
    ('development', 'Development Skills', 'Software engineering, code quality, and development workflow skills.'),
    ('design', 'Design Skills', 'UI/UX design, frontend interfaces, and visual systems.'),
    ('ai-ml', 'AI/ML Skills', 'Model training, fine-tuning, and deployment.'),
    ('3d-blender', '3D/Blender Skills', 'Blender 3D modeling, animation, and automation workflows.'),
    ('productivity', 'Productivity Skills', 'Personal task management, organization, and productivity tools.'),
    ('web-automation', 'Web Automation', 'Browser automation, testing, and web interaction.'),
    ('thinking-frameworks', 'Thinking Frameworks', 'Mental models, decision frameworks, and structured thinking.'),
    ('writing-docs', 'Writing & Documentation', 'Content creation, documentation, and writing assistance.'),
    ('third-party', 'Third-Party Skills', 'Cataloged third-party skills with upstream sources (link-only).'),
    ('custom', 'Custom Skills', 'User-created skills with no upstream source.'),
]

STATUS_MAP = {
    'active': '✅ Active',
    'planned': '📋 Planned',
    'in-progress': '🔄 In Progress',
    'deprecated': '⚠️ Deprecated',
}

def load_skill_info(skill_path):
    """Load skill info from SKILL.md frontmatter."""
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return None

    try:
        content = skill_md.read_text(encoding='utf-8')
        if not content.startswith('---'):
            return None
        _, fm_content, _ = content.split('---', 2)
        fm = yaml.safe_load(fm_content)
        return fm
    except Exception:
        return None

def get_status(fm):
    """Determine skill status from frontmatter."""
    if fm and 'status' in fm:
        return fm['status'].lower()
    if fm and all(k in fm for k in ['name', 'description', 'version']):
        return 'active'
    return 'planned'

def format_table_row(fm, status):
    """Format a single row for the category table."""
    skill_id = fm.get('name', 'unknown')
    name = fm.get('name', 'Unknown').replace('-', ' ').title()
    desc = fm.get('description', 'No description')
    ver = fm.get('version', '0.0.0')
    status_badge = STATUS_MAP.get(status.lower(), '📋 Planned')

    return f"| `{skill_id}` | {name} | {status_badge} | {desc} |"

def generate_index():
    """Generate the full CATEGORY_INDEX.md content."""
    skills_dir = Path(__file__).parent.parent / 'skills'
    output_path = Path(__file__).parent.parent / 'docs' / 'CATEGORY_INDEX.md'

    lines = []
    lines.append("# Category Index — Complete Skill Listing")
    lines.append("")
    lines.append("Auto-generated index of all skills in this repository, organized by category.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for cat_id, cat_name, cat_desc in CATEGORIES:
        cat_dir = skills_dir / cat_id
        lines.append(f"## {cat_name} (`skills/{cat_id}/`)")
        lines.append("")
        lines.append(cat_desc)
        lines.append("")

        if cat_dir.exists():
            skills = []
            for skill_dir in sorted(cat_dir.iterdir()):
                if skill_dir.is_dir():
                    fm = load_skill_info(skill_dir)
                    if fm:
                        status = get_status(fm)
                        skills.append((skill_dir.name, fm, status))

            if skills:
                lines.append("| Skill ID | Name | Status | Description |")
                lines.append("|----------|------|--------|-------------|")
                for _, fm, status in skills:
                    lines.append(format_table_row(fm, status))
            else:
                lines.append("*No skills in this category yet.*")
        else:
            lines.append("*Category directory not found.*")

        lines.append("")
        lines.append("---")
        lines.append("")

    # Legend
    lines.append("## Legend")
    lines.append("")
    lines.append("- ✅ **Active** — Fully implemented, tested, ready to use")
    lines.append("- 📋 **Planned** — Specified in collection, not yet implemented")
    lines.append("- 🔄 **In Progress** — Currently being developed")
    lines.append("- ⚠️ **Deprecated** — Superseded or no longer maintained")
    lines.append("")
    lines.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*")
    lines.append(f"*Run `scripts/update-category-index.py` to regenerate this index*")

    return '\n'.join(lines)

def main():
    content = generate_index()
    output_path = Path(__file__).parent.parent / 'docs' / 'CATEGORY_INDEX.md'

    existing = ''
    if output_path.exists():
        existing = output_path.read_text(encoding='utf-8')

    if content.strip() != existing.strip():
        output_path.write_text(content, encoding='utf-8')
        print(f"Updated {output_path}")
    else:
        print("Category index already up to date")

if __name__ == '__main__':
    main()