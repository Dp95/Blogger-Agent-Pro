"""Tools used by agents: saving, simple analysis, RSS fetching"""
from __future__ import annotations
import os, json, glob, pathlib, logging
from typing import List, Dict, Any

from .agent_utils import safe_read, slugify_title

try:
    import feedparser
except Exception:
    feedparser = None

def save_blog_post_to_file(title: str, content: str, directory: str = './out') -> str:
    os.makedirs(directory, exist_ok=True)
    safe_title = slugify_title(title)
    filename = f"{safe_title}.md"
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(f"# {title}\n\n")
        fh.write(content)
    return path

def analyze_codebase(path: str) -> Dict[str, Any]:
    files = []
    for root, _, fns in os.walk(path):
        for fn in fns:
            files.append(os.path.join(root, fn))
    total_lines = 0
    ext_counts = {}
    sample = files[:20]
    for fp in files:
        try:
            text = safe_read(fp)
            total_lines += text.count('\n') + 1
        except Exception:
            continue
        _, ext = os.path.splitext(fp)
        ext_counts[ext or '<noext>'] = ext_counts.get(ext or '<noext>', 0) + 1
    top_ext = sorted(ext_counts.items(), key=lambda kv: kv[1], reverse=True)[:8]
    return {"file_count": len(files), "total_lines": total_lines, "top_extensions": top_ext, "sample_files": sample}

def fetch_rss_headlines(feeds: List[str], limit_per_feed: int = 5) -> List[Dict[str, str]]:
    results = []
    if not feedparser:
        return results
    for f in feeds:
        try:
            parsed = feedparser.parse(f)
            for entry in parsed.entries[:limit_per_feed]:
                results.append({"title": entry.get('title',''), "link": entry.get('link',''), "summary": entry.get('summary','')})
        except Exception:
            continue
    return results
