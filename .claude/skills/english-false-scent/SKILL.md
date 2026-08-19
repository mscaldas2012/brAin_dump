---
name: english-false-scent
description: Identify and repair false-scent constructions — sentences that lead the reader into an incorrect grammatical parse at the opening, requiring a re-read when the correct structure becomes clear. Source: Fowler & Fowler, The King's English, 1908.
---

# English False Scent

Use this skill when a sentence forces the reader to stop, back up, and reparse because its opening promised a grammatical construction that the sentence does not deliver.

Source concept: A false scent is laid when the way a sentence begins leads the reader to expect a construction that the rest of the sentence does not complete — the opening functions as a grammatical decoy, and the reader's first parse must be abandoned and replaced. (Fowler & Fowler, *The King's English*, 1908)

## Rules

- **The re-read test**: read the sentence at normal reading speed. If a word arrives that does not fit the construction the reader was building from the opening, and the reader must re-parse from an earlier point, a false scent is present. The reader should never have to move backward in a sentence to understand it.
- **Type 1 — misleading opening modifier**: an adjectival or participial phrase at the start implies a subject that does not become the main clause subject. *"Walking through the gate, the garden came into view."* The participial phrase implies a person walking; "the garden" is not that person. Repair: make the implied subject the grammatical subject: *"Walking through the gate, she saw the garden."*
- **Type 2 — misleading parallel**: the first element of a list or series establishes a grammatical form (noun, infinitive, gerund) that a later element abandons. *"His duties were to file reports, attending meetings, and that he managed correspondence."* Each element promises the form of the first (*to file*) but the sentence delivers gerund then clause. Repair: make all elements the same form (see `english-unequal-yokefellows`).
- **Type 3 — misleading head noun**: a long noun phrase or embedded modifier appears between the sentence's grammatical subject and its verb, causing the reader to mistake the true subject. *"Decisions that the committee had deferred, in many cases for procedural reasons, requires final action."* "Requires" arrives after a plural noun ("reasons"); the reader may misparse. Repair: move the modifier or use a relative clause that stays close to its noun.
- **Type 4 — ambiguous pronoun**: a pronoun appears to reference the most recent noun but references an earlier one. *"He handed the file to his colleague, and then he filed the originals."* Which "he"? Repair: name one of the referents, or restructure to remove the ambiguity.
- The general remedy: ensure the sentence's grammatical shape from its first word signals its logical shape. If the opening commits to a construction, complete it.

## Review Shape

Use the preserve shape for strong models:

```
Principle:
<english-false-scent: one sentence naming the concept>

Preserve:
<supplied passage>

Why:
<confirm that each sentence's opening commits to a grammatical construction that the sentence completes — identify any potential misleads and explain why each resolves without re-reading>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Use the repair shape for weak passages:

```
Principle:
<english-false-scent: one sentence naming the concept>

Weak:
<sentence or passage containing a false scent>

Fault:
<identify the false-scent type (misleading modifier / misleading parallel / misleading head noun / ambiguous pronoun); describe the incorrect parse the reader makes and the word at which it fails>

Better:
<revised sentence where the grammatical shape from the first word matches the logical shape the sentence completes>

Why:
<name the specific restructuring: what grammatical promise did the opener make, and how does the revision honour it from the start?>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Start `Principle` with the exact skill name `english-false-scent`.

## Objective Rubric

- No sentence in the revision requires the reader to reparse after reaching a word that does not fit the expected construction.
- Every opening participial or adjectival phrase has the correct grammatical subject as the subject of the main clause.
- Every series or parallel list uses the same grammatical form for all elements.
- Every pronoun has an unambiguous referent identifiable without re-reading the surrounding text.

Pass only when every applicable check passes.

## Source Boundary

Examples may be drawn from public-domain English prose (pre-1928) or invented passages clearly labeled as such. Fowler & Fowler, *The King's English* (1908) is in the public domain. Do not invent quotations attributed to named authors. Note: for unequal parallel structures, see `english-unequal-yokefellows`; for dangling participials as a standalone fault, see `english-wrong-turning`.
