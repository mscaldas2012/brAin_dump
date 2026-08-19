---
name: design-decomposition
description: Interview to classify a task against the four decomposition axes (independent-parallel, dependency/graph-based, pipeline/sequential, data-parallel) and recommend a workflow pattern. Use before spawning subagents or designing a multi-step pipeline, not after.
argument-hint: [task-description]
---

# Design decomposition

Follows `rules/subagent-orchestration.md`'s four-axis table. The point of
running this *before* writing any orchestration code is that the wrong axis
produces a decomposition that looks reasonable and still fails — e.g. fixed
per-file subagent spawning applied to a task that actually needed a
discovery pass first.

## Step 1 — ask the classifying questions

1. **Are the subtasks known in advance, or do they have to be discovered?**
   If known in advance (comparing N named things, N known providers) →
   independent-parallel. If the actual structure isn't known until explored
   (an unfamiliar codebase, an unmapped dependency graph) → dependency/
   graph-based.
2. **Does one piece of work depend on a prior piece's verified output, as a
   mandatory order?** If yes → pipeline/stage-based, regardless of what the
   other answers suggest. A mandatory-order dependency overrides an instinct
   toward parallelism — don't force parallel structure onto a task that has
   a real sequential dependency.
3. **Are the units independent records/documents with no cross-record
   dependency?** → data-parallel. If volume is large and the workflow is
   non-blocking, flag that batch processing (`rules/batch-processing.md`,
   `batch-feasibility-check` skill) may be a better fit than live subagents
   at scale — recommend checking that before committing to a subagent-based
   design for a data-parallel task.

## Step 2 — recommend based on the answer

| Answer | Recommended pattern |
|---|---|
| Independent-parallel | Spawn one subagent per known unit, in one coordinator turn (see parallelism mechanics in `rules/subagent-orchestration.md`) |
| Dependency/graph-based | Run a discovery pass first; don't spawn per-file/per-unit until coarse module/interface boundaries are known. See the legacy-codebase worked pattern in `rules/subagent-orchestration.md` |
| Pipeline/stage-based | Sequential steps, each verified before the next begins — consider whether any of the sequencing needs a programmatic gate (`scaffold-enforcement-gate` skill) rather than trusting prompt ordering |
| Data-parallel | Subagents for moderate volume; batch processing for scale — check feasibility with `batch-feasibility-check` before deciding |

## Step 3 — check for the degenerate case

If the answer is dependency/graph-based, ask one more question: does the
discovered structure look like it might collapse into one large tangled
component with no clean seams (real spaghetti, not just "some coupling")?
If the user isn't sure yet, say that's expected before the discovery pass
runs — flag it as something to re-check once discovery actually happens,
and name the two fallbacks from `rules/subagent-orchestration.md` for when
it does turn out too coupled: staged/sequential decomposition (parallelize
independent leaves first, work inward through the core in sequence), or
seam-based decomposition (split by testable interfaces instead of module
ownership, accepting overlapping context for real parallelizability).

## Step 4 — don't recommend more sophistication than the task needs

If the task decomposes cleanly on one axis with no discovered complexity,
say so and stop — don't add nested subagent trees or nested nested
coordinators "to be thorough" when a flat coordinator-plus-fixed-subagents
shape already covers it. Recommending more structure than the diagnosis
calls for is the same over-engineering instinct flagged elsewhere in this
toolkit, just applied to decomposition depth instead of tool count or
review infrastructure.
