"""BlogEditor: applies editing passes, style consistency, and user feedback."""
from __future__ import annotations
from typing import Any, Dict, Optional

class BlogEditor:
    def __init__(self, name: str = 'blog_editor'):
        self.name = name

    def edit(self, post: Dict[str,Any], feedback: Optional[str] = None) -> Dict[str,Any]:
        body = post.get('body','')
        # basic normalization: strip extra whitespace, ensure single newline between sections
        import re
        body = re.sub(r'\n{3,}', '\n\n', body).strip()
        if feedback:
            fb = feedback.lower()
            if 'shorten' in fb or 'concise' in fb:
                words = body.split()
                body = ' '.join(words[:300])
            if 'expand' in fb or 'more detail' in fb:
                body = body + '\n\n' + ('Additional details to expand the section.' * 20)
        post['body'] = body
        return post
