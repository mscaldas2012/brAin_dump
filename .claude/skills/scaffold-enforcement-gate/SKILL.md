---
name: scaffold-enforcement-gate
description: Scaffold a programmatic enforcement gate (hook pair, or orchestrator-level check) for a compliance-critical sequencing dependency between two steps. Use when a step must not run before another has genuinely completed — e.g. identity verification before a financial action — and a prompt instruction alone isn't enough.
argument-hint: [prerequisite-step] [gated-step]
---

# Scaffold enforcement gate

Follows `rules/enforcement-vs-guidance.md`. Do not skip straight to writing
code — the interview below exists because a gate built on the wrong
identifier, or built where a prompt would genuinely have sufficed, is worse
than no gate at all (false confidence in the first case, wasted engineering
in the second).

## Step 1 — confirm this needs a gate at all

Ask, don't assume: does a violation here cost something real (money,
safety, compliance, data integrity), or is it a stylistic/ordering
preference? If the answer is genuinely "no real cost to occasional
deviation," stop here and say so — recommend a prompt instruction or a
few-shot example instead, and explain why per `enforcement-vs-guidance.md`'s
opening test. Don't scaffold infrastructure for a problem that doesn't
need it.

## Step 2 — gather the specifics

If it does need a gate, get from the user (or infer from the codebase and
confirm):

1. **The prerequisite step** — the tool/function/step that must complete
   first, and what "genuinely completed" means for it (not just "was
   called" — e.g. `get_customer` must have returned `verified: true`, not
   merely been invoked).
2. **The gated step** — the tool/function/step that must not proceed
   without it.
3. **The linking identifier** — what value has to match between the two
   (e.g. `customer_id`). This is what distinguishes "prerequisite never
   ran" from "prerequisite ran for a *different* target than the one this
   call is about" — both are real failure modes, and the gate needs to
   catch both, not just existence.
4. **Harness capability** — does the target environment have a real hook
   mechanism (pre/post tool-call interception), or is this a raw
   orchestrator loop with no such interception point available?

## Step 3a — hooks available

Generate two pieces, matching `enforcement-vs-guidance.md`'s pattern:

- A post-execution hook on the prerequisite step that writes the linking
  identifier to session-scoped state, **only when the prerequisite
  genuinely succeeded** (not merely ran).
- A pre-execution hook on the gated step that blocks unless that state
  exists *and* matches the identifier in the call being made.

Also add (as a complement, not a substitute — say this explicitly in the
generated code's comments) the linking identifier as a required schema field
on the gated step, so the model gets a typed nudge in the common case even
though the hook is what actually guarantees correctness.

State storage: default to a plain file keyed by session ID unless the user
has described genuine concurrent writers to the *same* state (e.g. multiple
subagents mutating shared state in parallel) — that's the one case where a
heavier mechanism is justified; don't reach for one otherwise.

## Step 3b — no hooks available

Generate the equivalent check as explicit control flow in the orchestrator
script itself, executed **before** constructing the call to the gated step
— not inside the gated step's own prompt. Make the failure mode of getting
this wrong concrete in a comment: putting the check in the gated step's
prompt is the same probabilistic-compliance mistake this whole exercise
exists to avoid, just relocated one level down.

## Step 4 — flag the inert-gate caveat

If the target harness has any documented condition under which this kind of
gate can become advisory-only (e.g. a permissive session-level flag that
suppresses enforcement), mention it explicitly in a comment near the
generated gate and ask the user to confirm their deployment doesn't run
under that condition. Don't let a gate ship silently assuming it's always
enforced.
