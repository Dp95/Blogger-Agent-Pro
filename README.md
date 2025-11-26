# Blogger Agent Pro

**Blogger Agent Pro** is a production-ready multi-agent system that automates the full blog creation workflow. From planning to writing, editing, and social media promotion, this system streamlines content creation, saving hours per week for technical bloggers and teams.

---

## Problem Statement
Writing blogs manually is laborious and time-consuming, requiring research, drafting, editing, and formatting each piece from scratch. Manual blog writing struggles to scale, forcing writers to compromise on quality or hire additional staff. Automation allows writers to focus on strategic direction, creative refinement, and adding unique insights.

---

## Solution Statement
Blogger Agent Pro uses specialized agents to:

- Research topics and gather information from multiple sources
- Generate outlines or full drafts based on tone, length, and audience
- Schedule and distribute posts across multiple platforms
- Monitor engagement metrics and suggest improvements

This transforms blog management into a streamlined, data-driven process.

---

## Architecture
The core system is the `blogger_agent`, a multi-agent ecosystem coordinated by the **interactive_blogger_agent**:

### Sub-Agents:
- **Content Strategist (`robust_blog_planner`)**: Creates structured outlines and integrates code snippets for technical blogs.
- **Technical Writer (`robust_blog_writer`)**: Produces detailed blog posts from approved outlines.
- **Editor (`blog_editor`)**: Iteratively edits the post based on user feedback.
- **Social Media Marketer (`social_media_writer`)**: Generates social media promotions for platforms like Twitter and LinkedIn.

### Tools:
- **File Saving (`save_blog_post_to_file`)**: Exports final blog post to Markdown.
- **Codebase Analysis (`analyze_codebase`)**: Scans directories for code context and summaries.
- **Validation Checkers**: Ensure outlines and posts meet quality standards.

---

## Workflow
1. **Analyze Codebase (Optional)**: Understand structure and content of user-provided code.  
2. **Plan**: Generate blog post outline via `robust_blog_planner`.  
3. **Refine**: Apply user feedback to improve the outline.  
4. **Visuals**: Select preferred visual content options.  
5. **Write**: `robust_blog_writer` generates the blog post.  
6. **Edit**: `blog_editor` iteratively refines content based on feedback.  
7. **Social Media**: Optionally generate social media posts using `social_media_writer`.  
8. **Export**: Save the final post as a Markdown file.

---

## Value Statement
Blogger Agent Pro reduces blog development time by 6–8 hours per week, allowing higher-quality content production across multiple domains. Future plans include integrating a trend-scanning agent to automatically generate blog topics.



---

## Installation

- Python 3.11.3 recommended.
- Create a virtual environment (e.g., `python -m venv venv`) and activate it.
- Install dependencies:

```bash
pip install -r requirements.txt

---
