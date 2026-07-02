#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["requests"]
# ///
"""Replace Medium media-embed placeholder lines in migrated posts.

Medium's RSS feed renders gist/YouTube embeds as escaped <a> tags pointing at
medium.com/media/<hash>. Those endpoints sit behind a Cloudflare challenge, so
the hash -> real source mapping below was extracted once from the live post
pages in a browser. If a future post adds a new embed, load the post in a
browser and check window.__APOLLO_STATE__ (MediaResource entries) or fetch
https://medium.com/media/<hash> from the page's own JS console.

Gists are inlined as fenced code blocks (fetched from the GitHub API);
YouTube videos become a locally-hosted thumbnail linking to the video.

Usage (deps declared inline above, auto-installed by uv):
    uv run scripts/fix_embeds.py   # after migrate_medium.py
"""

import re
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"
IMG_DIR = ROOT / "static" / "img" / "medium"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

MEDIA = {
    "00ef1050cf444c66c01acfc76b57a5d1": ("gist", "743ef95a8107591fbf36e011463d1b35"),
    "151b11782280cebcec48e00a21259213": ("youtube", "7YcW25PHnAA"),
    "19dd5233ac790332af0ec3034b1ce8c1": ("gist", "1bc6bb7d194e54140f5f06377f37e5e6"),
    "39a0d93815f43d85e91dcf1369cb0cb6": ("youtube", "KUB-aJXquUA"),
    "3f3a5b5f130cc7077fa22acfe340a817": ("gist", "4a8dedcb87375e2d16d562a0179fc6f2"),
    "4623a7ff7d76bde774763b79023d0b77": ("gist", "b219fa8b303d433ddb9a65d4979b945d"),
    "5d0af6a473b4e9fc76a970a472bed856": ("gist", "56285dc42ba522dd69b77b942ebe851d"),
    "7af7011ae46de1c426575aa72cd3aa11": ("youtube", "pGYAg7TMmp0"),
    "a19e522e8e72e13e77db28998236216b": ("youtube", "tum6VbSDJkA"),
    "a21019a0fa67bd00aedb2a46b04dec06": ("youtube", "k0bb7UYy0pY"),
    "d79dee36c24d5a1e89a26f2df9c2b657": ("gist", "842366c609a3be6f93802969991d3aa0"),
    "e711879bfb18e8bd6fa6a3f1c23bd68a": ("youtube", "TzeBrDU-JaY"),
    "e8f75b7f066f55f1160a2b013fa27268": ("gist", "88ffc134bb315adf5106348fc60d8e03"),
    "f5de6b5a21c02e550d273c1537b7b5b3": ("gist", "0351416456f9bab3b76d1d0583bf13b8"),
    "ff9d8616e3379514fea14eb93c60a4c6": ("gist", "52189d4b844ec29a40fdd56918204711"),
}

LANG_BY_EXT = {
    ".py": "python", ".js": "javascript", ".rb": "ruby", ".sh": "bash",
    ".yml": "yaml", ".yaml": "yaml", ".json": "json", ".html": "html",
    ".css": "css", ".sql": "sql", ".java": "java", ".txt": "",
}


def gist_markdown(gist_id):
    r = requests.get(f"https://api.github.com/gists/{gist_id}", headers=UA, timeout=30)
    r.raise_for_status()
    data = r.json()
    blocks = []
    for fname, f in data["files"].items():
        lang = (f.get("language") or "").lower()
        if not lang:
            lang = LANG_BY_EXT.get(Path(fname).suffix.lower(), "")
        if lang == "dockerfile" or fname.lower() == "dockerfile":
            lang = "dockerfile"
        content = f["content"].rstrip("\n")
        header = "" if fname.startswith("gistfile") else f"**`{fname}`**\n\n"
        blocks.append(f"{header}```{lang}\n{content}\n```")
    return "\n\n".join(blocks)


def youtube_markdown(video_id):
    title = "Watch on YouTube"
    try:
        o = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": f"https://www.youtube.com/watch?v={video_id}", "format": "json"},
            headers=UA, timeout=30,
        )
        if o.ok:
            title = o.json().get("title", title)
    except Exception:
        pass
    url = f"https://www.youtube.com/watch?v={video_id}"
    img_name = f"yt-{video_id}.jpg"
    try:
        thumb = requests.get(f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg", headers=UA, timeout=30)
        thumb.raise_for_status()
        (IMG_DIR / img_name).write_bytes(thumb.content)
        return f"[![{title}](/img/medium/{img_name})]({url})\n\n*Video: [{title}]({url})*"
    except Exception:
        return f"*Video: [{title}]({url})*"


def main():
    replacements = {}  # hash -> markdown, built lazily
    for md_file in sorted(POSTS_DIR.glob("*.md")):
        text = md_file.read_text()
        hashes = set(re.findall(r"medium\.com/media/([0-9a-f]{32})", text))
        if not hashes:
            continue
        for h in hashes:
            if h not in MEDIA:
                print(f"  ! unknown media hash {h} in {md_file.name} — see module docstring")
                continue
            if h not in replacements:
                kind, ref = MEDIA[h]
                replacements[h] = gist_markdown(ref) if kind == "gist" else youtube_markdown(ref)
                print(f"  resolved {h[:8]} ({kind})")
            # Replace the whole escaped-anchor line with the real content
            pattern = re.compile(r"^.*medium\.com/media/" + h + r".*$", flags=re.MULTILINE)
            text = pattern.sub(lambda m: replacements[h], text)
        md_file.write_text(text)
        print(f"✓ {md_file.name}")


if __name__ == "__main__":
    main()
