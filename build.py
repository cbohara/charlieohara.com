#!/usr/bin/env python3
"""
build.py — Static site generator for charlieohara.com.

Reads markdown posts from content/posts/, renders them (plus the homepage and
blog listing) through Jinja2 templates, and outputs a fully static site to output/.

Usage:
    python build.py
    python -m http.server -d output   # preview locally at http://localhost:8000
"""

import shutil
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

# Paths
ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content" / "posts"
TEMPLATE_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "output"

# Markdown extensions for nicer rendering
MD_EXTENSIONS = ["fenced_code", "tables", "smarty", "toc", "attr_list"]


def format_date(value):
    """Format a frontmatter date (date/datetime or string) as 'June 26, 2026'."""
    if value is None:
        return ""
    if hasattr(value, "strftime"):
        return value.strftime("%B %-d, %Y")
    return str(value)


def load_posts():
    """Load all markdown posts, parse frontmatter, convert to HTML."""
    posts = []
    if not CONTENT_DIR.exists():
        return posts
    for md_file in sorted(CONTENT_DIR.glob("*.md")):
        post = frontmatter.load(md_file)
        html_content = markdown.markdown(post.content, extensions=MD_EXTENSIONS)
        posts.append(
            {
                "title": post.get("title", md_file.stem.replace("-", " ").title()),
                "date": post.get("date"),
                "date_display": format_date(post.get("date")),
                "excerpt": post.get("excerpt", ""),
                "slug": md_file.stem,
                "content": html_content,
                "url": f"/posts/{md_file.stem}/",
            }
        )
    # Sort by date, newest first
    posts.sort(key=lambda p: str(p["date"] or ""), reverse=True)
    return posts


def build():
    """Build the entire site."""
    # Clean output
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    posts = load_posts()

    # --- Homepage (also lists every post in the Writing section) ---
    index_html = env.get_template("index.html").render(posts=posts, current_page="home")
    (OUTPUT_DIR / "index.html").write_text(index_html)

    # --- Each post gets its own page at /posts/<slug>/ ---
    post_template = env.get_template("post.html")
    for post in posts:
        post_dir = OUTPUT_DIR / "posts" / post["slug"]
        post_dir.mkdir(parents=True)
        post_html = post_template.render(post=post, current_page="writing")
        (post_dir / "index.html").write_text(post_html)

    # --- Copy static assets to output root (css/, js/, img/) ---
    if STATIC_DIR.exists():
        for item in STATIC_DIR.iterdir():
            dest = OUTPUT_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

    # --- Copy CNAME and .nojekyll for GitHub Pages ---
    for f in ["CNAME", ".nojekyll"]:
        src = ROOT / f
        if src.exists():
            shutil.copy2(src, OUTPUT_DIR / f)

    print(f"✓ Built {len(posts)} post(s) → {OUTPUT_DIR}/")
    print(f"  Preview: python -m http.server -d {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
