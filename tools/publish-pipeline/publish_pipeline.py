#!/usr/bin/env python3
"""Blog publish pipeline CLI.

load_draft -> run all three audits -> gate -> (escalate if needed) -> publish.

The gate (gate.check_gate) is pure deterministic Python, called directly in
this orchestrator's own control flow before publish.do_publish() is ever
invoked — per .claude/rules/enforcement-vs-guidance.md's "hookless" pattern:
since this script *is* the orchestrator (not an LLM deciding call order), the
check belongs in real code here, not in a prompt. The audits themselves still
use real LLM judgment (via audits.py, forced structured output) — only the
pass/fail decision is deterministic.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
load_dotenv(HERE / ".env")

import audits  # noqa: E402
import gate  # noqa: E402
import publish  # noqa: E402
import report  # noqa: E402
from errors import PipelineError  # noqa: E402

import json

with open(HERE / "config.json", encoding="utf-8") as f:
    CONFIG = json.load(f)

INBOX = publish.BLOG_ROOT / "inbox"


def _slug_for(source_path: Path) -> str:
    return re.sub(r"^\d{8}-", "", source_path.stem)


def _pick_draft(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).resolve()
        if not path.exists():
            sys.exit(f"error: {path} does not exist")
        return path
    if not INBOX.exists():
        sys.exit(f"error: no draft given and {INBOX} does not exist")
    candidates = sorted(
        (p for p in INBOX.iterdir() if p.is_file() and not p.name.startswith(".")),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        sys.exit(f"error: no draft given and {INBOX} is empty")
    return candidates[0]


def run_audits(draft_text: str, slug: str) -> dict:
    """Runs the three audits in sequence, persisting each via gate.record_audit
    as soon as it succeeds. If one raises, the ones that already succeeded
    stay recorded (a re-run only needs to redo what actually failed — see
    gate.check_gate's "missing" list), and the PipelineError carries the
    completed-so-far results as partial_results rather than losing them."""
    print("Running audits...")
    content_hash = gate.compute_hash(draft_text)
    completed: dict = {}

    print("  voice-check...")
    try:
        voice_result = audits.run_voice_check(draft_text)
    except PipelineError as e:
        e.partial_results = {**(e.partial_results or {}), "audits_completed": list(completed)}
        e.attempted = f"audit_voice: {e.attempted}"
        raise
    gate.record_audit(slug, content_hash, "voice_check", voice_result)
    completed["voice_check"] = voice_result
    print(f"    score: {voice_result['score']}/10, {len(voice_result['anti_patterns'])} anti-pattern(s)")

    print("  prose-linter...")
    try:
        prose_result = audits.run_prose_lint(draft_text)
    except PipelineError as e:
        e.partial_results = {**(e.partial_results or {}), "audits_completed": list(completed)}
        e.attempted = f"audit_prose: {e.attempted}"
        raise
    gate.record_audit(slug, content_hash, "prose_linter", prose_result)
    completed["prose_linter"] = prose_result
    print(
        f"    {prose_result['total_flags']} flag(s), "
        f"{prose_result['tier1_signature_words']} Tier-1 signature word(s)"
    )

    print("  rhythm-audit...")
    try:
        rhythm_result = audits.run_rhythm_audit(draft_text)
    except PipelineError as e:
        e.partial_results = {**(e.partial_results or {}), "audits_completed": list(completed)}
        e.attempted = f"audit_rhythm: {e.attempted}"
        raise
    gate.record_audit(slug, content_hash, "rhythm_audit", rhythm_result)
    completed["rhythm_audit"] = rhythm_result
    high = [f for f in rhythm_result.get("flags", []) if f.get("severity") == "high"]
    print(f"    {len(rhythm_result.get('flags', []))} flag(s), {len(high)} high-severity")

    return completed


def handle_escalation(slug: str, draft_text: str, result: gate.GateResult) -> bool:
    print("\n--- Voice drift needs a human call ---")
    print(result.reason)
    for flag in result.details.get("flags", []):
        print(f"  [{flag['severity']}] {flag['category']}: \"{flag['quote']}\" — {flag['note']}")
    answer = input("\nIs this drift intentional? [y/N] ").strip().lower()
    if answer == "y":
        gate.acknowledge_drift(slug, gate.compute_hash(draft_text))
        return True
    return False


def _pr_body(audit_results: dict, gate_reason: str) -> str:
    lines = ["Opened automatically by the publish pipeline. Audit summary:", ""]
    vc = audit_results.get("voice_check")
    if vc:
        lines.append(f"- **voice-check**: {vc['score']}/10, {len(vc.get('anti_patterns', []))} anti-pattern(s)")
    pl = audit_results.get("prose_linter")
    if pl:
        lines.append(f"- **prose-linter**: {pl['total_flags']} flag(s), {pl['tier1_signature_words']} Tier-1")
    ra = audit_results.get("rhythm_audit")
    if ra:
        lines.append(f"- **rhythm-audit**: {len(ra.get('flags', []))} flag(s)")
    lines.append("")
    lines.append(f"Gate: {gate_reason}")
    return "\n".join(lines)


def do_publish(source_path: Path, draft_text: str, dry_run: bool, audit_results: dict, gate_reason: str) -> dict:
    dest, year, month, slug = publish.derive_destination(source_path)

    if source_path.suffix.lower() == ".html":
        new_html = publish.ensure_beacon(draft_text)
    else:
        new_html = publish.ensure_beacon(publish.convert_markdown_to_html(draft_text))

    existing_posts = publish.scan_posts()
    previous = publish.find_previous_post(existing_posts, dest.name[:8])
    new_html, updated_previous_html = publish.wire_navigation(new_html, year, month, dest.name, previous)

    title, description = publish.extract_title_and_description(new_html)
    new_post = publish.PostInfo(
        path=dest, date_str=dest.name[:8], year=year, month=month,
        filename=dest.name, title=title or slug, description=description,
    )
    all_posts = sorted([new_post, *existing_posts], key=lambda p: p.date_str, reverse=True)

    index_path = publish.BLOG_ROOT / "index.html"
    current_index_html = index_path.read_text(encoding="utf-8")
    new_index_html = publish.build_index_html(current_index_html, all_posts)

    changed_files = {new_post.rel_from_root: new_html, "index.html": new_index_html}
    if previous is not None and updated_previous_html is not None:
        changed_files[previous.rel_from_root] = updated_previous_html

    # Persist to the local worktree checkout first, regardless of dry_run —
    # this is the on-disk record of what's being published, independent of
    # whether the GitHub push below succeeds.
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(new_html, encoding="utf-8")
    index_path.write_text(new_index_html, encoding="utf-8")
    if previous is not None and updated_previous_html is not None:
        previous.path.write_text(updated_previous_html, encoding="utf-8")

    if dry_run:
        return {"published": True, "path": str(new_post.rel_from_root), "dry_run": True}

    base_branch = os.environ.get("GITHUB_BASE_BRANCH", "main")
    target_branch = f"publish/{slug}"
    commit_sha = publish.commit_to_branch(
        changed_files, commit_message=f"Publish: {title}", base_branch=base_branch, target_branch=target_branch
    )
    pr_url = publish.open_or_update_pull_request(
        target_branch, base_branch, title=f"Publish: {title}", body=_pr_body(audit_results, gate_reason)
    )
    source_path.unlink()

    return {
        "published": True, "path": str(new_post.rel_from_root),
        "commit_sha": commit_sha, "branch": target_branch, "pr_url": pr_url,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit and publish a blog draft.")
    parser.add_argument("draft", nargs="?", help="Path to the draft. Defaults to the newest file in /inbox.")
    parser.add_argument("--dry-run", action="store_true", help="Skip the GitHub push; write output locally.")
    args = parser.parse_args()

    source_path = _pick_draft(args.draft)
    slug = _slug_for(source_path)
    draft_text = source_path.read_text(encoding="utf-8")

    print(f"Draft: {source_path}")
    print(f"Slug: {slug}\n")

    audit_results: dict = {}
    try:
        audit_results = run_audits(draft_text, slug)

        result = gate.check_gate(slug, draft_text, CONFIG)
        escalation_record: dict | None = None

        if result.status == "needs_escalation":
            acknowledged = handle_escalation(slug, draft_text, result)
            escalation_record = {"acknowledged": acknowledged}
            if acknowledged:
                result = gate.check_gate(slug, draft_text, CONFIG)
            else:
                outcome = {"published": False, "reason": "author declined to confirm flagged voice drift"}
                print("\n" + report.render(slug, audit_results, result.status, result.reason, escalation_record, outcome))
                sys.exit(1)

        if not result.passed:
            print(f"\nGate blocked: {result.reason}")
            outcome = {"published": False, "reason": result.reason}
            print("\n" + report.render(slug, audit_results, result.status, result.reason, escalation_record, outcome))
            sys.exit(1)

        print("\nGate passed. Publishing...")
        outcome = do_publish(source_path, draft_text, args.dry_run, audit_results, result.reason)
        print("\n" + report.render(slug, audit_results, result.status, result.reason, escalation_record, outcome))
        if outcome.get("pr_url"):
            print(f"\nPR: {outcome['pr_url']}")
    except PipelineError as e:
        print(f"\n{e.render()}")
        outcome = {"published": False, "reason": f"[{e.type}] {e.message}"}
        print(
            "\n"
            + report.render(
                slug, audit_results, "error", str(e), None, outcome,
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
