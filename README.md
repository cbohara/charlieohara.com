# charlieohara.com

My personal site — Data Engineer · MLOps.

A single scroll-down page (Writing → Certifications → Projects) with markdown-driven
blog posts, built by a small Python static site generator and deployed to GitHub Pages.

## Local Development

```bash
# First-time setup (once)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Preview the whole site locally (no push needed)

Build, then serve the `output/` folder — this is the exact same site that gets
deployed, so you can check everything before committing:

```bash
python build.py                       # render templates + posts -> output/
python -m http.server -d output 8000  # open http://localhost:8000
```

Or as a one-liner that rebuilds and serves:

```bash
python build.py && python -m http.server -d output 8000
```

After editing a template, CSS, or a post, re-run `python build.py` and refresh the
browser. (Static-file serving doesn't auto-rebuild — the `build.py` step is what
regenerates the HTML.)

If you used the venv without activating it, prefix the commands with `.venv/bin/`,
e.g. `.venv/bin/python build.py`.

`output/` and `.venv/` are gitignored — nothing generated is committed. The site is
built fresh by GitHub Actions on every push to `main`.

## Writing a New Post

Create a markdown file in `content/posts/` (the filename becomes the URL slug):

```markdown
---
title: "Your Post Title"
date: 2026-07-01
excerpt: "A one-line summary shown on the homepage Writing section."
---

Your post content here...
```

Rebuild with `python build.py`. Each post is published at `/posts/<slug>/`, and the
homepage **Writing** section lists every post automatically (newest first).

There is no separate blog index page — the homepage Writing section is the full list.
If the post count ever gets large, reintroduce a `/writing/` archive page in `build.py`.

## How It Works

- `build.py` reads `content/posts/*.md`, renders them (plus the homepage) through the
  Jinja2 templates, and writes a fully static site to `output/`.
- `templates/base.html` — shared `<head>`, nav, and footer.
- `templates/index.html` — the homepage (hero, Writing, Certifications, Projects).
- `templates/post.html` — individual blog post layout.
- `static/` — `css/`, `js/`, `img/`; copied to the output root, referenced with
  absolute (`/...`) paths so they resolve from `/posts/<slug>/` too.
- Nav links (`Writing`, `Certifications`, `Projects`) are in-page anchors that scroll
  the homepage; only individual posts have their own URLs.

## Deployment

Push to `main` — `.github/workflows/deploy.yml` builds the site and deploys it to
GitHub Pages automatically.

> **One-time setup:** the repo's Pages source must be set to **GitHub Actions**
> (Settings → Pages → Build and deployment → Source). With the older "Deploy from a
> branch" mode, the build step is ignored and Pages would serve the raw repo root.

The `CNAME` file (`www.charlieohara.com`) and `.nojekyll` are copied into `output/`
by `build.py`, so the custom domain and asset paths survive each deploy.

## Stack

- **Build**: Python (`markdown`, `Jinja2`, `python-frontmatter`)
- **Templates**: Jinja2 (`templates/`)
- **Styles**: Vanilla CSS (`static/css/redesign.css`)
- **Hosting**: GitHub Pages via GitHub Actions
