---
name: human-review-calibration
description: Stratified sampling, calibrating confidence scores against ground truth, and when to route to human review independent of confidence
paths:
  - "**/*review*.*"
  - "**/*confidence*.*"
  - "**/*calibrat*.*"
---

# Human review calibration

## Aggregate accuracy hides segment-level failure

A headline number like "97% overall accuracy" can mask a badly-performing
document type, field, or confidence bucket that's too small to move the
aggregate — the aggregate is, by construction, dominated by whatever segment
is largest, not whatever segment is worst. Cutting human review on the
strength of an aggregate number alone risks cutting review exactly where
it's still needed, on a segment the aggregate was never sensitive enough to
flag.

**Validate accuracy by document type and field segment before reducing
review on high-confidence extractions.** The validation has to happen at
the segment level to be meaningful — a global number, however good, doesn't
tell you which segments are actually fine to stop reviewing.

## Stratified sampling, not plain random

Sample *within* each segment (document type, field, confidence bucket)
rather than randomly across the whole population. Plain random sampling
across a mixed population dilutes small-but-real segment-level failures —
a segment that's 5% of volume and failing badly can easily be
under-represented in a naive random sample large enough to feel confident
about the aggregate, while still being too small in that sample to actually
surface its own failure rate. Stratified sampling deliberately samples each
segment on its own terms, which is what actually catches this.

## Confidence is usable only once calibrated

A raw confidence score is not inherently meaningful — what a "0.85" actually
means, empirically, has to be checked against a **labeled validation set**
before it's trusted for routing decisions. Calibration is the step that
turns a number the model emits into a number that corresponds to an actual
empirical accuracy rate.

**Contrast with `escalation-and-ambiguity.md`:** that rule treats
self-reported confidence as an unreliable trap with no calibration path
offered, because production escalation decisions typically lack stable,
easily-labeled ground truth to calibrate against. This rule is the
*calibration path* that makes confidence usable — available specifically
because structured extraction is a repeatable, boundable task where ground
truth can actually be accumulated over time (a labeled validation set is a
realistic thing to build for extraction; it's a much harder thing to build
for "should this customer interaction have escalated"). Rule of thumb:
uncalibrated confidence is a trap everywhere it appears; calibrated and
validated confidence is usable, and this is specifically where the
calibration work that makes it usable gets done.

## Route on ambiguity, independent of confidence

Send to human review whenever confidence is low, **and** independently,
whenever the source material is ambiguous or internally contradictory —
these are two separate triggers, not one. A contradictory source needs
human judgment regardless of how confidently the model picked one of the
conflicting values; high confidence on a pick made from contradictory
source material doesn't make that pick more trustworthy, since the
confidence is being measured against the model's own internal consistency,
not against which of the contradictory sources is actually correct.

## Traps

| Trap | Why it's wrong |
|---|---|
| "97% accuracy, cut review" without segment-level validation | The aggregate can mask a badly-performing segment too small to move it |
| Plain random sampling presented as sufficient for accuracy validation | Dilutes small-but-real segment-level failures a stratified sample would catch |
| Trusting a raw confidence threshold with no calibration step | An uncalibrated score's numeric value doesn't correspond to any known empirical accuracy rate |
| High model confidence offsetting an ambiguous or contradictory source | It doesn't — confidence measures internal consistency, not correctness against a genuinely contradictory source; route to human review regardless of confidence level |
