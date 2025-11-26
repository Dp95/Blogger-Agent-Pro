"""SocialMediaWriter: creates promotional copy tailored to platforms."""
from __future__ import annotations
from typing import Any, Dict, List, Optional

class SocialMediaWriter:
    def __init__(self, name: str = 'social_media_writer'):
        self.name = name

    def create_promotions(self, post: Dict[str,Any], platforms: Optional[List[str]] = None) -> Dict[str,str]:
        platforms = platforms or ['twitter','linkedin']
        title = post.get('title','')
        body = post.get('body','')
        excerpt = ' '.join(body.split()[:30])
        promos = {}
        for p in platforms:
            if p.lower() == 'twitter':
                promos['twitter'] = f"{title} — {excerpt}... Read: <link> #AI #Dev"                    elif p.lower() == 'linkedin':
                promos['linkedin'] = f"{title}\n\n{excerpt}... Read the full article: <link>"                    else:
                promos[p] = f"{title} - {excerpt}"                return promos
