"""Renders the end-of-run summary — printed to the terminal always, and saved
under reports/ so past runs stay reviewable."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

REPORTS_DIR = Path(__file__).resolve().parent / "reports"


def render(
    slug: str,
    audits: dict[str, Any],
    gate_status: str,
    gate_reason: str,
    escalation: dict[str, Any] | None,
    outcome: dict[str, Any],
) -> str:
    lines: list[str] = []
    lines.append(f"# Publish Pipeline Report — {slug}")
    lines.append(f"_{datetime.now().isoformat(timespec='seconds')}_")
    lines.append("")

    lines.append("## Audits")
    vc = audits.get("voice_check")
    if vc:
        lines.append(f"- **voice-check**: {vc['score']}/10")
        for p in vc.get("anti_patterns", []):
            lines.append(f"  - [{p['severity']}] {p['category']}: \"{p['quote']}\"")
    pl = audits.get("prose_linter")
    if pl:
        lines.append(
            f"- **prose-linter**: {pl['total_flags']} flag(s), "
            f"{pl['tier1_signature_words']} Tier-1 signature word(s)"
        )
    ra = audits.get("rhythm_audit")
    if ra:
        flag_summary = ", ".join(f"{f['type']} ({f['severity']})" for f in ra.get("flags", [])) or "none"
        lines.append(f"- **rhythm-audit**: {flag_summary}")
    lines.append("")

    lines.append("## Gate")
    lines.append(f"- **Status**: {gate_status}")
    lines.append(f"- **Reason**: {gate_reason}")
    if escalation:
        decision = "acknowledged (intentional)" if escalation.get("acknowledged") else "declined"
        lines.append(f"- **Escalation**: voice-check drift — {decision}")
    lines.append("")

    lines.append("## Outcome")
    if outcome.get("published"):
        lines.append(f"- Published: `{outcome['path']}`")
        if outcome.get("commit_sha"):
            lines.append(f"- Commit: `{outcome['commit_sha']}` on branch `{outcome.get('branch', '?')}`")
        if outcome.get("pr_url"):
            lines.append(f"- PR: {outcome['pr_url']}")
        if outcome.get("dry_run"):
            lines.append("- (dry-run — not pushed to GitHub, no branch/PR created)")
    else:
        lines.append(f"- Not published: {outcome.get('reason', 'gate did not pass')}")

    text = "\n".join(lines) + "\n"

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    (REPORTS_DIR / f"{slug}-{timestamp}.md").write_text(text, encoding="utf-8")

    return text
