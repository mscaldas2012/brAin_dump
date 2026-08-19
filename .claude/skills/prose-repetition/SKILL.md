---
name: prose-repetition
description: Diagnose idea-level repetition in prose — not word-level (handled by sentence skills) but structural: the same claim restated in different language, the same example used twice, an argument that circles back to its opening without synthesis. Extracts a claim list and evidence inventory, then applies four fault tests: paraphrase restatement, example reuse, structural circularity, cumulative echo. For long texts uses the structural skeleton's claim summaries. Source: Aristotle Rhetoric and Topics, Fowler & Fowler The King's English (1908), Strunk Elements of Style (1918), Quiller-Couch On the Art of Writing (1916).
---

# Prose Repetition

Use this skill when a piece feels longer than it needs to be — when it seems to circle the same territory, when the reader senses they have been here before without being able to point to an exact repeated sentence, or when the ending restates the opening without seeming to have traveled. Word-level repetition is a sentence concern; this skill operates at the level of ideas, examples, and structure.

**Minimum text unit:** Full text for Tier 1 (under 3,000 words) and Tier 2 (3,000–20,000 words). For Tier 3 (over 20,000 words): use the structural skeleton's claim summaries (the "Core" field from the prose-structure skeleton protocol) as the claim list; evidence inventory for Tier 3 is limited to named examples visible in section openings and closings. Note that Tier 3 analysis is structural approximation — local example reuse within sections may not be detectable from the skeleton alone.

