---
name: post-blog
description: Publish a new blog post from the /inbox folder to the brain_dump blog. ALWAYS use this skill when the user says "post the blog", "publish my post", "/post-blog", "post the file in inbox", "post my blog", "publish this to the blog", or any variation asking to move content from the inbox to the live blog. This skill handles markdown-to-HTML conversion using the existing blog's look and feel, file placement in the correct year/month folder, Cloudflare analytics injection, index.html updates (5 most recent as tiles, older as a list), and wiring up Home/Previous/Next navigation between posts.
---

# Post Blog

Publishes one or more files from the `/inbox` folder to the blog at the root of the `brain_dump` directory.

**Cloudflare analytics token:** `763b29a7634e48e48bbdcb37b13ba83a`

---

## Step 1 — Inventory the inbox

List all files in `{blog_root}/inbox/`. Skip `.DS_Store` and hidden files. If there are multiple files, process them one at a time, newest first.

---

## Step 2 — Determine the destination path

- **Date:** use today's date in `YYYYMMDD` format
- **Slug:** derive from the source filename — strip any existing date prefix, remove the extension, keep hyphens (e.g., `loops-and-metrics.md` → `loops-and-metrics`)
- **Destination:** `{blog_root}/{YYYY}/{MM}/{YYYYMMDD}-{slug}.html`
- Create the year/month directory if it doesn't exist

---

## Step 3 — Produce the HTML

### If the source is already HTML

1. Ensure the Cloudflare beacon is present inside `<head>` (see beacon snippet below)
2. Skip to Step 4

### If the source is Markdown

Convert to a full standalone HTML page that matches the blog's established look and feel. Read the most recent existing post for the exact CSS — copy it verbatim rather than approximating it. The structure:

**`<head>`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE FROM # HEADING}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500&family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
<style>
  /* — copy full CSS block from most recent post — */
</style>
<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "763b29a7634e48e48bbdcb37b13ba83a"}'></script><!-- End Cloudflare Web Analytics -->
</head>
```

**Hero section** (dark gradient header):
- `<p class="hero-kicker">` — short topic label inferred from content (e.g., "On AI Agents")
- `<h1>` — the `# Title` from markdown; if title has two parts separated by a period, make the second part italic: `Loops Are Overrated. <em>Metrics Are Not.</em>`
- `<p class="hero-subtitle">` — first paragraph or a one-sentence summary
- `<p class="hero-meta">` — `{Month YYYY} · {N} min read` (~200 words per minute)
- `<div class="hero-scroll"><span></span></div>`

**Article body** (`<article class="content">`):
- First content paragraph → `<p class="lede">` (larger, lighter intro)
- `## Section headings` → optionally preceded by `<p class="section-label">short label</p>`, then `<h2>`
- `---` → `<hr class="divider">` (use `class="divider heavy"` for major breaks)
- `**bold**` → `<strong>`, `*italic*` → `<em>`, `` `code` `` → `<code>`
- `[text](url)` → `<a href="url" target="_blank" rel="noopener">text</a>`
- Bullet lists with bold labels (e.g., `**Tone consistency:** desc`) → `<ul><li><strong>Label:</strong> desc</li></ul>`
- Blockquotes → `<blockquote>`

**Article footer:**
```html
<footer class="article-footer">
  <p>Written in the spirit of the brain dump: working through ideas by putting them in writing.</p>
</footer>
```

**Post nav CSS** (add to the `<style>` block if not already there):
```css
.post-nav { max-width: 720px; margin: 0 auto; padding: 2.5rem 2rem; border-top: 1px solid var(--rule); display: flex; justify-content: space-between; align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--muted); }
.post-nav a { color: var(--muted); text-decoration: none; letter-spacing: 0.05em; }
.post-nav a:hover { color: var(--accent); }
```

---

## Step 4 — Scan all published posts

Scan `{blog_root}` for all `*.html` files under `/{YYYY}/{MM}/` subfolders. Exclude files inside subdirectories like `sdd/`, SVG viewers, spec files, and `index.html` at the root.

Collect each post's: path, date (from filename prefix `YYYYMMDD`), title (from `<title>` tag), and description (from `hero-subtitle` or `lede` paragraph).

Sort all posts by date, newest first. Insert the new post at the top.

---

## Step 5 — Add navigation to the new post

Before the closing `</body>`, add:

```html
<nav class="post-nav">
  <a href="../../index.html">← Home</a>
  <a href="{relative-path-to-previous-post}">← Previous</a>
</nav>
```

Relative path from `{YYYY}/{MM}/` to another post:
- Same month: just the filename
- Different month, same year: `../{MM}/{filename}`
- Different year: `../../{YYYY}/{MM}/{filename}`

---

## Step 6 — Update the previous post's navigation

Find the post immediately before the new one in date order. Edit its HTML to add or update the Next link:

```html
<nav class="post-nav">
  <a href="../../index.html">← Home</a>
  <a href="{its-previous-post}">← Previous</a>
  <a href="{relative-path-to-new-post}">Next →</a>
</nav>
```

If the previous post already has a nav, add the Next link to it. If it has no nav, add the full block.

---

## Step 7 — Update index.html

Rebuild `<main class="content">` with:

**Top section — 5 most recent posts** as `post-card` tiles, grouped by year then month (same structure as the existing index). When a month has multiple posts in the top 5, stack them with `style="margin-top:1rem;"` on the second card onward.

**Bottom section — all older posts** as a simple list:

```html
<div class="previous-posts">
  <p class="previous-label">Previous Posts</p>
  <ul class="post-list">
    <li><span class="post-list-date">Mar 29, 2026</span><a href="2026/03/20260329-the_end_of_software_development.html">The End of Software as We Knew It</a></li>
    <!-- ... more posts, newest first within this list ... -->
  </ul>
</div>
```

Add these CSS rules to the index `<style>` block if not already present:
```css
.previous-posts { margin-top: 3rem; }
.previous-label { font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 0.68rem; letter-spacing: 0.25em; text-transform: uppercase; color: var(--muted); padding-bottom: 0.75rem; border-bottom: 1px solid var(--rule); margin-bottom: 1.5rem; }
.post-list { list-style: none; }
.post-list li { padding: 0.6rem 0; border-bottom: 1px solid var(--rule); font-family: 'Source Serif 4', serif; font-size: 0.95rem; }
.post-list li a { color: var(--ink); text-decoration: none; }
.post-list li a:hover { color: var(--accent); }
.post-list .post-list-date { font-family: 'DM Sans', sans-serif; font-size: 0.72rem; color: var(--muted); margin-right: 0.75rem; letter-spacing: 0.05em; }
```

---

## Step 8 — Push to GitHub

Use `mcp__github__push_files` to commit all changed files (new post, updated previous post, updated index.html) in a single API call. Do NOT use `git commit` or `git push` shell commands — sandbox git lock files cause failures.

---

## Step 9 — Clean up inbox

Delete the original source file from `/inbox` once the HTML is successfully pushed.

---

## Final checklist

Before reporting done, verify each item:
- [ ] HTML file exists at correct `{YYYY}/{MM}/{YYYYMMDD}-{slug}.html` path
- [ ] Cloudflare beacon present in `<head>`
- [ ] New post has `<nav class="post-nav">` with Home and Previous links
- [ ] Previous post updated with Next → link pointing to new post
- [ ] `index.html` shows exactly 5 most recent as cards, all older as a list
- [ ] All files pushed to GitHub via `mcp__github__push_files`
- [ ] Source file removed from `/inbox`
