#!/usr/bin/env python3
"""Check that every curated item still resolves to its first-party source."""

from __future__ import annotations

import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "news.json"
UA = "Mozilla/5.0 (compatible; AISignalVerifier/1.0)"
SSL_CONTEXT = ssl.create_default_context()


def check(url: str) -> tuple[int, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Range": "bytes=0-2048"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20, context=SSL_CONTEXT) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.geturl() or url
    except Exception as exc:  # Network exceptions are expected for protected sites.
        return 0, str(exc)


def main() -> int:
    items = json.loads(DATA.read_text(encoding="utf-8"))
    failures = 0
    for item in items:
        status, final = check(item["url"])
        if 200 <= status < 400:
            marker = "OK"
        elif status in (401, 403, 429):
            marker = "PROTECTED"
        else:
            marker = "REVIEW"
            failures += 1
        print(f"[{marker}] {item['id']} -> HTTP {status} | {final}")
    print(
        f"\nChecked {len(items)} curated links; {failures} need human review. "
        "PROTECTED means the origin blocks automated checks; verify titles/dates through its official RSS."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
