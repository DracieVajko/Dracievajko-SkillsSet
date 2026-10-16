#!/usr/bin/env python3
"""
Focused regression tests for the skills tooling:

    scripts/validate-frontmatter.py
    scripts/update-category-index.py

Uses only the Python standard library (unittest) and runs each script as a
subprocess against a throwaway repository root, so the real repository is never
touched.

Run with:
    python scripts/test_skills_tooling.py
    python -m unittest discover -s scripts -p "test_*.py"
"""

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
VALIDATOR = SCRIPTS / 'validate-frontmatter.py'
INDEXER = SCRIPTS / 'update-category-index.py'

VALID_FRONTMATTER = """---
name: {name}
description: Use when testing the skills tooling.
version: 1.0.0
author: tester
category: core
---

# {name}
"""


class RepoFixture:
    """Build a minimal but structurally valid repository in a temp directory."""

    def __init__(self, base):
        self.root = Path(base)
        for root_name in ('01-my-skills', '02-my-modified-skills', '03-third-party-skills'):
            (self.root / root_name).mkdir(parents=True, exist_ok=True)
        (self.root / '03-third-party-skills' / 'odysseus').mkdir(parents=True, exist_ok=True)
        (self.root / 'catalog').mkdir(parents=True, exist_ok=True)
        (self.root / 'docs').mkdir(parents=True, exist_ok=True)
        self.catalog = []
        self.write_catalog()
        self.write_link_files()

    def write_skill(self, rel_dir, text=None, name=None):
        directory = self.root / rel_dir
        directory.mkdir(parents=True, exist_ok=True)
        if text is None:
            text = VALID_FRONTMATTER.format(name=name or directory.name)
        (directory / 'SKILL.md').write_text(text, encoding='utf-8', newline='\n')
        return directory

    def write_link_files(self, skill_links=(), unverified_links=()):
        ody = self.root / '03-third-party-skills' / 'odysseus'
        (ody / 'skill-links.txt').write_text(
            '\n'.join(skill_links) + ('\n' if skill_links else ''),
            encoding='utf-8', newline='\n')
        (ody / 'unverified-links.txt').write_text(
            '\n'.join(unverified_links) + ('\n' if unverified_links else ''),
            encoding='utf-8', newline='\n')

    def write_catalog(self):
        (self.root / 'catalog' / 'items.json').write_text(
            json.dumps(self.catalog, indent=2), encoding='utf-8', newline='\n')


def run(script, root, *args):
    return subprocess.run(
        [sys.executable, str(script), '--root', str(root), *args],
        capture_output=True, text=True, encoding='utf-8', cwd=str(root),
    )


class BaseTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = RepoFixture(self._tmp.name)


class ValidatorDiscoveryTests(BaseTest):
    def test_discovers_all_three_roots(self):
        self.repo.write_skill('01-my-skills/agent-harnesses/original-a')
        self.repo.write_skill('02-my-modified-skills/agent-harnesses/modified-a')
        self.repo.write_skill('03-third-party-skills/agent-harnesses/third-a')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Validated 3 skills', result.stdout)

    def test_empty_branch_is_valid(self):
        self.repo.write_skill('01-my-skills/agent-harnesses/original-a')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_required_root_fails(self):
        import shutil
        shutil.rmtree(self.repo.root / '03-third-party-skills')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing required skill root '03-third-party-skills/'", result.stdout)

    def test_excluded_backup_content_is_ignored(self):
        self.repo.write_skill('01-my-skills/agent-harnesses/original-a')
        self.repo.write_skill('01-my-skills/_backups/agent-harnesses/ghost')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Validated 1 skills', result.stdout)
        self.assertNotIn('ghost', result.stdout)

    def test_repo_directory_name_is_not_an_exclusion(self):
        """Exclusions are exact directory names, not Dracievajko-* globs.

        An ancestor directory named exactly like the repository, and a skill
        folder whose name merely starts with ``Dracievajko-``, must both be
        discovered.
        """
        self.repo.write_skill('01-my-skills/Dracievajko-AI-Agent-Collection/kept')
        self.repo.write_skill('01-my-skills/agent-harnesses/Dracievajko-something-else')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Validated 2 skills', result.stdout)

    def test_exclusion_is_exact_name_not_prefix(self):
        """A skill folder named like an excluded sibling repo must still be found."""
        self.repo.write_skill('01-my-skills/agent-harnesses/Dracievajko-SkillsSet-extra')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Validated 1 skills', result.stdout)

    def test_excluded_skill_folder_is_skipped(self):
        """An exact excluded directory name is skipped at any depth below a root."""
        self.repo.write_skill('01-my-skills/agent-harnesses/keep')
        self.repo.write_skill('01-my-skills/agent-harnesses/_private-review')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Validated 1 skills', result.stdout)


