#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["requests"]
# ///
"""Convert Medium format=json exports to markdown posts in content/posts/.

Medium's RSS feed only serves the 10 most recent posts; the 4 older posts were
exported by fetching https://medium.com/@cbohara/<slug>?format=json from a
logged-in browser page (the endpoint is Cloudflare-protected against plain
HTTP clients). The export at scripts/data/medium_missing_posts.json bundles
each post's structured paragraphs plus a mediaResourceId -> embed-src map
resolved the same way.

Gists are inlined as fenced code blocks, YouTube embeds become locally-hosted
thumbnails linking to the video, giphy embeds become inline gifs, and images
are downloaded to static/img/medium/.

Usage (deps declared inline above, auto-installed by uv):
    uv run scripts/migrate_medium_json.py [export.json]
"""

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests

from fix_embeds import gist_markdown, youtube_markdown

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"
IMG_DIR = ROOT / "static" / "img" / "medium"
DEFAULT_EXPORT = ROOT / "scripts" / "data" / "medium_missing_posts.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

# Medium paragraph types
P, H3, IMG, BQ, PQ, PRE, ULI, OLI, IFRAME, H4, MIXTAPE = 1, 3, 4, 6, 7, 8, 9, 10, 11, 13, 14


def utf16_slice(text, start, end):
    """Markup offsets are UTF-16 code units, not code points."""
    b = text.encode("utf-16-le")
    return b[2 * start : 2 * end].decode("utf-16-le")


def utf16_len(text):
    return len(text.encode("utf-16-le")) // 2


def escape_md(text):
    return re.sub(r"([*_`\[\]])", r"\\\1", text)


def wrap(seg, styles, href):
    """Wrap an escaped text segment in inline markdown markers."""
    if not seg.strip():
        return seg
    # keep whitespace outside the markers so emphasis stays valid markdown
    lead = seg[: len(seg) - len(seg.lstrip())]
    trail = seg[len(seg.rstrip()) :]
    core = seg.strip()
    if 10 in styles:  # code
        core = f"`{core}`"
    if 1 in styles:  # bold
        core = f"**{core}**"
    if 2 in styles:  # italic
        core = f"*{core}*"
    if href:
        core = f"[{core}]({href})"
    return f"{lead}{core}{trail}"


def render_text(text, markups):
    """Apply Medium markups (bold/italic/code/link) to a paragraph's text."""
    n = utf16_len(text)
    if n == 0:
        return ""
    # per-unit annotation: set of style types + link href
    styles = [set() for _ in range(n)]
    hrefs = [None] * n
    for m in markups:
        for i in range(m["start"], min(m["end"], n)):
            if m["type"] == 3:
                hrefs[i] = m.get("href")
            else:
                styles[i].add(m["type"])
    # emit maximal runs with identical annotation
    out, run_start = [], 0
    for i in range(1, n + 1):
        if i == n or styles[i] != styles[run_start] or hrefs[i] != hrefs[run_start]:
            seg = utf16_slice(text, run_start, i)
            is_code = 10 in styles[run_start]
            seg = seg if is_code else escape_md(seg)
            out.append(wrap(seg, styles[run_start], hrefs[run_start]))
            run_start = i
    return "".join(out)


def download_image(url, name):
    resp = requests.get(url, headers=UA, timeout=30)
    resp.raise_for_status()
    (IMG_DIR / name).write_bytes(resp.content)
    return f"/img/medium/{name}"


def image_markdown(para, slug, index):
    image_id = para["metadata"]["id"]
    ext = Path(image_id).suffix.lower() or ".jpg"
    if ext == ".jpeg":
        ext = ".jpg"
    if ext == ".":
        ext = ".jpg"
    path = download_image(f"https://miro.medium.com/v2/{image_id}", f"{slug}-{index}{ext}")
    caption = render_text(para.get("text", ""), para.get("markups", []))
    md = f"![]({path})"
    if caption.strip():
        md += f"\n\n{caption}"
    return md


