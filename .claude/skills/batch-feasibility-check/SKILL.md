---
name: batch-feasibility-check
description: Compute whether a batch-processing approach can meet a given SLA, or determine the required submission cadence if it can. Use before committing a recurring job to batch processing, or when deciding batch vs. real-time for a specific workflow.
argument-hint: [sla] [max-processing-time] [workflow-description]
---

# Batch feasibility check

Follows `rules/batch-processing.md`. Do the qualitative check before the
math — a workflow that's blocking/synchronous fails this check regardless
of what the numbers say, and doing the arithmetic first can create a false
sense that a numeric answer settles a category question it doesn't.

## Step 1 — is this workflow batch-eligible at all?

Ask: is anything waiting on this result synchronously (a human, a blocking
CI check, another system in a request/response path)? If yes, stop here —
batch is disqualified regardless of cost savings, per
`rules/batch-processing.md`'s core distinction. Say so plainly and recommend
real-time calls; don't proceed to the math for a workflow that's already
disqualified on category grounds.

If the workflow is genuinely non-blocking/latency-tolerant, continue.

## Step 2 — identify which shape of question this is

Two different shapes, and mixing them up produces wrong math:

- **Continuous arrival**: documents/records keep arriving and need an
  ongoing submission cadence to meet a rolling deadline. → Step 3a.
- **Single fixed-volume batch**: a bounded set of work (e.g. "tonight's
  5,000 records") with one deadline. → Step 3b.

## Step 3a — continuous-arrival math

Gather:
- `SLA` — the deadline from arrival to completion the job must meet.
- `max_processing_time` — the batch window's own worst case (ask the user
  for the actual documented figure for their batch provider; don't assume
  a number).

Compute `N ≤ SLA − max_processing_time`, where `N` is the maximum allowable
gap between submission batches.

- If `N > 0`: report the feasible submission cadence, and recommend
  building in a safety margin below the raw `N` (don't submit at exactly
  the theoretical maximum interval).
- If `N ≤ 0`: report **infeasible under any submission strategy** — state
  this plainly, don't suggest "tune the interval tighter" as if there's a
  smaller positive interval to find. Recommend either moving the job to
  real-time calls or renegotiating the SLA.

## Step 3b — fixed-volume bounded-window check

Gather the deadline and the batch window's worst-case processing time.
Check simply whether the batch, submitted at the start of the window, can
complete before the deadline. No submission-cadence math applies here —
don't import Step 3a's formula into a problem that doesn't have a
submission-interval variable at all.

## Step 4 — operational reminders regardless of outcome

If the check comes back feasible, still flag:
- Refine the prompt against a small sample before submitting full volume.
- Plan `custom_id` assignment at request-build time, traceable to the source
  record — not derived from anything the model produces.
- Plan for resubmission of only failed items by `custom_id`, not the whole
  batch, in the failure-handling design.
- If a hard cutoff exists, build a time buffer for cancellation — there's no
  documented guaranteed cancellation speed.
