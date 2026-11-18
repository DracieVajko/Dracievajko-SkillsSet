# Scripts

Small, standard-library-only tools that keep the repository honest. Every
script runs standalone from the repository root and exits `0` on success, `1`
on failure, so CI can call them directly.

| Script | Purpose |
|--------|---------|
| `validate-frontmatter.py` | Validate the frontmatter of every `skills/original/**/SKILL.md`: required fields, name/folder match, version format, known category, description length, file length, duplicate names |
| `check-sync.py` | Verify that the derived rule copies (`instructions/opencode/project-template/agent-rules/`, `instructions/profiles/`, `AGENTS-combined.md`, routing tables) still match `instructions/modules/` |
| `update-category-index.py` | Generate `docs/CATEGORY_INDEX.md` and the generated repository-count blocks; `--check` verifies without writing |
| `check-links.py` | Request every catalogued external URL and report HTTP failures (availability only, never a security or license check) |
| `check-markdown-links.py` | Verify that relative Markdown links in the repository resolve to existing files |
| `install-skills.ps1` / `install-skills.sh` | Install or remove the original skills in an agent's skills directory, with timestamped backups |
| `test_skills_tooling.py` | Regression tests that drive the scripts as subprocesses against a throwaway repository |
| `test_script_units.py` | Unit tests that call the tooling functions directly |
| `test_import_smoke.py` | Smoke test that the tooling modules stay importable |

## Running them

```bash
python scripts/validate-frontmatter.py
python scripts/check-sync.py
python scripts/update-category-index.py
python scripts/check-markdown-links.py
python -m unittest discover -s scripts -p "test_*.py"
```

`check-links.py` is the only one that touches the network; it is scheduled
monthly rather than run on every push.

## Design decisions

- **Each script stands alone.** No script imports another. They are copied
  around and run by hand, and a shared helper module would break that. The
  cost is that a few constants (for example the catalog link file names) and
  the link-file parsing appear in more than one script. That duplication is
  deliberate: it keeps every tool runnable on its own.
- **The catalog is the single source of truth.** `catalog/items.json` and the
  filesystem drive the generated index and the generated counts. No script
  keeps a second copy of the numbers.
- **Availability is not trust.** `check-links.py` reports whether a URL
  responds. It says nothing about the license, the content or the security of
  the linked file.
- **Vendored content keeps upstream links.** Bundled third-party skills under
  `skills/third-party/` keep the relative links upstream wrote. Links to
  sibling upstream skills that are not bundled are reported as warnings, not
  failures.

## Requirements

Python 3.9+ and PyYAML:

```bash
pip install --requirement scripts/requirements.txt
```
