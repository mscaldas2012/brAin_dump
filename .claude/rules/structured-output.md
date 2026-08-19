---
name: structured-output
description: Schema-based structured output, when few-shot beats more instructions, and how to validate/retry extraction failures
paths:
  - "**/*extract*.*"
  - "**/*schema*.*"
  - "**/*tool*.*"
  - "**/*agent*.*"
---

# Structured output

## Schemas eliminate syntax errors, not semantic ones

`tool_use` + a JSON schema is the reliable path to structured output — it
eliminates malformed-JSON failures entirely. It does **not** prevent
semantic errors: a value in the wrong field, a total that doesn't sum, a
plausible-looking but factually wrong extraction. Those need the validation
layer described below, not a bigger or stricter schema — a schema
constrains *shape*, not business logic or arithmetic correctness. If a
semantic-error scenario is being fixed by "switch to tool_use," that's
already in place and isn't the actual fix; the fix is validation.

### Nullable fields, not universally required fields

Mark a field optional/nullable when the source material may genuinely lack
that information. Marking everything required "for completeness"
incentivizes fabrication — a model with a required field and no real value
to put there will produce a plausible-looking placeholder rather than admit
absence. Required fields belong on data that's actually always present;
everything else should be nullable, with the model expected to say "not
present" honestly.

### Enum pattern for extensible/ambiguous categories

`"other"` + a free-text detail field for categories the enum can't fully
enumerate ahead of time; `"unclear"` for genuine ambiguity in the source.
Don't force a value into a bad-fit enum option just because the schema
doesn't have an escape hatch — build the escape hatch in.

## Few-shot: the specific trigger condition

Few-shot examples (2-4 targeted ones) are the right lever specifically when
**detailed instructions already exist and ambiguous cases still produce
inconsistency.** This is a narrower claim than "add examples to improve
output" — if instructions don't exist yet, write the instructions first;
few-shot is for the case where instructions are already thorough and the
remaining inconsistency is coming from judgment calls that can't be fully
enumerated in prose (tool selection between similar options, a
coverage-gap judgment call, refund-vs-escalate routing).

**What makes an example useful isn't the input/output pair alone — it's the
reasoning.** A good few-shot example shows *why* one action was chosen over
a plausible alternative, so the model generalizes the underlying judgment to
novel cases it hasn't seen a literal example of — not just pattern-matches
against a fixed set of pre-specified inputs.

Don't reach for "add more detailed instructions/rules" when the actual
diagnosis is this trigger condition — more rules is the right move only
before instructions exist or are genuinely thin; once thorough instructions
already exist and inconsistency persists on ambiguous cases specifically,
more rules is treating the wrong layer.

## Validation, retry, and feedback loops

The core mechanism: on a validation failure, retry **with the specific
error included**, not a bare "try again." A follow-up request should carry
all three of: the original document/input, the failed extraction, and the
specific validation error — not just one or two of the three.

Retry has real limits, and recognizing them matters as much as running the
loop: retrying is ineffective when the required information is genuinely
absent from the source (not a formatting problem, an information-availability
problem) or when the source itself contains an inherent error (a typo
printed in the original document). No number of retries fixes either case —
recognize when a mismatch is a document-level problem rather than an
extraction-quality problem, and route it to human review instead of
retry-looping indefinitely.

**Self-correction pattern for arithmetic-style checks**: carry a
`calculated_total` field alongside the `stated_total` the source claims, and
a `conflict_detected` boolean when they genuinely disagree — this catches
real inconsistency in the source itself, distinct from an extraction
mistake. Adding more schema rules doesn't fix a cross-field arithmetic
error — a schema constrains shape, not the relationship between fields.

**Feedback-loop design for dismissal-pattern analysis**: a `detected_pattern`
field tracking which construct in the source triggered a given finding lets
later analysis identify which patterns are frequently dismissed as false —
this is the extraction-quality analog of `review-architecture.md`'s
false-positive management, applied to extraction findings instead of code
review findings.

### Implementing retry-with-feedback via hooks

Where a harness's post-execution hook is available, it can implement this
pattern at the orchestration layer rather than purely in the prompt:
a `block` decision with a `reason` rejects an extraction and surfaces that
reason to the model on its next turn — the loop continues automatically,
and the model often re-issues the tool call on its own initiative in
response. A non-blocking `additionalContext`-style output can flag an issue
without blocking. And a deterministic result-rewrite (no model judgment
involved) can fix what's fixable without another round-trip at all.

Hooks like this are stateless per call — an attempt counter or
previous-extraction state has to be held externally (e.g. a small tracker
object the hook function closes over), not assumed to persist inside the
hook itself between invocations.

## Traps

| Trap | Why it's wrong |
|---|---|
| "Switch to tool_use" as the fix for a semantic-error scenario | tool_use already eliminates syntax errors; semantic correctness needs the validation layer, not a bigger schema |
| Marking every field required "for completeness" | Incentivizes fabrication on fields the source may genuinely lack — use nullable instead |
| "Add more detailed instructions/rules" when instructions already exist and inconsistency is on ambiguous judgment calls | Wrong layer — that's the specific trigger condition for few-shot, not more prose |
| Confusing precision-on-well-defined-categories work with ambiguous-judgment-call work | The former is explicit-criteria territory (`review-architecture.md`'s false-positive management); the latter is few-shot territory — different fixes for different failure shapes |
| Treating retry as universal | A genuine document-level error or missing source information won't resolve no matter how many retries — recognize and route to human review instead |
| "Add more schema rules" as a fix for a cross-field arithmetic mismatch | Schema constrains shape, not the relationship between fields — that needs a self-correction check (`calculated_total`/`conflict_detected`), not a stricter schema |
| Treating tool_choice `"any"` and forced-tool selection as interchangeable when guaranteed structured output is needed | See `tool-interface-design.md` — `"any"` still leaves the model choosing which tool; only forced selection removes the choice entirely |
