---
name: english-wrong-turning
description: Identify and repair wrong-turning sentences — constructions that commit to a grammatical path in the opening which they cannot complete: dangling participials, abandoned constructions, misattached relative clauses, and mixed conditionals. Source: Fowler & Fowler, The King's English, 1908.
---

# English Wrong Turning

Use this skill when a sentence's grammatical opening commits to a construction that the sentence fails to complete — forcing an awkward recovery, a false grammatical agreement, or invisible repair work by the reader.

Source concept: A wrong turning occurs when a writer starts a sentence down a syntactic path, then finds they cannot reach the intended destination by that route — rather than reversing and beginning again, they patch over the inconsistency, leaving the grammatical promise of the opening unfulfilled. (Fowler & Fowler, *The King's English*, 1908)

## Rules

- **The grammatical-promise test**: identify what grammatical commitment the sentence's first phrase makes. Does the sentence keep it? If not, the sentence has taken a wrong turning. The test must be applied at the first clause boundary — the moment the opening phrase ends, a promise has been made.
- **Type 1 — dangling participial** (the most common wrong turning): an opening participial phrase implies a subject that does not become the main clause subject. *"Having decided to leave, the evening was declared over."* The participle "Having decided" implies a person who decided; the main clause subject is "the evening," which cannot have decided anything. Test: ask what the opening participle grammatically implies as its subject; check whether that subject is the main clause subject. Repair: make the implied subject the grammatical subject — *"Having decided to leave, they declared the evening over."*
- **Type 2 — abandoned construction**: the sentence begins with a structure it cannot complete. *"The reason why she resigned was because she felt ignored."* The construction *"the reason... was because"* conflates the reason (a statement) with a cause (a *because*-clause), treating the reason as though it were itself a further cause. Repair: *"The reason she resigned was that she felt ignored"* or *"She resigned because she felt ignored."*
- **Type 3 — misattached relative clause**: a *which-* or *who-* clause appears to modify the wrong noun. *"He handed the report to his manager which contained the final figures."* Does *which* modify "report" or "manager"? Repair: move the clause immediately after its intended referent — *"He handed his manager the report, which contained the final figures."*
- **Type 4 — mixed conditional**: a conditional sentence uses tenses that imply inconsistent modal relationships. *"If he were here today, he will tell you himself."* The past subjunctive (*were*) signals a hypothetical contrary-to-fact; *will* signals confident future. Repair: choose one — *"If he were here today, he would tell you himself"* (hypothetical) or *"If he is here today, he will tell you himself"* (open condition).

## Review Shape

Use the preserve shape for strong models:

```
Principle:
<english-wrong-turning: one sentence naming the concept>

Preserve:
<supplied passage>

Why:
<apply the grammatical-promise test to every opening participial phrase, relative clause, and conditional: confirm that each opening commits to a construction the sentence completes — identify any potential wrong turns and explain why each resolves correctly>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Use the repair shape for weak passages:

```
Principle:
<english-wrong-turning: one sentence naming the concept>

Weak:
<sentence containing a wrong turning>

Fault:
<identify the wrong-turning type (dangling participial / abandoned construction / misattached relative / mixed conditional); name the grammatical promise the opening makes and the point where the sentence fails to keep it>

Better:
<revised sentence that keeps the grammatical promise from the first phrase>

Why:
<name the specific repair: what was the implied subject, the correct construction form, or the consistent tense pattern?>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Start `Principle` with the exact skill name `english-wrong-turning`.

## Objective Rubric

- Every opening participial phrase has the correct grammatical subject as the subject of the main clause.
- No construction of the form *"the reason... was because"* remains; *that* or a restructured sentence is used instead.
- Every *which* or *who* clause immediately follows the noun it modifies with no intervening noun that could serve as an alternative referent.
- Every conditional sentence uses a consistent tense pattern: either past subjunctive + conditional (*were... would*) or present indicative + future (*is... will*), not a mixture of both.

Pass only when every applicable check passes.

## Source Boundary

Examples may be drawn from public-domain English prose (pre-1928) or invented passages clearly labeled as such. Fowler & Fowler, *The King's English* (1908) is in the public domain. Do not invent quotations attributed to named authors. Note: for false-scent constructions where the opening misleads without dangling, see `english-false-scent`; for unequal parallel structures, see `english-unequal-yokefellows`.
