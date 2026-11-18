#!/usr/bin/env python3
"""
Check availability of the external skill URLs.

Reads catalog/links/skill-links.txt and catalog/links/pinned-links.txt, requests
each URL and reports HTTP failures. It verifies URL availability only; it does
not verify content, license, security or runtime compatibility.

Usage
    python scripts/check-links.py
    python scripts/check-links.py --timeout 20 --workers 8
    python scripts/check-links.py --limit 10

Exit codes
    0 = no hard failures (warnings such as 403/429 are allowed)
    1 = at least one URL returned a hard failure or could not be reached
"""

from __future__ import annotations

import argparse
import concurrent.futures
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

LINK_FILES = ('skill-links.txt', 'pinned-links.txt')
USER_AGENT = 'DracieVajko-SkillsSet-LinkCheck/1.0 (+https://github.com/DracieVajko/Dracievajko-SkillsSet)'
WARNING_CODES = {403, 429}
ALLOWED_SCHEMES = frozenset({'http', 'https'})


def read_links(root: Path) -> list[tuple[str, str]]:
    """Return (link file name, url) pairs for every catalogued external link."""
    links: list[tuple[str, str]] = []
    for name in LINK_FILES:
        path = root / 'catalog' / 'links' / name
        if not path.is_file():
            raise FileNotFoundError(f"Missing link file: {path}")
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            url = line.strip()
            if url and not url.startswith('#'):
                links.append((name, url))
    return links


def check_url(url: str, timeout: float) -> tuple[str, int | None, str]:
    """Request one URL and return (url, status, error).

    Only http and https URLs are requested; any other scheme is reported as an
    unsupported scheme without touching the network.
    """
    scheme = urllib.parse.urlparse(url).scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        return url, None, f'unsupported scheme: {scheme or "none"}'

    request = urllib.request.Request(
        url,
        headers={'User-Agent': USER_AGENT, 'Range': 'bytes=0-0'},
    )
    try:
        # nosec B310 - the scheme is validated against ALLOWED_SCHEMES above,
        # so only http and https URLs ever reach the network layer.
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return url, response.status, ''
    except urllib.error.HTTPError as exc:
        return url, exc.code, str(exc)
    except urllib.error.URLError as exc:
        return url, None, str(exc.reason)
    except Exception as exc:  # network stack and malformed URL failures
        return url, None, str(exc)


def collect_results(
    links: list[tuple[str, str]],
    timeout: float,
    workers: int,
) -> list[tuple[str, int | None, str]]:
    """Check every URL concurrently and return the results."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = [pool.submit(check_url, url, timeout) for _, url in links]
        return [future.result() for future in concurrent.futures.as_completed(futures)]


def classify_results(
    results: list[tuple[str, int | None, str]],
) -> tuple[list[tuple[str, int | None, str]], list[tuple[str, int | None, str]]]:
    """Split results into (warnings, failures). A status is ok for 2xx and 3xx."""
    warnings: list[tuple[str, int | None, str]] = []
    failures: list[tuple[str, int | None, str]] = []
    for url, status, error in results:
        if status is not None and 200 <= status < 400:
            continue
        if status in WARNING_CODES:
            warnings.append((url, status, error))
        else:
            failures.append((url, status, error))
    return warnings, failures


def report(
    warnings: list[tuple[str, int | None, str]],
    failures: list[tuple[str, int | None, str]],
) -> None:
    """Print warnings and failures in a stable, sorted order."""
    for url, status, error in sorted(warnings):
        print(f"WARN: HTTP {status} {url} ({error})")
    for url, status, error in sorted(failures):
        label = f"HTTP {status}" if status is not None else "NO RESPONSE"
        print(f"FAIL: {label} {url} ({error})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=None, help='Repository root (defaults to the parent of this script).')
    parser.add_argument('--timeout', type=float, default=20.0, help='Per-request timeout in seconds.')
    parser.add_argument('--workers', type=int, default=8, help='Concurrent requests (default: 8).')
    parser.add_argument('--limit', type=int, default=0, help='Check only the first N URLs (0 = all).')
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve() if args.root else Path(__file__).resolve().parent.parent
    try:
        links = read_links(root)
    except OSError as exc:
        print(f"ERROR: {exc}")
        return 1
    if args.limit > 0:
        links = links[:args.limit]

    print(f"Checking {len(links)} external URL(s) with {args.workers} worker(s)...")
    results = collect_results(links, args.timeout, args.workers)

    warnings, failures = classify_results(results)
    report(warnings, failures)
    print(
        f"Summary: {len(results) - len(warnings) - len(failures)} ok, "
        f"{len(warnings)} warning(s), {len(failures)} failure(s)"
    )
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
