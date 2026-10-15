# GitHub Publishing Guide

This guide covers publishing the Dracievajko AI Agent Collection to GitHub.

## Pre-Publication Checklist

### 1. Security Review
- [ ] Run secret scan: `gitleaks detect --source .`
- [ ] Verify no API keys, tokens, or credentials in any file
- [ ] Check `.gitignore` excludes: `.env`, `*.key`, `*.pem`, `config.local.*`, `*.log`, `node_modules/`, `__pycache__/`
- [ ] Verify no Tailscale IPs, local paths, or internal hostnames in public files
- [ ] Sanitize `system-prompts/repository-hygiene.md` examples (already done)

### 2. Content Review
- [ ] All maintained documentation in English
- [ ] Slovak originals preserved in `archive/slovak/`
- [ ] All third-party skills have provenance headers
- [ ] Link-only skills (142+) not copied — only cataloged
- [ ] Custom skills marked as `original` authorship
- [ ] No private/personal information in any file

### 3. Structure Validation
- [ ] Run `python scripts/validate-frontmatter.py`
- [ ] Run `python scripts/update-category-index.py`
- [ ] Run `npx markdownlint-cli2 "skills/**/*.md" "docs/*.md" "README.md"`
- [ ] Verify all skills have `SKILL.md`
- [ ] Verify Odysseus link files: one raw URL per line, no headers

### 4. Licensing
- [ ] Root `LICENSE` file (MIT for original content)
- [ ] Third-party skills retain original licenses
- [ ] `inventories/skills-catalog.json` has license info per skill
- [ ] No blanket license applied to third-party content

---

## Repository Initialization

```bash
cd Dracievajko-AI-Agent-Collection

# Initialize git
git init
git branch -M main

# Add all files
git add .

# Initial commit
git commit -m "feat: initial release of Dracievajko AI Agent Collection

- 17 OpenCode skills (core, development, design, ai-ml, 3d-blender)
- 1 custom skill (ticktick-tasks)
- 142+ third-party skills cataloged (link-only)
- 9 personas (jayce, bruno, atlas, elias, adrian, orion, victor, marcus, jericho)
- 10 agent rule modules + main AGENTS.md
- 9 specialized agent profiles
- System prompts (general, coding, cad, trading, repository hygiene)
- Odysseus direct link files (validated, all, unverified, by-category, presets)
- Templates, presets, catalogs, documentation
- Validation scripts and CI/CD workflow"

# Add remote
git remote add origin https://github.com/DracieVajko/Dracievajko-AI-Agent-Collection.git

# Push
git push -u origin main
```

---

## Post-Publication

### 1. GitHub Settings
- [ ] Enable Issues
- [ ] Enable Discussions
- [ ] Add repository description: "Personal curated collection of AI-agent skills, prompts, personas, and agent rules for OpenCode, Odysseus, and compatible frameworks"
- [ ] Add topics: `ai-agents`, `opencode`, `odysseus`, `skills`, `prompts`, `personas`, `agent-rules`, `mcp`, `llm`
- [ ] Enable dependency graph and dependabot alerts

### 2. Branch Protection (Recommended)
- [ ] Protect `main` branch
- [ ] Require PR reviews (1)
- [ ] Require status checks: `validate`, `lint-markdown`, `validate-skill-structure`
- [ ] Require branches up to date before merging

### 3. Releases
- [ ] Create first release: `v1.0.0` — "Initial release"
- [ ] Tag format: `vYYYY.MM.DD` for collection releases
- [ ] Include ZIP of public-ready tree in release assets

### 4. Community
- [ ] Add `CONTRIBUTING.md` to root (already in `docs/`)
- [ ] Add `CODE_OF_CONDUCT.md` (Contributor Covenant)
- [ ] Add `SECURITY.md` for vulnerability reporting
- [ ] Pin key issues/discussions

---

## Ongoing Maintenance

### Adding New Skills
1. Create skill directory under appropriate `skills/category/`
2. Add `SKILL.md` with valid frontmatter
3. Run `python scripts/validate-frontmatter.py`
4. Run `python scripts/update-category-index.py`
5. Update `inventories/skills-catalog.json` with provenance
6. Submit PR

### Updating Third-Party Catalog
1. Add new raw URL to `odysseus/skill-links-all.txt`
2. If verified, also add to `odysseus/skill-links-validated.txt`
3. Add to appropriate `odysseus/by-category/*.txt`
4. Update `inventories/provenance-tracking.json`
5. Submit PR

### Validating Links
```bash
# Check Odysseus links are valid raw URLs
python -c "
import re
with open('odysseus/skill-links-all.txt') as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if line and not line.startswith('https://raw.githubusercontent.com/'):
            print(f'Line {i}: Not a raw GitHub URL: {line}')
        if ' ' in line:
            print(f'Line {i}: Contains spaces: {line}')
"
```

---

## ZIP Archive Creation

```bash
# Create public-ready ZIP (excludes archive/, .git/, private files)
cd ..
zip -r Dracievajko-AI-Agent-Collection.zip Dracievajko-AI-Agent-Collection \
  -x "*/archive/*" "*/.git/*" "*/.github/*" "*.log" "*.tmp" \
  "*/node_modules/*" "*/__pycache__/*" "*.DS_Store" "Thumbs.db"

# Verify
unzip -l Dracievajko-AI-Agent-Collection.zip | head -20
```

---

## Notes for Odysseus Users

Odysseus users need **direct raw URLs to SKILL.md files**. After publishing:

1. Update `odysseus/skill-links-validated.txt` with actual raw URLs from your GitHub repo
2. Format: `https://raw.githubusercontent.com/DracieVajko/Dracievajko-AI-Agent-Collection/main/skills/core/using-superpowers/SKILL.md`
3. Regenerate category and preset files
4. Document that these are now verified working links

---

## License Compliance

This repository contains:
- **Original content** (MIT) — system prompts, personas, custom skills, documentation
- **Third-party skills** (various MIT) — included with provenance, original licenses preserved
- **Cataloged skills** (link-only) — no content copied, attribution only

**Do not** apply the repository MIT license to third-party skill content. Each skill directory indicates its license in `SKILL.md` frontmatter and `inventories/skills-catalog.json`.