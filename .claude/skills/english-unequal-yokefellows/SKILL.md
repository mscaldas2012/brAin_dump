---
name: english-unequal-yokefellows
description: Identify and repair unequal yokefellows — elements joined by conjunction (and, or, but) that appear to be parallel but occupy different grammatical categories or logical levels, creating a false symmetry the structure cannot support. Source: Fowler & Fowler, The King's English, 1908.
---

# English Unequal Yokefellows

Use this skill when a conjunction joins elements that look parallel but are grammatically or logically mismatched — different parts of speech, different clause types, or different levels of abstraction yoked together as though they were equivalent.

Source concept: Unequal yokefellows are elements joined by "and" or a similar conjunction as though they were grammatical equals when they are not — a noun and a clause, a gerund and an infinitive, an adjective and a noun phrase — the conjunction flattering them with a parallelism they cannot honestly claim. (Fowler & Fowler, *The King's English*, 1908)

## Rules

- **The parallel-slot test**: replace each conjoined element individually as the sole occupant of its syntactic slot. If every element can stand alone in that slot in the same grammatical form, they are genuine yokefellows. If any element requires the sentence to be restructured to stand alone there, the elements are unequal.
- **Type 1 — noun + clause**: *"The agenda covered budgets, staffing, and what we planned for the fourth quarter."* The first two elements are nouns; the third is a clause. Repair: all nouns (*"budgets, staffing, and Q4 plans"*) or all clauses (*"what the budget showed, what staffing required, and what we planned for Q4"*).
- **Type 2 — adjective + noun phrase**: *"She was patient, methodical, and a natural teacher."* Two adjectives and a noun phrase. Repair: all adjectives (*"patient, methodical, and gifted as a teacher"*) or restructure (*"She was patient and methodical, and a natural teacher"*).
- **Type 3 — gerund + infinitive**: *"He enjoyed hiking and to run in the mornings."* Gerund and infinitive as joint object. Repair: *"He enjoyed hiking and running"* or *"He liked to hike and to run."*
- **Type 4 — active + passive clause**: *"The team prepared the brief and the contract was approved."* One active clause, one passive. Repair: one voice throughout — *"The team prepared the brief and obtained approval of the contract."*
- **Type 5 — different logical levels**: coordinating a general claim with a specific instance, or an abstract principle with a concrete action, as though they were equivalent members of a list. Repair: use a subordinating conjunction (*"not only... but also"*, *"and, specifically,"*) or break into separate sentences to make the relationship explicit.

## Review Shape

Use the preserve shape for strong models:

```
Principle:
<english-unequal-yokefellows: one sentence naming the concept>

Preserve:
<supplied passage>

Why:
<apply the parallel-slot test to every conjoined structure: confirm that each element occupies the same grammatical slot in the same grammatical form>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Use the repair shape for weak passages:

```
Principle:
<english-unequal-yokefellows: one sentence naming the concept>

Weak:
<passage containing unequal yokefellows>

Fault:
<identify the conjunction; name the unequal elements by type (noun/clause, adjective/noun phrase, gerund/infinitive, active/passive, or different logical levels); apply the parallel-slot test>

Better:
<revised passage with all conjoined elements made genuinely parallel>

Why:
<name the grammatical form chosen for the repaired parallel and confirm all elements now occupy the same syntactic slot>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Start `Principle` with the exact skill name `english-unequal-yokefellows`.

## Objective Rubric

- Every pair or series joined by *and, or, but,* or *nor* consists of elements in the same grammatical form (all nouns, all infinitives, all gerunds, all adjectives, all clauses).
- No element in a conjoined series requires the sentence to be restructured to stand alone in its syntactic slot.
- No active and passive clauses are joined as coordinate equals.
- Where elements of genuinely different logical levels were conjoined, the revision makes the relationship between them explicit through subordination or separate sentences.

Pass only when every applicable check passes.

## Source Boundary

Examples may be drawn from public-domain English prose (pre-1928) or invented passages clearly labeled as such. Fowler & Fowler, *The King's English* (1908) is in the public domain. Do not invent quotations attributed to named authors. Note: for false-scent sentences where misleading parallel structure causes re-reading, see `english-false-scent`.
