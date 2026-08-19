# Blog publish pipeline

A standalone CLI that audits a draft (voice, prose, rhythm) before publishing
it to the blog, with a real programmatic gate — not a checklist the model is
trusted to follow.

## Setup

```bash
uv sync
cp .env.example .env   # fill in ANTHROPIC_API_KEY and GITHUB_TOKEN
```

## Usage

```bash
# Audits the newest file in ../../inbox, publishes if the gate passes
uv run publish_pipeline.py

# Audit and publish a specific draft
uv run publish_pipeline.py path/to/draft.md

# Exercise the pipeline without pushing to GitHub
uv run publish_pipeline.py --dry-run
```

`--dry-run` writes the converted HTML, updated `index.html`, and updated
previous-post nav to their real destinations locally so you can `git diff`
them, but skips the GitHub push and does not delete the source from `/inbox`.

## How the gate works

State lives in `state/<slug>.json`, keyed by the sha256 of the draft's
current content. `publish_post` only runs once, for that exact hash:

- all three audits (`voice_check`, `prose_linter`, `rhythm_audit`) have
  recorded results,
- `voice_check.score >= voice_score_threshold`, no HIGH-severity anti-pattern,
- `prose_linter.total_flags <= prose_flag_threshold` and zero Tier-1
  signature words,
- no `rhythm_audit` flag has `severity: "high"`,
- the draft doesn't contain any name in `config.json`'s `blocked_names`
  (hard block, no override).

Editing the draft after auditing changes its hash, so the recorded audits no
longer apply and the gate re-arms automatically — no separate bookkeeping.

If the only outstanding issue is a MEDIUM/LOW-severity voice-check flag, the
CLI treats it as a judgment call rather than a hard failure: it prints the
flag and asks you in the terminal whether the drift was intentional. A "yes"
is recorded against that content hash and clears the gate; a "no" leaves it
blocked.

The gate itself (`gate.py`) is plain deterministic Python — no LLM call is
involved in the pass/fail decision, only in producing the audit inputs it
reads.

**Note on design vs. the original plan:** the plan that was approved for this
tool described wiring the gate as a Claude Agent SDK `PreToolUse` hook around
an agent that decides when to call each audit tool. Building it, that
sequencing turned out to have no actual judgment call in it — the pipeline
always runs all three audits, in a fixed order, every time — so an LLM
deciding *when* to call them added latency and an untestable failure surface
for no benefit. Per `.claude/rules/enforcement-vs-guidance.md`'s "hookless"
pattern (this script *is* the orchestrator, not an LLM loop), the same gate
guarantee is implemented as a direct function call in `publish_pipeline.py`
before `publish.do_publish()` — equally real, and easier to reason about.
`claude-agent-sdk` is still a listed dependency if a future version wants an
agent to *fix* flagged issues and loop back through the audits on its own.

## Audits

`voice-check`, `prose-linter`, and `rhythm-audit` are loaded directly from
`.claude/skills/*/SKILL.md` in this repo — their real prompts, not a
reimplementation. `voice-check` and `prose-linter` get a forced `tool_use`
schema layered on top so their judgment produces typed fields the gate can
threshold on; `rhythm-audit`'s own `scripts/analyze.py` is fully
deterministic and is called directly, with no LLM involved at all.

Because the wrapper schema constrains what the model reports (not how it
judges), scores here should track what running the skill directly inside
Claude Code produces — but isn't guaranteed to match exactly.

## GitHub push

Uses the Git Data API (`publish.push_to_github`) to build one commit covering
every changed file (new post, updated previous post's nav, `index.html`) in a
single atomic push — not one commit per file. Reads the repo slug from
`git remote get-url origin` and the branch from `GITHUB_BRANCH` (defaults to
`main`).

## Verification

See `.claude/agents/agentic-architecture-reviewer.md` — run it against this
directory before treating a change here as done; self-review from the same
session that wrote the code is the exact bias it exists to counter.
