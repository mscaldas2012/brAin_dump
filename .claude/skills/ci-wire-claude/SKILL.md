---
name: ci-wire-claude
description: Scaffold a CI pipeline step that invokes Claude headlessly with reproducible, minimal-discovery config, structured/schema-constrained output, and correct exit-code branching. Use when adding an automated Claude-driven step to a CI/CD pipeline.
argument-hint: [ci-platform] [task-description]
---

# CI wire Claude

Follows `rules/ci-integration.md`. Generate the actual pipeline step
(GitHub Actions, GitLab CI, or whatever platform the user names) in that
platform's native syntax — this skill's job is applying the pattern
correctly to a real config file, not producing pseudocode.

## Step 1 — confirm the two non-negotiables up front

Before generating anything, confirm with the user (or set explicitly if
they haven't specified):

1. **Reproducible/minimal-discovery invocation** — the step must not rely on
   whatever hooks/skills/MCP servers/config happen to be sitting on the
   runner. If the target harness has a bare/minimal-discovery mode, use it;
   pass all needed context explicitly instead (system prompt additions,
   settings, agent definitions) rather than relying on ambient discovery.
2. **Explicit credentials** — a minimal-discovery mode typically won't pick
   up interactive login state. Wire the API key from the CI platform's own
   secrets store as an environment variable — never hardcode it into the
   workflow file, and flag this explicitly if the user's draft has it
   inline.

## Step 2 — structured output if the step's result feeds anything downstream

If the CI step's output is consumed by a later step (posting a comment,
gating a merge, writing a report), generate it with structured/
schema-constrained output rather than parsing prose:
- Request a JSON (or platform-equivalent) output format.
- If a schema can be supplied, supply one — narrow enough that a later step
  can extract fields directly.
- Add an explicit step (or a comment marking where one belongs) that treats
  a schema-validation failure as a **hard pipeline failure**, not a silent
  fallback to unstructured text. If the target harness is known to fall back
  silently on a bad schema, add an explicit validation step before trusting
  the output, rather than assuming the platform will catch it.

## Step 3 — exit-code branching

Wire the pipeline step's pass/fail on the invocation's exit code directly
(`0` = success, non-zero = failure) — not on parsing the response text for
success/failure language. This mirrors `rules/agentic-loop-control.md`'s
core discipline (branch on the structured signal, not parsed content) at
the CI-invocation layer instead of the loop layer.

## Step 4 — if this is a review step specifically

Ask if this step is doing code review. If so:
- Recommend a separate review-tuning file/channel (severity definitions,
  nit caps, skip rules, re-review convergence instructions) rather than
  folding review tuning into general project-context config — cite
  `rules/ci-integration.md`'s project-context-vs-review-context split.
- Run the review as an independent step/session with its own context, not
  reusing the session that produced the change under review.
- If this pipeline will re-run review on the same PR after updates, add an
  explicit instruction to include prior findings and report only new/
  unaddressed issues — otherwise expect repeated re-litigation of the same
  already-fixed nits.

## Step 5 — sanity check against the workflow's actual blocking-ness

If the step is meant to gate a merge (blocking), double-check with the user
that nothing about this invocation depends on batch processing or any other
non-guaranteed-latency mechanism — cite `rules/batch-processing.md` if
relevant. A CI step that's supposed to be a hard gate has no room for an
unbounded-latency dependency inside it.
