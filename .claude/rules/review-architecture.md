---
name: review-architecture
description: Why self-review underperforms, how to split large-diff review to avoid attention dilution, and how to manage false positives without losing trust
paths:
  - "**/*review*.*"
  - "**/*agent*.*"
---

# Review architecture

## Self-review is a structural bias, not a laziness problem

A model reviewing its own recent work retains the reasoning context from
generating it, and is structurally less likely to question decisions it just
made in the same session. This is not fixed by "enable extended thinking for
self-review" or "prompt it to be more critical" — both are same-session
workarounds for a bias that comes from the session itself, not from
insufficient reasoning effort or insufficient instruction. Re-running the
same self-review three times and comparing doesn't help either, if the bias
is systematic rather than random — repeating a biased process produces
correlated results, not independent confirmation.

**The fix is architectural: an independent review instance, with no access
to the generating instance's prior reasoning.** A fresh instance that only
sees the diff and the criteria — not the conversation that produced the
diff — outperforms self-review instructions or extended thinking, because
it isn't carrying forward the bias in the first place.

## Splitting large-diff review

A single mega-pass over a large multi-file change produces attention
dilution and contradictory findings across files — not because the model
lacks capacity, but because attention quality degrades independent of
context-window size. **A bigger or higher-tier model does not fix this** —
it's an attention-quality problem, not a capacity problem, and more room in
the window doesn't buy more attention per file.

Correct split: **per-file local analysis passes, plus a separate cross-file
integration pass.** Each file gets focused attention on its own, and the
integration pass is where cross-file consistency and interaction effects get
checked — instead of one pass trying to hold both concerns at once.

Two adjacent bad fixes, worth naming because they look plausible: shifting
the burden onto the author ("require smaller PR submissions") sidesteps
fixing the review architecture itself rather than fixing it; and requiring
consensus across multiple redundant passes before flagging anything actually
suppresses real findings that only surface intermittently — consensus
filtering optimizes for agreement, not for correctness, and a real issue
that one pass catches and another misses is exactly the kind of finding
consensus-gating throws away.

## Managing false positives without losing trust

**"Be conservative" or "only report high-confidence findings" does not
improve precision** — it's not a real lever, just an instruction that sounds
like one. What actually improves precision is explicit categorical
report-vs-skip criteria per finding category, with concrete examples at each
severity level rather than adjectives alone ("major," "minor" mean nothing
without an example anchoring what belongs in each).

**Trust doesn't stay scoped to the category that earned it.** A high
false-positive rate in one finding category (say, style nits) erodes trust
in *all* categories from that reviewer, including genuinely accurate ones
(say, security flags) — once a developer starts ignoring noisy findings,
they tend to stop reading the accurate ones too, because they've stopped
trusting the source, not just the noisy category.

Two different remediation levers, and they're not interchangeable:

- **Immediate**: temporarily disable the high-false-positive category
  entirely, to restore trust in what's left right away.
- **Long-term**: fix the underlying criteria for that category properly,
  separately, before re-enabling it.

Don't conflate these — "disable it" is the fast fix for the trust problem
today; "fix the prompt/criteria" is the real fix, and it happens on its own
timeline, not as a substitute for the immediate step.

Use explicit, named finding categories rather than a vague catch-all ("any
other major issue") — an unstructured bucket produces inconsistent
classification across runs, which undermines exactly the precision this
section is about.

## What a second pass should and shouldn't check

A second review instance shouldn't re-verify what a deterministic check
already covers reliably and cheaply — e.g. re-checking `stated_total`
against `calculated_total` arithmetic when a hook already does that at zero
marginal cost (see `structured-output.md`'s self-correction pattern). Its
actual value is catching what a deterministic arithmetic check structurally
*can't* see — compensating errors, for instance: two separate line-item
mistakes that happen to cancel out, producing a correct-looking total while
the underlying content is genuinely wrong. Point the independent-instance
review at the class of problem only judgment can catch; let cheap
deterministic checks handle everything they're capable of catching on their
own.

## Traps

| Trap | Why it's wrong |
|---|---|
| "Enable extended thinking" or "prompt it to be more critical" for self-review | Same-session workarounds for a structural bias that comes from the shared reasoning context, not from insufficient effort |
| "Re-run three times and compare" as a self-review fix | Doesn't help if the bias is systematic — correlated repeats of a biased process aren't independent confirmation |
| A bigger/higher-tier model proposed to fix attention dilution on a large diff | Doesn't address an attention-quality problem — more context capacity isn't more attention per file |
| "Require smaller PRs" as the fix for review inconsistency on large diffs | Shifts the burden to the author instead of fixing the review architecture itself |
| Requiring multi-pass consensus before flagging anything | Suppresses real findings that only surface intermittently — optimizes for agreement, not correctness |
| "Be conservative" / "only report high-confidence findings" as a precision fix | Not a real lever — doesn't actually change precision; use explicit categorical criteria instead |
| Fixing the underlying category criteria as the *first* response to an active trust problem | Too slow for the immediate need — disable the category first, fix criteria on its own timeline |
| A vague catch-all finding category ("any other major issue") | Produces inconsistent classification across runs |
| A second review pass re-verifying what a deterministic check already covers | Wastes the pass on something already reliable and cheap; point independent review at what only judgment can catch |
