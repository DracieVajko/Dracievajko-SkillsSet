#!/usr/bin/env bash
#
# Install or remove the original skills in an OpenCode skills directory.
#
# Existing skill folders are moved to a timestamped backup before being
# replaced, so an existing installation is never overwritten in place.
#
# With --uninstall the installed skill folders are moved into the backup
# directory instead: nothing is deleted, and folders that do not belong to
# this collection are left untouched.
#
# Usage:
#   ./scripts/install-skills.sh
#   ./scripts/install-skills.sh --target .agents/skills
#   ./scripts/install-skills.sh --uninstall
#   ./scripts/install-skills.sh --dry-run

set -euo pipefail

target="${HOME}/.config/opencode/skills"
backup_root="${HOME}/.config/opencode/skill-backups"
dry_run=0
uninstall=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target)
        target="$2"
        shift 2
        ;;
        --backup-root)
        backup_root="$2"
        shift 2
        ;;
        --dry-run)
        dry_run=1
        shift
        ;;
        --uninstall)
        uninstall=1
        shift
        ;;
        -h|--help)
        sed -n '2,20p' "$0"
        exit 0
        ;;
        *)
        echo "Unknown argument: $1" >&2
        exit 2
        ;;
    esac
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="${repo_root}/skills/original"

if [[ ! -d "${source_dir}" ]]; then
    echo "Skill source directory not found: ${source_dir}" >&2
    exit 1
fi

shopt -s nullglob
skills=("${source_dir}"/*/)
if [[ ${#skills[@]} -eq 0 ]]; then
    echo "No skills found under: ${source_dir}" >&2
    exit 1
fi

timestamp="$(date +%Y%m%d-%H%M%S)"
installed=0
removed=0

if [[ ${dry_run} -eq 1 ]]; then
    echo "DRY RUN: target=${target}"
fi

if [[ ! -d "${target}" ]]; then
    if [[ ${uninstall} -eq 1 ]]; then
        echo "Nothing to remove: target directory does not exist: ${target}"
        exit 0
    fi
    if [[ ${dry_run} -eq 1 ]]; then
        echo "Would create: ${target}"
    else
        mkdir -p "${target}"
    fi
fi

for skill_dir in "${skills[@]}"; do
    name="$(basename "${skill_dir}")"
    destination="${target}/${name}"

    if [[ ${uninstall} -eq 1 ]]; then
        if [[ -e "${destination}" ]]; then
            backup="${backup_root}/${timestamp}/${name}"
            if [[ ${dry_run} -eq 1 ]]; then
                echo "Would remove: ${destination} -> ${backup}"
            else
                mkdir -p "$(dirname "${backup}")"
                mv "${destination}" "${backup}"
                echo "Removed ${name} -> ${backup}"
            fi
            removed=$((removed + 1))
        fi
        continue
    fi

    if [[ -e "${destination}" ]]; then
        backup="${backup_root}/${timestamp}/${name}"
        if [[ ${dry_run} -eq 1 ]]; then
            echo "Would back up: ${destination} -> ${backup}"
        else
            mkdir -p "$(dirname "${backup}")"
            mv "${destination}" "${backup}"
        fi
    fi

    if [[ ${dry_run} -eq 1 ]]; then
        echo "Would install: ${name} -> ${destination}"
    else
        cp -R "${skill_dir}" "${destination}"
        echo "Installed ${name} -> ${destination}"
    fi
    installed=$((installed + 1))
done

if [[ ${dry_run} -eq 1 ]]; then
    echo "DRY RUN complete: ${installed} skill(s) would be installed"
elif [[ ${uninstall} -eq 1 ]]; then
    echo "Done: ${removed} skill(s) removed from ${target} (moved to ${backup_root})"
else
    echo "Done: ${installed} skill(s) installed in ${target}"
fi
