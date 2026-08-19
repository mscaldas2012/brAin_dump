---
name: prose-argument-integrity
description: Diagnose structural failures in argumentative prose — not sentence-level logic but the connective tissue between claims: missing warrants, evidence that doesn't support its claim, claims that contradict each other, conclusions stronger than the premises allow. Extracts a logical spine (thesis, claim sequence, evidence links) and maps the warrant between each adjacent claim pair. Five named faults: unjustified leap, evidence mismatch, contradiction, circular warrant, scope drift. For long texts uses chapter-level claim summaries. Genre scope: argumentative and opinion prose only — skip for narrative, memoir, or purely descriptive writing. Source: Aristotle Rhetoric and Sophistical Refutations, Fowler & Fowler The King's English (1908).
---

# Prose Argument Integrity

Use this skill when an argumentative piece feels unconvincing without the individual claims being obviously false — when the reasoning moves but doesn't carry weight, when evidence is present but doesn't seem to settle the question, when the conclusion seems to arrive from somewhere other than where the argument led. The fault is not in the claims themselves but in the connections between them.

**Genre scope:** This skill applies to argumentative prose — essays, opinion pieces, nonfiction arguments, analytical writing — where claims are advanced and supported. For narrative, memoir, or purely descriptive writing, skip this skill or apply it only to explicitly argumentative passages within such works.

**Minimum text unit:** Full text for Tier 1 (under 3,000 words) and Tier 2 (3,000–20,000 words). For Tier 3 (over 20,000 words): chapter-level claim summaries — for each chapter, state the central claim, the main evidence offered, and the chapter's contribution to the overall thesis. Run the warrant map on the chapter summaries rather than the full text.

