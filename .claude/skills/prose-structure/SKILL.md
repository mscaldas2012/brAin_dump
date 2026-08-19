---
name: prose-structure
description: Macro-level diagnostic router for whole-text architecture. Detects text length, extracts a structural skeleton for long texts, then diagnoses seven dimensions — opening, ending, flow, pacing, tone consistency, repetition, argument integrity — in priority order. Routes to prose-* sub-skills and applies the top two priority skills in full. Use as the entry point for any structural review above the sentence and paragraph level.
---

# Prose Structure

Use this skill when a piece's sentence-level writing is adequate but something larger is wrong — the reader loses the thread, the ending feels unearned, the energy dissipates halfway through, the argument circles without arriving. This skill diagnoses at the architectural level and routes to the appropriate `prose-*` sub-skill.

Source concept: Aristotle identifies three essential parts of any discourse — the statement of the subject, the argument, and the epilogue — and holds that "the most necessary parts are the statement and the proof." Everything else exists to serve them; structural failure is when the parts serve themselves instead. (Aristotle, *Rhetoric*, Book III Ch. 13.) Quiller-Couch names four cardinal virtues of good prose — appropriateness, perspicuity, accuracy, persuasiveness — and establishes that violating any one is sufficient to break the reader's trust. (*On the Art of Writing*, Lecture II, 1916.) Good prose architecture serves the argument or narrative; poor architecture makes the reader carry the architecture.

---

## Length-Tier Protocol

Estimate the length of the text before running any diagnostic. State the tier at the top of the output.

**Tier 1 — Short** (under 3,000 words)
Read the full text. All seven dimensions apply. Run normally.

**Tier 2 — Medium** (3,000–20,000 words)
Read the full text. Before diagnosing, run an extraction pass: note the first sentence of each major section, the last sentence of each major section, and the approximate word count per section. Use this map to navigate; run all seven dimensions on the full text.

**Tier 3 — Long** (over 20,000 words)
Skeleton extraction first. Before any diagnostic, extract a structural memo for each major section, in this format:

`[Section N | ~WW words | TONE-TAG] Core: <central claim or event in one sentence>. Opens: <first sentence>. Closes: <last sentence>.`

Concatenate the memos. Run all seven dimensions on the skeleton. Flag skeleton-based findings as structural approximations — paragraph-level faults (local transitions, localized repetition) may not be visible without reading the full section. For Dimensions 1 and 2 (Opening and Ending), always step back to the actual first and last five paragraphs of the full text; these cannot be diagnosed by proxy.

---

## Diagnostic Dimensions

Seven dimensions, checked in order. Each returns either Pass or a named fault with the corresponding sub-skill.

### Dimension 1 — Opening
Does the piece begin with the thing itself, or with a warm-up approach to the thing?

Fault categories: throat-clearing, delayed arrival, summary opener, rhetorical question opener, definition opener, unearned anecdote.

Route to: `prose-opening`

### Dimension 2 — Ending
Does the piece close, or does it stop?

Fault categories: summary repeat, soft question-hook, imported thought, abrupt stop, virtue claim, callback failure.

Route to: `prose-ending`

### Dimension 3 — Flow
Does each section earn the next? Is there a through-line — an organizing logic by which section N sets up section N+1?

Fault categories: missing bridge between sections (the subject of one section has no stated relationship to the subject of the next), topic drift (a section begins about X and ends about Y with no acknowledged turn), stall-and-restart (the argument stops, then resumes on the same point without acknowledgment), mechanical transition (words like "However," "Moreover," "In addition" papering over a disconnection rather than naming it).

Route to: `prose-flow`

### Dimension 4 — Pacing
Is the conceptual weight distributed appropriately across the piece? A heavy section should not follow another heavy section without relief; a light section should not stretch beyond its carrying capacity.

Fault categories: density pile-up (three or more consecutive dense, conceptually loaded sections with no breathing room), over-inflation (one idea stretched far beyond what it can sustain, filling space that belongs to what comes next), gear-change without cause (abrupt shift in section length or density with no tonal or rhetorical signal).

Route to: `prose-pacing`

### Dimension 5 — Tone Consistency
Does the register hold across the piece, or does the voice shift in ways the piece does not earn?

Fault categories: tonal whiplash (warm → clinical → snarky across adjacent sections), unearned intimacy (sudden confessional register in an analytical piece), vocabulary-level inconsistency (Latinate formal prose in one section alongside colloquial casualness in the next), voice shift (the implied relationship between writer and reader changes mid-piece and never returns).

