"""Publish step — only reachable once gate.check_gate() has passed.

Ports the deterministic parts of .claude/skills/post-blog/SKILL.md as plain
Python (path derivation, scanning existing posts, prev/next nav wiring,
index.html rebuild). The one genuinely judgment-requiring part — converting
markdown prose into HTML that matches the blog's established look and feel —
stays a Claude call using that skill's Step 3 instructions verbatim.
"""

from __future__ import annotations

import base64
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import anthropic
import requests

from errors import PipelineError

REPO_ROOT = Path(__file__).resolve().parents[2]
BLOG_ROOT = REPO_ROOT
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
MODEL = os.environ.get("PUBLISH_MODEL", "claude-sonnet-4-5-20250929")
CLOUDFLARE_BEACON = (
    '<!-- Cloudflare Web Analytics --><script defer '
    "src='https://static.cloudflareinsights.com/beacon.min.js' "
    'data-cf-beacon=\'{"token": "763b29a7634e48e48bbdcb37b13ba83a"}\'>'
    "</script><!-- End Cloudflare Web Analytics -->"
)

EXCLUDED_DIR_NAMES = {"sdd"}
DATED_POST_RE = re.compile(r"^(\d{8})-(.+)\.html$")


@dataclass
class PostInfo:
    path: Path  # absolute
    date_str: str  # YYYYMMDD
    year: str
    month: str
    filename: str
    title: str
    description: str

    @property
    def rel_from_root(self) -> str:
        return f"{self.year}/{self.month}/{self.filename}"


def derive_destination(source_path: Path) -> tuple[Path, str, str, str]:
    """Returns (destination_path, year, month, slug)."""
    today = date.today()
    year, month = f"{today.year:04d}", f"{today.month:02d}"
    stem = source_path.stem
    slug = re.sub(r"^\d{8}-", "", stem)
    filename = f"{today.year:04d}{today.month:02d}{today.day:02d}-{slug}.html"
    dest = BLOG_ROOT / year / month / filename
    return dest, year, month, slug


def _load_skill_prompt(skill_name: str) -> str:
    text = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    return text.strip()


def convert_markdown_to_html(markdown_text: str) -> str:
    """Delegates prose->HTML conversion to Claude using post-blog's Step 3
    rules verbatim, plus the most recent published post as a CSS/structure
    reference (the skill instructs "copy it verbatim rather than approximating
    it")."""
    posts = scan_posts()
    reference_html = posts[0].path.read_text(encoding="utf-8") if posts else ""
    system_prompt = (
        _load_skill_prompt("post-blog")
        + "\n\nYou are being invoked as just Step 3 (HTML conversion) of this skill. "
        "Output ONLY the complete standalone HTML document — no commentary, no code fences."
    )
    user_content = (
        f"Reference post to copy CSS/structure from verbatim:\n\n{reference_html}\n\n"
        f"---\n\nMarkdown draft to convert:\n\n{markdown_text}"
    )
    client = anthropic.Anthropic()
    attempted = f"convert draft markdown to HTML via Anthropic messages.create (model={MODEL})"
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=8192,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )
    except (anthropic.APIConnectionError, anthropic.RateLimitError, anthropic.InternalServerError) as e:
        raise PipelineError(
            type="transient", message=str(e), attempted=attempted, is_retryable=True,
            recovery=["retry the same call after a short backoff"],
        ) from e
    except anthropic.AuthenticationError as e:
        raise PipelineError(
            type="permission", message=str(e), attempted=attempted, is_retryable=False,
            recovery=["check ANTHROPIC_API_KEY in .env"],
        ) from e
    except anthropic.APIStatusError as e:
        raise PipelineError(
            type="validation", message=str(e), attempted=attempted, is_retryable=False,
            details={"status_code": e.status_code},
        ) from e

    html = "".join(b.text for b in response.content if b.type == "text").strip()
    if html.startswith("```"):
        html = re.sub(r"^```[a-zA-Z]*\n", "", html)
        html = re.sub(r"\n```$", "", html)
    return html


def ensure_beacon(html: str) -> str:
    if "cloudflareinsights.com/beacon.min.js" in html:
        return html
    return html.replace("</head>", f"{CLOUDFLARE_BEACON}\n</head>")


def extract_title_and_description(html: str) -> tuple[str, str]:
    import html as html_module

    title_m = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    # hero-subtitle is the current template; hero-intro was used by earlier posts.
    desc_m = re.search(r'class="hero-subtitle">\s*(.*?)\s*</p>', html, re.DOTALL) or re.search(
        r'class="hero-intro">\s*(.*?)\s*</p>', html, re.DOTALL
    )
    title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
    description = re.sub(r"\s+", " ", desc_m.group(1)).strip() if desc_m else ""
    description = re.sub(r"<.*?>", "", description)
    return html_module.unescape(title), html_module.unescape(description)


