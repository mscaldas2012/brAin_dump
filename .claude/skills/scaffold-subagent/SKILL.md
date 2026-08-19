---
name: scaffold-subagent
description: Scaffold a subagent/AgentDefinition with a goals-not-steps system prompt, scoped tool access, and a structured-handoff builder stub. Use when adding a new subagent to a coordinator/orchestrator system.
argument-hint: [subagent-name] [role-description]
---

# Scaffold subagent

Follows `rules/subagent-orchestration.md`. The failure mode this skill
exists to prevent is a subagent definition that looks complete (has a name,
a description, a tool list) but is missing the structure that actually
makes it work well: a goal instead of a procedure, a tightly scoped tool
set, and a handoff builder that extracts facts instead of forwarding
transcript.

## Step 1 — decomposition check first

Before scaffolding anything, confirm this subagent is the right unit of
decomposition. If unclear, run `design-decomposition` first — a
well-written subagent definition for the wrong decomposition axis (e.g. one
subagent per file when the task needed module-level discovery first) is
still the wrong subagent.

## Step 2 — write the prompt as a goal, not a procedure

Ask the user for:
- The **objective** — what does success look like, concretely?
- **Constraints** — what's explicitly out of scope? (This is often more
  useful than what's in scope — a subagent that doesn't know what *not* to
  flag/change tends to over-reach.)
- **Success criteria** — how would the coordinator (or a human) know this
  subagent's output is good, without re-doing the work?
- **Output shape** — what does the coordinator actually need back, in a form
  it can use directly (not "a summary," but the specific fields)?

Refuse to write a numbered step-by-step procedure into the system prompt
unless the user explicitly insists after being told why goals-not-steps is
preferred (adaptability to what's actually discovered). If the task is
genuinely a fixed, well-understood sequence with no judgment calls, say so —
that may mean this isn't a subagent at all but a scripted step, which is a
legitimate answer.

Include, near the end of the generated prompt, an explicit instruction to
report failures through the shared error contract (`rules/error-contract.md`)
— what was attempted, category, whether retryable, partial results — rather
than a bare failure string.

## Step 3 — scope tools narrowly

List only the tools this subagent's stated objective actually requires.
For each tool the user wants to add "just in case" or "to reduce round
trips," push back explicitly and ask whether it's actually inside this
subagent's specialization — cite `rules/tool-interface-design.md`'s
tool-count discipline. If a narrow, high-frequency cross-role tool is
genuinely justified (a scoped lookup that would otherwise round-trip
constantly through the coordinator), that's fine — but name it explicitly
as that specific exception, not as general-purpose breadth.

## Step 4 — generate the handoff builder stub

Generate a function/template that produces the structured handoff shape,
not a passthrough of conversation history:

```
task: <one-line objective>
relevant_facts:
  <curated key facts the subagent actually needs>
constraints: <what's out of scope>
success_criteria: <how to know the output is good>
```

Leave the `relevant_facts` extraction itself as a clearly marked TODO for
the caller to fill in per invocation — this skill scaffolds the shape, it
doesn't (and can't) know what facts a specific invocation will actually
need to extract.

## Step 5 — note the parallelism mechanics if relevant

If the user mentions this subagent will run alongside others, add a comment
reminding that parallel execution means issuing multiple spawn calls within
a single coordinator turn — spreading them across turns is sequential
regardless of intent.