def embed_markdown(media_src, slug):
    """Turn a resolved embed src URL into markdown."""
    src = html.unescape(media_src or "")
    gist = re.search(r"gist\.github\.com/cbohara/([0-9a-f]+)\.js", src)
    if gist:
        return gist_markdown(gist.group(1))
    if "embedly" in src:
        qs = parse_qs(urlparse(src).query)
        target = (qs.get("url") or [""])[0]
        yt = re.search(r"[?&]v=([\w-]+)", target)
        if yt:
            return youtube_markdown(yt.group(1))
        if "giphy.com" in target:
            gif_url = (qs.get("image") or [""])[0]
            gif_id = gif_url.rstrip("/").split("/")[-2] if gif_url else "gif"
            try:
                path = download_image(gif_url, f"{slug}-giphy-{gif_id}.gif")
                return f"![]({path})"
            except Exception:
                pass
        if target:
            return f"*Embedded content: <{target}>*"
    return f"*Embedded content: <{src}>*" if src else ""


def convert(full_slug, post, media):
    title = post["title"]
    subtitle = post["content"].get("subtitle", "").strip()
    date = datetime.fromtimestamp(post["firstPublishedAt"] / 1000, tz=timezone.utc).date()
    link = f"https://medium.com/@cbohara/{full_slug}"
    slug = re.sub(r"-[0-9a-f]{8,}$", "", full_slug)

    paragraphs = post["content"]["bodyModel"]["paragraphs"]
    blocks, img_count = [], 0  # blocks: (paragraph_type, markdown)
    for i, para in enumerate(paragraphs):
        ptype, text = para["type"], para.get("text", "")
        # Medium repeats the title/subtitle as the first paragraphs — skip them
        if i < 2 and text.strip() in (title, subtitle) and ptype in (H3, H4, BQ, PQ):
            continue
        rendered = render_text(text, para.get("markups", []))
        if ptype == P:
            blocks.append((P, rendered))
        elif ptype == H3:
            blocks.append((H3, f"## {rendered}"))
        elif ptype == H4:
            blocks.append((H4, f"### {rendered}"))
        elif ptype in (BQ, PQ):
            blocks.append((BQ, f"> {rendered}"))
        elif ptype == PRE:
            blocks.append((PRE, f"```\n{text}\n```"))
        elif ptype == ULI:
            blocks.append((ULI, f"- {rendered}"))
        elif ptype == OLI:
            blocks.append((OLI, f"1. {rendered}"))
        elif ptype == IMG:
            img_count += 1
            blocks.append((IMG, image_markdown(para, slug, img_count)))
        elif ptype == IFRAME:
            media_id = para["iframe"]["mediaResourceId"]
            blocks.append((IFRAME, embed_markdown(media.get(media_id), slug)))
        elif ptype == MIXTAPE:
            href = para["mixtapeMetadata"]["href"]
            label = escape_md(text.split("\n")[0])
            blocks.append((MIXTAPE, f"[{label}]({href})"))
        else:
            print(f"  ! unhandled paragraph type {ptype}: {text[:60]!r}")
    # join blocks; consecutive items of the same list stay in one block
    parts = []
    prev_type = None
    for btype, md_block in blocks:
        if not md_block.strip():
            continue
        sep = "\n" if btype in (ULI, OLI) and btype == prev_type else "\n\n"
        parts.append(sep + md_block if parts else md_block)
        prev_type = btype
    body = "".join(parts)

    excerpt = subtitle
    if not excerpt:
        for para in paragraphs:
            if para["type"] == P and len(para.get("text", "")) > 40:
                t = para["text"]
                excerpt = t if len(t) <= 200 else t[:200].rsplit(" ", 1)[0] + "…"
                break

    md = (
        f"---\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        f"date: {date.isoformat()}\n"
        f"excerpt: {json.dumps(excerpt, ensure_ascii=False)}\n"
        f"medium: {link}\n"
        f"---\n\n"
        f"{body}\n"
    )
    out = POSTS_DIR / f"{slug}.md"
    out.write_text(md)
    print(f"✓ {date}  {slug}.md  ({len(body)} chars)")


def main():
    export = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_EXPORT
    data = json.loads(export.read_text())
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for full_slug, post in data["posts"].items():
        convert(full_slug, post, data["media"])


if __name__ == "__main__":
    main()
