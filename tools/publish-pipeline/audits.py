"""The three audits, ported from the real skills rather than reimplemented.

voice-check and prose-linter are pure LLM judgment — their SKILL.md prompts
(anti-pattern definitions, category lists, scoring guide) are loaded verbatim
and used as the system prompt, with a forced tool_use schema layered on top
so the gate gets typed fields instead of having to parse a Markdown report
(.claude/rules/structured-output.md).

rhythm-audit is fully deterministic — .claude/skills/rhythm-audit/scripts/analyze.py
already does the analysis and emits severity-tagged flags as JSON. No LLM call
is needed or made for it.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import anthropic

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
MODEL = os.environ.get("AUDIT_MODEL", "claude-sonnet-4-5-20250929")

_client: anthropic.Anthropic | None = None


def _client_singleton() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def _load_skill_prompt(skill_name: str) -> str:
    path = SKILLS_DIR / skill_name / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    return text.strip()


def _forced_tool_call(system_prompt: str, draft_text: str, tool_schema: dict[str, Any]) -> dict[str, Any]:
    response = _client_singleton().messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": draft_text}],
        tools=[tool_schema],
        tool_choice={"type": "tool", "name": tool_schema["name"]},
    )
    for block in response.content:
        if block.type == "tool_use":
            return block.input
    raise RuntimeError(f"model did not return the forced tool call {tool_schema['name']!r}")


VOICE_CHECK_SCHEMA = {
    "name": "voice_check_result",
    "description": "Structured result of the voice-check audit.",
    "input_schema": {
        "type": "object",
        "properties": {
            "score": {"type": "integer", "minimum": 1, "maximum": 10, "description": "Voice Alignment Score"},
            "anti_patterns": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "severity": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                        "quote": {"type": "string"},
                        "note": {"type": "string"},
                    },
                    "required": ["category", "severity", "quote", "note"],
                },
            },
            "signature_patterns": {
                "type": "object",
                "properties": {
                    "fragment_punches": {"type": "boolean"},
                    "personal_experience": {"type": "boolean"},
                    "specific_data": {"type": "boolean"},
                    "paragraph_length_ok": {"type": "boolean"},
                    "concrete_metaphors": {"type": "boolean"},
                },
                "required": [
                    "fragment_punches",
                    "personal_experience",
                    "specific_data",
                    "paragraph_length_ok",
                    "concrete_metaphors",
                ],
            },
            "top_fixes": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["score", "anti_patterns", "signature_patterns", "top_fixes"],
    },
}

PROSE_LINTER_SCHEMA = {
    "name": "prose_lint_result",
    "description": "Structured result of the prose-linter audit.",
    "input_schema": {
        "type": "object",
        "properties": {
            "genre": {"type": "string"},
            "signature_words": {
                "type": "array",
                "description": "Every Signature Words category instance found, any tier.",
                "items": {
                    "type": "object",
                    "properties": {
                        "word": {"type": "string"},
                        "tier": {"type": "integer", "enum": [1, 2, 3]},
                        "quote": {"type": "string"},
                    },
                    "required": ["word", "tier", "quote"],
                },
            },
            "transition_overload": {"type": "array", "items": {"type": "string"}},
            "filler_phrases": {"type": "array", "items": {"type": "string"}},
            "syntactic_flags": {"type": "array", "items": {"type": "string"}},
            "structural_flags": {"type": "array", "items": {"type": "string"}},
            "tonal_tells": {"type": "array", "items": {"type": "string"}},
            "priority_fixes": {"type": "array", "items": {"type": "string"}},
        },
        "required": [
            "genre",
            "signature_words",
            "transition_overload",
            "filler_phrases",
            "syntactic_flags",
            "structural_flags",
            "tonal_tells",
            "priority_fixes",
        ],
    },
}


def run_voice_check(draft_text: str) -> dict[str, Any]:
    system_prompt = _load_skill_prompt("voice-check")
    return _forced_tool_call(system_prompt, draft_text, VOICE_CHECK_SCHEMA)


def run_prose_lint(draft_text: str) -> dict[str, Any]:
    system_prompt = _load_skill_prompt("prose-linter")
    result = _forced_tool_call(system_prompt, draft_text, PROSE_LINTER_SCHEMA)

    # Per structured-output.md: don't trust the model's own arithmetic for a
    # cross-field total. Compute the counts the gate relies on ourselves.
    tier1_count = sum(1 for w in result["signature_words"] if w.get("tier") == 1)
    total_flags = (
        len(result["signature_words"])
        + len(result["transition_overload"])
        + len(result["filler_phrases"])
        + len(result["syntactic_flags"])
        + len(result["structural_flags"])
        + len(result["tonal_tells"])
    )
    result["tier1_signature_words"] = tier1_count
    result["total_flags"] = total_flags
    return result


def run_rhythm_audit(draft_text: str) -> dict[str, Any]:
    script = SKILLS_DIR / "rhythm-audit" / "scripts" / "analyze.py"
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(draft_text)
        temp_path = f.name
    try:
        proc = subprocess.run(
            [sys.executable, str(script), temp_path],
            capture_output=True,
            text=True,
            check=True,
        )
    finally:
        Path(temp_path).unlink(missing_ok=True)
    return json.loads(proc.stdout)
