---
name: batch-processing
description: When batch processing is appropriate, the SLA feasibility check, correlation via custom_id, and failure/cancellation handling
paths: ["**/*batch*.py", "**/*batch*.ts", "**/*batch*.js"]
---

# Batch processing

## Appropriate vs. inappropriate use

A batch processing API trades cost for latency guarantees: substantial cost
savings, a wide processing window, but **no guaranteed latency SLA**. That
tradeoff is the entire decision:

- **Appropriate**: non-blocking, latency-tolerant work — overnight reports,
  weekly audits, nightly generation jobs, anything nobody is waiting on
  synchronously.
- **Inappropriate**: anything in a blocking workflow — pre-merge checks, or
  any path where a human or another system is waiting on the result before
  proceeding.

**Cost savings never override a hard latency requirement.** If a workflow
has a real blocking dependency on the result, that rules out batch
regardless of how much cheaper batch would be — this isn't a tuning
question, it's a category mismatch. A mixed system (some jobs blocking, some
not) should split by job, not force a single API choice across both: batch
the overnight report, keep the pre-merge check on real-time calls. Proposed
fixes like "poll for completion" or "add a real-time timeout fallback" don't
resolve this — polling still has no underlying SLA to poll toward, and a
fallback adds complexity for a mismatch that's simpler to just not create in
the first place.

## SLA feasibility check

Before committing a recurring job to batch, check:

```
N ≤ SLA − max_processing_time
```

where `N` is the available submission-cadence budget, `SLA` is the deadline
the job has to hit, and `max_processing_time` is the batch window's own
worst case. **If this is negative, batch cannot meet that SLA under any
submission strategy** — this is a feasibility result, not a "tune the
interval tighter" problem. Recognize infeasibility and don't try to
force-fit batch onto a deadline the processing window structurally can't
support; move that job to real-time calls instead, or renegotiate the SLA.

Two different shapes of this question, worth distinguishing: a
**continuous-arrival** job (documents keep coming in, need a submission
cadence) is the `N` math above. A **single fixed-volume nightly batch** is
a bounded-window feasibility question instead — does the whole batch fit
inside the window before the deadline — with no submission-interval math
needed at all. Don't apply the cadence formula to a problem that's actually
the simpler bounded-window shape, or vice versa.

## Correlation via `custom_id`

`custom_id` is assigned at request-build time — before the model runs — and
must trace back to the *source* document or record. It cannot be derived
from anything the model produces, since the whole point is being able to
match a result back to what was submitted even if results return out of
submission order (which they can).

**On partial failure, resubmit only the failed items by `custom_id`** —
never the whole batch. Resubmitting everything wastes the cost savings that
justified using batch in the first place and reprocesses items that already
succeeded.

## What batch does not support

No multi-turn tool calling for client-defined tools within a single batch
request — one shot per client tool call, no mid-batch continuation the way a
synchronous call supports. (Server-executed tools, where the provider itself
runs an agentic loop server-side, are a separate mechanism and not subject
to this limitation — don't conflate the two when deciding whether a
workflow with tool use is batch-compatible.)

## Cancellation and partial results

Batch results are effectively all-or-nothing while a batch is still in
progress — no per-item visibility, no partial retrieval mid-run. The
documented way to get partial results before natural completion is
cancellation: a canceled batch transitions to a terminal state and may
contain partial results for whatever was processed before the cancel took
effect. **There is no guaranteed cancellation speed** — build a time buffer
into any hard cutoff plan rather than assuming cancellation is near-instant.

Billing on a canceled batch splits by outcome: items that succeeded before
cancellation bill at the batch rate, items never dispatched bill at zero,
and any synchronous fallback processing of the remainder bills at the full
real-time rate — three different rates, not a single flat discount across
everything in the batch.

## Operational discipline

Refine prompts against a small sample before submitting full production
volume to batch. A prompt issue discovered after submitting the full volume
costs the full processing window to discover and the full resubmission cost
to fix — a small-sample check is cheap insurance against that.

## Traps

| Trap | Why it's wrong |
|---|---|
| Choosing batch for a blocking workflow because of the cost savings | Cost never overrides a hard latency requirement — this is a category mismatch, not a tuning question |
| "Poll for completion" as a fix for batch's lack of SLA | Polling doesn't fix the underlying missing SLA — there's nothing to poll toward with a guarantee |
| A negative `N` in the feasibility formula treated as "tune the interval" | It's an infeasibility result — no submission strategy fixes it; move the job off batch or change the SLA |
| Assuming batch supports the same client-tool multi-turn loop as a synchronous call | It doesn't — one shot per client tool call, no mid-batch continuation |
| Resubmitting an entire batch after a partial failure | Wasteful — resubmit only the failed `custom_id`s |
| Deriving `custom_id` from model output instead of assigning it at request-build time | Breaks the entire correlation mechanism this field exists for |
| Assuming near-instant cancellation | No documented speed SLA — plan a buffer into any cutoff |
| Treating batch cancellation billing as a flat discount | It's a three-way split by actual outcome per item, not one rate across the batch |
