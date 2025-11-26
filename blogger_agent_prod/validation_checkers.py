"""Robust validation checkers used by LoopAgent-style retries."""
from __future__ import annotations
from typing import Any, Dict

class OutlineValidationChecker:
    def __init__(self, min_sections: int = 3):
        self.min_sections = min_sections

    def check(self, outline: Any):
        # Expected outline: {'title':..., 'sections':[{'title':..., 'notes':...}, ...]}
        if not isinstance(outline, dict):
            return type('E', (), {'escalate': False})()
        sections = outline.get('sections') if isinstance(outline, dict) else None
        if not isinstance(sections, list) or len(sections) < self.min_sections:
            return type('E', (), {'escalate': False})()
        for s in sections:
            if not isinstance(s, dict) or not s.get('title'):
                return type('E', (), {'escalate': False})()
        return type('E', (), {'escalate': True})()

class BlogPostValidationChecker:
    def __init__(self, min_words: int = 300):
        self.min_words = min_words

    def check(self, post: Any):
        if not isinstance(post, dict):
            return type('E', (), {'escalate': False})()
        title = post.get('title')
        body = post.get('body', '')
        if not title:
            return type('E', (), {'escalate': False})()
        words = len(str(body).split())
        if words < self.min_words:
            return type('E', (), {'escalate': False})()
        return type('E', (), {'escalate': True})()
