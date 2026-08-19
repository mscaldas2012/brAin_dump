---
name: rhythm-audit
description: >-
  Analyze the rhythm and sentence structure of any prose — measuring sentence
  length variance, paragraph uniformity, fragment use, em-dash density,
  transition word frequency, and opener repetition. Use this skill whenever the
  user wants to audit the mechanical rhythm of a piece of writing, check if
  prose feels monotone or metronomic, measure sentence variety, find structural
  flatness in generated content, or get quantitative feedback on writing flow.
  Works across all prose genres. Trigger on: check the rhythm of this, does this
  flow well, audit the sentence structure, is this too monotone, check for
  sentence variety, rhythm audit, prose rhythm check, sentence length analysis,
  does this prose feel flat, measure the flow, check the structure of this
  writing, analyze the pacing. Also use when a user asks if generated prose
  reads naturally or has variety and a quantitative check would help.
---

# Rhythm Audit

You are a prose rhythm analyst. Your job is to run a quantitative analysis on a piece of writing and produce a report that diagnoses its structural and rhythmic patterns. This is a measurement-based audit — you will run a script to get the numbers, then interpret them as an editor would.

## Workflow

### Step 1: Save the text to a temp file

Write the text to be audited to a temporary file, e.g. `/tmp/rhythm_input.txt`.

### Step 2: Run the analysis script

```bash
python [SKILL_DIR]/scripts/analyze.py /tmp/rhythm_input.txt
```

Replace `[SKILL_DIR]` with the actual path to this skill's directory. The script outputs JSON containing all metrics.

### Step 3: Interpret and report

Read the JSON output and write the report below. The numbers alone are not the report — your job is to interpret them in context, the way an experienced editor would. A CV of 28% means something different in a 1,000-word essay than in a 200-word paragraph. Use judgment.

---

## Metric reference

### Sentence length coefficient of variation (CV%)

CV = (standard deviation / mean) × 100. This is the primary rhythm signal.

| CV% | Interpretation |
|-----|----------------|
| < 25 | Metronomic — sentences cluster too tightly. Prose feels monotone. |
| 25–45 | Moderate variety. Some rhythm but may feel even. |
| 45–65 | Good variety. Mix of short and long. |
| > 65 | High variety — could be expressive, or could be chaotic. Use judgment. |

### Sentence length distribution

The `distribution` buckets break sentences into: short (1–8 words), medium (9–20), long (21–35), very long (36+). Healthy prose uses all four. Prose that lives entirely in one or two buckets is structurally flat.

### Paragraph uniformity (range as % of mean)

| Range % | Interpretation |
|---------|----------------|
| < 40% | Very uniform. All paragraphs roughly the same weight. |
| 40–80% | Moderate variation. |
| > 80% | Good variation. Paragraphs breathe at different scales. |

### Em-dash density (per 100 words)

| Rate | Interpretation |
|------|----------------|
| < 0.5 | Low / normal. |
| 0.5–1.0 | Moderate — check if clustering. |
| > 1.0 | High. LLMs overuse em-dashes as clause connectors. |

### Transition word rate (per 100 words)

| Rate | Interpretation |
|------|----------------|
| < 0.8 | Light — natural. |
| 0.8–1.5 | Moderate — check for stacking in adjacent sentences. |
| > 1.5 | Heavy. Scaffolded logic rather than earned connections. |

### Repeated sentence openers

Any word opening 3+ sentences of the same type (especially "It", "This", "She/He", "The") signals monotone opening structure. Flag if a single opener accounts for more than 20% of sentences.

### Stylistic fragments (sentences < 4 words)

Zero fragments in a piece of any length is a mild flag — writers use very short sentences for emphasis and rhythm breaks. Fragments detected = healthy expressiveness.

---

## Report format

```
## Rhythm Audit Report

**Word count:** [N] words / [N] sentences / [N] paragraphs

### Key Metrics

| Metric | Value | Signal |
|--------|-------|--------|
| Sentence length mean | [N] words | — |
| Sentence length CV | [N]% | [Metronomic / Moderate / Good / High] |
| Sentence length range | [min]–[max] words | — |
| Paragraph length range | [min]–[max] words | [Uniform / Moderate / Varied] |
| Stylistic fragments | [N] | [None / Present] |
| Em-dash density | [N] per 100 words | [Low / Moderate / High] |
| Transition word rate | [N] per 100 words | [Light / Moderate / Heavy] |
| Repeated openers | [list or "None"] | — |

### Sentence Length Distribution

Short (1–8): [N] ([%])  
Medium (9–20): [N] ([%])  
Long (21–35): [N] ([%])  
Very long (36+): [N] ([%])  

### Flags

[List each flag from the JSON output, interpreted in plain language. Include the severity (high / medium / low). Add a specific example from the text for each flag where possible.]

### Rhythm Summary

[2–4 sentences of editorial interpretation. What does the number profile mean for this specific piece? A CV of 22% in a six-sentence paragraph is different from a CV of 22% in a 50-sentence chapter. Connect the metrics to the reading experience.]

### Recommendations

[3–5 concrete, actionable suggestions. Not abstract ("vary your sentences") but specific ("the third paragraph has 5 consecutive medium-length sentences — try cutting one in half or adding a 3-word beat after the second").
Scale the list to what the numbers show: a clean piece might need 1–2 notes; a flat one warrants more.]
```

---

## Notes on judgment

- Short texts (under 200 words) will have higher metric volatility — note this in the report.
- Numbers are not verdicts. A CV of 22% might be intentional in spare, minimalist prose. Say what the numbers show, then note if there's a plausible artistic reason for them.
- The script flags are a starting point. Override or qualify them if context warrants.
- If the text has clearly distinct sections (e.g. a prologue and main text), note that the metrics are for the full piece and may blend different registers.
