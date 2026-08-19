---
name: config-organization
description: How to decide between CLAUDE.md, a new rules/ file, or a skill when adding to this toolkit — and how to scope a rule once you've picked it
paths: ["agentic-best-practices/**"]
---

# Config organization

This rule governs how the rest of this toolkit is built. Read it before adding
a new file anywhere under `agentic-best-practices/` — including before adding
a 16th rule file that could instead be a section of an existing one.

It is also the pattern to hand to a target project: once this toolkit is
dropped into a real repo, the same three-way decision applies to whatever
that project adds on top (its own CLAUDE.md sections, its own rules, its own
skills).

## Decision 1 — CLAUDE.md, a rule, or a skill

Three different jobs, not three strengths of the same thing:

| | **CLAUDE.md** | **`rules/*.md`** | **`skills/*/SKILL.md`** |
|---|---|---|---|
| Answers | "What should Claude always know?" | Same, but split by topic and optionally scoped to a file pattern | "What should Claude know how to *do*, on demand?" |
| Loaded | Always, for its scope | Always (no `paths:`) or when a matching file is touched | Only on invocation — name+description are the only always-loaded part |
| Shape | Doctrine, standing context | Doctrine, standing context, narrower | A procedure with a start and an end |

If content describes an invariant that should color every relevant decision
Claude makes in this domain (e.g. "compliance-critical sequencing needs a
programmatic gate") — it's doctrine → CLAUDE.md or a rule. If content
describes steps to execute when asked (e.g. "scaffold a PreToolUse/PostToolUse
pair for this named dependency") — it's a workflow → a skill.

CLAUDE.md and rules are not competing homes for doctrine — see Decision 2 for
which one a given piece of doctrine belongs in.

## Decision 2 — root CLAUDE.md vs. a topic rule

Loading is additive/concatenated, never an override chain — a more specific
file does not replace a more general one, they all load together. So this
decision is about **bloat and precision**, not precedence:

- **Root `CLAUDE.md`** — the handful of invariants relevant to *every* piece
  of work in this domain, regardless of what file is being touched. Keep this
  short. If it's growing past a screenful, content belongs in a rule instead.
- **A `rules/*.md` file** — everything else, one file per cross-cutting theme
  (see the roadmap's dedupe map for how the 15 themes were chosen). A theme
  earns its own file when it has enough independent content to stand alone;
  don't fork a rule into two files just because it could be organized that
  way — that's the same over-splitting the exam material itself warns against
  ("18 tools instead of 4-5" is a tool-scoping trap, but the instinct behind
  it — more granularity feels more rigorous — applies just as wrongly here).

## Decision 3 — should a rule be path-scoped?

**Settled convention (see `README.md` for the full rule → glob table):**
every rule in this toolkit describes something that only makes sense in
agentic-system code — a rule about hooks, tool descriptions, or session
lifecycle has nothing to say about an unrelated file. So every rule gets a
`paths:` glob, tailored per rule to its actual subject, built from a shared
naming-convention vocabulary (`agent`, `subagent`, `orchestrator`,
`coordinator`, `hook`, `tool`, plus rule-specific terms like `session`,
`mcp`, `batch`, `escalat`, `review`) matched against both filenames and
conventional directories (`**/agents/**`, `**/hooks/**`, `**/tools/**`).
`00-config-organization.md` itself is the one exception — scoped to
`agentic-best-practices/**` since it's about extending the toolkit, not
about agent code in a target project.

This is a real, opinionated bet, not a neutral default — it trades recall
for precision. A file that implements exactly the pattern a rule describes
but doesn't follow the naming convention (e.g. a gate-enforcement hook
sitting in a file called `refund.py` with no "hook" or "agent" anywhere in
its name or path) won't trigger that rule. That tradeoff was made
deliberately: an unconditionally-loaded rule set costs context on every
single file touched in a project this toolkit is dropped into, most of
which have nothing to do with agent design — the naming convention is the
lever that keeps this toolkit's cost proportional to how much of a given
project is actually agentic-system code.

**When adopting this toolkit into a project that doesn't follow this
convention**, don't leave rules silently not firing — either rename to match
the vocabulary above, or edit each rule's `paths:` to match the project's
actual layout. Treat the globs in `README.md` as a starting convention this
toolkit ships with, not a fact about how every codebase is organized.

For any *new* rule added later: give it its own tailored glob following the
same method (rule-specific terms + the shared vocabulary, filenames and
directories both), and add it to `README.md`'s table in the same edit — the
table is meant to stay authoritative, not drift out of sync with the actual
frontmatter.

## Mechanics reference (no judgment calls, just the facts)

- Multiple matching rules all load together — there is no "most specific glob
  wins" behavior. Don't scope two rules to overlapping globs expecting one to
  suppress the other.
- `@path/to/file` import syntax works in both CLAUDE.md and rule files, for
  keeping an individual file lean without giving up the "one file per theme"
  organization above.
- None of this — CLAUDE.md, rules, Skills — exists at the raw Anthropic
  Messages API level, and none of it is auto-loaded by a `ClaudeSDKClient`
  Agent SDK app either (`setting_sources` must be set explicitly; Skills
  additionally need `"Skill"` in `allowed_tools`). If this toolkit's content
  is meant to reach a pure-SDK application rather than Claude Code itself,
  that wiring is the target project's responsibility, not something this
  toolkit can assume happens automatically.
