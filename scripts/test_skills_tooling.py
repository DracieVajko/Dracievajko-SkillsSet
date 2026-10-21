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
        (self.root / 'skills' / 'original').mkdir(parents=True, exist_ok=True)
        (self.root / 'catalog' / 'links').mkdir(parents=True, exist_ok=True)
        (self.root / 'docs').mkdir(parents=True, exist_ok=True)
        self.write_link_files()

    def write_skill(self, rel_dir, text=None, name=None):
        directory = self.root / rel_dir
        directory.mkdir(parents=True, exist_ok=True)
        if text is None:
            text = VALID_FRONTMATTER.format(name=name or directory.name)
        (directory / 'SKILL.md').write_text(text, encoding='utf-8', newline='\n')
        return directory

    def write_link_files(self, skill_links=(), pinned_links=()):
        links = self.root / 'catalog' / 'links'
        (links / 'skill-links.txt').write_text(
            '\n'.join(skill_links) + ('\n' if skill_links else ''),
            encoding='utf-8', newline='\n')
        (links / 'pinned-links.txt').write_text(
            '\n'.join(pinned_links) + ('\n' if pinned_links else ''),
            encoding='utf-8', newline='\n')


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
    def test_discovers_original_root(self):
        self.repo.write_skill('skills/original/original-a')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Validated 1 skills', result.stdout)

    def test_empty_root_is_valid(self):
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Validated 0 skills', result.stdout)

    def test_missing_required_root_fails(self):
        import shutil
        shutil.rmtree(self.repo.root / 'skills/original')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing required skill root 'skills/original/'", result.stdout)

    def test_excluded_backup_content_is_ignored(self):
        self.repo.write_skill('skills/original/original-a')
        self.repo.write_skill('skills/original/_backups/agent-harnesses/ghost')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Validated 1 skills', result.stdout)
        self.assertNotIn('ghost', result.stdout)

    def test_repo_directory_name_is_not_excluded(self):
        """Exclusions are exact directory names, not broad repository globs."""
        self.repo.write_skill('skills/original/example-collection/kept')
        self.repo.write_skill('skills/original/example-something-else')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Validated 2 skills', result.stdout)

    def test_exclusion_is_exact_name_not_prefix(self):
        """A skill folder named like an excluded sibling must still be found."""
        self.repo.write_skill('skills/original/_backups-extra')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Validated 1 skills', result.stdout)

    def test_excluded_skill_folder_is_skipped(self):
        """An exact excluded directory name is skipped at any depth below a root."""
        self.repo.write_skill('skills/original/keep')
        self.repo.write_skill('skills/original/_private-review')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Validated 1 skills', result.stdout)


class ValidatorFrontmatterTests(BaseTest):
    def test_valid_frontmatter_passes(self):
        self.repo.write_skill('skills/original/original-a')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('0 errors', result.stdout)

    def test_invalid_frontmatter_fails(self):
        self.repo.write_skill(
            'skills/original/broken',
            text="---\nname: broken\nversion: 1.0.0\n---\n\n# broken\n")
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing required field 'description'", result.stdout)

    def test_missing_frontmatter_fails(self):
        self.repo.write_skill('skills/original/plain', text='# no frontmatter\n')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn('No YAML frontmatter', result.stdout)

    def test_name_folder_mismatch_fails(self):
        self.repo.write_skill('skills/original/folder-name', name='other-name')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn('does not match folder', result.stdout)

    def test_optional_metadata_is_warning_not_error(self):
        self.repo.write_skill(
            'skills/original/minimal',
            text="---\nname: minimal\ndescription: Use when testing.\n---\n\n# minimal\n")
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Optional field 'version' not set", result.stdout)


class ValidatorCollisionTests(BaseTest):
    def test_same_scope_collision_is_error(self):
        self.repo.write_skill('skills/original/dup-one', name='dup')
        self.repo.write_skill('skills/original/dup-two', name='dup')
        result = run(VALIDATOR, self.repo.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Duplicate skill name 'dup' in scope 'skills/original'",
                      result.stdout)


class IndexerTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.repo.write_skill('skills/original/original-a')
        self.repo.write_link_files(
            skill_links=('https://raw.githubusercontent.com/example/example/main/skills/link-one/SKILL.md',),
            pinned_links=(
                'https://raw.githubusercontent.com/example/example-pinned/release/v1/skills/link-two/SKILL.md',),
        )
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

    def test_external_links_are_urls_not_missing_files(self):
        run(INDEXER, self.repo.root)
        content = self.index_path.read_text(encoding='utf-8')
        self.assertIn('External Skills (Links Only)', content)
        self.assertIn('### example/example (1)', content)
        self.assertIn('[`link-one`](https://raw.githubusercontent.com/example/example/main/skills/link-one/SKILL.md)', content)
        self.assertIn('### example/example-pinned (1)', content)
        self.assertNotIn('Category directory not found', content)

    def test_local_links_are_relative_to_docs(self):
        run(INDEXER, self.repo.root)
        content = self.index_path.read_text(encoding='utf-8')
        self.assertIn('(../skills/original/original-a/SKILL.md)', content)

    def test_no_removed_local_sections(self):
        run(INDEXER, self.repo.root)
        content = self.index_path.read_text(encoding='utf-8')
        self.assertNotIn('Modified local skills', content)
        self.assertNotIn('Third-party local skills', content)


class IndexerAuthorityTests(BaseTest):
    """Authoritative link files must fail loudly, never silently empty."""

    def setUp(self):
        super().setUp()
        self.repo.write_link_files(
            ['https://raw.githubusercontent.com/owner/repo/main/skills/alpha/SKILL.md'])

    def test_missing_authoritative_link_file_fails(self):
        (self.repo.root / 'catalog' / 'links' / 'pinned-links.txt').unlink()
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
    """Guards the maintained catalog and link data in the real repository."""

    @classmethod
    def setUpClass(cls):
        cls.repo = Path(__file__).resolve().parent.parent
        cls.catalog = cls.repo / 'catalog'
        cls.links = cls.catalog / 'links'

    def load(self, name):
        return json.loads((self.catalog / name).read_text(encoding='utf-8'))

    def link_urls(self):
        urls = []
        for name in ('skill-links.txt', 'pinned-links.txt'):
            text = (self.links / name).read_text(encoding='utf-8')
            urls.extend(line.strip() for line in text.splitlines()
                        if line.strip() and not line.strip().startswith('#'))
        return urls

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

    def test_items_authorship_partition(self):
        items = self.load('items.json')
        counts = Counter(i['authorship'] for i in items)
        self.assertEqual(len(items), 158)
        self.assertEqual(counts['link-only'], 154)
        self.assertEqual(counts['original'], 4)
        self.assertEqual(set(counts), {'link-only', 'original'})

    def test_link_file_counts(self):
        stable = [u for u in (self.links / 'skill-links.txt').read_text(encoding='utf-8').splitlines()
                  if u.strip() and not u.strip().startswith('#')]
        pinned = [u for u in (self.links / 'pinned-links.txt').read_text(encoding='utf-8').splitlines()
                  if u.strip() and not u.strip().startswith('#')]
        self.assertEqual(len(stable), 142)
        self.assertEqual(len(pinned), 12)
        self.assertEqual(len(stable) + len(pinned), 154)

    def test_catalog_link_urls_match_link_files(self):
        items = self.load('items.json')
        catalog_urls = {i['raw_url'] for i in items if i['authorship'] == 'link-only'}
        file_urls = set(self.link_urls())
        self.assertEqual(catalog_urls, file_urls)

    def test_all_link_urls_are_raw_github(self):
        for url in self.link_urls():
            self.assertTrue(url.startswith('https://raw.githubusercontent.com/'), url)

    def test_original_catalog_paths_exist(self):
        items = self.load('items.json')
        originals = [i for i in items if i['authorship'] == 'original']
        self.assertEqual(len(originals), 4)
        for item in originals:
            path = self.repo / item['local_skill_path']
            self.assertTrue(path.is_file(), item['local_skill_path'])

    def test_no_third_party_skill_bodies(self):
        third_party = self.repo / 'skills' / 'third-party'
        self.assertTrue((third_party / 'README.md').is_file())
        self.assertEqual(list(third_party.rglob('SKILL.md')), [])
        self.assertFalse((self.repo / 'skills' / 'adapted').exists())

    def test_no_link_record_has_a_local_skill_path(self):
        items = self.load('items.json')
        for item in items:
            if item['authorship'] == 'link-only':
                self.assertEqual(item.get('local_skill_path', ''), '')
                self.assertFalse(item.get('local_copy_included', False))

    def test_docs_index_has_expected_total(self):
        index = (self.repo / 'docs' / 'CATEGORY_INDEX.md').read_text(encoding='utf-8')
        self.assertIn('Total: **154** references.', index)
        self.assertIn('## Original Local Skills', index)
        self.assertIn('## External Skills (Links Only)', index)


if __name__ == '__main__':
    unittest.main(verbosity=2)
