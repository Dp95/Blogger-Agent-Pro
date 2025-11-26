"""Utility functions used across the blogger_agent package."""
import os, re, json
from typing import Any

def safe_read(path: str, max_chars: int = 20000) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return fh.read(max_chars)
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin-1') as fh:
            return fh.read(max_chars)
    except Exception:
        return ''

def slugify_title(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r'[^a-z0-9\-\_ ]+', '', s)
    s = s.replace(' ', '_')[:160]
    return s
