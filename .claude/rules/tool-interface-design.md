---
name: tool-interface-design
description: How to design and scope tool interfaces so a model selects the right one reliably, including the fix hierarchy for misrouting and tool_choice mode selection
paths:
  - "**/*tool*.*"
  - "**/tools/**"
  - "**/*mcp*.*"
  - "**/*agent*.*"
---

# Tool interface design

## The description is essentially the only selection signal

A model choosing between tools sees name, description, and input schema —
nothing else. No source code, no tests, no README. A thin description
("Retrieves customer information") causes unreliable selection among similar
tools not because the model is bad at the task, but because there's
genuinely nothing else for it to disambiguate on. Good descriptions include
input formats, example queries, edge cases, and explicit boundaries ("use
this vs. X when...").

**Keyword bleed is a different problem, wearing the same clothes.** A
system prompt that repeatedly mentions a phrase like "verify identity" can
pull the model toward a `verify_identity`-named tool even in unrelated
contexts — this is a *prompt* wording problem, not a tool description
problem. Rewriting the tool's description does nothing for this; the fix is
in whatever surrounding prompt is creating the keyword association. Before
fixing a misrouting symptom, confirm which of the two actually changed the
observed behavior.

## Fix hierarchy for misrouting — cheapest first

1. **Rewrite/expand the tool description.** Cheapest, addresses the root
   cause directly for the common case (thin description).
2. **Rename the tool**, if the name itself is what's misleading (e.g.
   `analyze_content` → `extract_web_results`).
3. **Split a generic tool into purpose-specific tools** with defined
   input/output contracts (e.g. `analyze_document` →
   `extract_data_points`, `summarize_content`, `verify_claim_against_source`).
4. **Consolidate genuinely redundant tools** into one. Valid, but higher
   effort than a "first thing to try" question usually wants — reach for
   this only once redundancy, not thinness, is the confirmed diagnosis.

Don't skip to step 3 or 4 as a first move, and don't treat a routing
classifier or a batch of few-shot examples as step 0 — both are
over-engineered relative to just fixing the description, and both add an
ongoing cost (a system to maintain, or recurring tokens) for what's usually
a documentation gap.

## Tool-count discipline

Giving an agent many tools — even individually well-written ones — degrades
selection reliability. This isn't about description quality; more options
increases decision complexity on its own. Agents with tools outside their
actual specialization tend to misuse them (a synthesis-focused agent
occasionally running its own web searches "just in case," for example).

The fix is architectural, not a prompt reminder telling the agent not to
overreach — that's the same probabilistic-compliance mistake
`enforcement-vs-guidance.md` names in a different context. Scope each
agent's tool set to its actual role. Where a narrow, high-frequency
cross-role tool is genuinely justified (e.g. a `verify_fact` lookup for a
synthesis agent that would otherwise round-trip constantly through the
coordinator for simple checks), grant that one specific tool — don't grant
broad access "to be safe" or "to reduce round trips." Route everything else
through the coordinator.

## `tool_choice` modes

| Value | Behavior | Use when |
|---|---|---|
| `"auto"` | Model may call a tool, or return plain text | Conversational use, where a text-only response is a valid outcome |
| `"any"` | Model must call *some* tool, but picks which | Guaranteed tool use is required, but which schema applies isn't known ahead of time (e.g. an unknown document type among several candidate schemas) |
| `{"type": "tool", "name": "..."}` (forced) | Model must call this exact tool | A specific step has to run first, deterministically — e.g. force `extract_metadata` before anything else, handling subsequent steps in a follow-up turn |

Don't confuse `"any"` with forced selection — `"any"` still leaves the
*choice of which tool* to the model; it only removes the option of skipping
tool use entirely. And don't use `"auto"` where structured output is
actually required — the model may legitimately return plain text with no
tool call, which is the wrong outcome for an extraction pipeline that needs
a guaranteed structured result every time.

## Constrained alternatives over generic tools

A generic, wide-surface tool (`fetch_url`) can often be replaced with a
narrower, purpose-built one (`load_document`, validated against a known
document set) — reducing both the space of things that can go wrong and the
model's decision surface at call time.

## Traps

| Trap | Why it's wrong |
|---|---|
| Adding few-shot examples as the *first* fix for tool misrouting | Treats the symptom, not the likely root cause (a thin description); adds a recurring token cost for what's usually a one-time documentation fix |
| Building a routing classifier or keyword pre-parser to fix selection reliability | Over-engineered — bypasses the model's native tool-selection reasoning and introduces a new system to maintain, for what's usually a description or scoping problem |
| Rewriting a tool's description to fix a keyword-bleed problem | Wrong diagnosis — bleed comes from surrounding system-prompt wording, not the tool's own description; confirm which one actually changed behavior before fixing either |
| "Give every agent every tool for flexibility" | Directly causes the misuse/selection-degradation this rule opens with — flexibility isn't free |
| Fixing tool-specialization misuse via a prompt instruction ("don't search unless...") | Probabilistic compliance for what should be an architectural (tool-scoping) fix — see `enforcement-vs-guidance.md` |
| Using `"auto"` where a guaranteed structured result is required | The model may return plain text with no tool call at all — wrong default for an extraction pipeline |
