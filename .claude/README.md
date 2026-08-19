# Agentic Best-Practices Toolkit

A portable set of Claude artifacts — doctrine (`CLAUDE.md`), rules
(`rules/`), scaffolding skills (`skills/`), and a review subagent
(`agents/`) — encoding the agentic-systems best practices from the CCA-F
study material (`study_material/` at the repo root). See `ROADMAP.md` for
how this was built and in what order.

This file documents one specific decision: **how every rule is path-scoped**,
since that decision is opinionated and worth being explicit about rather
than leaving implicit in 16 separate frontmatter blocks.

## The naming-convention decision

Every rule in this toolkit is about *agentic-system* code specifically — a
rule about hooks, tool descriptions, or session lifecycle has nothing
useful to say about an unrelated file. Loading all 16 unconditionally would
mean paying that context cost on every file in a project this toolkit is
dropped into, most of which won't be agent code at all.

So every rule (except the meta rule below) carries a `paths:` glob, built
from a shared vocabulary matched against both filenames and conventional
directories:

**Vocabulary:** `agent`, `subagent`, `orchestrator`, `coordinator`, `hook`,
`tool` — plus each rule's own specific terms (`session`, `mcp`, `batch`,
`escalat`, `review`, `context`, `confidence`/`calibrat`, `extract`/`schema`,
`loop`, `scratchpad`).

**This is a real tradeoff, not a neutral default.** A file that implements
exactly the pattern a rule describes but doesn't follow this naming
convention (e.g. a compliance gate living in a file called `refund.py`,
with no "hook" or "agent" anywhere in its name or path) won't trigger that
rule. That's accepted deliberately, in exchange for not loading agent-design
doctrine into every unrelated file a project touches. See
`rules/00-config-organization.md`'s Decision 3 for the full reasoning.

**If your project doesn't follow this naming convention**, either rename to
match the vocabulary above, or edit the `paths:` in each rule file to match
your actual layout. Treat the table below as this toolkit's shipped
starting convention, not a fact about how your codebase is organized.

## Rule → path scope table

| Rule | `paths:` |
|---|---|
| `00-config-organization.md` | `agentic-best-practices/**` (meta — scoped to the toolkit itself, not target-project agent code) |
| `enforcement-vs-guidance.md` | `*agent*`, `*subagent*`, `*orchestrat*`, `*coordinator*`, `*hook*`, `agents/**`, `hooks/**` |
| `error-contract.md` | `*tool*`, `*agent*`, `*subagent*`, `*hook*`, `tools/**`, `agents/**`, `hooks/**` |
| `agentic-loop-control.md` | `*loop*`, `*agent*`, `*orchestrat*`, `agents/**` |
| `subagent-orchestration.md` | `*agent*`, `*subagent*`, `*orchestrat*`, `*coordinator*`, `agents/**` |
| `tool-interface-design.md` | `*tool*`, `tools/**`, `*mcp*`, `*agent*` |
| `mcp-integration.md` | `*mcp*`, `mcp/**`, `*.mcp.json`, `*tool*` |
| `builtin-tool-selection.md` | `*agent*`, `agents/**`, `*tool*`, `tools/**` |
| `structured-output.md` | `*extract*`, `*schema*`, `*tool*`, `*agent*` |
| `batch-processing.md` | `*batch*.py`, `*batch*.ts`, `*batch*.js` |
| `review-architecture.md` | `*review*`, `*agent*` |
| `escalation-and-ambiguity.md` | `*escalat*`, `*agent*` |
| `context-preservation.md` | `*context*`, `*session*`, `*scratchpad*`, `*agent*` |
| `session-lifecycle.md` | `*session*`, `*agent*` |
| `human-review-calibration.md` | `*review*`, `*confidence*`, `*calibrat*` |
| `ci-integration.md` | `.github/workflows/**`, `*.yml`, `*.yaml` |

(Globs abbreviated above for readability — each is actually `**/<pattern>`
or `**/<pattern>/**` in the frontmatter; see each file for the literal list.)

## Known gaps in this convention

- **`builtin-tool-selection.md`** is about how Claude itself should use
  Grep/Glob/Read/Write/Edit — that guidance is arguably relevant while
  editing *any* file, not just agent-named ones. It's scoped like the rest
  anyway, for consistency and cost-control; if this turns out to bite in
  practice (the rule not firing somewhere it should have), it's the first
  candidate to reconsider loosening.
- **Multiple rules share overlapping globs** (`*agent*` appears in most of
  them) — this is intentional, not redundant. Per
  `rules/00-config-organization.md`'s mechanics reference, all matching
  rules load together; a file named `agent_loop.py` is expected to trigger
  both `agentic-loop-control.md` and `subagent-orchestration.md`
  simultaneously, since both are genuinely relevant to that file.
- **This convention hasn't been tested against a real adopting project
  yet.** Revisit per-rule globs once this toolkit actually gets dropped
  into something and you can observe which rules over-fire, under-fire, or
  never fire.
