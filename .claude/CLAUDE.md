# Agentic Best-Practices Toolkit

This file is doctrine, not documentation — the handful of invariants that
should shape *every* decision made while designing or implementing an
agentic system in a project this toolkit is dropped into. Each invariant
below is elaborated, with mechanics and worked examples, in a corresponding
`rules/*.md` file — this file states the invariant and points there; it
doesn't re-derive it.

See `rules/00-config-organization.md` before adding to this toolkit itself —
it governs whether new content belongs here, in a new rule, or in a skill.

## The invariants

1. **Compliance-critical sequencing gets a programmatic gate, never a prompt
   instruction alone.** If a step must happen before another for correctness,
   safety, or compliance reasons, prompt-based instructions carry a non-zero
   failure rate no matter how well they're worded — that's treated as
   categorical fact, not a matter of degree. The gate is a hook
   (`PreToolUse`/`PostToolUse` + persisted state) where the harness supports
   it, or an equivalent check in the orchestrator's own control flow where it
   doesn't. → `rules/enforcement-vs-guidance.md`

2. **Every tool result and subagent failure reports through one structured
   error contract** — category (transient / validation / business_rule /
   permission), whether it's retryable, what was attempted, any partial
   results, and concrete next steps. No generic `"failed"` strings, and no
   collapsing "found nothing" into the same shape as "couldn't check."
   → `rules/error-contract.md`

3. **Agentic loops branch on `stop_reason`, never on parsed natural-language
   completion signals or a bare iteration cap treated as the primary stop
   mechanism.** An iteration cap is a defensive backstop at most.
   → `rules/agentic-loop-control.md`

4. **Subagents get only what's explicitly passed to them.** No context
   inheritance is assumed; the coordinator is the sole router between them,
   and that's what actually implements hub-and-spoke — not a tool
   restriction. Handoffs are curated facts/constraints/success-criteria, not
   raw transcript. → `rules/subagent-orchestration.md`

5. **Tool sets are scoped narrow per agent role.** More tools — even
   individually well-described ones — degrades selection reliability; it
   isn't a capability upgrade. → `rules/tool-interface-design.md`

6. **When a coverage gap or misrouting is diagnosed, the root cause is traced
   to the decomposition or routing decision upstream, not to the executing
   unit that "did what it was told."** Every subagent can succeed
   individually while the system still fails, if the failure was in how the
   work was split up. → `rules/subagent-orchestration.md`

## Rule index

| Rule | Covers |
|---|---|
| `rules/00-config-organization.md` | How to extend this toolkit itself |
| `rules/enforcement-vs-guidance.md` | Programmatic gates vs. prompt-based compliance |
| `rules/error-contract.md` | The shared structured error/failure shape |
| `rules/agentic-loop-control.md` | `stop_reason` handling, loop termination |
| `rules/subagent-orchestration.md` | Hub-and-spoke, handoffs, decomposition strategy |
| `rules/tool-interface-design.md` | Tool descriptions, scoping, `tool_choice` |
| `rules/mcp-integration.md` | MCP server config, resources vs. tools |
| `rules/builtin-tool-selection.md` | Grep/Glob/Read/Write/Edit selection |
| `rules/structured-output.md` | Schemas, few-shot, validation/retry |
| `rules/batch-processing.md` | Message Batches API operational discipline |
| `rules/review-architecture.md` | Multi-instance review, false-positive management |
| `rules/escalation-and-ambiguity.md` | When to hand off to a human |
| `rules/context-preservation.md` | Long-interaction context, provenance |
| `rules/session-lifecycle.md` | Resume/fork/checkpoint semantics |
| `rules/human-review-calibration.md` | Confidence calibration, sampling |
| `rules/ci-integration.md` | Non-interactive/CI invocation |

All 16 rules above are built. See `ROADMAP.md` for status detail.

## Skills

On-demand scaffolding workflows in `skills/` — each generates the pattern
its dependency rule describes, for a specific component, rather than
restating the rule: `scaffold-enforcement-gate`, `scaffold-error-schema`,
`scaffold-subagent`, `batch-feasibility-check`, `design-decomposition`,
`ci-wire-claude`.

## Agents

`agents/agentic-architecture-reviewer.md` — a read-only subagent that audits
a design or diff against every rule above and reports findings; it doesn't
write fixes itself. Use it once a design exists to check, not while still
drafting one.
