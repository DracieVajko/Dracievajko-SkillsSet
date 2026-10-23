#!/usr/bin/env python3
"""
Check that duplicated rule copies have not drifted.

Source of truth
    instructions/modules/*.md

Derived copies
    instructions/opencode/project-template/agent-rules/*.md
    instructions/profiles/*.md                  (embedded module body)
    AGENTS-combined.md                          (embedded module body)
    AGENTS.md                                   (task-routing references)
    instructions/opencode/project-template/AGENTS.md

Usage
    python scripts/check-sync.py
    python scripts/check-sync.py --root <repository-root>

Exit codes
    0 = all copies are synchronized
    1 = at least one mismatch, missing file or stale routing entry
"""

import argparse
import sys
from pathlib import Path

MODULES_REL = Path('instructions') / 'modules'
TEMPLATE_REL = Path('instructions') / 'opencode' / 'project-template' / 'agent-rules'
PROFILES_REL = Path('instructions') / 'profiles'
COMBINED_REL = Path('AGENTS-combined.md')
AGENTS_REL = Path('AGENTS.md')
PROJECT_AGENTS_REL = Path('instructions') / 'opencode' / 'project-template' / 'AGENTS.md'

# One profile embeds one domain module.
PROFILE_MODULES = {
    'coding-agent.md': 'coding.md',
    'debugging-agent.md': 'debugging.md',
    'document-agent.md': 'documents.md',
    'engineering-agent.md': 'engineering-3d.md',
    'frontend-agent.md': 'frontend.md',
    'investing-agent.md': 'investing.md',
    'local-ai-agent.md': 'local-ai-infra.md',
    'planning-agent.md': 'planning.md',
    'research-agent.md': 'research-learning.md',
}


def normalize(text):
    return text.replace('\r\n', '\n').strip()


def read_text(path):
    return normalize(path.read_text(encoding='utf-8'))


def module_files(root):
    base = root / MODULES_REL
    if not base.is_dir():
        raise FileNotFoundError(f"Missing module directory: {base}")
    return sorted(path for path in base.glob('*.md') if path.is_file())


def check_module_copies(root, errors):
    modules = module_files(root)
    template_dir = root / TEMPLATE_REL
    if not template_dir.is_dir():
        errors.append(f"Missing template rule directory: {template_dir}")
        return modules
    template_files = sorted(path.name for path in template_dir.glob('*.md') if path.is_file())
    module_names = [path.name for path in modules]
    for missing in sorted(set(module_names) - set(template_files)):
        errors.append(f"Missing template copy: {TEMPLATE_REL / missing}")
    for extra in sorted(set(template_files) - set(module_names)):
        errors.append(f"Template copy has no source module: {TEMPLATE_REL / extra}")
    for module in modules:
        copy = template_dir / module.name
        if copy.is_file() and read_text(module) != read_text(copy):
            errors.append(f"Template copy differs from module: {module.relative_to(root)}")
    return modules


def check_profiles(root, errors):
    profiles_dir = root / PROFILES_REL
    for profile_name, module_name in PROFILE_MODULES.items():
        profile = profiles_dir / profile_name
        module = root / MODULES_REL / module_name
        if not profile.is_file():
            errors.append(f"Missing profile: {profile.relative_to(root)}")
            continue
        if not module.is_file():
            errors.append(f"Missing module for profile {profile_name}: {module.relative_to(root)}")
            continue
        if read_text(module) not in read_text(profile):
            errors.append(f"Profile does not embed module: {profile.relative_to(root)} <- {module.relative_to(root)}")


def check_combined(root, errors, modules):
    combined = root / COMBINED_REL
    if not combined.is_file():
        errors.append(f"Missing combined rule file: {COMBINED_REL}")
        return
    combined_text = read_text(combined)
    for module in modules:
        if read_text(module) not in combined_text:
            errors.append(f"AGENTS-combined.md is missing module: {module.relative_to(root)}")


def check_routing(root, errors, modules):
    agents = root / AGENTS_REL
    project_agents = root / PROJECT_AGENTS_REL
    agents_text = read_text(agents) if agents.is_file() else ''
    project_text = read_text(project_agents) if project_agents.is_file() else ''
    if not agents.is_file():
        errors.append(f"Missing routing file: {AGENTS_REL}")
    if not project_agents.is_file():
        errors.append(f"Missing routing file: {PROJECT_AGENTS_REL}")
    for module in modules:
        name = module.name
        if f"instructions/modules/{name}" not in agents_text:
            errors.append(f"AGENTS.md task routing is missing: instructions/modules/{name}")
        if f"- {name}:" not in project_text:
            errors.append(f"Project template routing is missing: {name}")


def main(argv=None):
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

    errors = []
    try:
        modules = check_module_copies(root, errors)
        check_profiles(root, errors)
        check_combined(root, errors, modules)
        check_routing(root, errors, modules)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAILED: {len(errors)} synchronization error(s)")
        return 1

    print(
        f"OK: {len(modules)} modules synchronized across template copies, "
        f"{len(PROFILE_MODULES)} profiles, AGENTS-combined.md and routing tables"
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
