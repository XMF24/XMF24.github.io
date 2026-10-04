#!/usr/bin/env python3
"""Regenerate the offline-friendly data/news.js from data/news.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "data" / "news.json"
target = ROOT / "data" / "news.js"
data = json.loads(source.read_text(encoding="utf-8"))
target.write_text(
    "window.AI_NEWS_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)
print(f"Synced {len(data)} items to {target.relative_to(ROOT)}")
