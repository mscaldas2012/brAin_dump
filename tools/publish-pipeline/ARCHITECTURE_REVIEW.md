# Architecture review — tools/publish-pipeline

Run via the `agentic-architecture-reviewer` agent against `.claude/rules/*.md`, on branch `review/publish-pipeline-architecture`. All 7 issues below were then fixed by three coder agents (one per file: `publish.py`, `audits.py`, `publish_pipeline.py`), verified to compile together and to honor the cross-file `validate_html` contract.

## Issues (most severe first)

- [x] **1. LLM HTML output unvalidated; failures propagate silently**
  `publish.py:124` (`ensure_beacon`, `extract_title_and_description`) and `:186` (`wire_navigation`/`add_next_link`)
  `convert_markdown_to_html`'s output is never structurally validated. If the model's output is truncated or malformed (missing `</head>` or `</body>`), `ensure_beacon`'s `.replace()` and `wire_navigation`'s `re.sub()` silently no-op instead of erroring, and `extract_title_and_description` falls back to `""`/the slug. The pipeline will commit and open a PR for broken HTML with no signal anywhere that conversion failed.
  → Add validation after `convert_markdown_to_html` (require `</html>`, `</body>`, `</head>`, non-empty `<title>`) that raises `PipelineError(type="validation", ...)` with the raw output in `details` if any are missing.

- [x] **2. `stop_reason` never checked; truncation misread as transient**
  `audits.py:52` (`_forced_tool_call`) and `publish.py:92` (`convert_markdown_to_html`)
  Neither Anthropic call site inspects `response.stop_reason`. In `_forced_tool_call` (max_tokens=4096), a genuinely long draft that reliably exceeds the token budget gets misdiagnosed as "unusual and often transient" with recovery "retry the same call" — an identical retry fails identically every time. `convert_markdown_to_html` (max_tokens=8192) doesn't even check for incomplete output before treating joined text blocks as a finished HTML document.
  → Check `response.stop_reason` explicitly at both call sites; raise a distinct `PipelineError` (or use prefill continuation) on `"max_tokens"` instead of collapsing it into a blind-retry case.

- [x] **3. Full 9-step SKILL.md loaded for a Step-3-only call**
  `publish.py:76` (`convert_markdown_to_html`)
  The entire `post-blog` `SKILL.md` — including Step 8 ("push to GitHub") and Step 9 ("delete the source file") — is loaded verbatim into the system prompt, relying on a trailing suppression sentence to keep the model from acting on the other 8 steps. Steps 8–9 directly contradict the "output ONLY the HTML document, no commentary" instruction for this call. The code's own defensive code-fence stripping (`:118-120`) is evidence the model doesn't reliably honor the suppression instruction already.
  → Extract only the Step 3 section of `SKILL.md` programmatically (or maintain it as a standalone prompt fragment) instead of sending the full skill.

- [x] **4. HTML conversion uses plain text, not forced `tool_choice`**
  `publish.py:92` (`convert_markdown_to_html`)
  Relies on a plain-text completion plus a prompt instruction for clean output, unlike voice-check and prose-linter, which correctly force `tool_choice` for guaranteed structured output.
  → Force a tool call with a single required `html_document` string field, matching the pattern already used for the two audits.

- [x] **5. One audit's failure aborts two independent audits**
  `publish_pipeline.py:64` (`run_audits`)
  Aborts the entire audit stage on voice-check's first failure, even though prose-linter and rhythm-audit are independent — rhythm-audit doesn't even call the Anthropic API. A transient rate limit on voice-check alone discards rhythm-audit's free, local, deterministic analysis for that pass.
  → Run the three audits independently (try/except per audit, continue regardless of one's outcome) and aggregate into the `partial_results`/coverage-annotation shape from `error-contract.md`.

- [x] **6. Ambiguous draft picked by heuristic, no confirmation**
  `publish_pipeline.py:46` (`_pick_draft`) and `:189` (`source_path.unlink()`)
  When no draft is given explicitly, silently resolves multiple `/inbox` candidates to the most-recently-modified file, then runs paid audits, opens a PR, and deletes the chosen source file on success — all before the user can say "no, the other one."
  → When more than one candidate exists and none was passed explicitly, list the candidates and require explicit selection instead of silently choosing "most recent."

- [x] **7. `sys.exit`/`RuntimeError` bypass the error contract**
  `publish_pipeline.py:46` (`_pick_draft`) and `publish.py:299` (`_repo_slug`)
  `_pick_draft` uses bare `sys.exit(f"error: ...")` strings; `_repo_slug` raises/propagates a plain `RuntimeError`/`CalledProcessError`. `main()` only catches `PipelineError`, so a `_repo_slug` failure propagates as a raw traceback and `report.render()` never runs — no report gets written under `reports/` for that failure, unlike every other failure mode in the pipeline.
  → Route both through `PipelineError` so every failure path produces a report and a consistent, actionable message.

## Noted as done correctly (not a finding)

`gate.py`'s enforcement design correctly implements the hookless orchestrator-control-flow pattern from `enforcement-vs-guidance.md`: content-hash keying checks the linking identifier rather than mere existence, and drift-acknowledgment correctly re-arms on any new voice-check result rather than silently carrying forward a stale human approval.

## Scope note

This is a solo CLI tool (one script, one operator), not a multi-agent orchestrator with subagents as separate processes. Rules judged genuinely not applicable here: `agentic-loop-control.md` (beyond the narrower `stop_reason` gap above — finding 2), `batch-processing.md`, `mcp-integration.md` (a standalone script structurally cannot call MCP tools; using the GitHub REST API directly is correct here), `review-architecture.md` (audits review externally-authored draft content, not the pipeline's own prior output), `session-lifecycle.md`, `human-review-calibration.md` (the voice-check score is a rubric gate, not a calibrated confidence score used for routing), `ci-integration.md` (no CI wiring exists yet), `builtin-tool-selection.md` (governs Claude Code's own tool selection, not this Python code's file I/O), `subagent-orchestration.md` (no subagent spawning — the one relevant angle, independent-audit sequencing, is captured under finding 5 instead).
