---
name: builtin-tool-selection
description: When to use Grep vs. Glob vs. Read/Write/Edit, and the fallback pattern when Edit's anchor match isn't unique
paths:
  - "**/*agent*.*"
  - "**/agents/**"
  - "**/*tool*.*"
  - "**/tools/**"
---

# Built-in tool selection

## Content search vs. path search

| Tool | Operates on | Typical use |
|---|---|---|
| **Grep** | File *contents* | Find all callers of a function, locate an error string, trace usage |
| **Glob** | File *paths/names* | Find files matching a naming pattern (e.g. `**/*.test.tsx`) |

Using Glob to search inside file contents doesn't work — it only matches
paths. Using Grep purely to filter by file extension works, but it's the
wrong tool for that job; Glob is purpose-built for path patterns and is the
better default whenever the criterion is about the file's name or location
rather than what's inside it.

## Full-file vs. targeted operations

| Tool | Operates on | Typical use |
|---|---|---|
| **Read** | Full file | Load contents to reason about, or before a Write |
| **Write** | Full file | Create a new file, or replace one entirely |
| **Edit** | A targeted region, via unique text matching | A small, precise change with an unambiguous anchor |

**When Edit fails because the anchor text isn't unique, fall back to Read
the full file, then Write the modified version back** — not retrying Edit
repeatedly with reworded anchor text. Iterating on the anchor string is a
plausible-feeling instinct but isn't the stated fallback pattern; Read+Write
gets a guaranteed correct result on the first attempt once the anchor
uniqueness problem shows up, instead of guessing at a new anchor that might
also turn out non-unique.

## Incremental exploration, not upfront bulk reading

Start with Grep to find entry points, then Read to follow imports and trace
flow from there. Reading every file in a codebase upfront before starting
analysis doesn't scale and front-loads cost that incremental
Grep-then-Read tracing avoids — most of what gets read upfront in a bulk
pass turns out irrelevant to the actual task.

## Alias/re-export tracing

A function can be re-exported under multiple names. Grep-ing for only the
original name can miss call sites that go through an alias. Before tracing
usage of something that might be re-exported, enumerate all the names it's
exported under first, then Grep for each individually — a single Grep pass
on the original name alone is not a complete usage trace.

## Traps

| Trap | Why it's wrong |
|---|---|
| Using Glob to search file contents | Glob only matches paths/names, never content |
| Using Grep purely to filter by extension | Works, but Glob is the purpose-built tool for path/name patterns |
| Retrying Edit repeatedly with reworded anchor text after a non-unique-match failure | The stated fallback is Read the full file, then Write it back — not iterating on the anchor string |
| Reading every file in a codebase upfront before starting analysis | Doesn't scale; incremental Grep → Read tracing is the pattern that avoids front-loading irrelevant cost |
| Grep-ing only a function's original name when tracing its usage | Misses call sites through a re-exported alias — enumerate all exported names first |