class ValidatorFrontmatterTests(BaseTest):
    def test_valid_frontmatter_passes(self):
        self.repo.write_skill('01-my-skills/agent-harnesses/original-a')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('0 errors', result.stdout)

    def test_invalid_frontmatter_fails(self):
        self.repo.write_skill(
            '01-my-skills/agent-harnesses/broken',
            text="---\nname: broken\nversion: 1.0.0\n---\n\n# broken\n")
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing required field 'description'", result.stdout)

    def test_missing_frontmatter_fails(self):
        self.repo.write_skill('01-my-skills/agent-harnesses/plain', text='# no frontmatter\n')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn('No YAML frontmatter', result.stdout)

    def test_name_folder_mismatch_fails(self):
        self.repo.write_skill('01-my-skills/agent-harnesses/folder-name', name='other-name')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn('does not match folder', result.stdout)

    def test_optional_metadata_is_warning_not_error(self):
        self.repo.write_skill(
            '01-my-skills/agent-harnesses/minimal',
            text="---\nname: minimal\ndescription: Use when testing.\n---\n\n# minimal\n")
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Optional field 'version' not set", result.stdout)


class ValidatorCollisionTests(BaseTest):
    def test_same_scope_collision_is_error(self):
        self.repo.write_skill('01-my-skills/agent-harnesses/dup-one', name='dup')
        self.repo.write_skill('01-my-skills/agent-harnesses/dup-two', name='dup')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Duplicate skill name 'dup' in scope '01-my-skills/agent-harnesses'",
                      result.stdout)

    def test_cross_scope_collision_is_warning(self):
        self.repo.write_skill('01-my-skills/agent-harnesses/variant')
        self.repo.write_skill('03-third-party-skills/agent-harnesses/variant')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Name 'variant' appears in multiple scopes", result.stdout)


class IndexerTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.repo.write_skill('01-my-skills/agent-harnesses/original-a')
        self.repo.write_skill('03-third-party-skills/agent-harnesses/third-a')
        self.repo.write_link_files(
            skill_links=('https://raw.githubusercontent.com/example/example/main/skills/link-one/SKILL.md',),
            unverified_links=(
                'https://raw.githubusercontent.com/example/example-pinned/release/v1/skills/link-two/SKILL.md',),
        )
        self.repo.catalog = [
            {'name': 'original-a', 'authorship': 'original',
             'local_skill_path': '01-my-skills/agent-harnesses/original-a/SKILL.md',
             'category': 'custom', 'verification': 'verified'},
            {'name': 'third-a', 'authorship': 'third-party',
             'local_skill_path': '03-third-party-skills/agent-harnesses/third-a/SKILL.md',
             'category': 'core', 'verification': 'verified'},
            {'name': 'planned-skill', 'authorship': 'unresolved',
             'local_skill_path': '', 'category': 'development', 'verification': 'planned'},
        ]
        self.repo.write_catalog()
        self.index_path = self.repo.root / 'docs' / 'CATEGORY_INDEX.md'

    def test_generation_is_deterministic(self):
        first = run(INDEXER, self.repo.root)
        self.assertEqual(first.returncode, 0, first.stderr)
        content_a = self.index_path.read_text(encoding='utf-8')
        second = run(INDEXER, self.repo.root)
        self.assertEqual(second.returncode, 0, second.stderr)
        content_b = self.index_path.read_text(encoding='utf-8')
        self.assertEqual(content_a, content_b)

    def test_check_reports_stale_then_fresh(self):
        stale = run(INDEXER, self.repo.root, '--check')
        self.assertEqual(stale.returncode, 1)
        self.assertIn('STALE', stale.stdout)

        run(INDEXER, self.repo.root)
        fresh = run(INDEXER, self.repo.root, '--check')
        self.assertEqual(fresh.returncode, 0, fresh.stdout)
        self.assertIn('up to date', fresh.stdout)

    def test_check_does_not_rewrite(self):
        run(INDEXER, self.repo.root)
        before = self.index_path.read_text(encoding='utf-8')
        self.index_path.write_text(before + '\n<!-- hand edit -->\n', encoding='utf-8')
        edited = self.index_path.read_text(encoding='utf-8')
        run(INDEXER, self.repo.root, '--check')
        self.assertEqual(self.index_path.read_text(encoding='utf-8'), edited)

    def test_link_only_references_are_urls_not_missing_files(self):
        run(INDEXER, self.repo.root)
        content = self.index_path.read_text(encoding='utf-8')
        self.assertIn('Link-Only References', content)
        self.assertIn('### example/example (1)', content)
        self.assertIn('[`link-one`](https://raw.githubusercontent.com/example/example/main/skills/link-one/SKILL.md)', content)
        self.assertIn('### example/example-pinned (1)', content)
        self.assertNotIn('Category directory not found', content)

    def test_unresolved_entries_come_from_catalog(self):
        run(INDEXER, self.repo.root)
        content = self.index_path.read_text(encoding='utf-8')
        self.assertIn('Unresolved Inventory Entries', content)
        self.assertIn('`planned-skill`', content)

    def test_local_links_are_relative_to_docs(self):
        run(INDEXER, self.repo.root)
        content = self.index_path.read_text(encoding='utf-8')
        self.assertIn('(../01-my-skills/agent-harnesses/original-a/SKILL.md)', content)
        self.assertIn('(../03-third-party-skills/agent-harnesses/third-a/SKILL.md)', content)


