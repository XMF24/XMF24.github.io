#!/usr/bin/env python3
"""Collect public AI news metadata from first-party sources.

This script intentionally does not auto-publish news. It produces raw,
reviewable candidates under data/collected.json. A human or LLM editor must
still verify the original article and produce the curated data/news.json file.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "collected.json"
UA = "Mozilla/5.0 (compatible; AISignalCollector/1.0; +https://localhost)"
TIMEOUT = 30

SOURCES = {
    "openai": "https://openai.com/news/rss.xml",
    "google_ai": "https://blog.google/technology/ai/rss/",
    "anthropic": "https://www.anthropic.com/news",
    "microsoft_sitemap": "https://blogs.microsoft.com/post-sitemap3.xml",
    "baidu_support": "https://cloud.baidu.com/support/news",
    "tencent_sitemap": "https://www.tencent.com/post-sitemap.xml",
}


def fetch(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        raw = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")


def clean_html(value: str) -> str:
    value = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(unescape(value).split())


def iso(value: str) -> str:
    """Return an ISO-compatible string without changing the source timezone."""
    value = value.strip()
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.isoformat()
    except ValueError:
        return value


def parse_rss(source: str, xml_text: str, limit: int = 12) -> list[dict]:
    root = ET.fromstring(xml_text)
    items = []
    for node in root.findall("./channel/item")[:limit]:
        items.append(
            {
                "source": source,
                "title": (node.findtext("title") or "").strip(),
                "summary": clean_html(node.findtext("description") or ""),
                "published_at": iso(node.findtext("pubDate") or ""),
                "url": (node.findtext("link") or "").strip(),
                "source_tier": "first-party",
            }
        )
    return items


def parse_anthropic(html_text: str, limit: int = 12) -> list[dict]:
    pattern = re.compile(
        r'<a href="(?P<url>/news/[^"]+)"[^>]*>.*?'
        r'<time[^>]*>(?P<date>[^<]+)</time>.*?'
        r'<span[^>]*>(?P<title>.*?)</span></a>',
        re.I | re.S,
    )
    items = []
    for match in pattern.finditer(html_text):
        title = clean_html(match.group("title"))
        if not title:
            continue
        items.append(
            {
                "source": "anthropic",
                "title": title,
                "published_at": match.group("date").strip(),
                "url": "https://www.anthropic.com" + match.group("url"),
                "source_tier": "first-party",
            }
        )
        if len(items) >= limit:
            break
    return items


def parse_sitemap(source: str, xml_text: str, url_filter=None, limit: int = 15) -> list[dict]:
    root = ET.fromstring(xml_text)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    rows = []
    for node in root.findall(".//s:url", ns):
        url = node.findtext("s:loc", default="", namespaces=ns)
        lastmod = node.findtext("s:lastmod", default="", namespaces=ns)
        if not url or (url_filter and not url_filter(url)):
            continue
        slug = url.rstrip("/").split("/")[-1]
        title = " ".join(slug.replace("-", " ").split()).strip()
        rows.append(
            {
                "source": source,
                "title": title,
                "published_at": lastmod,
                "url": url,
                "source_tier": "first-party",
            }
        )
    rows.sort(key=lambda row: row["published_at"], reverse=True)
    return rows[:limit]


def parse_baidu(html_text: str, limit: int = 8) -> list[dict]:
    pattern = re.compile(
        r'href="(?P<url>/support/news\?action=detail&amp;id=\d+)"[^>]*>(?P<title>.*?)</a>',
        re.I | re.S,
    )
    items = []
    seen = set()
    for match in pattern.finditer(html_text):
        title = clean_html(match.group("title"))
        url = unescape(match.group("url")).replace("&amp;", "&")
        if not title or url in seen:
            continue
        seen.add(url)
        items.append(
            {
                "source": "baidu",
                "title": title,
                "published_at": "",
                "url": "https://cloud.baidu.com" + url,
                "source_tier": "first-party",
            }
        )
        if len(items) >= limit:
            break
    return items


def main() -> int:
    collected: dict[str, list[dict]] = {}
    errors: dict[str, str] = {}

    fetchers = {
        "openai": lambda text: parse_rss("OpenAI", text),
        "google_ai": lambda text: parse_rss("Google AI", text),
        "anthropic": parse_anthropic,
        "microsoft_sitemap": lambda text: parse_sitemap(
            "Microsoft", text, url_filter=lambda url: "/blog/2026/" in url, limit=15
        ),
        "baidu_support": parse_baidu,
        "tencent_sitemap": lambda text: parse_sitemap(
            "Tencent", text, url_filter=lambda url: "/2026/" in url or "/newsroom/" in url, limit=15
        ),
    }

    for key, url in SOURCES.items():
        try:
            text = fetch(url)
            collected[key] = fetchers[key](text)
            print(f"[ok] {key}: {len(collected[key])} items")
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ValueError) as exc:
            errors[key] = str(exc)
            print(f"[warn] {key}: {exc}", file=sys.stderr)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "notice": "Raw discovery output only. Curate and verify before publication.",
        "sources": SOURCES,
        "errors": errors,
        "items": collected,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0 if collected else 1


if __name__ == "__main__":
    raise SystemExit(main())
