---
name: agentic-loop-control
description: How to correctly branch an agentic loop on stop_reason, and the loop-termination anti-patterns to never write
paths:
  - "**/*loop*.*"
  - "**/*agent*.*"
  - "**/*orchestrat*.*"
  - "**/agents/**"
---

# Agentic loop control

The agentic loop is: send request → inspect the response's stop signal →
execute requested tools if any → append results → repeat. The entire
discipline of this rule is: **branch on the structured stop signal, never on
anything you'd have to infer from the content.**

## `stop_reason` glossary

| Value | What triggers it | Correct loop behavior |
|---|---|---|
| `tool_use` | The model wants to call one or more tools and is waiting on results | Loop again — execute the tool(s), append the result(s), send the request again. This is the only value where you have genuinely new information to feed back in. |
| `pause_turn` | A server-side tool or the server's own internal loop hit its own iteration ceiling — not a failure, a checkpoint | Append and resend unchanged, without adding a `tool_result` block. Bounded continuation with a safety cap — not "retries" in the failure sense, since nothing failed. |
| `end_turn` | The model finished its response naturally, with or without tool use | Terminate the loop, return the final output. |
| `max_tokens` | The response was cut off by the token limit for that request | No natural loop continuation. Handle via **prefill continuation**: feed the truncated assistant content back as the start of the next assistant turn (no new user message needed) — the model treats it as its own prior words and continues from exactly where it stopped. Do not treat this the same as `pause_turn`. |
| `stop_sequence` | Output matched a configured stop string | Terminate — final by design, since you set that cutoff intentionally. Continuing here defeats the point of having set it. |
| `refusal` | The model declined to continue for safety reasons | Terminate. Never retry the identical request — it's a terminal safety decision, not a transient failure. Surface it for human review if it looks like a false positive on a legitimate use case; don't try to route around it programmatically. |

The loop condition should key on `stop_reason == "tool_use"` specifically —
not `stop_reason != "end_turn"`. Those are not equivalent once the other
terminal values are accounted for; the second form would incorrectly try to
loop on `refusal` or mishandle `max_tokens`.

## What isn't a `stop_reason`

- `error` is not a value in this field at all — API-level errors (rate
  limits, overload) fail the request before any `stop_reason` comes back.
  Handle those with a try/except around the call itself, not as a branch
  inside `stop_reason` handling.
- Account-level usage/rate limits are enforced via HTTP errors, a separate
  mechanism from the per-request token cap. Don't conflate the two.
- A tool's own configured hard-use-count limit, if one exists, surfaces as an
  error *inside the tool result* when exceeded — not as a `stop_reason`.

## Three loop-termination anti-patterns

All three share one root cause: treating something other than the
structured stop signal as the source of truth for whether the turn is done.

1. **Parsing the response text for completion language** — e.g. checking
   whether the word "done" appears anywhere in the output. Fragile: the
   model can phrase completion in ways a parser misses, or use similar
   language mid-task without meaning to stop.
2. **Using an arbitrary iteration cap as the primary stop mechanism** — e.g.
   "loop at most 10 times" as the actual control logic, rather than a
   defensive backstop. Either cuts off work that genuinely needed more
   iterations, or masks that `stop_reason` isn't actually being checked at
   all. A cap belongs as a secondary safety bound underneath real
   `stop_reason` branching, never as the primary signal.
3. **Treating the presence of assistant text as a completion indicator** —
   e.g. "if there's any text in the response, we're done." Wrong because a
   model routinely emits explanatory text *alongside* a `tool_use` block in
   the same turn ("Let me check that...") — text presence doesn't mean the
   turn is over.

## Reference shape

```
while stop_reason == "tool_use":
    result = run_tool(...)
    messages.append(assistant_turn_with_tool_use)
    messages.append(tool_result_turn)
    response = call_api(messages)
    stop_reason = response.stop_reason

# branch on the terminal values here
if stop_reason == "pause_turn": resend unchanged, capped — nothing failed
if stop_reason == "end_turn": return content
if stop_reason == "max_tokens": prefill_continue(content)
if stop_reason == "stop_sequence": return content        # final by design
if stop_reason == "refusal": handle_refusal(response)    # never retry
```

Wrap the API call itself (not the `stop_reason` branch) in error handling
for `429`/`529`-class failures — those are a separate mechanism from this
loop entirely.

## Traps

| Trap | Why it's wrong |
|---|---|
| `while stop_reason != "end_turn"` as the loop condition | Not equivalent to keying on `"tool_use"` once `pause_turn`, `max_tokens`, `stop_sequence`, and `refusal` are all real possible terminal values |
| Collapsing `pause_turn` handling into `max_tokens` handling, or vice versa | Different responses required — one is a checkpoint (resend unchanged), the other is a real truncation (prefill continuation) |
| Text-based / NLP-based completion detection | Structural (`stop_reason`) is always the answer over parsed content, regardless of how the parsing is dressed up |
| Making an iteration cap the star of the loop design | Belongs as a backstop under real `stop_reason` branching, never as the primary termination logic |
| Retrying an identical request after a `refusal` | Terminal safety decision, not a transient failure — retrying the same prompt doesn't change the outcome and isn't the right recovery path |
| Handling `429`/`529` inside the `stop_reason` branch | Those are pre-`stop_reason` HTTP failures; they need a try/except around the call, not a case in the branch |
