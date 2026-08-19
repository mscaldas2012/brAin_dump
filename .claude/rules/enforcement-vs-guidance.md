---
name: enforcement-vs-guidance
description: When a rule or sequencing requirement needs a programmatic gate instead of a prompt instruction, and how to build the gate with or without hooks
paths:
  - "**/*agent*.*"
  - "**/*subagent*.*"
  - "**/*orchestrat*.*"
  - "**/*coordinator*.*"
  - "**/*hook*.*"
  - "**/agents/**"
  - "**/hooks/**"
---

# Enforcement vs. guidance

The single most load-bearing rule in this toolkit — most other rules
reference this one instead of re-deriving it. Read this before writing any
prompt instruction that says "always," "must," or "never."

## The test

Prompt-based instructions carry a non-zero failure rate no matter how well
they're worded. That's a categorical fact about how the model works, not a
matter of degree you can write your way out of with a stronger sentence. So
the question is never "is this instruction clear enough" — it's:

**Does a violation here cost something real — money, safety, compliance,
data integrity — or is it a stylistic/ordering preference with no real cost
to occasional deviation?**

- Real cost → **programmatic gate**. Non-negotiable.
- No real cost → a prompt instruction, or a few-shot example, is genuinely
  fine. Don't over-engineer a gate for a preference nobody will be harmed by
  breaking.

Classic instance: identity verification before a financial operation. A
refund tool that fires before customer identity is confirmed isn't a
"sometimes gets the order wrong" bug — it's a wrong-account financial
transaction. That's cost-of-violation territory, not preference territory.

## Building the gate, with hooks available (Claude Code / Agent SDK harness)

Two hooks, one persisted piece of state:

1. **`PostToolUse` on the prerequisite step** writes verified state to a
   session-scoped location once the prerequisite genuinely succeeded — e.g.
   a file at a path keyed by session ID, containing the verified identifier.
2. **`PreToolUse` on the gated step** blocks (exit code 2) unless that state
   exists **and** the identifier in the gated call matches what was
   verified. Checking existence alone isn't enough — it also has to catch
   "verified customer A, then tried to act on customer B."

```
# PostToolUse on get_customer
if result.verified:
    write_state(f".state/verified-{session_id}", result.customer_id)

# PreToolUse on process_refund
verified_id = read_state(f".state/verified-{session_id}")
if verified_id is None or verified_id != call.params.customer_id:
    exit(2)  # blocks the call
```

**Don't rely on the transcript for this.** Some harnesses expose a
transcript path to hooks, but it's written asynchronously and can lag the
in-memory conversation — not a reliable source for a real-time sequencing
guarantee. State has to be written and read explicitly.

**A schema-level required field is a complement, never a substitute.**
Making the identifier a required parameter on the gated tool's schema nudges
the model toward passing it correctly and gives clean typed data — but the
model can still populate that field with a fabricated or stale value without
the hook-based check. The schema requirement and the hook solve different
problems; only the hook is deterministic.

**Filesystem state is usually the right call, not a database.** These hooks
fire sequentially within one session — there's no real concurrency to
justify a KV store or database. Reach for something heavier only when you
have genuine concurrent writers (e.g. several subagents spawned in parallel,
all mutating *shared* state at once) — a different problem than a
single-session sequencing gate. Adding infrastructure a problem doesn't need
is its own anti-pattern (see `review-architecture.md`'s false-positive
"add a classifier" trap for the same shape of mistake in a different
context).

## Building the gate, without hooks (raw Agent SDK, no harness hooks)

The mechanism above doesn't exist at the raw API / hookless-SDK level, but
the underlying discipline still applies — it just has to live somewhere
else: **the orchestrator's own control flow**, checked before constructing
the next call.

```
# Orchestrator, not the downstream step's own prompt
last_verified = fetch_state_written_by(prior_step)
if not last_verified:
    raise  # or retry, or abort — a real branch in real code
response = client.messages.create(..., next_step_call)
```

**The check has to live in the orchestrator, not inside the gated step's own
prompt.** Putting "first check that the prior step ran" into the *gated
step's* system prompt and hoping it self-polices is the exact same
probabilistic-compliance mistake, just relocated one level down — it's
still the model being asked to enforce something on itself via instruction.
The only place in a hookless deployment where you get real code execution
instead of LLM judgment is the orchestrator's own script, so that's where
the gate has to be.

## A gate you're relying on can go inert — know when

Even "hard" programmatic gates aren't unconditionally hard. Example: a
harness's plan-mode write-block is enforced by default, but conditional on
a separate session-level flag (whether "bypass permissions" is available for
that session). In that specific combined state, the harness still *tells*
the model to plan without editing — but nothing technically stops a write
if the model attempts one. The status indicator can say the gate is active
while the actual enforcement underneath is inert, collapsing it to the same
tier as a plain instruction.

The lesson generalizes beyond that one example: before treating any gate as
a hard guarantee, confirm the specific deployment configuration doesn't have
a documented condition under which that gate stops actually enforcing.
"There's a gate" and "the gate is currently enforcing" are not always the
same fact.

## Traps

| Trap | Why it's wrong |
|---|---|
| "Strengthen the system prompt to say X is mandatory" for a compliance-critical ordering problem | Plausible-sounding, but prompts stay probabilistic regardless of wording — this is the exact anti-pattern this rule exists to block |
| A routing/classifier fix proposed for what's actually a sequencing problem | Solves tool *availability*, not tool *ordering* — different failure mode |
| Few-shot examples proposed as a substitute for a hard guarantee | Improves typical-case behavior, doesn't eliminate the failure rate — still not deterministic |
| Putting the enforcement check inside the gated step's own prompt in a hookless setup | Same probabilistic-compliance mistake, just relocated — the check must live in code that executes, not in a prompt the model is trusted to follow |
| Treating a gate as unconditionally hard without checking its enforcement conditions | Some gates (e.g. plan-mode's write-block under bypass-permissions) become advisory-only under specific, documented configurations |
| Reaching for a database/KV store for sequential, single-session state | Real concurrency (parallel subagents mutating shared state) justifies it; a single-session ordering gate doesn't |
