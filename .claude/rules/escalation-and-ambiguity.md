---
name: escalation-and-ambiguity
description: The legitimate triggers for escalating to a human, why confidence and sentiment are unreliable proxies, and the first-line fix for miscalibrated escalation
paths:
  - "**/*escalat*.*"
  - "**/*agent*.*"
---

# Escalation and ambiguity

## Three legitimate triggers, and only three

1. **Explicit request for a human.** Honor immediately — no prior
   investigation gate required first. If someone asks for a human, that's
   the trigger on its own; don't make them justify it or wait for an
   automated attempt to fail first.
2. **A genuine policy gap** — the governing policy is *silent* on the
   situation, not merely that the situation is hard to resolve. "Hard but
   covered by policy" (a standard damage-replacement case with clear
   evidence, say) resolves autonomously. "Policy silent" (a request the
   policy simply never addresses — matching a competitor's price when
   policy only covers same-site adjustments, say) escalates. The dividing
   line is whether the applicable rule exists and is just being applied
   carefully, versus whether there is no applicable rule at all.
3. **Inability to make meaningful progress** — genuinely stuck, not merely
   slow or effortful.

Difficulty and escalation-worthiness are not the same axis. A hard case with
an applicable policy is still autonomous work; only genuine silence or
genuine inability crosses into escalation.

## Frustration and sentiment are not a fourth trigger

Acknowledge frustration and keep working the problem if it's within
capability to resolve — sentiment on its own doesn't change what's actually
solvable. Escalate on sentiment only if the customer reiterates that they
specifically want a human — at which point it collapses back into trigger 1,
not a new trigger of its own.

## Confidence and sentiment are unreliable proxies for complexity

Self-reported model confidence and customer sentiment are both flagged as
unreliable signals for whether a case is actually complex enough to warrant
escalation. A model is often confidently wrong precisely on the cases that
are actually hard — high self-reported confidence doesn't correlate with
being right on the cases where it matters most. Sentiment doesn't correlate
with underlying complexity either — a frustrated customer can have a simple
issue, and a calm one can have a genuinely policy-silent situation.

*(Contrast with `human-review-calibration.md`: this is about confidence used
raw, with no calibration path, for escalation decisions specifically — where
production ground truth for "should this have escalated" is hard to
accumulate. That rule covers a different, calibratable use of confidence in
a task shape where ground truth genuinely can be built up.)*

## Ambiguous identity — never resolve by heuristic

If a lookup returns multiple plausible matches (which customer, which
record), the correct move is to ask for an additional identifier — never to
pick one via a heuristic like "most recent" or "most likely." A heuristic
guess that's wrong here has the same category of consequence as the
identity-verification gate in `enforcement-vs-guidance.md` — silently acting
on the wrong record is not a graceful degradation, it's a wrong action taken
confidently.

## The proportionate first fix for miscalibrated escalation

When escalation calibration is off (escalating too much, too little, or on
the wrong signal), the first-line fix is **explicit escalation criteria plus
few-shot examples** in the governing prompt — not a classifier, not a
confidence-threshold model, not a sentiment model. This is the same
proportionality principle as `tool-interface-design.md`'s fix hierarchy and
`review-architecture.md`'s false-positive management: try the cheap,
prompt-level fix that directly targets the diagnosed cause before reaching
for new infrastructure. A dedicated classifier or ML model is a real option,
but it's not the first move — it's what you reach for only once
criteria-plus-examples has been tried and genuinely isn't enough.

## Traps

| Trap | Why it's wrong |
|---|---|
| Escalating because a case is hard, when policy actually covers it | Difficulty and policy-silence are different things — only the latter is a legitimate trigger |
| Treating customer frustration/sentiment as an escalation trigger on its own | Acknowledge and keep resolving within capability; escalate only if the customer reiterates wanting a human specifically |
| Using self-reported model confidence to gate escalation | Unreliable — the model is often confidently wrong exactly on the hard cases |
| Using sentiment analysis to gate escalation | Doesn't correlate with actual complexity |
| Resolving multiple ambiguous customer/record matches via a heuristic ("most recent") | Risks silently acting on the wrong record — ask for an additional identifier instead |
| Deploying a classifier or confidence-threshold model as the first fix for miscalibrated escalation | Over-engineered as a first move — explicit criteria + few-shot examples is the proportionate first intervention |
