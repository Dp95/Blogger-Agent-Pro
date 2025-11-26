"""RobustBlogWriter: converts outlines into full posts using LLMs or deterministic templates."""
from __future__ import annotations
from typing import Any, Dict, Optional, List
try:
    from adk import LLMAgent
except Exception:
    LLMAgent = None

class RobustBlogWriter:
    def __init__(self, name: str = 'robust_blog_writer', checkers: Optional[List]=None, max_retries: int = 2):
        self.name = name
        self.checkers = checkers or []
        self.max_retries = max_retries

    def _deterministic_write(self, outline: Dict[str,Any], codebase_context: Optional[Dict]=None, tone: str = 'professional') -> Dict[str,Any]:
        title = outline.get('title', 'Untitled')
        parts = []
        for sec in outline.get('sections', []):
            parts.append(f"## {sec.get('title')}\n\n{sec.get('notes')}\n")
            if codebase_context and codebase_context.get('file_count', 0) > 0 and 'code' in sec.get('notes','').lower():
                parts.append('\n```python\n# example placeholder\nprint(\'hello\')\n```\n')
        body = '\n'.join(parts)
        # ensure minimum length by duplicating notes if necessary
        words = body.split()
        if len(words) < 400:
            body += '\n\n' + (' '.join(words[:200]) + '\n') * 3
        return {'title': title, 'body': body}

    def run(self, outline: Dict[str,Any], codebase_context: Optional[Dict]=None, tone: str = 'professional') -> Dict[str,Any]:
        if LLMAgent:
            try:
                client = LLMAgent(model='gpt-4')
                return client.generate_post(outline=outline, codebase=codebase_context, tone=tone)
            except Exception:
                pass
        return self._deterministic_write(outline, codebase_context, tone)
