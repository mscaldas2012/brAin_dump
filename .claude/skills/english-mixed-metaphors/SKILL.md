---
name: english-mixed-metaphors
description: Identify and repair mixed metaphors — two or more figures of speech in close proximity whose literal images are visually or logically incompatible, whether the individual figures are fresh, dying, or drawn from incompatible conceptual domains. Distinct from english-dying-metaphors, which addresses whether a single figure has worn out. Source: Fowler & Fowler, The King's English, 1908.
---

# English Mixed Metaphors

Use this skill when two or more figures of speech in the same sentence or adjacent sentences produce a visual collision — their literal images cannot coexist without absurdity.

Source concept: A mixed metaphor occurs when a writer, having started with one figure of speech, shifts to another that is incompatible with the first — the images, if taken literally together, would be visually or logically absurd. The mixing reveals that the writer has stopped seeing the images and is stringing verbal units together by habit. (Fowler & Fowler, *The King's English*, 1908)

## Rules

- **The literal-scene test**: take both (or all) metaphors in the sentence and place them together in a literal scene. Is the resulting image visually coherent? *"We need to iron out the teething troubles"* — a literal scene of ironing and teething is absurd. *"Burning the midnight oil and keeping our shoulders to the wheel"* — fire and heavy pushing in the same scene. If the scene is incoherent, the metaphors are mixed.
- **Type 1 — mixed dying metaphors** (most common): two worn-out phrases drawn from incompatible conceptual domains placed side by side. Each might pass alone; together they make the underlying images absurd. *"He grasped the nettle and bit the bullet"* — nettles and bullets in the same hand. Repair: use one (the stronger) or replace both with plain literal statement.
- **Type 2 — fresh mixed with dying**: one figure that still evokes a real image is contaminated by a dying metaphor from an incompatible domain. The dying metaphor pollutes the live one. Repair: remove the dying metaphor and complete the fresh figure, or replace both with plain statement.
- **Type 3 — domain collision**: two figures that are individually reasonable but come from mutually exclusive physical or conceptual domains — fire and water, growth and machinery, organic and mechanical. *"The roots of the company's engine"* — root systems and engines cannot share a scene. Repair: choose one domain and sustain it, or use plain statement.
- **Dead metaphors do not mix**: a fully dead metaphor — one entirely absorbed into ordinary language with no residual visual force (*the foot of a mountain, the arm of a chair, grasping an idea*) — cannot be mixed because it is no longer a figure. Do not diagnose collisions between dead metaphors. The test applies only to figures that still carry some visual or sensory suggestion.
- Distinguish from `english-dying-metaphors`: the dying-metaphors skill asks whether a single figure has worn out. This skill asks whether multiple figures are compatible with each other. A single fresh metaphor cannot be a mixed metaphor; a single dying metaphor is not a mixed metaphor. The mixed case requires at least two figures in collision.

## Review Shape

Use the preserve shape for strong models:

```
Principle:
<english-mixed-metaphors: one sentence naming the concept>

Preserve:
<supplied passage>

Why:
<apply the literal-scene test to every pair of figures in proximity: confirm they come from compatible domains and produce no absurd visual collision — or confirm that all figures in the passage are fully dead and therefore not in visual contact with each other>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Use the repair shape for weak passages:

```
Principle:
<english-mixed-metaphors: one sentence naming the concept>

Weak:
<sentence or passage containing mixed metaphors>

Fault:
<identify the colliding figures; apply the literal-scene test; name the incompatible domains (fire/water, growth/machinery, etc.); classify the type (dying+dying / fresh+dying / domain collision)>

Better:
<revised passage — one figure sustained consistently, or both replaced with plain literal statement>

Why:
<explain which figure was kept (and why it is the stronger or more relevant) or why plain statement serves better than either figure>

Rubric:
<at least two objective checks, each marked Pass or Fail>
```

Start `Principle` with the exact skill name `english-mixed-metaphors`.

## Objective Rubric

- Every pair of figures in the revision passes the literal-scene test: placed together in a literal scene, their images are coherent.
- No two figures from incompatible physical or conceptual domains (fire/water, growth/machinery, organic/mechanical) appear in the same sentence.
- Where both figures were dying, the revision uses either one figure or plain statement — not both.
- No fully dead metaphor has been flagged as mixed (dead metaphors carry no visual force and cannot produce a visual collision).

Pass only when every applicable check passes.

## Source Boundary

Examples may be drawn from public-domain English prose (pre-1928) or invented passages clearly labeled as such. Fowler & Fowler, *The King's English* (1908) is in the public domain. Do not invent quotations attributed to named authors. Note: for the question of whether a single figure retains visual power, see `english-dying-metaphors`.
