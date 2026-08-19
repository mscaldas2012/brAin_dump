"""Shared structured error shape (.claude/rules/error-contract.md).

Every external call in this pipeline (Anthropic API, the rhythm-audit
subprocess, GitHub's REST/Git-Data API) raises PipelineError on failure
instead of letting a raw exception propagate as a bare traceback — so the
top-level CLI can tell a caller what category of failure happened, whether
retrying makes sense, what was already attempted, and what (if anything) was
salvaged before the failure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

ErrorType = Literal["transient", "validation", "business_rule", "permission"]


@dataclass
class PipelineError(Exception):
    type: ErrorType
    message: str
    attempted: str
    is_retryable: bool
    details: dict[str, Any] = field(default_factory=dict)
    partial_results: dict[str, Any] | None = None
    recovery: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        Exception.__init__(self, self.message)

    def __str__(self) -> str:  # so a bare `raise` / logger still prints something useful
        return f"[{self.type}] {self.message} (attempted: {self.attempted})"

    def render(self) -> str:
        lines = [f"ERROR [{self.type}]{' (retryable)' if self.is_retryable else ''}: {self.message}"]
        lines.append(f"  attempted: {self.attempted}")
        if self.details:
            lines.append(f"  details: {self.details}")
        if self.partial_results:
            lines.append(f"  partial results preserved: {list(self.partial_results.keys())}")
        if self.recovery:
            lines.append(f"  try: {'; '.join(self.recovery)}")
        if self.alternatives:
            lines.append(f"  alternatives: {'; '.join(self.alternatives)}")
        return "\n".join(lines)
