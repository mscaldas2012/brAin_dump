---
name: error-contract
description: The shared structured shape every tool result and subagent failure should report through, instead of ad hoc strings or booleans
paths:
  - "**/*tool*.*"
  - "**/*agent*.*"
  - "**/*subagent*.*"
  - "**/*hook*.*"
  - "**/tools/**"
  - "**/agents/**"
  - "**/hooks/**"
---

# Error contract

Every tool result and subagent failure that isn't a clean success reports
through one shape. Not because the exact field names matter in isolation,
but because a generic `"Operation failed"` string collapses categorically
different failures into one undifferentiated signal — and the caller (a
coordinator, a retry loop, a human) can't choose the right response to a
signal that doesn't say what actually happened.

## The shape

```yaml
type: transient | validation | business_rule | permission
message: string              # human-readable summary
details: object               # category-specific structured fields
is_retryable: boolean         # load-bearing — prevents wasted retries
attempted: string             # what was actually tried
partial_results: object | null  # anything usable recovered before failure
next_steps:
  recovery: [string]          # what the caller could try
  alternatives: [string]      # fallback paths if recovery isn't possible
```

## The four categories

| Category | Example | Retry? | Caller behavior |
|---|---|---|---|
| **Transient** | Timeout, service unavailable | Yes | Retry, possibly with backoff |
| **Validation** | Malformed input, bad ID format | Only after correcting the input — not a blind identical retry | Fix the input, then retry |
| **Business rule** | Refund exceeds policy limit | No | Explain to the user / escalate |
| **Permission** | Caller lacks access rights | No | Escalate / report the limitation |

`is_retryable` is what actually drives caller behavior — don't make the
caller re-derive it from `type` by convention. Set it explicitly, every
time. And note validation is genuinely nuanced: not retryable *as the
identical call*, but can succeed once the input is corrected first. If code
or a prompt is checking "is this retryable" only to blindly resend the same
arguments, that's wrong for the validation category specifically — the
retry has to carry a corrected input, not just resend.

## Access failure ≠ valid empty result

A tool that ran successfully and legitimately found nothing returns a
**success** with an empty payload. That is not this error shape at all —
it never touches `type`/`is_retryable`/etc. Conflating "I looked and there's
nothing there" with "I couldn't look" breaks every downstream consumer's
ability to trust an empty result. If a caller can't tell the difference
between "zero matches" and "the search never actually ran," it will either
distrust real empty results or silently accept a masked failure as if it
were data. Keep these as structurally distinct paths, not two ways of
producing the same shape.

## Local recovery before escalation

A subagent (or any component with its own retry capability) should absorb
and retry its own transient failures internally, using this shape only
internally to decide *whether* it can recover — not surfacing every internal
retry attempt to its caller. Only propagate upward what couldn't be
resolved locally, and when it does propagate, `attempted` and
`partial_results` are not optional — they're what let the coordinator make
an informed recovery decision instead of guessing. A coordinator that gets
paged for every transient hiccup a subagent already recovered from on its
own is drowning in noise that adds nothing.

## Never terminate the whole workflow over one failure

If one subagent (or one step, one document, one section) fails and reports
through this contract, the coordinator's default response is to propagate
the structured context and decide from there — not to kill the entire
multi-agent run. A single subagent's exhausted retries doesn't mean the rest
of the system's work is invalid; it means one piece of it has a gap that
needs to be represented, not one failure that needs to cascade.

## Coverage annotations for synthesis-type outputs

When multiple sources/sections/subagents feed one aggregated output, don't
let a partial failure silently shrink the output or get filled with vague,
unearned prose ("this area appears less documented"). Mark it explicitly:

```json
{
  "sections": [
    {"topic": "pricing", "status": "complete", "sources_succeeded": 4, "content": "..."},
    {"topic": "features", "status": "complete", "sources_succeeded": 5, "content": "..."},
    {"topic": "sentiment", "status": "gap", "failure_type": "transient",
     "attempted": "scrape reviews.example.com for 5 vendors",
     "alternatives": ["retry with a different source", "use an alternate API"],
     "content": null}
  ]
}
```

The gap section says what was tried and why it's missing, using the same
`attempted`/`alternatives` vocabulary as the base contract — a reader (human
or coordinator) can act on that. A silently shrunk output or a vague
placeholder gives them nothing to act on.

## Traps

| Trap | Why it's wrong |
|---|---|
| Retrying every failed call N times regardless of category | Wastes calls on business-rule/permission errors that can never succeed via retry, no matter the category — those need a completely different response, not more attempts |
| A generic `"Operation failed"` / `"unavailable"` string, even after internal retries are exhausted | Still removes the caller's ability to differentiate response strategy — the exact anti-pattern this contract exists to prevent, and "we retried first" doesn't excuse a generic status at the point of final propagation |
| Treating "zero results" and "couldn't check" as the same shape | Breaks trust in every future empty result from that source |
| "Validation errors are always retryable" or "always never retryable" | Neither — not retryable identically, retryable once corrected; conflating the two produces either wasted blind retries or a caller that gives up on genuinely fixable input |
| A coordinator that gets escalated every resolved transient hiccup | Defeats the purpose of local recovery, floods the coordinator with noise it can't act on |
| Killing an entire multi-agent run because one component reported through this contract | Correct pattern is propagate-and-decide, not terminate; use a coverage annotation instead |
| Silently shrinking an aggregated output instead of marking the gap | Readers can't tell "this doesn't exist" from "this wasn't covered" |
