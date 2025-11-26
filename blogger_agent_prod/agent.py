"""interactive_blogger_agent (production-grade)

Orchestrates the blog creation workflow using specialized sub-agents and tools.
Designed to integrate with google-adk when available; otherwise uses robust fallbacks.

Key features:
- Orchestration of planning, writing, editing, validation, saving, and promotion
- Integration points for external tools (RSS, Google Trends, code analysis)
- Clear, testable interfaces for sub-agents
"""
from __future__ import annotations
import os, json
from typing import Any, Dict, Optional

try:
    from adk import Agent, LoopAgent, EventActions  # real ADK primitives
except Exception:
    # Fallback lightweight primitives for local testing
    class Agent:
        def __init__(self, name: str, model: str = "gpt-4", description: str | None = None, **kwargs):
            self.name = name
            self.model = model
            self.description = description or ""

    class EventActions:
        def __init__(self, escalate: bool = False):
            self.escalate = escalate

    class LoopAgent(Agent):
        def __init__(self, *args, max_retries: int = 3, checkers: list | None = None, **kwargs):
            super().__init__(name=args[0] if args else "loop_agent", **kwargs)
            self.max_retries = max_retries
            self.checkers = checkers or []

        def loop_execute(self, fn, *args, **kwargs):
            last = None
            for i in range(self.max_retries):
                last = fn(*args, **kwargs)
                ok = True
                for c in self.checkers:
                    res = c.check(last)
                    if not getattr(res, "escalate", False):
                        ok = False
                        break
                if ok:
                    return last
            return last

from .agent_utils import safe_read, slugify_title
from .tools import save_blog_post_to_file, analyze_codebase, fetch_rss_headlines
from .validation_checkers import OutlineValidationChecker, BlogPostValidationChecker
from .sub_agents.strategist import RobustBlogPlanner
from .sub_agents.writer import RobustBlogWriter
from .sub_agents.editor import BlogEditor
from .sub_agents.social_media import SocialMediaWriter

class InteractiveBloggerAgent(Agent):
    """Top-level orchestrator for blog creation."""
    def __init__(self, name: str = "interactive_blogger_agent", model: str = "gpt-4", **kwargs):
        super().__init__(name=name, model=model, **kwargs)
        # instantiate subagents
        self.planner = RobustBlogPlanner(checkers=[OutlineValidationChecker()])
        self.writer = RobustBlogWriter(checkers=[BlogPostValidationChecker(min_words=400)])
        self.editor = BlogEditor()
        self.social = SocialMediaWriter()
        # tools
        self.save = save_blog_post_to_file
        self.analyze_code = analyze_codebase

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = context.get("prompt", "Write a technical blog post")[:1000]
        codebase_path = context.get("codebase_path")
        feeds = context.get("rss_feeds", [])

        code_ctx = None
        if codebase_path and os.path.exists(codebase_path):
            code_ctx = self.analyze_code(codebase_path)

        # 1) discover trending topics optionally
        rss_headlines = []
        if feeds:
            rss_headlines = fetch_rss_headlines(feeds)

        # 2) plan
        outline = self.planner.run(prompt=prompt, codebase_context=code_ctx, extras={"rss_headlines": rss_headlines})

        # ensure outline has title
        if not outline.get("title"):
            outline["title"] = prompt.split('\n')[0][:80]

        # 3) write the post
        post = self.writer.run(outline=outline, codebase_context=code_ctx, tone=context.get("tone", "technical"))

        # 4) edit stage (user feedback path may be provided in context['feedback'])
        feedback = context.get("feedback")
        if feedback:
            post = self.editor.edit(post, feedback=feedback)
        else:
            post = self.editor.edit(post, feedback=None)

        # 5) save result
        filepath = self.save(post["title"], post["body"], directory=context.get("output_dir", "./out"))

        # 6) social promos
        promos = self.social.create_promotions(post, platforms=context.get("platforms", ["twitter", "linkedin"]))

        return {
            "outline": outline,
            "post": post,
            "file_path": filepath,
            "promotions": promos,
            "codebase_context": code_ctx,
        }

if __name__ == "__main__":
    a = InteractiveBloggerAgent()
