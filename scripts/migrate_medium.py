#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "beautifulsoup4", "markdownify"]
# ///
"""Convert Medium posts (via the RSS feed) to markdown posts in content/posts/.

Downloads each post's images to static/img/medium/ and rewrites the links,
and records the original Medium URL in the `medium:` frontmatter field
(rendered as an "Originally posted on Medium" line by templates/post.html).

Note: the feed renders gist/YouTube embeds as bare medium.com/media/... links;
run fix_embeds.py afterwards to replace those with real content.

Usage (deps declared inline above, auto-installed by uv):
    uv run scripts/migrate_medium.py
"""

import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

FEED_URL = "https://medium.com/@cbohara/feed"
ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"
IMG_DIR = ROOT / "static" / "img" / "medium"

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
NS = {"content": "http://purl.org/rss/1.0/modules/content/"}

# Manual title tweaks (two posts share the feed title "The Linux Command Line")
TITLE_OVERRIDES = {
    "https://medium.com/@cbohara/the-linux-command-line-19a4489ca0df":
        "Linux Command Line - Package Management",
}


def clean_link(link):
    """Strip Medium's RSS tracking query string."""
    p = urlparse(link)
    return f"{p.scheme}://{p.netloc}{p.path}"


def make_slug(link, used):
    """File slug from the Medium URL path, minus the trailing hex hash."""
    tail = urlparse(link).path.rstrip("/").split("/")[-1]
    slug = re.sub(r"-[0-9a-f]{8,}$", "", tail)
    if slug in used:
        slug = tail  # collision (e.g. two posts w/ same title): keep the hash
    used.add(slug)
    return slug


def download_image(src, slug, index):
    """Fetch a Medium CDN image into static/img/medium/, return new site path."""
    ext = Path(urlparse(src).path).suffix.lower()
    resp = requests.get(src, headers=UA, timeout=30)
    resp.raise_for_status()
    if not ext:
        ctype = resp.headers.get("content-type", "")
        ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
               "image/webp": ".webp"}.get(ctype.split(";")[0], ".jpg")
    if ext == ".jpeg":
        ext = ".jpg"
    name = f"{slug}-{index}{ext}"
    (IMG_DIR / name).write_bytes(resp.content)
    return f"/img/medium/{name}"


def excerpt_from(soup):
    """First paragraph, trimmed to ~200 chars on a word boundary."""
    for p in soup.find_all("p"):
        text = p.get_text(" ", strip=True)
        if len(text) > 40:
            if len(text) <= 200:
                return text
            return text[:200].rsplit(" ", 1)[0] + "…"
    return ""


def convert(item, used_slugs):
    link = clean_link(item.find("link").text)
    title = TITLE_OVERRIDES.get(link, item.find("title").text)
    date = datetime.strptime(item.find("pubDate").text[:16], "%a, %d %b %Y").date()
    html = item.find("content:encoded", NS).text
    slug = make_slug(link, used_slugs)

    soup = BeautifulSoup(html, "html.parser")

    # Drop Medium's invisible stat-tracking pixel
    for img in soup.find_all("img"):
        if "medium.com/_/stat" in (img.get("src") or ""):
            img.decompose()

    # Download images locally and point at them
    for i, img in enumerate(soup.find_all("img"), 1):
        src = img.get("src")
        if not src:
            continue
        try:
            img["src"] = download_image(src, slug, i)
        except Exception as e:
            print(f"  ! image failed, keeping remote URL: {src} ({e})")

    # Medium uses h3/h4 for section headings; site posts use h2/h3.
    # Promote h3 first so former h4s aren't promoted twice.
    for h in soup.find_all("h3"):
        h.name = "h2"
    for h in soup.find_all("h4"):
        h.name = "h3"

    excerpt = excerpt_from(soup)

    body = markdownify(str(soup), heading_style="ATX", bullets="-")
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    fm_title = json.dumps(title, ensure_ascii=False)
    fm_excerpt = json.dumps(excerpt, ensure_ascii=False)
    md = (
        f"---\n"
        f"title: {fm_title}\n"
        f"date: {date.isoformat()}\n"
        f"excerpt: {fm_excerpt}\n"
        f"medium: {link}\n"
        f"---\n\n"
        f"{body}\n"
    )
    out = POSTS_DIR / f"{slug}.md"
    out.write_text(md)
    print(f"✓ {date}  {slug}.md  ({len(body)} chars)")


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    resp = requests.get(FEED_URL, headers=UA, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    used_slugs = set()
    for item in root.iter("item"):
        convert(item, used_slugs)


if __name__ == "__main__":
    main()