def scan_posts() -> list[PostInfo]:
    posts: list[PostInfo] = []
    for year_dir in sorted(BLOG_ROOT.glob("[0-9][0-9][0-9][0-9]")):
        if not year_dir.is_dir():
            continue
        for month_dir in sorted(year_dir.glob("[0-9][0-9]")):
            if not month_dir.is_dir() or month_dir.name in EXCLUDED_DIR_NAMES:
                continue
            for html_file in sorted(month_dir.glob("*.html")):
                m = DATED_POST_RE.match(html_file.name)
                if not m:
                    continue
                title, description = extract_title_and_description(html_file.read_text(encoding="utf-8"))
                posts.append(
                    PostInfo(
                        path=html_file,
                        date_str=m.group(1),
                        year=year_dir.name,
                        month=month_dir.name,
                        filename=html_file.name,
                        title=title or html_file.stem,
                        description=description,
                    )
                )
    posts.sort(key=lambda p: p.date_str, reverse=True)
    return posts


def _relative_link(frm_year: str, frm_month: str, to_year: str, to_month: str, to_filename: str) -> str:
    if frm_year == to_year and frm_month == to_month:
        return to_filename
    if frm_year == to_year:
        return f"../{to_month}/{to_filename}"
    return f"../../{to_year}/{to_month}/{to_filename}"


def find_previous_post(all_posts: list[PostInfo], new_date_str: str) -> PostInfo | None:
    """all_posts must be sorted newest-first and must NOT include the new post."""
    older = [p for p in all_posts if p.date_str < new_date_str]
    return older[0] if older else None


def wire_navigation(
    new_html: str, new_year: str, new_month: str, new_filename: str, previous: PostInfo | None
) -> tuple[str, str | None]:
    """Returns (new_post_html_with_nav, updated_previous_html_or_None)."""
    nav_parts = ['<a href="../../index.html">← Home</a>']
    if previous is not None:
        prev_link = _relative_link(new_year, new_month, previous.year, previous.month, previous.filename)
        nav_parts.append(f'<a href="{prev_link}">← Previous</a>')
    nav_html = f'<nav class="post-nav">\n  ' + "\n  ".join(nav_parts) + "\n</nav>\n"
    new_html_with_nav = re.sub(r"</body>", nav_html + "</body>", new_html, count=1)

    updated_previous_html = None
    if previous is not None:
        prev_content = previous.path.read_text(encoding="utf-8")
        next_link = _relative_link(previous.year, previous.month, new_year, new_month, new_filename)
        updated_previous_html = add_next_link(prev_content, next_link)

    return new_html_with_nav, updated_previous_html


def add_next_link(previous_html: str, next_link: str) -> str:
    if 'class="post-nav"' not in previous_html:
        nav_html = (
            '<nav class="post-nav">\n'
            '  <a href="../../index.html">← Home</a>\n'
            f'  <a href="{next_link}">Next →</a>\n'
            "</nav>\n"
        )
        return re.sub(r"</body>", nav_html + "</body>", previous_html, count=1)

    if re.search(r'<a href="[^"]*">Next →</a>', previous_html):
        return re.sub(r'<a href="[^"]*">Next →</a>', f'<a href="{next_link}">Next →</a>', previous_html)

    return re.sub(
        r"(</nav>)",
        f'  <a href="{next_link}">Next →</a>\n\\1',
        previous_html,
        count=1,
    )


def _format_display_date(date_str: str) -> str:
    d = date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))
    return d.strftime("%b %-d, %Y") if os.name != "nt" else d.strftime("%b %d, %Y").replace(" 0", " ")


def _esc(text: str) -> str:
    import html as html_module

    return html_module.escape(text, quote=False)


def build_index_html(current_index_html: str, all_posts: list[PostInfo]) -> str:
    recent, older = all_posts[:5], all_posts[5:]

    groups: list[tuple[str, str, list[PostInfo]]] = []
    for post in recent:
        if groups and groups[-1][0] == post.year and groups[-1][1] == post.month:
            groups[-1][2].append(post)
        else:
            groups.append((post.year, post.month, [post]))

    month_names = {
        "01": "January", "02": "February", "03": "March", "04": "April",
        "05": "May", "06": "June", "07": "July", "08": "August",
        "09": "September", "10": "October", "11": "November", "12": "December",
    }

    year_blocks: list[tuple[str, list[tuple[str, list[PostInfo]]]]] = []
    for year, month, posts_in_month in groups:
        if year_blocks and year_blocks[-1][0] == year:
            year_blocks[-1][1].append((month, posts_in_month))
        else:
            year_blocks.append((year, [(month, posts_in_month)]))

    main_parts = ['  <div class="year-group">']
    for year, month_groups in year_blocks:
        main_parts.append(f'    <p class="year-label">{year}</p>\n')
        for month, posts_in_month in month_groups:
            main_parts.append('    <div class="month-group">')
            main_parts.append(f'      <p class="month-label">{month_names[month]}</p>\n')
            for i, post in enumerate(posts_in_month):
                style = ' style="margin-top:1rem;"' if i > 0 else ""
                main_parts.append(
                    f'      <a class="post-card" href="{post.rel_from_root}"{style}>\n'
                    f'        <p class="post-date">{_format_display_date(post.date_str)}</p>\n'
                    f'        <h2 class="post-title">{_esc(post.title)}</h2>\n'
                    f'        <p class="post-desc">{_esc(post.description)}</p>\n'
                    f'        <span class="post-arrow">→</span>\n'
                    f"      </a>\n"
                )
            main_parts.append("    </div>\n")
        main_parts.append("")
    main_parts.append("  </div>\n")

    if older:
        main_parts.append('  <div class="previous-posts">')
        main_parts.append('    <p class="previous-label">Previous Posts</p>')
        main_parts.append('    <ul class="post-list">')
        for post in older:
            main_parts.append(
                "      <li>\n"
                f'        <span class="post-list-date">{_format_display_date(post.date_str)}</span>\n'
                f'        <a href="{post.rel_from_root}">{_esc(post.title)}</a>\n'
                "      </li>"
            )
        main_parts.append("    </ul>")
        main_parts.append("  </div>\n")

    new_main = '<main class="content">\n' + "\n".join(main_parts) + "\n</main>"
    return re.sub(r'<main class="content">.*?</main>', new_main, current_index_html, count=1, flags=re.DOTALL)


