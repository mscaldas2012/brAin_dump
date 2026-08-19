---
name: prose-flow
description: Diagnose whether a prose text has a through-line — an organizing logic by which each section earns the next. Produces a flow map of every section transition and names five faults: missing bridge, topic drift, stall and restart, mechanical transition, through-line break. For long texts uses a sliding-window protocol. Source: Forster Aspects of the Novel (1927), Strunk Elements of Style (1918), Aristotle Rhetoric Book III.
---

# Prose Flow

Use this skill when a piece is difficult to follow — not because sentences are unclear but because the reader keeps losing the thread between sections. The fault is at the joints, not the panels. Individual sections may be strong; the problem is that they do not pull the reader from one to the next.

**Minimum text unit:** Full text for Tier 1 (under 3,000 words) and Tier 2 (3,000–20,000 words). For Tier 3 (over 20,000 words): sliding-window protocol — read adjacent section pairs in sequence; see Long-Text Protocol below.

Source concept: "The king died and then the queen died" is a story. "The king died and then the queen died of grief" is a plot. "The time-sequence is preserved, but the sense of causality overshadows it." (E.M. Forster, *Aspects of the Novel*, Chapter 5, 1927.) A text with flow has plot-logic between its sections — causal, consequential, or logical necessity — not merely story-logic (sequential, temporal). At every joint, the reader should be able to answer not only "what comes next?" but "why does this come next?" A text that can only answer the first question moves but does not flow. Strunk establishes the enabling condition: "Begin each paragraph with a sentence that suggests the topic or helps the reader see at a glance what the paragraph is about." (Rule 9, *Elements of Style*, 1918.) When each section opens by declaring its subject, the handoff between sections is visible. When openings are vague, transitions are invisible.

---

## Through-Line Test

Before mapping individual transitions, identify the piece's through-line: the single organizing logic that explains why sections appear in this order.

A through-line can be causal ("X caused Y, which led to Z"), argumentative ("claim → evidence → objection → rebuttal → conclusion"), narrative ("setup → complication → resolution"), or thematic ("each section adds a new dimension to a governing idea"). What it cannot be is merely sequential ("section 2 follows section 1 because section 2 is next").

State the through-line in one sentence before mapping transitions. If no through-line can be stated — if the description changes depending on which section you're reading — name this as Fault 5 (through-line break), which is the most serious flow fault and the only one that cannot be repaired at the transition level.

---

## Fault Taxonomy

Five named faults.

### Fault 1 — Missing Bridge
Section N ends on one subject; Section N+1 opens on a different subject with no connecting statement. The reader must supply the logical or narrative link. The gap is invisible from within either section but jarring at the transition.

*Test:* Read the last sentence of Section N and the first sentence of Section N+1. Could a reader who knew only these two sentences state why N+1 follows N? If not, the bridge is missing.

*Distinction:* A bridge need not be a transitional sentence. The final sentence of Section N can open a pressure or question that the first sentence of Section N+1 immediately relieves — an implicit bridge. But it must be there in some form.

### Fault 2 — Topic Drift
A section begins about subject A and ends, through a series of small steps, at subject B — without acknowledging the migration. The reader arrives at subject B without having been taken there, only having slipped. The next section then finds the reader misaligned.

*Test:* State the subject of the section's first sentence; state the subject of its last sentence. If they differ, and no sentence within the section announces the shift, the section has drifted.

### Fault 3 — Stall and Restart
The argument or narrative stalls — stops advancing — then resumes the same claim or narrative beat from a new angle, as if the intervening material hadn't happened. Unlike a deliberate recap, which acknowledges itself ("to put this more directly," "in other terms"), the stall and restart presents itself as continuation while actually circling.

*Signs:* A section ends by summarizing what it argued; the next section opens by arguing the same claim from a slightly different angle, with no bridge stating "this is a different approach to the same problem." The argument spins rather than moves.

### Fault 4 — Mechanical Transition
A transitional word or phrase at a section boundary where no genuine logical relationship exists. The transition word names a relationship (contrast: *however, but, yet*; addition: *moreover, furthermore, additionally*; consequence: *therefore, thus, consequently*) that the surrounding content does not support.

*Test:* Remove the transitional word. Does the actual relationship between sections become clearer without it? If yes, the word was papering over an absent connection. Replace it with a bridge sentence that names the real relationship — or acknowledge that the connection must be built.

*Common form:* "However" used to introduce a section that does not contrast with the previous one. The word signals contrast; the content delivers continuation.

### Fault 5 — Through-Line Break
The piece has no discernible through-line: no consistent organizing logic that explains why sections appear in this order. Individual sections may be well-written; individual transitions may be locally smooth; but the piece as a whole cannot be said to be moving in any direction. This is the most serious flow fault.

*Test:* State the through-line in one sentence. If the statement changes depending on which section you're reading — if the piece seems to be about different things in different sections, with no governing logic connecting them — the through-line is broken.

*Repair path:* Through-line break requires restructuring, not local repair. Identify what the piece is actually about — which sections share a coherent organizing logic — and rebuild the sequence around that. Sections that cannot be connected to the through-line should be treated as candidates for removal or relocation.

---

## Long-Text Protocol (Tier 3 — over 20,000 words)

1. From the skeleton, identify all section boundaries (headers, chapter breaks, major scene divisions).
2. For each adjacent pair (Section N, Section N+1): read the last 150 words of Section N and the first 150 words of Section N+1.
3. Apply the bridge test (Fault 1) and mechanical transition test (Fault 4) to each pair.
4. For topic drift (Fault 2) and stall/restart (Fault 3), which require reading the full section: apply these only to sections flagged as suspicious from the skeleton — sections where the closing sentence's subject differs from the opening sentence's subject.
5. Produce the flow map from these readings and note which findings are based on section pairs vs. full section reads.

---

## Review Shape

```
Through-line:
<state the piece's organizing logic in one sentence — or: "Through-line not identifiable: Fault 5">

Flow Map:
[Section name / opening phrase] → [Next section]: Pass — or — [Fault type]: <one sentence describing the specific gap, drift, stall, or false connector>
[repeat for every transition]

Faults:
1. [Fault type] at [location]: <description — what is missing, what has drifted, what is stalling, what connector is false>
2. [Fault type] at [location]: <description>
...

Priority repair:
```

Apply the standard repair shape to the highest-priority fault:

```
Principle:
prose-flow: <one sentence naming the fault>

Weak:
<the transition passage as it stands — last paragraph of Section N and first paragraph of Section N+1>

Fault:
<identify the specific gap, drift, stall, or false connector; apply the relevant test>

Better:
<revised transition — bridge sentence added, drift corrected, stall untangled, false connector replaced with a statement of actual relationship>

Why:
<name what changed and confirm what the reader can now do that they could not before — specifically: they can now answer "why does this come next?">

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

---

## Objective Rubric

- The through-line is stated in one sentence, or Fault 5 (through-line break) is named with a location.
- Every section transition is marked Pass or a named fault — no transition skipped.
- Each named fault includes the specific location and a one-sentence description of the problem.
- No transitional word remains that names a relationship the surrounding content does not support.
- The priority repair produces a transition where the reader can answer "why does this come next?"

Pass only when every applicable check passes.

## Source Boundary

E.M. Forster *Aspects of the Novel* (1927) is in the public domain in the United States. Strunk *The Elements of Style* (1918) is public domain. Aristotle's *Rhetoric* is public domain. Examples should be invented passages clearly labeled as such, or drawn from public-domain prose (pre-1928). Do not invent quotations attributed to named authors.
