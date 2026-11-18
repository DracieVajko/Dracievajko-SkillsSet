#!/usr/bin/env python3
"""Unit tests for the skills tooling modules.

These tests call the tooling functions directly instead of running the scripts
as subprocesses, so a broken helper is reported with the failing assertion
rather than only through a command exit code.

Run with:
    python -m unittest discover -s scripts -p "test_*.py"
    python scripts/test_script_units.py
"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent

VALID_FRONTMATTER = """---
name: {name}
description: Use when testing the tooling.
version: 1.0.0
author: tester
category: core
---

# {name}

Body text.
"""


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_links = _load("check_links", "check-links.py")
check_markdown_links = _load("check_markdown_links", "check-markdown-links.py")
check_sync = _load("check_sync", "check-sync.py")
update_category_index = _load("update_category_index", "update-category-index.py")
validate_frontmatter = _load("validate_frontmatter", "validate-frontmatter.py")


class ToolingFixture:
    """Build a minimal but structurally valid repository in a temp directory."""

    def __init__(self, base):
        self.root = Path(base)
        (self.root / 'skills' / 'original').mkdir(parents=True, exist_ok=True)
        (self.root / 'catalog' / 'links').mkdir(parents=True, exist_ok=True)
        (self.root / 'docs').mkdir(parents=True, exist_ok=True)
        self.write_links()

    def write_links(self, stable=(), pinned=()):
        links = self.root / 'catalog' / 'links'
        (links / 'skill-links.txt').write_text(
            '\n'.join(stable) + ('\n' if stable else ''), encoding='utf-8')
        (links / 'pinned-links.txt').write_text(
            '\n'.join(pinned) + ('\n' if pinned else ''), encoding='utf-8')

    def write_skill(self, name, text=None):
        directory = self.root / 'skills' / 'original' / name
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / 'SKILL.md'
        path.write_text(text or VALID_FRONTMATTER.format(name=name),
                        encoding='utf-8', newline='\n')
        return path

    def write_items(self, items):
        catalog = self.root / 'catalog'
        catalog.mkdir(parents=True, exist_ok=True)
        (catalog / 'items.json').write_text(
            json.dumps(items, ensure_ascii=False, indent=4) + '\n',
            encoding='utf-8', newline='\n')


class FixtureTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = ToolingFixture(self._tmp.name)


class ValidateFrontmatterTests(FixtureTestCase):
    def test_valid_skill_reports_no_errors_or_warnings(self):
        path = self.repo.write_skill('good-skill')
        frontmatter, text, error = validate_frontmatter.parse_frontmatter(path)
        self.assertIsNone(error)
        errors, warnings = validate_frontmatter.validate_skill(path, frontmatter, text)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_missing_required_field_is_an_error(self):
        path = self.repo.write_skill('no-name', text='---\ndescription: x\n---\n\n# x\n')
        frontmatter, text, error = validate_frontmatter.parse_frontmatter(path)
        self.assertIsNone(error)
        errors, _ = validate_frontmatter.validate_skill(path, frontmatter, text)
        self.assertTrue(any("Missing required field 'name'" in e for e in errors), errors)

    def test_name_must_match_the_folder(self):
        path = self.repo.write_skill('folder-name', text=VALID_FRONTMATTER.format(name='other-name'))
        frontmatter, text, error = validate_frontmatter.parse_frontmatter(path)
        errors, _ = validate_frontmatter.validate_skill(path, frontmatter, text)
        self.assertTrue(any('does not match folder' in e for e in errors), errors)

    def test_unknown_category_is_a_warning_not_an_error(self):
        path = self.repo.write_skill(
            'odd-category',
            text=VALID_FRONTMATTER.format(name='odd-category').replace(
                'category: core', 'category: not-a-real-category'))
        frontmatter, text, error = validate_frontmatter.parse_frontmatter(path)
        errors, warnings = validate_frontmatter.validate_skill(path, frontmatter, text)
        self.assertEqual([], errors)
        self.assertTrue(any("Unknown category 'not-a-real-category'" in w for w in warnings), warnings)

    def test_invalid_version_is_a_warning(self):
        path = self.repo.write_skill(
            'bad-version',
            text=VALID_FRONTMATTER.format(name='bad-version').replace(
                'version: 1.0.0', 'version: 1.0'))
        frontmatter, text, error = validate_frontmatter.parse_frontmatter(path)
        errors, warnings = validate_frontmatter.validate_skill(path, frontmatter, text)
        self.assertEqual([], errors)
        self.assertTrue(any('MAJOR.MINOR.PATCH' in w for w in warnings), warnings)

    def test_long_description_is_a_warning(self):
        long_description = 'x' * (validate_frontmatter.DESCRIPTION_DOC_LIMIT + 1)
        path = self.repo.write_skill(
            'long-description',
            text=VALID_FRONTMATTER.format(name='long-description').replace(
                'description: Use when testing the tooling.',
                f'description: {long_description}'))
        frontmatter, text, error = validate_frontmatter.parse_frontmatter(path)
        errors, warnings = validate_frontmatter.validate_skill(path, frontmatter, text)
        self.assertEqual([], errors)
        self.assertTrue(any('chars, above the documented' in w for w in warnings), warnings)

    def test_missing_frontmatter_is_reported(self):
        path = self.repo.write_skill('no-frontmatter', text='# just a heading\n')
        frontmatter, text, error = validate_frontmatter.parse_frontmatter(path)
        self.assertIsNone(frontmatter)
        self.assertIn('No YAML frontmatter', error)

    def test_duplicate_names_in_the_same_scope_are_an_error(self):
        records = [
            {'name': 'dup', 'scope': 'original', 'path': 'a/SKILL.md'},
            {'name': 'dup', 'scope': 'original', 'path': 'b/SKILL.md'},
        ]
        errors, warnings = validate_frontmatter.check_name_collisions(records)
        self.assertTrue(any("Duplicate skill name 'dup'" in e for e in errors), errors)
        self.assertEqual([], warnings)

    def test_same_name_in_different_scopes_is_a_warning(self):
        records = [
            {'name': 'shared', 'scope': 'original', 'path': 'a/SKILL.md'},
            {'name': 'shared', 'scope': 'third-party', 'path': 'b/SKILL.md'},
        ]
        errors, warnings = validate_frontmatter.check_name_collisions(records)
        self.assertEqual([], errors)
        self.assertTrue(any('multiple scopes' in w for w in warnings), warnings)


class CheckLinksTests(FixtureTestCase):
    def test_read_links_skips_comments_and_blank_lines(self):
        self.repo.write_links(
            stable=['https://example.com/a/SKILL.md'],
            pinned=['# comment', '', 'https://example.com/b/SKILL.md'])
        links = check_links.read_links(self.repo.root)
        self.assertEqual(2, len(links))
        self.assertIn(('skill-links.txt', 'https://example.com/a/SKILL.md'), links)
        self.assertIn(('pinned-links.txt', 'https://example.com/b/SKILL.md'), links)

    def test_read_links_requires_both_link_files(self):
        (self.repo.root / 'catalog' / 'links' / 'pinned-links.txt').unlink()
        with self.assertRaises(FileNotFoundError):
            check_links.read_links(self.repo.root)

    def test_non_http_schemes_are_rejected_without_a_request(self):
        for url in ('file:///etc/passwd', 'ftp://example.com/x', 'gopher://example.com'):
            status, error = check_links.check_url(url, 1.0)[1:]
            self.assertIsNone(status, url)
            self.assertIn('unsupported scheme', error, url)

    def test_https_scheme_is_accepted(self):
        self.assertIn('https', check_links.ALLOWED_SCHEMES)
        self.assertNotIn('file', check_links.ALLOWED_SCHEMES)

    def test_classify_results_separates_ok_warning_and_failure(self):
        results = [
            ('https://ok.example', 200, ''),
            ('https://redirect.example', 301, ''),
            ('https://forbidden.example', 403, 'forbidden'),
            ('https://missing.example', 404, 'not found'),
            ('https://dead.example', None, 'timeout'),
        ]
        warnings, failures = check_links.classify_results(results)
        self.assertEqual(1, len(warnings))
        self.assertEqual('https://forbidden.example', warnings[0][0])
        self.assertEqual(2, len(failures))
        self.assertEqual(
            {'https://missing.example', 'https://dead.example'},
            {url for url, _, _ in failures})


class CheckSyncTests(FixtureTestCase):
    def _write_module_and_copy(self, body='Rule body.\n', copy_body=None):
        modules = self.repo.root / 'instructions' / 'modules'
        modules.mkdir(parents=True, exist_ok=True)
        (modules / 'coding.md').write_text(body, encoding='utf-8')
        template = self.repo.root / 'instructions' / 'opencode' / 'project-template' / 'agent-rules'
        template.mkdir(parents=True, exist_ok=True)
        (template / 'coding.md').write_text(
            body if copy_body is None else copy_body, encoding='utf-8')

    def test_normalize_strips_line_endings_and_outer_space(self):
        self.assertEqual('line', check_sync.normalize('\r\n  line  \r\n'))

    def test_module_files_requires_the_module_directory(self):
        with self.assertRaises(FileNotFoundError):
            check_sync.module_files(self.repo.root)

    def test_identical_template_copy_passes(self):
        self._write_module_and_copy()
        errors = []
        modules = check_sync.check_module_copies(self.repo.root, errors)
        self.assertEqual([], errors)
        self.assertEqual(1, len(modules))

    def test_diverged_template_copy_is_detected(self):
        self._write_module_and_copy(copy_body='Different body.\n')
        errors = []
        check_sync.check_module_copies(self.repo.root, errors)
        self.assertTrue(any('Template copy differs from module' in e for e in errors), errors)

    def test_missing_template_copy_is_detected(self):
        self._write_module_and_copy()
        (self.repo.root / 'instructions' / 'opencode' / 'project-template'
         / 'agent-rules' / 'coding.md').unlink()
        errors = []
        check_sync.check_module_copies(self.repo.root, errors)
        self.assertTrue(any('Missing template copy' in e for e in errors), errors)


class UpdateCategoryIndexTests(FixtureTestCase):
    def test_parse_link_files_requires_both_authoritative_files(self):
        (self.repo.root / 'catalog' / 'links' / 'skill-links.txt').unlink()
        with self.assertRaises(FileNotFoundError):
            update_category_index.parse_link_files(self.repo.root)

    def test_parse_link_files_sorts_and_skips_comments(self):
        self.repo.write_links(
            stable=['https://raw.githubusercontent.com/o/r/main/skills/b/SKILL.md',
                    '# a comment'],
            pinned=['https://raw.githubusercontent.com/o/r/main/skills/a/SKILL.md'])
        references = update_category_index.parse_link_files(self.repo.root)
        self.assertEqual(2, len(references))
        self.assertEqual(['a', 'b'], [r['name'] for r in references])
        self.assertTrue(all(r['repo'] == 'o/r' for r in references), references)

    def test_non_raw_urls_are_reported_as_unknown_repo(self):
        self.repo.write_links(
            stable=['https://github.com/o/r/blob/main/skills/b/SKILL.md'])
        references = update_category_index.parse_link_files(self.repo.root)
        self.assertEqual(['unknown'], [r['repo'] for r in references])

    def test_generate_is_deterministic(self):
        self.repo.write_skill('alpha-skill')
        self.repo.write_links(stable=['https://github.com/o/r/blob/main/skills/ext/SKILL.md'])
        self.repo.write_items([])
        first = update_category_index.generate(self.repo.root)
        second = update_category_index.generate(self.repo.root)
        self.assertEqual(first, second)

    def test_generate_lists_local_skills_and_links(self):
        self.repo.write_skill('alpha-skill')
        self.repo.write_links(stable=['https://github.com/o/r/blob/main/skills/ext/SKILL.md'])
        self.repo.write_items([])
        content = update_category_index.generate(self.repo.root)
        self.assertIn('alpha-skill', content)
        self.assertIn('https://github.com/o/r/blob/main/skills/ext/SKILL.md', content)
        self.assertIn('Auto-generated', content)


class CountsTests(FixtureTestCase):
    def _write_count_targets(self, body='placeholder\n'):
        """Create every file the counts generator expects to update."""
        targets = {
            'README.md': body,
            'catalog/README.md': body,
            'ATTRIBUTION.md': body,
            'skills/third-party/README.md': body,
        }
        for rel_path, text in targets.items():
            path = self.repo.root / rel_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f"intro\n\n{update_category_index.COUNTS_BLOCK_START}\n\n"
                f"{update_category_index.COUNTS_BLOCK_END}\n\noutro\n",
                encoding='utf-8', newline='\n')

    def test_compute_counts_reads_catalog_and_filesystem(self):
        self.repo.write_skill('alpha-skill')
        self.repo.write_skill('beta-skill')
        self.repo.write_links(
            stable=['https://raw.githubusercontent.com/o/r/main/skills/a/SKILL.md'],
            pinned=['https://raw.githubusercontent.com/o/r/main/skills/b/SKILL.md'])
        self.repo.write_items([
            {'id': 'original/alpha-skill', 'name': 'alpha-skill', 'authorship': 'original'},
            {'id': 'o/r:a', 'name': 'a', 'authorship': 'link-only'},
        ])
        counts = update_category_index.compute_counts(self.repo.root)
        self.assertEqual(2, counts['original_skills'])
        self.assertEqual(0, counts['bundled_third_party'])
        self.assertEqual(2, counts['external_link_only'])
        self.assertEqual(1, counts['stable_links'])
        self.assertEqual(1, counts['pinned_links'])
        self.assertEqual(2, counts['catalog_records'])
        self.assertEqual(1, counts['catalog_original'])
        self.assertEqual(1, counts['catalog_link_only'])

    def test_counts_block_is_written_between_the_markers(self):
        self._write_count_targets()
        self.repo.write_skill('alpha-skill')
        problems = update_category_index.update_counts_blocks(self.repo.root, write=True)
        self.assertEqual([], problems)
        text = (self.repo.root / 'README.md').read_text(encoding='utf-8')
        self.assertIn('| Original skills | 1 |', text)
        self.assertIn('intro', text)
        self.assertIn('outro', text)
        # The surrounding prose must survive the update.
        self.assertTrue(text.startswith('intro'))

    def test_counts_update_is_idempotent(self):
        self._write_count_targets()
        self.repo.write_skill('alpha-skill')
        update_category_index.update_counts_blocks(self.repo.root, write=True)
        first = (self.repo.root / 'README.md').read_text(encoding='utf-8')
        update_category_index.update_counts_blocks(self.repo.root, write=True)
        second = (self.repo.root / 'README.md').read_text(encoding='utf-8')
        self.assertEqual(first, second)

    def test_stale_counts_block_is_reported_in_check_mode(self):
        self._write_count_targets()
        self.repo.write_skill('alpha-skill')
        update_category_index.update_counts_blocks(self.repo.root, write=True)
        (self.repo.root / 'README.md').write_text(
            (self.repo.root / 'README.md').read_text(encoding='utf-8')
            .replace('| Original skills | 1 |', '| Original skills | 99 |'),
            encoding='utf-8', newline='\n')
        problems = update_category_index.update_counts_blocks(self.repo.root, write=False)
        self.assertTrue(any('stale' in p for p in problems), problems)

    def test_missing_markers_are_reported(self):
        (self.repo.root / 'README.md').write_text('no markers here\n', encoding='utf-8')
        problems = update_category_index.update_counts_blocks(self.repo.root, write=True)
        self.assertTrue(any('markers are missing' in p for p in problems), problems)


class MarkdownLinksTests(FixtureTestCase):
    def _write(self, rel_path, text):
        path = self.repo.root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def test_existing_target_produces_no_problems(self):
        self._write('docs/page.md', 'See [other](other.md).\n')
        self._write('docs/other.md', '# Other\n')
        problems, warnings = check_markdown_links.check_file(
            self.repo.root / 'docs' / 'page.md', self.repo.root)
        self.assertEqual([], problems)
        self.assertEqual([], warnings)

    def test_missing_target_is_reported(self):
        self._write('docs/page.md', 'See [gone](gone.md).\n')
        problems, warnings = check_markdown_links.check_file(
            self.repo.root / 'docs' / 'page.md', self.repo.root)
        self.assertTrue(any('gone.md' in p for p in problems), problems)
        self.assertEqual([], warnings)

    def test_external_links_and_anchors_are_ignored(self):
        self._write('docs/page.md', '[site](https://example.com) [anchor](#top)\n')
        problems, warnings = check_markdown_links.check_file(
            self.repo.root / 'docs' / 'page.md', self.repo.root)
        self.assertEqual([], problems)
        self.assertEqual([], warnings)

    def test_code_block_examples_are_ignored(self):
        self._write('docs/page.md', '```\n[example](missing-in-example.md)\n```\n')
        problems, warnings = check_markdown_links.check_file(
            self.repo.root / 'docs' / 'page.md', self.repo.root)
        self.assertEqual([], problems)

    def test_vendored_links_are_warnings_not_failures(self):
        self._write('skills/third-party/some-skill/SKILL.md', '[ref](../other/SKILL.md)\n')
        problems, warnings = check_markdown_links.check_file(
            self.repo.root / 'skills' / 'third-party' / 'some-skill' / 'SKILL.md',
            self.repo.root)
        self.assertEqual([], problems)
        self.assertTrue(any('vendored upstream link' in w for w in warnings), warnings)


if __name__ == '__main__':
    unittest.main()
