---
name: subagent-orchestration
description: Hub-and-spoke coordination, structured handoffs, and how to pick a decomposition strategy before spawning subagents
paths:
  - "**/*agent*.*"
  - "**/*subagent*.*"
  - "**/*orchestrat*.*"
  - "**/*coordinator*.*"
  - "**/agents/**"
---

# Subagent orchestration

## Hub-and-spoke, and what actually implements it

The coordinator is the sole agent that decomposes tasks, invokes subagents,
and aggregates results. All error handling and information routing happens
in the coordinator's context. Subagents don't talk to each other directly.

**What implements this is not a tool restriction.** A subagent invoked
through a spawn mechanism (a `Task`-style tool, an `Agent` call) has no
addressing channel to reach a peer subagent regardless of what tools it
holds — its only path back to anywhere is returning a result to whoever
called it. Withholding a spawn tool from a subagent doesn't prevent lateral
peer communication, because that was never structurally possible to begin
with; it prevents that subagent from spawning *its own* children, i.e. it
keeps the tree flat. Don't diagnose a hub-and-spoke violation as a missing
tool restriction — the actual enforcement is: the coordinator is the only
one with a spawn tool at all, subagents get only the context explicitly
handed to them, and all error handling stays in the coordinator's context.

Nesting (a subagent that itself spawns children) is legitimate and is
**recursive hub-and-spoke**, not a violation — each level becomes a local
coordinator for its own children. Don't over-apply nesting as "the more
sophisticated design" when a flat coordinator-plus-fixed-subagents shape
already covers the task; that's the same over-engineering instinct
`enforcement-vs-guidance.md` warns against in a different context.

## Context isolation is explicit-only

Subagents do not automatically inherit the coordinator's conversation
history or any shared memory. The entire channel from parent to child is
whatever string is explicitly written into the spawn call's prompt. There is
no partial or implicit inheritance to rely on — assuming a subagent "already
knows" something because it's part of the same run is a bug, not an
optimization.

## Structured handoff, not raw transcript

"Structured" here means content discipline, not a required format — it's
still just a string being passed. The discipline is: extract and distill
specific facts before handoff, rather than passing the raw conversation
transcript wholesale.

**Bad** (raw transcript):
```
User: What's our Q3 revenue?
Assistant: [tool call] ...$4.2M, up 12% YoY.
User: What about churn?
Assistant: [tool call] ...3.1%...
[35 more turns]
```

**Good** (extracted facts, constraints, success criteria):
```
task: "Draft a one-slide board summary"
relevant_facts:
  q3_revenue: "$4.2M (+12% YoY)"
  churn_rate: "3.1%"
constraints: "One slide, exec tone, no raw data tables"
success_criteria: "Approved without follow-up data requests"
```

The raw-transcript version leaks tool-call syntax and meta-commentary into
the receiving subagent's context, balloons it with noise, and can cause the
downstream agent to imitate patterns that belonged to a different exchange
entirely. The difference between the two examples isn't the mechanism — both
are a string in a prompt — it's whether someone did the extraction work
before the handoff, or pushed that burden onto the receiving agent.

## Goals, not steps

Subagent prompts should specify the objective and what "good" looks like,
not a fixed procedure to execute in order. A prompt that hands over
mechanical steps ("read file X, list violations, return line numbers")
instead of a goal with context fails on two fronts: no success
criteria/constraints for the subagent to reason against (which guide? what
counts as a violation worth flagging?), and often a useless output shape for
whatever aggregates the result afterward. Per-unit fan-out (spawning one
subagent per file, per module, per record) is not itself the flaw — that's
often correct decomposition. The flaw is missing the
task+facts+constraints+success-criteria structure, the same discipline as
the handoff example above.

```
Evaluate the file against our style guideline [link]. Only flag violations
of this specific guideline — do not flag general code quality issues
outside its scope. For each issue found, report: line #, severity, suggested
fix. Report all findings, not just a select few. If you encounter any
errors, report that back too, describing the error and whether we should
retry.
```

Note the last sentence: it's asking the subagent to report through the
shape defined in `error-contract.md` rather than silently swallowing a
problem or returning a vague status.

## Parallel means one turn, not one-per-turn

Parallel subagent execution means the coordinator emits multiple spawn calls
within a single response/turn. Spreading calls across separate turns is
sequential, regardless of whether the intent was parallelism — a model can
emit multiple spawn-tool calls in one assistant turn and those run
concurrently; issuing them one turn at a time does not. This is the
mechanical basis for scaling guidance like "2-4 subagents for a comparison
task, more for broader research" — it requires the orchestrating prompt to
actually recognize subtask independence and issue the calls together, not
just have independent subtasks available.

## Choosing a decomposition strategy — four axes