class IndexerAuthorityTests(BaseTest):
    """Authoritative catalog inputs must fail loudly, never silently empty.

    catalog/items.json and the odysseus link files are the only trusted inputs
    for the generated index. A missing or malformed one must make the generator
    (and therefore --check) exit nonzero instead of producing a "fresh" index.
    """

    def setUp(self):
        super().setUp()
        self.repo.write_link_files(
            ['https://raw.githubusercontent.com/owner/repo/main/skills/alpha/SKILL.md'])
        self.items_path = self.repo.root / 'catalog' / 'items.json'

    def test_missing_authoritative_catalog_fails_generation(self):
        self.items_path.unlink()
        result = run(INDEXER, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Catalog file not found', result.stdout)

    def test_malformed_authoritative_catalog_fails_generation(self):
        self.items_path.write_text('[{"id": "x",}]', encoding='utf-8')
        result = run(INDEXER, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn('ERROR:', result.stdout)

    def test_catalog_that_is_not_an_array_fails(self):
        self.items_path.write_text('{"items": []}', encoding='utf-8')
        result = run(INDEXER, self.repo.root, '--check')
        self.assertEqual(result.returncode, 1)
        self.assertIn('must contain a JSON array', result.stdout)

    def test_malformed_authoritative_catalog_cannot_pass_freshness_check(self):
        # Baseline: a good catalog produces a fresh index.
        generated = run(INDEXER, self.repo.root)
        self.assertEqual(generated.returncode, 0, generated.stderr)
        fresh = run(INDEXER, self.repo.root, '--check')
        self.assertEqual(fresh.returncode, 0, fresh.stdout)
        self.assertIn('OK:', fresh.stdout)

        # Corrupt the authoritative input: the freshness check must fail, not
        # report the index as up to date.
        self.items_path.write_text('{ this is not json', encoding='utf-8')
        result = run(INDEXER, self.repo.root, '--check')
        self.assertEqual(result.returncode, 1)
        self.assertIn('ERROR:', result.stdout)
        self.assertNotIn('is up to date', result.stdout)

    def test_missing_authoritative_link_file_fails(self):
        ody = self.repo.root / '03-third-party-skills' / 'odysseus'
        (ody / 'unverified-links.txt').unlink()
        result = run(INDEXER, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Missing authoritative link file', result.stdout)

    def test_check_does_not_write_on_success(self):
        run(INDEXER, self.repo.root)
        index_path = self.repo.root / 'docs' / 'CATEGORY_INDEX.md'
        before = index_path.read_bytes()
        mtime_before = index_path.stat().st_mtime_ns
        result = run(INDEXER, self.repo.root, '--check')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(index_path.read_bytes(), before)
        self.assertEqual(index_path.stat().st_mtime_ns, mtime_before)


class CatalogDataTests(unittest.TestCase):
    """Guards the maintained catalog data in the real repository.

    These tests read catalog/ directly (not a fixture) so stale totals and
    malformed maintained JSON fail the suite.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo = Path(__file__).resolve().parent.parent
        cls.catalog = cls.repo / 'catalog'

    def load(self, name):
        return json.loads((self.catalog / name).read_text(encoding='utf-8'))

    def test_every_maintained_catalog_json_file_parses(self):
        files = sorted(self.catalog.rglob('*.json'))
        self.assertTrue(files, 'no catalog JSON files found')
        for path in files:
            with self.subTest(path=path.relative_to(self.repo).as_posix()):
                json.loads(path.read_text(encoding='utf-8'))

    def test_items_json_has_no_duplicate_ids(self):
        items = self.load('items.json')
        ids = [item['id'] for item in items]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        self.assertEqual(duplicates, [])

    def test_items_csv_matches_items_json(self):
        items = self.load('items.json')
        with (self.catalog / 'items.csv').open(encoding='utf-8', newline='') as handle:
            rows = list(csv.reader(handle))
        # The CSV carries a UTF-8 BOM, so the first header cell is '\ufeff"id"'.
        data_rows = rows[1:]
        self.assertEqual(len(data_rows), len(items))
        self.assertEqual(
            Counter(row[0] for row in data_rows),
            Counter(item['id'] for item in items),
        )

    def test_categories_catalog_is_link_only_plus_local_third_party(self):
        items = self.load('items.json')
        link_only = {i['id'] for i in items if i['authorship'] == 'link-only'}
        third_party = {i['id'] for i in items if i['authorship'] == 'third-party'}
        recorded = {i['id'] for i in self.load('categories/skills.json')}
        self.assertEqual(len(recorded), 154)
        self.assertLessEqual(link_only, recorded)
        self.assertEqual(recorded - link_only, third_party)

    def test_odysseus_link_file_counts(self):
        ody = self.repo / '03-third-party-skills' / 'odysseus'

        def urls(filename):
            text = (ody / filename).read_text(encoding='utf-8')
            return [line.strip() for line in text.splitlines()
                    if line.strip() and not line.strip().startswith('#')]

        stable = urls('skill-links.txt')
        pinned = urls('unverified-links.txt')
        self.assertEqual(len(stable), 142)
        self.assertEqual(len(pinned), 12)
        self.assertEqual(len(stable) + len(pinned), 154)

    def test_items_authorship_partition(self):
        items = self.load('items.json')
        counts = Counter(i['authorship'] for i in items)
        self.assertEqual(len(items), 184)
        self.assertEqual(counts['link-only'], 136)
        self.assertEqual(counts['third-party'], 18)
        self.assertEqual(counts['unresolved'], 23)
        self.assertEqual(counts['candidate_upstream'], 6)
        self.assertEqual(counts['original'], 1)

    def test_unresolved_scopes_are_distinct_and_documented(self):
        items = self.load('items.json')
        unresolved = {i['name'] for i in items if i['authorship'] == 'unresolved'}
        candidates = {i['name'] for i in items if i['authorship'] == 'candidate_upstream'}
        sources = self.load('unresolved-sources.json')
        custom = {i['name'] for i in sources if i['source_type'] == 'custom-or-unverified'}
        candidate_rows = {i['name'] for i in sources if i['source_type'] == 'third-party-candidate'}

        self.assertEqual(len(unresolved), 23)
        self.assertEqual(len(custom), 22)
        self.assertEqual(len(sources), 28)
        # Scope 28 = 22 custom-or-unverified + 6 candidate-upstream.
        self.assertEqual(custom | candidate_rows, {i['name'] for i in sources})
        # Candidate scopes agree across both authoritative-external and historical files.
        self.assertEqual(candidate_rows, candidates)
        # The documented single-record gap between 23 and 22.
        self.assertEqual(unresolved - custom, {'writing-great-skills'})

    def test_context_engineering_records_are_distinct_references(self):
        items = self.load('items.json')
        path = '03-third-party-skills/agent-harnesses/context-engineering/SKILL.md'
        records = [i for i in items if i.get('local_skill_path') == path]
        self.assertEqual(len(records), 2)
        self.assertEqual({r['repository'] for r in records},
                         {'https://github.com/addyosmani/agent-skills',
                          'https://github.com/composio-community/opencode-skills'})
        # Both records point at one local copy; the origin is not claimed twice.
        composio, = [r for r in records if 'composio' in r['repository']]
        self.assertIn('Alternative upstream reference', composio['compatibility_notes'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
