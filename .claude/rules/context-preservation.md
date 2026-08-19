---
name: context-preservation
description: How to keep critical specifics alive across long interactions and large codebase exploration, and how to preserve provenance when synthesizing from multiple sources
paths:
  - "**/*context*.*"
  - "**/*session*.*"
  - "**/*scratchpad*.*"
  - "**/*agent*.*"
---

# Context preservation

## Progressive summarization loses specifics, permanently

Condensing history flattens numeric values, percentages, dates, and
stated expectations into vaguer language. Once a summarization pass has
already discarded a specific number, it's gone for the rest of the
session — there's no getting it back from the summary alone. "Summarize
more aggressively" is not a fix for context pressure; it's the mechanism
that causes this exact loss, just applied harder.

**Fix: a persistent facts block**, carrying amounts, dates, order/record
numbers, and current statuses, included in every prompt *outside* the
summarized/compacted history — so it survives compaction instead of being
subject to it. In a harness where `/compact`-style mid-session compaction
exists, treat it as a form of this same progressive-summarization risk: safe
only when paired with a facts block or scratchpad that protects the
specifics compaction would otherwise flatten. Multi-issue sessions should
keep structured issue data in its own layer, separate from narrative
history, for the same reason.

This is a content-quality problem, not a can-we-skip-sending-it problem —
you still have to send the full conversation history on every request (no
server-side memory exists to lean on instead). The facts block doesn't
replace history; it's protected content riding alongside it.

## Lost in the middle

Models reliably attend to the start and end of long inputs, not reliably to
the middle. Put key summaries at the *beginning* of aggregated input, with
explicit section headers — not at the end, and not buried in the middle of
a long assembled document.

## Trim tool output before it enters context

Tool results accumulate volume disproportionate to relevance — a call
returning 40 fields when 5 are actually relevant is common. Trim at the
tool-response layer, before the result enters context at all — not via a
prompt instruction asking the model to "ignore" irrelevant fields once
they're already there. Instructing a model to ignore something already in
its context is weaker than never putting it there.

Upstream agents feeding a downstream agent with a limited context budget
should hand over structured data — facts, citations, relevance scores — not
verbose prose or full reasoning chains. The receiving agent's budget is
better spent on what it needs to act on than on reconstructing what the
upstream agent already worked out.

## Large codebase exploration

Extended exploration sessions show a specific degradation signature: the
model starts saying "typically these follow pattern X" instead of citing
the specific classes/files it actually found earlier — a sign that specifics
have been lost to summarization pressure, the same failure as above, just in
an exploration context.

- **Scratchpad files** — persist key findings to a file and reference it for
  later questions, externalizing memory outside the token window entirely
  rather than trusting it to survive in conversation history.
- **Subagent delegation for narrow verbose exploration** — spawn a subagent
  for something like "find all test files" and keep the main agent at a
  high level, so the noise of the search itself doesn't enter the main
  context (see `subagent-orchestration.md`).
- **Phase summarization** — summarize a completed phase's findings and
  inject that summary into the next phase's starting context. This is
  *not* the same anti-pattern as risky rolling summarization from earlier
  in this rule — the difference is deliberateness: phase summarization is a
  planned extraction step at a natural boundary, done once, with specifics
  protected by a scratchpad or facts block; rolling summarization is
  continuous lossy compression applied repeatedly under pressure.
- **Crash recovery via manifest** — each unit of work exports its state to a
  manifest at a known location; on resume, the coordinator loads that
  manifest and injects it into the resumed prompt, instead of restarting
  the entire exploration from scratch. A bigger context window fixes none
  of the above — this is an attention/specificity problem, not a capacity
  problem (same point `review-architecture.md` makes about large-diff
  review).

## Provenance in multi-source synthesis

Source attribution gets lost the moment summarization compresses findings
without preserving the mapping from claim back to source. The fix is a
**structured claim-source mapping** — claim, evidence excerpt, source
URL/document name — preserved and merged by whatever does the synthesis,
never paraphrased into an unattributed blob. Attribution embedded only in
prose (rather than a structured field) tends to get silently dropped in
later passes, since prose is exactly what subsequent summarization targets.

**Conflicting statistics from credible sources get annotated with both,
attributed** — never arbitrarily resolved by picking the more plausible
number, and never averaged or split. Both of those are fabrication dressed
up as reconciliation; the honest output is "source A says X, source B says
Y," not a synthesized third number nobody actually reported.

**Check dates before calling two numbers a contradiction.** A numeric
difference across time isn't necessarily a contradiction — require
publication/collection dates in structured outputs so this can actually be
checked, rather than assumed.

**Who decides what to do about a conflict is not the same as who surfaces
it.** A document-analysis step surfaces a conflicting value with annotation;
the *coordinator* — which has the fuller view of the whole pipeline —
decides how to reconcile it; *synthesis* preserves both values with
attribution in the final output rather than making the reconciliation call
itself. Synthesis lacks the visibility to judge which source is more
trustworthy in context; that judgment belongs upstream, at the coordinator.

**Format should match content type** — financial data as tables, news as
prose, technical findings as structured lists. Uniform formatting "for
consistency" destroys information; prose-ifying a pricing table, for
instance, is a real loss dressed up as tidiness.

## Traps

| Trap | Why it's wrong |
|---|---|
| "Summarize more aggressively" as a context-pressure fix | This is the risk itself, not a cure — it's what causes specifics to be lost |
| "Bigger context window" as a fix for degradation or attention issues | Treats a management/attention-quality problem as a capacity problem — capacity isn't the constraint |
| Instructing the model to "ignore" irrelevant tool-output fields via prompt | Weaker than trimming at the response layer before the content enters context at all |
| Putting key summaries at the end of aggregated input | Models attend more reliably to the start and end, not reliably to the middle — lead with the summary |
| Relying on conversation recall alone through a long exploration instead of scratchpad files | Externalized findings survive; in-context recall degrades with distance and pressure |
| Restarting an exploration from scratch after a crash instead of a manifest-based resume | Wastes already-completed work for no reason |
| Treating deliberate phase summarization as equivalent to risky rolling summarization | They're different in kind, not degree — deliberateness plus specifics-protection is what makes phase summarization safe |
| Synthesis "resolving" a source conflict by picking the more plausible number or averaging | Fabrication — annotate both with attribution instead |
| Treating two different numbers as an automatic contradiction without checking dates | A numeric difference across time may not be a contradiction at all |
| Synthesis (rather than the coordinator) deciding how to reconcile a conflict | Wrong owner — synthesis lacks the pipeline-wide visibility the coordinator has |
| Uniform formatting applied "for consistency" across different content types | Destroys information that format-appropriate output would have preserved |
