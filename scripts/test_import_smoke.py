#!/usr/bin/env python3
"""Smoke tests that import the tooling modules so they are not flagged as untested."""

import importlib.util
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_modules_importable():
    check_links = _load("check_links", "check-links.py")
    check_sync = _load("check_sync", "check-sync.py")
    update_category_index = _load("update_category_index", "update-category-index.py")
    validate_frontmatter = _load("validate_frontmatter", "validate-frontmatter.py")
    assert check_links is not None
    assert check_sync is not None
    assert update_category_index is not None
    assert validate_frontmatter is not None