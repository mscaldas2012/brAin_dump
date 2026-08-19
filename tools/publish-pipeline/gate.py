"""Deterministic publish gate — no LLM calls, no judgment.

Per .claude/rules/enforcement-vs-guidance.md: a compliance-relevant sequencing
requirement (all three audits must have run against the *current* draft) gets
a programmatic gate, not a prompt instruction. The linking identifier here is
the sha256 of the draft's current content — editing the draft changes the
hash, so previously-recorded audits stop satisfying the gate automatically.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

STATE_DIR = Path(__file__).resolve().parent / "state"

REQUIRED_AUDITS = ("voice_check", "prose_linter", "rhythm_audit")


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _state_path(slug: str) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR / f"{slug}.json"


def load_state(slug: str) -> dict[str, Any]:
    path = _state_path(slug)
    if not path.exists():
        return {"audits": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(slug: str, state: dict[str, Any]) -> None:
    _state_path(slug).write_text(json.dumps(state, indent=2), encoding="utf-8")


def _entry(state: dict[str, Any], content_hash: str) -> dict[str, Any]:
    audits = state.setdefault("audits", {})
    return audits.setdefault(
        content_hash,
        {"voice_check": None, "prose_linter": None, "rhythm_audit": None, "drift_acknowledged": False},
    )


def record_audit(slug: str, content_hash: str, audit_name: str, result: dict[str, Any]) -> None:
    if audit_name not in REQUIRED_AUDITS:
        raise ValueError(f"unknown audit: {audit_name}")
    state = load_state(slug)
    entry = _entry(state, content_hash)
    entry[audit_name] = result
    save_state(slug, state)


def acknowledge_drift(slug: str, content_hash: str) -> None:
    state = load_state(slug)
    entry = _entry(state, content_hash)
    entry["drift_acknowledged"] = True
    save_state(slug, state)


@dataclass
class GateResult:
    status: str  # "pass" | "blocked" | "needs_escalation"
    reason: str
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.status == "pass"


def check_gate(slug: str, draft_text: str, config: dict[str, Any]) -> GateResult:
    content_hash = compute_hash(draft_text)
    state = load_state(slug)
    entry = state.get("audits", {}).get(content_hash)

    if entry is None:
        return GateResult(
            "blocked",
            "No audits recorded for this draft's current content. Run audit_voice, "
            "audit_prose, and audit_rhythm first.",
            {"missing": list(REQUIRED_AUDITS), "content_hash": content_hash},
        )

    missing = [a for a in REQUIRED_AUDITS if entry.get(a) is None]
    if missing:
        return GateResult(
            "blocked",
            f"Missing audit(s) for this draft's current content: {', '.join(missing)}. "
            "If you edited the draft since last auditing, all three must run again.",
            {"missing": missing, "content_hash": content_hash},
        )

    voice = entry["voice_check"]
    prose = entry["prose_linter"]
    rhythm = entry["rhythm_audit"]

    voice_threshold = config["voice_score_threshold"]
    if voice["score"] < voice_threshold:
        return GateResult(
            "blocked",
            f"voice-check score {voice['score']}/10 is below the threshold of {voice_threshold}.",
            {"check": "voice_check.score", "score": voice["score"], "threshold": voice_threshold},
        )

    high_severity_voice = [p for p in voice.get("anti_patterns", []) if p.get("severity") == "HIGH"]
    if high_severity_voice:
        return GateResult(
            "blocked",
            f"voice-check found {len(high_severity_voice)} HIGH-severity anti-pattern(s).",
            {"check": "voice_check.anti_patterns", "flags": high_severity_voice},
        )

    prose_threshold = config["prose_flag_threshold"]
    if prose["tier1_signature_words"] > 0:
        return GateResult(
            "blocked",
            f"prose-linter found {prose['tier1_signature_words']} Tier-1 LLM signature word(s) "
            "(these are the strongest AI tells and always block).",
            {"check": "prose_linter.tier1_signature_words", "count": prose["tier1_signature_words"]},
        )
    if prose["total_flags"] > prose_threshold:
        return GateResult(
            "blocked",
            f"prose-linter flag count {prose['total_flags']} exceeds the threshold of {prose_threshold}.",
            {"check": "prose_linter.total_flags", "count": prose["total_flags"], "threshold": prose_threshold},
        )

    high_severity_rhythm = [f for f in rhythm.get("flags", []) if f.get("severity") == "high"]
    if high_severity_rhythm:
        return GateResult(
            "blocked",
            f"rhythm-audit found {len(high_severity_rhythm)} high-severity flag(s): "
            + "; ".join(f["type"] for f in high_severity_rhythm),
            {"check": "rhythm_audit.flags", "flags": high_severity_rhythm},
        )

    non_high_voice_flags = [p for p in voice.get("anti_patterns", []) if p.get("severity") in ("MEDIUM", "LOW")]
    if non_high_voice_flags and not entry.get("drift_acknowledged"):
        return GateResult(
            "needs_escalation",
            "voice-check flagged MEDIUM/LOW-severity deviations that may be intentional. "
            "Confirm with the author before publishing.",
            {"check": "voice_check.anti_patterns", "flags": non_high_voice_flags, "content_hash": content_hash},
        )

    blocked_names = config.get("blocked_names", [])
    lowered = draft_text.lower()
    hits = [name for name in blocked_names if name.lower() in lowered]
    if hits:
        return GateResult(
            "blocked",
            f"Draft mentions blocked name(s): {', '.join(hits)}. This is a hard block — no override.",
            {"check": "blocked_names", "hits": hits},
        )

    return GateResult("pass", "All gate checks passed.", {"content_hash": content_hash})
