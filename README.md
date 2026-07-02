# charlieohara.com

My personal site — Data Engineer · MLOps.

A single scroll-down page (Writing → Certifications → Projects) with markdown-driven
blog posts, built by a small Python static site generator and deployed to GitHub Pages.

## Local Development

Dependencies are managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml` +
`uv.lock`). There is no setup step — `uv run` creates the venv and installs
dependencies automatically on first use.

### Preview the whole site locally (no push needed)

Build, then serve the `output/` folder — this is the exact same site that gets
deployed, so you can check everything before committing:

```bash
uv run build.py                       # render templates + posts -> output/
python3 -m http.server -d output 8000 # open http://localhost:8000
```

Or as a one-liner that rebuilds and serves:

```bash
uv run build.py && python3 -m http.server -d output 8000
```

After editing a template, CSS, or a post, re-run `uv run build.py` and refresh the
browser. (Static-file serving doesn't auto-rebuild — the `build.py` step is what
regenerates the HTML.)

`output/` and `.venv/` are gitignored — nothing generated is committed. The site is
built fresh by GitHub Actions on every push to `main`.

## Writing a New Post

Create a markdown file in `content/posts/` (the filename becomes the URL slug):

```markdown
---
title: "Your Post Title"
date: 2026-07-01
excerpt: "A one-line summary shown on the post cards."
---

Your post content here...
```

Rebuild with `uv run build.py`. Each post is published at `/posts/<slug>/`. The
homepage **Blog** section shows the 4 most recent posts, and the full archive
(every post, newest first) lives at `/blog/`.

## How It Works

- `build.py` reads `content/posts/*.md`, renders them (plus the homepage) through the
  Jinja2 templates, and writes a fully static site to `output/`.
- `templates/base.html` — shared `<head>`, nav, and footer.
- `templates/index.html` — the homepage (hero, Blog, Projects, Certifications).
- `templates/blog.html` — the full post archive at `/blog/`.
- `templates/post.html` — individual blog post layout.
- `static/` — `css/`, `js/`, `img/`; copied to the output root, referenced with
  absolute (`/...`) paths so they resolve from `/posts/<slug>/` too.
- Nav links (`Blog`, `Projects`, `Certifications`) are in-page anchors that scroll
  the homepage; the archive and individual posts have their own URLs.

## Deployment

Push to `main` — `.github/workflows/deploy.yml` builds the site and deploys it to
GitHub Pages automatically.

> **One-time setup:** the repo's Pages source must be set to **GitHub Actions**
> (Settings → Pages → Build and deployment → Source). With the older "Deploy from a
> branch" mode, the build step is ignored and Pages would serve the raw repo root.

The `CNAME` file (`www.charlieohara.com`) and `.nojekyll` are copied into `output/`
by `build.py`, so the custom domain and asset paths survive each deploy.

## Migrated Medium Posts

Older posts were imported from [Medium](https://medium.com/@cbohara) by
`scripts/migrate_medium.py` (RSS feed → markdown + local images) followed by
`scripts/fix_embeds.py` (inlines gist embeds as code blocks, converts YouTube
embeds to linked thumbnails). The RSS feed only serves the 10 most recent
posts; the 4 older ones were exported as structured JSON from a browser
(see `scripts/data/`) and converted by `scripts/migrate_medium_json.py`.
Each post records its original URL in `medium:` frontmatter, which
`templates/post.html` renders as an "Originally posted on Medium" line.
All are one-off scripts with dependencies declared inline (PEP 723) — run
them with `uv run scripts/<name>.py`.

## Stack

- **Build**: Python via uv (`markdown`, `Jinja2`, `python-frontmatter`)
- **Templates**: Jinja2 (`templates/`)
- **Styles**: Vanilla CSS (`static/css/redesign.css`)
- **Hosting**: GitHub Pages via GitHub Actions
