---
name: session-lifecycle
description: Continue vs. resume vs. fork semantics, what forking does and doesn't protect, and when to start fresh instead of resuming
paths:
  - "**/*session*.*"
  - "**/*agent*.*"
---

# Session lifecycle

## The API underneath is stateless — say this out loud before anything else

No server-side memory exists between calls. Every request is
self-contained; "memory" in a conversation is something the caller builds by
resending the full message history on every call. Any answer that implies
the server remembers something you didn't explicitly send in *this* request
is wrong, no matter how it's dressed up (an invented session/history
parameter, a claim that context is retained automatically for some window of
time, or that caching lets you omit history — caching only reduces the
cost/latency of reprocessing content already sent, it never lets you send
less than the full history).

Everything below — continue, resume, fork, checkpointing — is a
harness-level or application-level mechanism built *on top of* that
stateless substrate, not an exception to it.

## Three mechanisms, three different jobs

| Mechanism | What it does | Use when |
|---|---|---|
| **Continue** | Finds the most recent session automatically, no ID tracking | Single-conversation apps, restarting after a crash — "just pick up where I left off" |
| **Resume** | Takes a specific captured session ID; **mutates that session** — new turns append to its existing history, no separate copy is preserved | Multiple sessions in flight (multi-user app), or continuing something specific that isn't necessarily the most recent |
| **Fork** | Resume-with-a-flag: creates a new session ID whose history starts as a copy of the original. The original is untouched and independently resumable afterward | Exploring a divergent approach from a shared analysis baseline, without risking the original line of work |

Fork doesn't stand alone as its own primitive — it's specifically a resume
variant with copy-on-branch behavior, not a fourth, unrelated mechanism.

## Fork protects conversation, not files

Sessions track the **conversation** — prompts, tool calls, tool results,
responses — not filesystem state. Two consequences worth holding onto
independently, because they're easy to conflate into one intuition that's
wrong in both directions:

1. **Forking does not protect file edits.** If a forked or resumed agent
   edits files, those edits are real and land on shared disk regardless of
   which session made them — forking branches the conversation, not the
   filesystem. "I'll fork so I can undo this risky refactor's file changes"
   is not something fork alone gives you. If undoable file state is also
   needed, pair fork with a separate file-checkpointing mechanism or git —
   fork is not a substitute for either.
2. **Rewinding files does not rewind conversation.** The inverse also holds:
   restoring file contents to an earlier state leaves session
   history/context exactly as it was — the two are genuinely independent
   axes, not two views of the same underlying state.

## Don't resume blindly across changed state

When resuming a session after the underlying files have changed since the
prior run, the agent does not automatically know previously-analyzed files
are now stale — that has to be stated explicitly, or the resumed reasoning
proceeds over outdated assumptions about what's on disk.

**When prior tool results are stale or no longer trustworthy, starting a new
session with a structured summary is more reliable than resuming.**
Resuming carries forward tool-result state that may no longer be valid;
injecting a fresh, curated summary into a new session sidesteps that risk
entirely rather than trying to patch around it mid-resume.

## Cross-host resume

Session state is typically local to the machine that created it. For
cross-host continuation (CI workers, ephemeral containers), the more robust
approach is generally not to rely on resume at all: capture the results
actually needed (analysis output, decisions, diffs) as application state and
inject them into a fresh session's prompt on the new host. This is more
reliable than shipping session transcript files around, since resuming stale
tool results across environments risks desyncing from what's actually true
in that environment.

## Cost is a second-order but real concern

Resending full history every call is correct, not optional — but it isn't
free. Token cost and context-window usage grow every turn a session lives.
A long-lived session needs a deliberate compaction strategy (see
`context-preservation.md` for how to do this without losing specifics)
before this becomes a real cost or context-limit problem, not an
afterthought bolted on once it already is one.

## Traps

| Trap | Why it's wrong |
|---|---|
| Assuming any server-side memory persists a session between calls | Nothing persists server-side — "memory" is entirely the caller resending full history each time |
| Treating prompt caching as a way to omit history from a request | Caching only reduces cost/latency of reprocessing already-sent content — full history still has to be sent every call |
| Treating resume as always the safer/lower-effort default | Wrong whenever underlying tool results are stale — a fresh session with a curated summary is more reliable in that case |
| Assuming an agent will infer file changes on its own after a resume | It won't — changes have to be stated explicitly, or reasoning proceeds over stale assumptions |
| Treating fork as protection against needing to revert file edits | Fork branches conversation only — pair with file checkpointing or git for undoable file state |
| Shipping raw session transcript files across hosts for cross-host continuation | Prefer capturing results as application state and injecting into a fresh session — more robust than transcript-file transfer |
