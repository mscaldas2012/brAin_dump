---
name: english-style
description: Triage any English prose passage and identify which english-* skills to apply, in priority order. Use as the entry point when faults are not immediately obvious or when a full diagnostic is needed before targeted repair. Routes across all 23 skills in the english-* set.
---

# English Style

Use this skill when facing a prose passage whose primary faults are not immediately obvious, or when you want a complete diagnostic before choosing which specific skill to invoke. This skill diagnoses and routes — it does not repair directly, but it applies the top-priority skill at the end.

Source concept: Good prose is direct, simple, brief, vigorous, and lucid. Faults of style fall into six tiers, checked in priority order — grammatical errors that mislead the reader before economy, vocabulary before imagery, structure before judgment. Identify the tier first; then the skill. (Synthesized from Quiller-Couch, Fowler & Fowler, Orwell, Strunk, and Spencer.)

---

## Diagnostic Tiers

Check the passage against all six tiers in order. Note every fault found.

### Tier 1 — Grammar and Construction
*Check first. These mislead the reader about sentence structure and must be repaired before anything else.*

| If you see… | Invoke |
|---|---|
| A sentence that requires re-reading — the first parse fails when a word arrives that does not fit | `english-false-scent` |
| An opening participial or adjectival phrase whose implied subject is not the main clause subject | `english-wrong-turning` |
| Items joined by *and / or / but* that are different grammatical forms (noun + clause, gerund + infinitive, active + passive) | `english-unequal-yokefellows` |

### Tier 2 — Voice and Economy
*Highest density of improvement. Passive constructions, inflated verb-phrases, and surplus words.*

| If you see… | Invoke |
|---|---|
| *was / were / been / being* + past participle with no expressed agent | `english-stationary-passive` |
| Passive construction with an expressed *by-* phrase; or *there is / there are / it was* as expletive opening | `english-active-voice` |
| *make / give / take / have / perform / conduct / achieve* + abstract noun in *-tion / -sion / -ment / -ance* | `english-noun-verb-inversion` |
| *render inoperative / give rise to / make contact with / with respect to / in view of the fact that / -ize* formations | `english-verbal-false-limbs` |
| *the fact that / it should be noted that / each and every / owing to the fact that* / redundant modifier pairs | `english-omit-needless-words` |
| Systemic pattern of abstract nouns + passive constructions throughout the whole passage | `english-jargon` |

### Tier 3 — Vocabulary
*Words chosen for status, atmosphere, or evasion rather than precision.*

| If you see… | Invoke |
|---|---|
| *utilize, facilitate, implement, epoch-making, transformative*; foreign phrases as ornament | `english-pretentious-diction` |
| Evaluative terms (*authentic, important, significant, democratic*) without surrounding content that gives them meaning | `english-meaningless-words` |
| Archaic words (*forsooth, methinks, ere, prithee, perchance, 'tis, 'twas*) in otherwise modern prose | `english-wardour-street` |
| *not un- / not in- / less than helpful / not without merit / more than adequate* | `english-not-un-formation` |
| Varied terms (synonyms, circumlocutions) used for the same person, concept, or object across a passage | `english-elegant-variation` |

### Tier 4 — Imagery
*Figures of speech that have worn out, collide, or are less economical than their compressed form.*

| If you see… | Invoke |
|---|---|
| Figurative language present — does each figure still call up a specific image? | `english-dying-metaphors` |
| Two or more figures in close proximity — do they share a compatible literal scene? | `english-mixed-metaphors` |
| A simile or analogy spelled out at length where a metaphor or plain statement would serve | `english-economy-of-figures` |

### Tier 5 — Structure and Emphasis
*Where the weight of the sentence falls, and whether it falls in the right place.*

| If you see… | Invoke |
|---|---|
| Sentence ends on a hedge, qualifier, or weak function word; key element buried mid-sentence | `english-end-emphasis` |
| A series or list where items are not the same grammatical form; correlative pairs (*both…and*) that are unbalanced | `english-parallel-construction` |
| Vague quantities (*a large number of, many, some*) or general categories where specific names/numbers are available | `english-concrete-language` |
| A subordinate clause, parenthetical, or modifier longer than the main clause it belongs to | `english-wens` |
| Subject phrase is long and complex — more than ten words before the main verb arrives | `english-sentence-weight` |

### Tier 6 — Authorial Judgment
*Apply last. Requires knowledge of the passage's purpose and the writer's intent.*

| If you see… | Invoke |
|---|---|
| A passage that seems to exist for the writer's pleasure rather than the reader's need: extended analogies, digressions, over-elaborate phrases that pass the compression test but fail the function test | `english-murder-your-darlings` |

---

## Triage Procedure

1. Read the passage once at normal speed. Mark any sentence that requires re-reading. → **Tier 1.**
2. Scan for passive constructions and padding words (*was/were, the fact that, -tion nominalizations, in view of*). → **Tier 2.**
3. Read for word choices. Flag Latinate abstractions, archaisms, empty evaluative claims. → **Tier 3.**
4. Identify all figures of speech. Apply the image test (Tier 4a) and the collision test (Tier 4b) to each. → **Tier 4.**
5. Read for sentence endings and list structures. Note trailing qualifiers and long subjects. → **Tier 5.**
6. Ask: does any passage exist for the writer's satisfaction rather than the reader's need? → **Tier 6.**

Report all faults found, then rank by tier (Tier 1 faults outrank Tier 2, etc.); within the same tier, rank by frequency and severity.

---

## Review Shape

```
Triage:
<supplied passage>

Findings:
Tier 1 (Grammar): <Pass — or — [specific fault identified], skill: english-X>
Tier 2 (Voice/Economy): <Pass — or — [specific fault identified], skill: english-X>
Tier 3 (Vocabulary): <Pass — or — [specific fault identified], skill: english-X>
Tier 4 (Imagery): <Pass — or — [specific fault identified], skill: english-X>
Tier 5 (Structure): <Pass — or — [specific fault identified], skill: english-X>
Tier 6 (Judgment): <Pass — or — [specific fault identified], skill: english-X>

Priority diagnosis:
1. <english-X> — <one sentence naming the specific fault and where it appears>
2. <english-X> — <one sentence naming the specific fault and where it appears>
3. <english-X> — <one sentence naming the specific fault and where it appears>

Applying <top priority skill>:
<Full Repair or Preserve shape output from that skill>
```

Start the `Triage` block with the exact supplied passage.

---

## Objective Rubric

- Every tier returned either Pass or a named fault with its corresponding skill — no tier was skipped.
- The priority diagnosis lists faults in tier order (Tier 1 before Tier 2), with the most severe or frequent fault within a tier ranked first.
- The top-priority skill's full repair shape is applied to the most urgent fault found.
- No fault catchable by any listed skill has been left unnamed in the findings.

Pass only when every applicable check passes.

## Source Boundary

This skill synthesizes diagnostic frameworks from public-domain sources: Quiller-Couch (1916), Fowler & Fowler (1908), Orwell (1946 — paraphrase only), Strunk (1918), and Spencer (1852). Examples used in individual skill outputs must follow that skill's own Source Boundary.