Diagnose the task's natural structure *before* picking how to split it up.
This diagnosis is the actual skill — not memorizing one fixed decomposition
template and applying it everywhere.

| Axis | Structure | Fits when | Degrades to |
|---|---|---|---|
| **Independent-parallel** (angle-based) | Known independent comparison points upfront | Comparing N known things (providers, approaches, regions) | — (this is the clean case) |
| **Dependency/graph-based** (discovered) | Structure isn't known upfront, requires an exploration pass first | Legacy/unfamiliar codebases, unknown module boundaries | Sequential (prompt chaining), if the discovered graph is too coupled to parallelize |
| **Pipeline/stage-based** (sequential) | Each stage depends on the prior stage's verified output — mandatory order | Any workflow with a real prerequisite dependency between steps | — (this one's supposed to be sequential; don't force parallelism onto it) |
| **Data-parallel** (embarrassingly parallel) | Independent records/documents, no cross-record dependency | Structured extraction across many independent documents | At scale, often batch processing (`batch-processing.md`) instead of live subagents |

**For dependency/graph-based work specifically** (e.g. "add comprehensive
tests to a 200-file legacy codebase with no existing coverage"): don't
default to one subagent per file. A codebase like this has undiscovered,
uneven structure — wildly varying file complexity, unknown cross-file
dependencies, no upfront knowledge of where real module boundaries sit.
Fixed per-file decomposition guesses at structure that hasn't been found
yet, and can't correctly test functionality that spans files it was never
given visibility into.

Correct approach:
1. Run a discovery pass first — understand the codebase, identify coarse
   *modules* (not raw files) as the decomposition unit.
2. Draw module boundaries along dependency lines, not by directory or
   file-size grouping alone — grouping wrong reproduces the same problem one
   level up.
3. Spawn subagents per module, not per file.
4. Close with a verification pass using real tooling (coverage measurement,
   not subagent self-report) and spawn targeted follow-up work for any gaps
   found. Trusting N independent subagents' self-reports ("I wrote tests")
   is not sufficient confirmation of completeness.

If the discovered dependency graph degenerates into one large tangled
component (real spaghetti code, no clean module seams), two fallbacks, not
one forced fit: (a) staged/sequential decomposition — topologically order
what you can, test independent leaves in parallel first, work inward through
the entangled core in sequence; or (b) seam-based decomposition on the
entangled core itself — decompose by testable entry points/interfaces
instead of by module ownership, accepting overlapping context across
subagents in exchange for actual parallelizability.

## Iterative refinement is a designed pattern, not error recovery

Coordinator evaluates synthesis output for coverage gaps → re-delegates to
the relevant subagents with **targeted** follow-up queries → re-invokes
synthesis → repeats until coverage is sufficient. This is a first-class
pattern for closing gaps, not a fallback for when something broke.
Re-running the *entire* pipeline again is not the same fix as a targeted
re-delegation — the first wastes the work that already succeeded, the
second doesn't.

## Checkpointing for long runs

A long multi-agent run should persist intermediate state (the coordinator's
plan, each completed subagent's result) to external storage as it
progresses, not keep everything only in the ephemeral context window. A
failure partway through then resumes from the last checkpoint instead of
discarding all completed work and restarting the entire run from zero.

## Traps

| Trap | Why it's wrong |
|---|---|
| Restricting a subagent's spawn tool "to prevent it talking to peers" | Peer-to-peer communication was never structurally possible under this model regardless of tool grants; the restriction actually just prevents that subagent from having its own children |
| Blaming the executing subagent when every subagent "worked" but coverage is still incomplete | Root cause is almost always upstream, in the coordinator's decomposition or routing — trace the diagnosis to the decision, not the execution |
| Assuming subagents inherit coordinator context "because they're part of the same run" | Never automatic — always explicit, every time |
| Passing raw conversational transcript as a subagent handoff | Leaks structure/noise downstream and risks pattern imitation across an unrelated exchange |
| Procedural step-by-step subagent prompts instead of goals + success criteria | Reduces adaptability to what the subagent actually finds, and the flaw isn't the fan-out granularity — it's the missing structure |
| Describing spawn calls issued "across multiple turns" as parallel | That's sequential; true parallelism is multiple spawn calls in one turn |
| Fixed per-file decomposition for a task with unknown/discovered structure | Guesses at boundaries that haven't been found yet; needs a discovery pass and module-level (not file-level) units first |
| Treating "run the whole pipeline again" as equivalent to targeted re-delegation | Wastes already-completed work; iterative refinement is specifically the targeted version |
| Discarding all completed work and restarting a run from scratch after a partial failure | Correct pattern is checkpointing to external storage and resuming from the last completed point |