Route to: `prose-tone-consistency`

### Dimension 6 — Repetition
Is any idea restated in different language without acknowledgment? Is any example used more than once without acknowledgment? Does the piece's structure return to its opening premise without having traveled?

Fault categories: paraphrase restatement (the same claim made twice in different clothes, presented as if it were a new claim), example reuse (an illustrative case used twice without acknowledgment), structural circularity (the ending restates the opening premise without synthesis — the piece has moved in a circle, not a line).

Route to: `prose-repetition`

### Dimension 7 — Argument Integrity *(essay and opinion only)*
For argumentative prose: does each claim follow from the last, or are there logical gaps the reader is left to bridge?

Fault categories: unjustified leap (claim B is asserted after claim A without establishing the connection), evidence mismatch (an example or piece of evidence is paired with a claim it does not support), contradiction (a claim made early is contradicted by a claim made later, without acknowledgment or resolution).

Route to: `prose-argument-integrity`

*Skip Dimension 7 for pure narrative, memoir, or descriptive prose where no argumentative chain is present. Note the skip explicitly: "Dim 7 (Argument): N/A — genre is [narrative / descriptive / memoir]."*

---

## Triage Procedure

1. Estimate length. Determine tier. Extract skeleton if Tier 3.
2. Check Dimension 1 (Opening). Read actual opening text regardless of tier.
3. Check Dimension 2 (Ending). Read actual ending text regardless of tier.
4. Check Dimension 3 (Flow) on full text or skeleton.
5. Check Dimension 4 (Pacing) on full text or skeleton.
6. Check Dimension 5 (Tone) on full text or skeleton.
7. Check Dimension 6 (Repetition) on full text or skeleton.
8. Check Dimension 7 (Argument) if applicable.

**Priority ranking:** Dimension 1 and 2 faults (framing) outrank interior faults. Among interior faults: a flow failure (reader loses the thread entirely) outranks a pacing fault; a pacing fault outranks tonal inconsistency; tonal inconsistency outranks local repetition; argument integrity faults rank by severity of the logical gap.

Apply the top two priority sub-skills in full at the end of the report, in priority order. If only one fault is found, apply that skill alone.

---

## Review Shape

```
Prose Structure Audit
Mode: Tier [1 / 2 / 3] — [full text / full text + extraction map / skeleton]
Text: [title or opening phrase, max 80 characters]
Length: [approximate word count]

Findings:
Dim 1 (Opening):    [Pass — or — fault name · prose-opening]
Dim 2 (Ending):     [Pass — or — fault name · prose-ending]
Dim 3 (Flow):       [Pass — or — fault name · prose-flow]
Dim 4 (Pacing):     [Pass — or — fault name · prose-pacing]
Dim 5 (Tone):       [Pass — or — fault name · prose-tone-consistency]
Dim 6 (Repetition): [Pass — or — fault name · prose-repetition]
Dim 7 (Argument):   [Pass / N/A — or — fault name · prose-argument-integrity]

Priority diagnosis:
1. [prose-X] — [one sentence naming the specific structural fault and where it appears]
2. [prose-X] — [one sentence naming the specific structural fault and where it appears]
3. [prose-X] — [one sentence naming the specific structural fault and where it appears]

Applying [#1 priority skill]:
[Full repair or preserve output from that skill, using that skill's review shape]

Applying [#2 priority skill]:
[Full repair or preserve output from that skill, using that skill's review shape]
```

---

## Objective Rubric

- The mode (tier and extraction method) is stated at the top and the diagnostic is consistent with what that mode can see — skeleton-based findings are flagged as approximations.
- Every dimension returned either Pass or a named fault with its sub-skill — no dimension skipped without explanation.
- Dimensions 1 and 2 were diagnosed from actual opening and ending text, not skeleton.
- The priority diagnosis lists faults in dimension order (Dim 1–2 before Dim 3–7) with the most severe fault ranked first within each group.
- The top two priority sub-skills' full output — using each skill's exact review shape — is applied to the two most urgent structural faults, in priority order.
- No structural fault visible from the text (or skeleton) has been left unnamed.

Pass only when every applicable check passes.

## Source Boundary

Aristotle's *Rhetoric* is public domain. Quiller-Couch *On the Art of Writing* (1916) is public domain. Fowler & Fowler *The King's English* (1908) is public domain. Sub-skill outputs must follow each sub-skill's own source boundary. Do not invent quotations attributed to named authors.