Source concept: Aristotle defines the enthymeme as "a sort of syllogism starting from probabilities or signs" — the characteristic argument form of rhetoric, where one or more premises are left unstated because they are assumed to be shared by the audience. (*Rhetoric*, Book I Ch. 2.) The failure mode: when the unstated premise is not actually shared, or not actually true, the argument moves without landing. The reader nods at each step and arrives at the conclusion without being convinced — because somewhere in the chain, the step that should have been stated was left invisible. Fowler identifies precision as one of the five vocabulary virtues: the exact word excludes synonyms that do not match the intended sense. (*The King's English*, Chapter I, 1908.) Applied to argument: the exact claim excludes formulations that are technically similar but logically different. A claim stated imprecisely is a claim that can be supported and refuted simultaneously — which is no claim at all.

---

## Logical Spine Extraction

Before mapping warrants, extract the logical spine of the piece. This is not a summary — it is a map of the argument's structure, with each element in its logical (not necessarily textual) order.

**Thesis:** The main claim the piece is trying to establish. One sentence, compressed.

**Claim sequence:** The sub-claims that contribute to establishing the thesis, in the order they appear. Each claim in one sentence. For each claim, note the evidence offered:

```
Claim N: <one compressed sentence>
Evidence: <what is offered — quotation, example, statistic, analogy, authority — and what it directly shows>
```

**Conclusion:** The final statement of the thesis, as it appears at the close of the piece. This may be identical to the thesis, or it may be transformed — the thesis restated in a form made possible by the intervening argument.

**Warrant map:** For each adjacent pair (Claim N → Claim N+1), identify the warrant — the logical bridge that connects them. State what a reader must accept for Claim N+1 to follow from Claim N. Then assess the warrant's status:

- **Shared:** The warrant is so widely accepted that no reader would question it; it does not need to be stated.
- **Contextual:** The warrant has been established earlier in the piece; the reader already has it.
- **Contestable:** The warrant is not universally shared and has not been established in the piece; it needs to be stated and defended.
- **Missing:** No coherent warrant connects Claim N to Claim N+1; the logical bridge has not been built.
- **Circular:** The warrant already assumes the truth of the conclusion; the argument begs the question.

---

## Fault Taxonomy

Five named faults, drawn from the warrant map and evidence review.

### Fault 1 — Unjustified Leap
Claim B is asserted after Claim A without establishing the logical connection. The reader must supply the bridge. The warrant is Contestable or Missing — it is neither self-evident nor established in the piece — and the argument proceeds as if the connection were obvious.

*Test:* State Claim A and Claim B in compressed form. Ask: "Given that A is true, why must B be true?" State the warrant in one sentence. Is the warrant stated anywhere in the piece? Is it so widely accepted that any reader would grant it without hesitation? If neither: Fault 1.

*Distinction:* An unjustified leap is not a case of the argument being wrong — the warrant may be true. It is a case of the argument proceeding as if the warrant needs no defense, when it does. The repair is not to remove the claim but to state the warrant.

### Fault 2 — Evidence Mismatch
A piece of evidence is paired with a claim it does not directly support. The evidence may be accurate, relevant, and interesting, but its logical relationship to the claim requires an unstated intermediate step. The reader must work to see the connection.

*Test:* State the claim in compressed form. State what the evidence directly establishes — not what it suggests, implies, or is consistent with, but what it proves or makes probable. Are these the same? Or does getting from "what the evidence shows" to "what the claim asserts" require an additional warrant that the piece does not provide?

*Common form:* The evidence establishes a weaker version of the claim. The claim says X always; the evidence shows X in one case. The claim says X causes Y; the evidence shows X and Y are correlated. The evidence is consistent with the claim but does not establish it.

*Distinction:* For inductive arguments — where evidence makes a claim probable rather than certain — the standard is proportionality, not certainty. The fault applies when the evidence, even at its strongest inductive reading, does not make this claim more probable than competing claims. If the evidence makes a weaker version of the claim probable, state that version.

### Fault 3 — Contradiction
Two claims in the piece are logically inconsistent: they cannot both be true given the same premises. The piece asserts one thing in one section and something incompatible in another, without acknowledging the tension.

*Test:* State the two claims in compressed form. Is there a coherent set of conditions under which both are true? If not — if one entails the negation of the other, or if each depends on an assumption the other denies — they are in contradiction.

*Distinction:* A contradiction is not a case of emphasizing different aspects of a complex question. It is a case where one claim, if true, makes another claim false. The repair is not to pick one and abandon the other, but to identify whether a more nuanced position can contain both, or whether one must be given up.

*Note:* Contradictions in argumentative prose are often between an early methodological claim ("we cannot rely on our moral intuitions here") and a later substantive claim that implicitly relies on moral intuitions. The early claim restricts the argument; the later claim violates the restriction.

### Fault 4 — Circular Warrant
The argument offers as a warrant (the bridge between evidence and claim) something that already assumes the truth of the claim it is meant to support. The argument moves in a loop: Claim → Evidence → Warrant → Claim. Also: the evidence is true only if the claim is already true — the claim is doing the work the evidence was supposed to do.

*Test:* State the claim, the evidence, and the warrant. Does accepting the warrant require accepting the claim? If yes, the warrant is circular: the conclusion is doing the work of the premise.

*Common form:* An argument for ECP that treats certain passages as meaning eternal torment because the traditional interpretation says so — and then treats the traditional interpretation as evidence for ECP. The tradition and the interpretation are mutually supporting, but neither independently establishes the claim.

### Fault 5 — Scope Drift
The conclusion is stronger or weaker than the premises warrant. The evidence and argument establish a modest claim; the conclusion states a bolder one. Or the reverse: the argument has established a strong case, but the conclusion retreats to a hedged formulation that the preceding argument has already exceeded.

*Test (over-reach):* State the strongest claim the premises establish. State the conclusion. Is the conclusion stronger than the premises can support? If yes, the conclusion is over-reaching — it claims more than the argument proved.

*Test (under-reach):* State the strongest claim the premises establish. State the conclusion. Is the conclusion weaker than what the premises clearly support? If yes, the conclusion is retreating — the argument earned more than the writer claimed.

*Distinction:* Appropriate qualification — acknowledging uncertainty, noting where evidence is thin, using "suggests" rather than "proves" when evidence is inductive — is not scope drift. The fault applies when the qualification level of the conclusion does not match the qualification level of the argument: an argument that proved X definitely should not conclude "perhaps X."

---

## Long-Text Protocol (Tier 3 — over 20,000 words)

1. For each chapter, extract: thesis contribution (what this chapter establishes toward the book's main argument), central evidence, and how this claim connects to the preceding and following chapter.
2. Run the warrant map on the chapter-level contribution sequence.
3. Apply the five fault tests to the chapter-level spine.
4. Note that local evidence mismatches (within a chapter) are not visible at this level; the Tier 3 analysis catches structural argument faults (leaps between chapters, contradictions across chapters, overall scope) but not section-level evidence handling.

---

## Review Shape

```
Thesis:
<the main claim the piece is trying to establish — one compressed sentence>

Logical Spine:
Claim 1: <one sentence>
  Evidence: <what is offered and what it directly shows>
  Warrant to Claim 2: <the bridge — one sentence> | Status: [Shared / Contextual / Contestable / Missing / Circular]

Claim 2: <one sentence>
  Evidence: <what is offered and what it directly shows>
  Warrant to Claim 3: <the bridge> | Status: [...]

... (all claims)

Conclusion: <as stated — one sentence>
Thesis match: [the conclusion restates / transforms / over-reaches / under-reaches the thesis]

Faults:
1. [Fault type] at [Claim N → Claim N+1 / Evidence for Claim N / Claims N and M]: <description — state the warrant, the test applied, and the test result>
2. [Fault type] at [...]: <description>
...

Priority repair:
```

Apply the standard repair shape to the highest-priority fault:

```
Principle:
prose-argument-integrity: <one sentence naming the fault>

Weak:
<the passage containing the fault — the claim pair with missing warrant, the evidence-claim mismatch, or the contradicting claims, as they appear in the text>

Fault:
<state the claim(s), the warrant or evidence, and the test result — specifically: what must a reader accept for the argument to work that the piece does not give them?>

Better:
<the repair — for an unjustified leap: the warrant stated explicitly; for an evidence mismatch: the claim restated to match what the evidence shows, or additional evidence identified that would close the gap; for a contradiction: the tension acknowledged and resolved or contained; for circular warrant: an independent premise identified; for scope drift: the conclusion requalified to match the argument's reach>

Why:
<name what changed and confirm that a reader can now follow the step from one claim to the next without supplying anything the text does not provide>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Start `Principle` with the exact skill name `prose-argument-integrity`.

---

## Objective Rubric

- The logical spine is extracted before any fault diagnosis — thesis, all claims in sequence with their evidence, all warrants with their status, and the conclusion.
- Every warrant assessed as Contestable, Missing, or Circular is named as a fault.
- Every evidence-claim pair where the evidence does not directly establish the claim is named as a fault.
- Contradictions are named with both claims identified and their locations given.
- The scope of the conclusion is explicitly compared to the scope of the premises.
- The priority repair produces a passage where a reader can follow the logical step without supplying anything the piece does not give them.

Pass only when every applicable check passes.

## Source Boundary

Aristotle's *Rhetoric*, *Topics*, and *Sophistical Refutations* are public domain. Fowler & Fowler *The King's English* (1908) is public domain. Examples should be invented passages clearly labeled as such, or drawn from public-domain prose (pre-1928). Do not invent quotations attributed to named authors.