def _repo_slug() -> str:
    url = subprocess.run(
        ["git", "-C", str(BLOG_ROOT), "remote", "get-url", "origin"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    if not m:
        raise RuntimeError(f"could not parse GitHub repo slug from remote url: {url}")
    return m.group(1)


def push_to_github(changed_files: dict[str, str], commit_message: str, branch: str = "main") -> str:
    """changed_files: {repo-relative path: new content}. Returns the commit sha.

    Uses the Git Data API to build one tree/commit covering all files, so this
    lands as a single commit rather than one per file.
    """
    try:
        token = os.environ["GITHUB_TOKEN"]
    except KeyError as e:
        raise PipelineError(
            type="permission", message="GITHUB_TOKEN is not set", attempted="read GITHUB_TOKEN from environment",
            is_retryable=False, recovery=["set GITHUB_TOKEN in .env"],
        ) from e

    repo = _repo_slug()
    api = f"https://api.github.com/repos/{repo}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

    def _call(method: str, url: str, attempted: str, partial: dict[str, Any] | None = None, **kw) -> requests.Response:
        try:
            resp = requests.request(method, url, headers=headers, timeout=30, **kw)
            resp.raise_for_status()
            return resp
        except requests.exceptions.ConnectionError as e:
            raise PipelineError(
                type="transient", message=str(e), attempted=attempted, is_retryable=True,
                partial_results=partial, recovery=["retry — likely a network blip"],
            ) from e
        except requests.exceptions.Timeout as e:
            raise PipelineError(
                type="transient", message=str(e), attempted=attempted, is_retryable=True,
                partial_results=partial, recovery=["retry — the GitHub API request timed out"],
            ) from e
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status in (401, 403):
                raise PipelineError(
                    type="permission", message=str(e), attempted=attempted, is_retryable=False,
                    partial_results=partial, details={"status_code": status},
                    recovery=["check GITHUB_TOKEN has push access to this repo"],
                ) from e
            raise PipelineError(
                type="validation", message=str(e), attempted=attempted, is_retryable=False,
                partial_results=partial, details={"status_code": status, "body": e.response.text[:2000] if e.response is not None else None},
            ) from e

    ref = _call("GET", f"{api}/git/ref/heads/{branch}", f"read ref heads/{branch}")
    base_commit_sha = ref.json()["object"]["sha"]

    base_commit = _call("GET", f"{api}/git/commits/{base_commit_sha}", "read base commit")
    base_tree_sha = base_commit.json()["tree"]["sha"]

    tree_entries = []
    blobs_created: dict[str, str] = {}
    for path, content in changed_files.items():
        blob = _call(
            "POST", f"{api}/git/blobs", f"create blob for {path}",
            partial={"blobs_created": blobs_created},
            json={"content": base64.b64encode(content.encode("utf-8")).decode("ascii"), "encoding": "base64"},
        )
        blob_sha = blob.json()["sha"]
        blobs_created[path] = blob_sha
        tree_entries.append({"path": path, "mode": "100644", "type": "blob", "sha": blob_sha})

    tree = _call(
        "POST", f"{api}/git/trees", "create tree",
        partial={"blobs_created": blobs_created},
        json={"base_tree": base_tree_sha, "tree": tree_entries},
    )

    commit = _call(
        "POST", f"{api}/git/commits", "create commit",
        partial={"tree_sha": tree.json()["sha"], "blobs_created": blobs_created},
        json={"message": commit_message, "tree": tree.json()["sha"], "parents": [base_commit_sha]},
    )
    new_commit_sha = commit.json()["sha"]

    _call(
        "PATCH", f"{api}/git/refs/heads/{branch}", f"update ref heads/{branch}",
        partial={"commit_sha_created_but_not_pointed_to": new_commit_sha},
        json={"sha": new_commit_sha},
    )
    return new_commit_sha
