---
name: ci-integration
description: Non-interactive/headless invocation for CI pipelines — reproducibility, structured output, exit codes, and review-specific session isolation
paths: ["**/.github/workflows/**", "**/*.yml", "**/*.yaml"]
---

# CI/CD integration

## Non-interactive mode mechanics

A headless/print-style invocation (`-p`/`--print` in Claude Code's own CLI;
the equivalent flag in whatever harness a target project uses) runs without
an interactive UI and returns control to the calling process. Two mechanics
matter for wiring this into a pipeline:

- **Exit codes drive branching.** `0` on success, non-zero on failure — a CI
  step should check the exit code the same way it would check any other
  command's, not try to parse output for success/failure language.
- **Prevent interactive hangs.** Combined with an explicit tool-allowlist or
  a non-interactive permission mode, a run either proceeds or fails cleanly
  — it never blocks on a permission prompt with nobody there to answer it.
  A CI invocation that can still pause waiting for interactive approval is
  not actually headless yet, regardless of which flag started it.

## Reproducibility: a bare/minimal-discovery mode

The reproducible pattern for CI is a **bare/minimal-discovery mode** where
one exists: skip auto-discovery of hooks, skills, plugins, MCP servers,
auto-loaded memory, and CLAUDE.md, so the run produces the same result
regardless of what happens to be sitting in whatever machine or container
executes it. Without this, a pipeline that relies on non-interactive mode
alone can still behave differently machine to machine, because it's still
picking up ambient config from wherever it runs — non-interactive and
reproducible are not the same property, and a pipeline needs both.

Context has to be passed explicitly in this mode, via whatever the harness's
equivalent is of: an appended system prompt, an explicit settings file, an
explicit MCP config, explicit agent definitions. Nothing ambient gets picked
up automatically — that's the entire point of using this mode.

**Authentication is a real, expected gotcha here, not a bug**: a bare/
minimal-discovery mode typically does not read interactive-login credentials
(OAuth tokens, system keychain) even for a user who's normally logged in
interactively — deliberately, for the same reproducibility reason. It needs
an explicit API key (an environment variable, or a documented equivalent
credential-helper mechanism) rather than relying on ambient login state. In
a real pipeline, that key lives in the CI provider's own secrets store,
injected as an environment variable at runtime — never committed alongside
the workflow definition.

## Structured output for machine consumption

Non-interactive mode typically supports a structured output format (JSON,
alongside plain text) — and, where the harness supports it, a schema can be
supplied to constrain that structured output to a specific shape. The
structured result should land in its own field, separate from any
plain-text summary field, so a pipeline can extract exactly what it needs
(e.g. piping to a JSON processor and posting extracted fields as inline PR
comments) without parsing prose.

**An invalid schema should be a hard, visible error** — not a silent
fallback to unstructured output. A pipeline step that silently degrades to
plain text on a malformed schema will pass when it should have failed, and
whatever downstream step expected structured output breaks in a way that
looks unrelated to the actual cause. If the harness in use is known to
silently fall back instead of hard-erroring, treat that as a gap to guard
against explicitly (validate the schema separately before relying on it),
not as acceptable behavior to route around case by case.

## Project context vs. review-specific context

General project context (build/test commands, conventions, architecture) is
one input to a CI-invoked run. **Review-specific tuning is a separate
concern and deserves its own file/channel, treated as the higher-priority
instruction for review behavior specifically** — severity definitions, nit
volume caps, skip rules (generated code, lockfiles, vendored dependencies),
repo-specific checks, and re-review convergence behavior (below) all belong
there rather than mixed into general project context. Folding review-tuning
into the same file as general project context makes both harder to reason
about: general context should apply to every task, review tuning should
apply only when reviewing.

## Session isolation for review

The session that wrote a change is a worse reviewer of that change than an
independent instance — same underlying bias as `review-architecture.md`'s
self-review problem, restated as a CI-specific requirement. Run review as
a background/independent process with its own context window, specifically
so it (a) doesn't consume the main session's context and (b) isn't
reasoning from inside the context that produced the change, biased toward
justifying decisions it just made.

## Re-review convergence

When a review runs more than once against the same PR (after a fix, after
another commit), include prior findings in context and instruct the review
explicitly to report only new or still-unaddressed issues. Without this, a
PR can bounce through repeated review rounds re-litigating the same
already-addressed style nit instead of converging toward "done" — a rule
like "after the first review, suppress new nits and only post
higher-severity findings" is the kind of explicit convergence instruction
that stops this.

## Traps

| Trap | Why it's wrong |
|---|---|
| Assuming non-interactive mode alone gives reproducible CI behavior | It only means the run doesn't block on interactive input — without a bare/minimal-discovery mode, it still auto-picks-up ambient hooks/skills/MCP/config from whatever machine runs it |
| Treating "not logged in" under a bare/minimal-discovery mode as a bug | Expected — that mode deliberately skips interactive-login credentials; requires an explicit API key |
| Assuming a malformed output schema degrades silently to plain text | Should be a hard, visible error — a silent fallback lets a broken pipeline step pass when it should have failed |
| Mixing review-specific tuning into general project-context files | Review tuning (severity, nit caps, skip rules, convergence behavior) deserves its own higher-priority channel, not folding into always-loaded general context |
| Running review in the same session that produced the change | Same self-review bias as `review-architecture.md` — use an independent session/instance |
| Re-running review with no memory of prior findings | Produces repeated re-litigation of already-addressed nits instead of converging — feed prior findings back in and instruct "new/unaddressed only" |
