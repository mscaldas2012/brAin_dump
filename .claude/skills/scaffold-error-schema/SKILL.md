---
name: scaffold-error-schema
description: Generate the shared structured error/failure type for a tool, subagent, or pipeline step, pre-filled with the four categories from the error contract. Use when adding a new tool or component that can fail and needs to report failure in a way callers can actually act on.
argument-hint: [component-name]
---

# Scaffold error schema

Follows `rules/error-contract.md`. The goal is a type/dataclass/schema in
whatever language the target codebase uses, not a generic description —
generate it in-language, matching existing conventions in the surrounding
code (if the codebase already has a result/error type pattern, extend that
pattern rather than introducing a second, competing one).

## Step 1 — confirm the shape

Emit (adapted to the target language's idioms — dataclass, interface,
struct, JSON Schema, whatever fits):

```
type: transient | validation | business_rule | permission
message: string
details: object            # category-specific — ask what fields this component's
                            # failures actually need; don't leave this generic
is_retryable: boolean       # set explicitly per failure, never inferred from type alone
attempted: string
partial_results: object | null
next_steps:
  recovery: [string]
  alternatives: [string]
```

## Step 2 — ask what "empty but successful" looks like for this component

Before finishing, get the user to state explicitly what a **valid, non-error
empty result** looks like for this specific component (e.g. "zero search
matches" vs. "search couldn't run"). Generate that as a clearly separate
success-path return, not a variant of the error type — the whole point of
`error-contract.md`'s access-failure-vs-empty-result distinction is that
these must never share a shape. If the component can't produce a meaningful
"legitimately found nothing" case, say so rather than forcing one.

## Step 3 — wire the four categories to this component's actual failure modes

Don't leave the four categories abstract — ask the user (or infer from the
component's actual dependencies) for at least one concrete example of each
category that's realistic for this component, and note it as a comment:

- Transient: what's the actual timeout/unavailability case here?
- Validation: what malformed input is actually possible here?
- Business rule: what policy/limit does this component enforce, if any?
  (If none, say so — not every component has this category.)
- Permission: what access failure is actually possible here?

If a category genuinely doesn't apply to this component, say so rather than
padding the type with a category that will never be used — but check twice
before concluding that, since permission and business-rule failures are
often missed until they happen in production.

## Step 4 — local recovery reminder

If this component is a subagent or has its own retry capability, add a
short comment reminding that transient failures should be retried locally
first, and only what can't be resolved locally should propagate through
this contract — with `attempted` and `partial_results` populated, not left
as placeholders.
