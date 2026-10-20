# GitHub Publishing Guide

This guide covers publishing the collection to GitHub.

## Pre-Publication Checklist

### Content

- [ ] No secrets, API keys, tokens or credentials in any file.
- [ ] No local paths, private IPs or internal hostnames in public files.
- [ ] No third-party skill code is bundled; external skills are links only.
- [ ] No archives, backups or historical catalog views.
- [ ] All maintained documentation is in English.
- [ ] The catalog contains 2 original and 154 link-only records.

### Validation

```bash
python scripts/validate-frontmatter.py
python scripts/update-category-index.py --check
python -m unittest discover -s scripts -p "test_*.py"
```

The CI workflow in `.github/workflows/skills-tooling.yml` runs the same checks.

### Link Check

The 154 upstream URLs were checked on 2026-10-20 and returned HTTP 200. Re-check
before publishing if the upstream repositories may have changed:

```bash
python - <<'PY'
import urllib.request
from pathlib import Path

for name in ('skill-links.txt', 'pinned-links.txt'):
    for line in (Path('catalog/links') / name).read_text(encoding='utf-8').splitlines():
        url = line.strip()
        if not url or url.startswith('#'):
            continue
        request = urllib.request.Request(url, method='HEAD',
                                         headers={'User-Agent': 'link-check/1.0'})
        with urllib.request.urlopen(request, timeout=20) as response:
            print(response.status, url)
PY
```

## Initialize and Push

The local repository is initialized on branch `master`. The existing GitHub
repository is `Dracievajko-SkillsSet`; its default branch is `master`, and
`main` is kept in sync for compatibility.

For a fresh clone, configure the remote and push:

```bash
git remote add origin https://github.com/DracieVajko/Dracievajko-SkillsSet.git
git push -u origin master
git push origin master:main
```

Authentication is required before pushing. Use one of:

```bash
gh auth login
# or configure a personal access token / SSH key for GitHub
```

Do not commit credentials. For normal updates, push without force. Force-push
only when intentionally replacing history, and preserve the old history first
with a local Git bundle or a separate backup branch.

## Post-Publication

- Enable Issues and Discussions.
- Add a repository description and topics: `ai-agents`, `opencode`, `odysseus`,
  `skills`, `prompts`, `personas`, `agent-rules`, `mcp`, `llm`.
- Protect `master` and require the CI checks `test`, `validate` and
  `category-index`.
- Create a release tag such as `v2026.10.20` if desired.

## Direct GitHub Links

After pushing, the canonical links have this form:

```text
https://github.com/DracieVajko/Dracievajko-SkillsSet/blob/master/skills/original/write-research-projects/SKILL.md
https://github.com/DracieVajko/Dracievajko-SkillsSet/blob/master/prompts/system/deep-research-writing-long.md
https://github.com/DracieVajko/Dracievajko-SkillsSet/blob/master/prompts/system/deep-research-writing-short.md
```

Replace the repository name only if the remote differs.

## Maintenance

### Add an Original Skill

1. Create `skills/original/<name>/SKILL.md`.
2. Validate frontmatter and regenerate the index.
3. Commit and push.

### Add an External Link

1. Add the raw URL to `catalog/links/skill-links.txt` or `pinned-links.txt`.
2. Add a matching `items.json` record with `authorship: link-only`.
3. Regenerate the index and run the tests.
4. Commit and push.

## License Compliance

- Original content is MIT licensed.
- External skills remain under their upstream licenses.
- No third-party code is redistributed.
- A link is not a license grant; verify terms before copying upstream content.

See [ATTRIBUTION.md](../ATTRIBUTION.md) and
[SAFETY-AND-LICENSES.md](SAFETY-AND-LICENSES.md).
