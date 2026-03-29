---
name: post-blog
description: Publish a new blog post to the brAin dump site. Use this skill when the user wants to publish a post (e.g. "post this", "publish the blog", "/post-blog"). Moves the file from /inbox, updates navigation, updates the index, and opens a PR.
---

The user wants to publish a new blog post to the brAin dump static site.

A new HTML file has been placed in the `/inbox` folder at the root of the project.

Follow these steps in order:

1. **Create a new git branch** for this publishing work (e.g. `publish/YYYYMMDD-<slug>`).

2. **Move the file** from `/inbox` into the appropriate folder based on today's date: `yyyy/MM/`.

3. **Rename the file** to prepend the current date: `yyyyMMdd-<original-filename>`.

4. **Add Cloudflare Web Analytics beacon**: Insert the beacon snippet from the Config section below just before the closing `</head>` tag in the new post HTML file.

5. **Add navigation footer to the new post**: edit the HTML file to add a footer bar with:
   - A "← Home" link back to `index.html` (relative path from the file's location)
   - A "← Previous" link to the last previously published blog post
   - The "Next →" slot left empty (no next post yet)

6. **Update the previously published blog's footer**: find the last published post and add/update its "Next →" link to point to the newly published post.

7. **Update `index.html`**:
   - Add the new post as the first/most recent entry
   - The index currently shows a flat list by year → month → post card
   - If a carousel is implemented in the future, the newest 4 posts go in the carousel and older ones move to the list below — apply that logic when applicable

8. **Commit all changes** to the branch with a clear commit message.

9. **Open a Pull Request** using `gh pr create` for the user to review before it goes live.

## Notes
- Always use today's date for the folder path and filename prefix
- Keep relative paths correct — files are nested under `yyyy/MM/` so links to `index.html` need `../../index.html`
- Match the existing look & feel of the site (same fonts, colors, card styles) when adding footer navigation
- Do not modify the content of the post itself, only add the footer navigation and the analytics beacon

## Config

Cloudflare Web Analytics beacon snippet — insert before `</head>` in every new post:

```html
<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "763b29a7634e48e48bbdcb37b13ba83a"}'></script><!-- End Cloudflare Web Analytics -->
```
