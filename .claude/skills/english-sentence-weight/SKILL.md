---
name: english-sentence-weight
description: Identify and reduce front-heavy sentences where a long or complex grammatical subject depletes the reader's attention before the main verb arrives. Source: Spencer, The Philosophy of Style, 1852.
---

# English Sentence Weight

Use this skill when sentences carry long, abstract, or heavily modified subjects that force the reader to process extensive qualification before the predicate — the part where the action and meaning live — finally appears.

Source concept: The grammatical subject occupies the reader's attention from the first word until the predicate arrives; a long or complex subject exhausts this attention before any meaning is delivered. Economy of attention requires keeping subjects short and direct so the reader's full mental energy is reserved for the predicate. (Spencer, *The Philosophy of Style*, 1852)

## Rules

- **The attention-threshold test**: count the words between the sentence's opening and its main verb. If this count exceeds approximately ten words and the subject is abstract or heavily modified, the sentence is front-heavy. The reader's attention is depleted before anything happens.
- **Heavy subject patterns**: (a) a long abstract nominal phrase as subject — *"The committee's recommendation to defer the project pending further budget review was accepted"*; (b) an embedded relative clause in subject position — *"The argument that had been advanced by the committee and was endorsed by most board members was rejected"*; (c) a stack of pre-nominal modifiers — *"A carefully worded, extensively annotated, much-revised statement of intent was issued."*
- **The split-off test**: can the content embedded in the subject be moved to the predicate or separated into its own sentence? *"The committee's recommendation to defer the project pending further review was accepted"* → *"The committee recommended deferring the project, pending further review. The board accepted."* If splitting produces two cleaner sentences, the original was front-heavy.
- **Restructure to a short subject**: convert complex nominal subjects to short nouns or pronouns and move the heavy content to the predicate or a following sentence. *"A careful examination of the evidence is needed"* → *"We need to examine the evidence carefully"* or *"The evidence needs careful examination."*
- Distinguish from `english-wens`: a wen is a disproportionately swollen sentence part anywhere in the sentence. Sentence weight is specifically the subject-position problem — the reader cannot reach the verb without first processing an over-long opening. A wen can appear mid-sentence or at the end; sentence weight always concerns the opening.

## Review Shape

Use the preserve shape for strong models:

```
Principle:
<english-sentence-weight: one sentence naming the concept>

Preserve:
<supplied passage>

Why:
<confirm that subjects are short and direct — count the words before the main verb in each sentence and confirm none are front-heavy — or explain why a longer subject is justified>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Use the repair shape for heavy passages:

```
Principle:
<english-sentence-weight: one sentence naming the concept>

Weak:
<sentence with a front-heavy subject>

Fault:
<count the words before the main verb; identify the heavy-subject pattern (abstract nominal / embedded relative / stacked modifiers); apply the split-off test>

Better:
<revised sentence(s) with a shorter subject, complex content moved to the predicate or extracted to a separate sentence>

Why:
<confirm the reader now reaches the main verb without first processing extensive qualification>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Start `Principle` with the exact skill name `english-sentence-weight`.

## Objective Rubric

- No sentence in the revision has more than approximately ten words before its main verb unless the subject is concrete and simple.
- No abstract nominal phrase serves as subject where a short noun, pronoun, or restructured sentence would serve.
- Every main verb is reachable from the sentence's opening without passing through an embedded relative clause or a stack of pre-nominal modifiers.
- No meaning has been lost by splitting or restructuring the heavy subject.

Pass only when every applicable check passes.

## Source Boundary

Spencer's *The Philosophy of Style* (1852) is in the public domain. Examples should be drawn from public-domain English prose (pre-1928) or invented passages clearly labeled as such. Do not invent quotations attributed to named authors. Note: for disproportionately swollen sentence parts in general, see `english-wens`; for key words not in end position, see `english-end-emphasis`.
