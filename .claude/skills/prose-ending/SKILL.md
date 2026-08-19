---
name: prose-ending
description: Diagnose whether a piece of writing closes or merely stops. Flags six named faults: summary repeat, soft question-hook, imported thought, abrupt stop, virtue claim, callback failure. Minimum text unit: last 5 paragraphs plus first paragraph (for callback check). Source: Aristotle Rhetoric Book III Ch. 19, Quiller-Couch (1916), Fowler & Fowler (1908).
---

# Prose Ending

Use this skill when reviewing the final paragraph or paragraphs of any prose piece — essay, article, chapter, blog post, nonfiction book section. An ending closes: it does not recapitulate what the reader just read, introduce material the piece hasn't earned, or dangle a question as a substitute for a conclusion.

**Minimum text unit:** Last 5 paragraphs (or up to 500 words) plus the first paragraph of the piece — the opening is required to check for callback obligations. For long texts (20,000+ words), this skill always reads the actual opening and ending of the full text, not the skeleton.

Source concept: Aristotle names four functions of the epilogue: to make the hearer well-disposed, to amplify or depreciate what has been argued, to put the hearer in the right emotional state, and — critically — "to refresh the memory." Refreshing memory is not repeating; it is the compressed restatement that allows the reader to leave with a clear impression of the whole. Aristotle adds a constraint: "In the epilogue, the speaker must not introduce a fresh argument, lest the hearer be put in doubt." (Aristotle, *Rhetoric*, Book III Ch. 19.) The corresponding failure mode is what Quiller-Couch calls the impulse to "perpetrate a piece of exceptionally fine writing" at the close — the bow at the curtain, where the writer performs completion rather than achieving it. (Quiller-Couch, *On the Art of Writing*, Lecture XII, 1916.)

---

## Fault Taxonomy

Six named faults, checked in order.

### Fault 1 — Summary Repeat
The ending rehearses, in order, the major claims or events of the piece. This is recapitulation, not synthesis. The reader has just read the piece; listing what it contained adds no new arrival.

*Test:* Does the ending contain any claim, synthesis, or implication not present earlier in the piece? If no — if the ending is built entirely from material already stated — it is a summary repeat.

*Distinction:* The compressed callback is not a summary repeat. Returning to a single image or phrase from the opening, transformed by the intervening argument, closes the circle without recapitulating the journey. The test is whether the callback carries something forward or merely points back.

### Fault 2 — Soft Question-Hook
The piece ends with a question — often beginning "Perhaps one day…", "What, then, is…", or "The question remains…" — as a device to seem open or profound. A question that the piece should have answered is evasion, not conclusion.

*Test:* Is the question one the piece was obligated to address? If yes, the question-hook is evasion. If the piece has genuinely established that the question is unanswerable or genuinely open, and the ending reflects this honestly rather than as a rhetorical gesture, the question may be earned.

### Fault 3 — Imported Thought
The ending introduces a claim, concept, or example that has not appeared earlier in the piece. Anything arriving only in the final paragraph needed to earn its position earlier — or does not belong in the piece.

*Test:* Does the final paragraph contain a noun — a person, place, concept, event — not named or established earlier? If yes, the ending is importing material.

*Source:* Aristotle: the epilogue must not start new subjects. The reader who meets a new idea in the final paragraph has no time to integrate it; the piece ends before the thought can land.

### Fault 4 — Abrupt Stop
The piece ends before the reader has been released. The text ceases without any signal that it is closing — no synthesis, no shift in register or pace, no sense of arrival. The reader reaches the last sentence and expects another.

*Test:* Does the final sentence read as a final sentence — does it carry any weight of completion — or does it read as a mid-piece sentence that happens to be last?

### Fault 5 — Virtue Claim
The ending makes a large general claim about values, significance, or meaning that the piece has not earned through its specific argument or evidence. The writer performs gravity at the close.

*Signs:* "Ultimately, what matters is…", "In the end, we are all…", "Perhaps the real lesson here is…", "At its core, this is a story about…"

*Test:* Could the virtue claim be appended to any piece on any topic? If yes, it has not been earned by this piece specifically — it is borrowed gravity.

### Fault 6 — Callback Failure
The opening established a specific detail, image, scene, or question that the ending fails to address or resolve. Not every piece requires a callback. But when the opening creates a structural promise — a scene opened but not closed, a question posed but not answered, a character introduced and then abandoned — the ending must honor it.

*Test:* Read the first paragraph. Does it contain a specific image, scene, character, or question? If yes: does the ending, or some earlier section, return to or resolve it? If no return and no resolution — the ending has left a structural obligation unfulfilled.

---

## Review Shape

Use the **Preserve** shape when the ending closes effectively:

```
Principle:
prose-ending: <one sentence naming what the ending does right>

Preserve:
<ending as supplied>

Why:
<confirm which fault is absent and why the ending earns its position — what it synthesizes, what structural obligation it fulfills, what it adds beyond what preceded it>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Use the **Repair** shape when one or more faults are present:

```
Principle:
prose-ending: <one sentence naming the primary fault>

Weak:
<ending as supplied>

Fault:
<name the fault (Fault 1–6); apply the relevant test — what is being repeated, imported, avoided, or left unresolved>

Better:
<revised ending — fault addressed: summary-repeat compressed to synthesis; question-hook replaced with arrival; imported thought removed; abrupt stop extended to a sentence of release; virtue claim grounded in the piece's specific content; callback obligation honored>

Why:
<name what changed and confirm what the ending now does that the original did not>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Start `Principle` with the exact skill name `prose-ending`.

---

## Objective Rubric

- The ending does not list or restate major claims already made in the piece.
- The ending contains no claim, concept, or example not established earlier in the piece.
- If the opening created a structural obligation (scene, question, image), the ending or an earlier section addresses it.
- The final sentence reads as a final sentence — it carries a sense of arrival, not continuation.
- Any question in the ending is earned by the piece having genuinely established that the question is open.
- No general moral or value claim appears that the piece has not earned through its specific argument or evidence.

Pass only when every applicable check passes.

## Source Boundary

Aristotle's *Rhetoric* is public domain. Quiller-Couch *On the Art of Writing* (1916) is public domain. Fowler & Fowler *The King's English* (1908) is public domain. Examples should be invented passages clearly labeled as such, or drawn from public-domain prose (pre-1928). Do not invent quotations attributed to named authors.