Source concept: Aristotle identifies redundancy as a form of logical weakness — restating a claim signals that it was not sufficiently made the first time. "To say a thing twice is… putting into the argument what is not in it." (*Rhetoric*, Book III.) Fowler names "tautology" as the repetition of an idea in a different word, phrase, or sentence — "not the repetition of the word itself, but of its meaning" — and "double emphasis" as the repetition of a point beyond the difficulty of the point. (Fowler & Fowler, *The King's English*, Part II, 1908.) Strunk's Rule 13 extends the principle to structure: "A sentence should contain no unnecessary words, a paragraph no unnecessary sentences, for the same reason that a drawing should have no unnecessary lines." (*Elements of Style*, Rule 13, 1918.) At the structural level: a piece should contain no unnecessary sections — no section that says what another section has already said. Quiller-Couch's twenty-three-word demonstration reduces "I was entirely indifferent as to the results of the game, caring nothing at all as to whether I had losses or gains" to eight words by removing duplicate expressions. (*On the Art of Writing*, Lecture V, 1916.) The same compression principle applies between sections.

---

## Extraction Protocol

Before running any fault test, extract two things from the text.

### Claim List
For each major section, state the central claim in one compressed sentence. Apply the compression principle: reduce the section's argument to its logical minimum — subject, verb, object. No qualifications, no examples, no hedging. If the section makes multiple claims, list them as sub-claims under the section heading.

*Format:*
```
[Section name]
Central claim: <one sentence>
Sub-claims (if any): <list>
```

### Evidence Inventory
List all named examples, anecdotes, quotations, historical events, persons, data points, or illustrative cases used anywhere in the text. For each, note the section(s) where it appears.

*Format:*
```
[Example / anecdote / quotation / case]  →  [Section(s) where used]
```

These two outputs — the claim list and the evidence inventory — are the working material for all four fault tests.

---

## Fault Taxonomy

Four named faults.

### Fault 1 — Paraphrase Restatement
Two sections (or passages within sections) assert logically equivalent claims, in different language, without acknowledging the relationship. The reader feels the argument is repeating but cannot identify an exact repeated sentence because none exists — the repetition is at the level of meaning.

*Compression test:* Reduce Claim A and Claim B each to their logical minimum. Are the compressed forms logically equivalent — does one entail the other, with no additional information in either direction? If yes, they are paraphrases, and one instance is doing no unique work.

*Distinction:* A claim can legitimately reappear if: (a) the second instance adds something the first did not (new evidence, a new angle, a qualification); or (b) the second instance explicitly acknowledges the first ("to approach this differently," "stated another way," "this is the same point made earlier, but it bears repeating because…"). Without (a) or (b), the restatement is a fault.

*Repair:* Identify which instance is stronger — better placed, more developed, more specifically supported. Keep it; cut or redirect the weaker one. If both instances have unique supporting material, merge them into one section where both the claim and its support appear together.

### Fault 2 — Example Reuse
An illustrative case, anecdote, quotation, or piece of evidence appears in the evidence inventory at more than one location, and the second use does not acknowledge the first.

*Test:* For any example appearing at two or more locations in the inventory: does the second use acknowledge the first? If no acknowledgment appears ("as noted earlier," "the same example applies here," "returning to the case of…"), the reuse is a fault.

*Distinction:* Deliberate return to an example is a structural technique — a case introduced early that is reexamined from a new angle later. The fault is unacknowledged reuse, which implies the writer forgot they had already used it, or assumes the reader forgot. Either undermines the piece's authority.

*Repair:* Either remove the second use entirely, or acknowledge the first explicitly and state why the example is being reconsidered. The acknowledgment converts a fault into a structural echo.

### Fault 3 — Structural Circularity
The piece's conclusion restates its opening premise without synthesis — the argument has traveled in a circle. The reader arrives where they started, and the journey has not moved the premise forward. No new claim has been established; the conclusion could have been stated before the piece began.

*Compression test:* Compress the opening claim and the closing claim each to their logical minimum. Are they logically equivalent? If yes, trace the journey between them: has anything been proved, demonstrated, or added in between? A legitimate circular structure (used in classical rhetoric's peroration) transforms the opening premise — the conclusion restates the premise but in a form enriched by the intervening argument. A circular fault returns to the premise unchanged.

*Signs:* A conclusion that opens "As we have seen…" and then summarizes the sections in order; a conclusion that repeats the thesis statement from the introduction in nearly identical language; a conclusion where every claim could have been stated in an abstract, before any of the supporting material had been presented.

*Repair:* The conclusion must add something the opening could not have contained: a synthesis (a claim that emerges only because the preceding sections were traversed), a consequence (what follows from having proved what was proved), or a transformed premise (the opening claim restated in a form that only makes sense in light of what came between).

### Fault 4 — Cumulative Echo
No single section repeats another explicitly, but the same idea appears across three or more sections, each time treated as if it is making a new point. No individual instance is a paraphrase restatement; the problem is the pattern across the whole text — the same ground is covered multiple times under different headings or from different angles, without each angle being necessary.

*Test:* Group the claims in the claim list by subject. If the same subject appears in the central claims of three or more sections, ask: does each section's treatment add something the others did not? Does each angle reveal a genuinely new dimension of the subject, or is it covering the same ground with different emphasis?

*Distinction:* A subject can legitimately recur across a piece if each recurrence adds substance — new evidence, a new implication, a new objection addressed. The fault is when the recurrences cover the same ground, adding only volume, not depth. The cumulative effect is that the piece feels longer than it is.

*Repair:* Identify which section's treatment of the subject is most complete and best positioned. Consolidate: incorporate the unique material from the other sections into one, and remove the redundant treatments entirely.

---

## Review Shape

```
Claim List:
[Section]          | Central Claim
<section name>     | <one compressed sentence>
<section name>     | <one compressed sentence>
... (all sections)

Evidence Inventory:
<Example / case / quotation>   →   <Section(s)>
... (all named examples)

Faults:
1. [Fault type]: <Claim A (location) and Claim B (location) — description of the repetition; compression test result>
2. [Fault type]: <Example (locations) — description of the reuse; acknowledgment test result>
3. [Fault type]: <description of circularity or echo — what is not being added>
...

Priority repair:
```

Apply the standard repair shape to the highest-priority fault:

```
Principle:
prose-repetition: <one sentence naming the fault>

Weak:
<the two instances of the repeated claim, example, or structure — as they appear in the text>

Fault:
<apply the relevant test — compression test for claims, acknowledgment test for examples, transformation test for circularity — and state the result>

Better:
<the repair: the stronger instance kept; the weaker cut or redirected; the example's second use acknowledged; the conclusion transformed to add what the opening could not have contained>

Why:
<name what was removed or changed and confirm what unique work each remaining section now does>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Start `Principle` with the exact skill name `prose-repetition`.

---

## Objective Rubric

- Every major section appears in the claim list with a compressed central claim — no section omitted.
- Every named example, anecdote, quotation, or case appears in the evidence inventory with its location(s).
- Each fault names the specific claim or example involved, states the test applied, and gives the test result.
- The priority repair produces a version where each section or instance is doing work the others are not.
- No two sections in the repaired piece assert logically equivalent claims without acknowledgment.

Pass only when every applicable check passes.

## Source Boundary

Aristotle's *Rhetoric* and *Topics* are public domain. Fowler & Fowler *The King's English* (1908) is public domain. Strunk *The Elements of Style* (1918) is public domain. Quiller-Couch *On the Art of Writing* (1916) is public domain. Examples should be invented passages clearly labeled as such, or drawn from public-domain prose (pre-1928). Do not invent quotations attributed to named authors.
