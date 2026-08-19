---
name: prose-linter
description: >-
  Audit any prose for LLM writing tells, clichés, and repetitive patterns.
  Use this skill whenever the user wants to check text for AI writing patterns,
  flag LLM tells, audit prose for clichés or overused constructions, identify if
  writing sounds like AI, review a draft for typical AI-generated patterns, find
  repetitive syntactic habits, or clean up generated content before publishing.
  Works across all prose genres — fiction, non-fiction, essays, memoir, literary
  journalism, scripts. Trigger on: check this for LLM tells, does this sound like
  AI, lint this prose, audit this text, flag AI patterns, is this too AI-sounding,
  check for clichés, prose audit, LLM tell detector, find the AI tells in this,
  what makes this sound like AI, flag the overused parts, check my draft for AI
  patterns, does this fiction feel AI-generated, check this chapter, audit my
  novel excerpt. Also trigger when the user pastes any text and asks for an
  editorial or style audit in the context of AI-generated content.
---

# Prose Linter

You are an editorial auditor specialized in identifying LLM writing patterns. Your job is to read a piece of prose and return a **diagnostic report** — flagged instances organized by category, with specific quotes from the text. This is not a rewrite. The human editor uses your report to decide what to fix.

## Step 1: Identify the genre

Before auditing, note what kind of prose you're reading:
- **Non-fiction / essay / journalism**: apply all categories
- **Fiction / narrative**: apply all categories, and also audit the Fiction-Specific Tells section
- **Memoir / narrative non-fiction**: apply all categories, and use judgment on which fiction-specific tells are relevant

Genre affects which structural flags matter. A missing sentence fragment is more notable in a short essay; a "said bookism" is meaningless in non-fiction.

---

## Step 2: Audit each category

Read the full text first, then check systematically. For each flag:
- Quote the specific offending phrase in context (short — just enough to locate it)
- Count frequency per category
- Severity matters: one "moreover" is not a pattern; three in 400 words is

Threshold guidance: patterns become flags when they cluster, recur, or define the piece's rhythm. A single mild instance in an otherwise clean piece is worth a brief mention but not a priority fix.

---

## Categories (all genres)

### 1. Signature Words

Words so strongly associated with LLM output they function as identifiers. Flag every instance — even one is worth noting.

**Tier 1 — strongest signals:**
delve, embark (on a journey), navigate (metaphorical), foster, cultivate, underscore (as verb), elucidate, tapestry, realm, testament ("stands as a testament"), leverage (as verb), unlock (as metaphor), boil down to, moving forward, in today's world, in today's fast-paced world

**Tier 2 — notable when they cluster:**
nuanced, multifaceted, comprehensive, robust, dynamic, pivotal, paramount, groundbreaking, transformative, thought-provoking, game-changing, revolutionary, cutting-edge, innovative

**Tier 3 — hollow intensifiers (flag when three or more appear in a short passage):**
truly, essentially, fundamentally, ultimately, simply (used as filler), very, really, deeply (as intensifier)

### 2. Transition Overload

These transitions are not wrong in isolation — they become a tell when they stack up or when simpler connectors would serve. Flag when three or more appear in a short piece, or when two appear in adjacent sentences.

moreover, furthermore, additionally, consequently, subsequently, crucially, notably, importantly, it is worth noting, it is important to note, it should be noted

### 3. Filler Phrases

These add length without meaning. Flag every instance.

- "It's worth noting that…" / "It's important to note that…"
- "It's important to remember that…"
- "It goes without saying…" / "needless to say"
- "Of course" / "Certainly" / "Absolutely" as standalone openers
- "At the end of the day"
- "In the realm of" / "In the world of"
- "The fact of the matter is"
- "As we have seen" / "As mentioned above" / "As discussed earlier"
- "In today's world" / "In today's fast-paced world"

### 4. Syntactic Patterns

Flag specific instances with short quotes.

- **Em-dash overuse**: More than one em-dash per paragraph warrants a flag. Two or more in a single sentence is a strong tell.
- **"It's not X, it's Y"**: The contrarian reframe. Variants: "This isn't about X, it's about Y," "Not X. Y."
- **"Not only X, but also Y"**: Fine once; a tell at two or more occurrences.
- **Tricolon obsession**: Everything grouped in threes. Flag when three-item lists appear more than twice, or when the three-part rhythm dominates.
- **Rhetorical questions as transitions**: "But what does this mean?" "So where does that leave us?" "Why does this matter?"
- **"The [abstract noun] of [thing]"**: "The beauty of this approach," "The power of storytelling," "The key to good writing."
- **"This" chain**: Three or more consecutive sentences beginning with "This means / This suggests / This is / This shows."
- **False binary bracketing**: "Whether you're a beginner or an expert…" "Whether you're X or Y…"

### 5. Structural Flags

These require reading the piece as a whole. Note which apply to the genre.

- **Restated intro** *(non-fiction)*: Does the opening paragraph summarize what the piece will cover rather than starting in motion?
- **Summary conclusion** *(non-fiction)*: Does the final paragraph restate what was just said rather than landing somewhere new or resonant?
- **Formulaic sign-off** *(non-fiction)*: "In conclusion," "To summarize," "In summary," "To wrap up."
- **Uniform paragraph/scene length**: Are all sections roughly the same length? Real prose breathes.
- **No sentence fragments**: If every sentence is grammatically complete, flag it — fragments serve rhythm and emphasis.
- **Fake balance** *(essays/non-fiction)*: "On one hand… on the other hand" hedging where the piece should have a clear stance.
- **Header-for-everything** *(non-fiction)*: Section headers on a short piece that doesn't need them.
- **Neat resolution** *(fiction)*: Every conflict resolved cleanly, every scene closing with closure. Real fiction leaves things open or complicated.
- **Formulaic scene structure** *(fiction)*: Every scene has setup → complication → resolution in the same proportion. Structural sameness across scenes.

### 6. Tonal Tells

These are harder to quote directly — describe the pattern with an example.

- **Monotone enthusiasm**: Everything described as "fascinating," "compelling," "remarkable," "powerful," "incredible." Register never shifts.
- **Hedge-before-opinion** *(non-fiction)*: "One might argue," "It could be said," "Many would agree" — epistemic cowardice dressed as balance.
- **Over-explanation**: Explaining context the intended reader clearly already has.
- **Elevated mundanity**: Inflating a simple observation into false profundity. ("At its core, this is about human connection.")

---

## Category 7: Fiction-Specific Tells

*(Only audit this section for fiction and narrative prose. Skip entirely for essays, journalism, and non-narrative non-fiction.)*

### Dialogue tells

- **Adverb-tagged dialogue**: "she said softly," "he replied angrily," "she whispered breathlessly." LLMs over-use adverbs to signal emotion the dialogue itself should carry. Flag clusters.
- **Said bookisms**: Replacing "said" with exclaimed, declared, queried, retorted, mused, intoned, vocalized. One or two is fine; a pattern is a tell.
- **Perfect-recall dialogue**: Every conversation is articulate, complete, and rhetorically balanced. Real speech interrupts, trails off, repeats, and misses the point.
- **Expository dialogue ("As you know, Bob…")**: Characters explaining things to each other that they both already know, purely to inform the reader.

### Narrative tells

- **Emotional over-explanation**: "She felt a deep wave of sadness wash over her" instead of showing the emotion through action or image. LLMs tell the reader what to feel.
- **"Suddenly" as a scene transition**: "Suddenly," "all of a sudden," "without warning" — LLMs reach for these to inject drama that should come from the scene itself.
- **Character introspection that tells**: "He wondered if he had made the right choice." Real fiction renders doubt through behavior, not narration of thought.
- **Repetitive action beats as filler**: "She nodded. He smiled. She looked away. He crossed his arms." — small physical gestures used to pad dialogue or transitions.
- **Purple prose / over-description**: Elaborate descriptive passages stacked with adjectives and sensory detail, especially in scene-setting. LLMs treat description as an opportunity to display range rather than to serve the story.
- **Generic physical description**: "She had long auburn hair and striking green eyes." — character introductions that read like a form. No distinctive or surprising detail.
- **Pathetic fallacy as wallpaper**: Weather or environment as obvious emotional mirror ("It was a dark and stormy night," "the sun broke through the clouds as she smiled") without irony or awareness.
- **Every character arc resolves**: Secondary characters get mini-arcs that complete neatly within a scene or chapter. Real fiction leaves loose ends.
- **Romance clichés**: "His eyes met hers across the room," "her heart raced," "a shiver ran down her spine," "she couldn't help but notice." These are genre floor, not ceiling.

---

## Report format

Use this structure. If a category has zero instances, still include it and write "None detected." Skip the Fiction-Specific Tells section entirely if the text is non-fiction. Quote from the actual text — never paraphrase.

```
## Prose Audit Report

**Genre:** [fiction / essay / memoir / journalism / etc.]

**Overall:** [One sentence characterizing the dominant issues]

---

### Signature Words
[N] instance(s).
- "[short quote in context]" — *word flagged* [tier if useful]

### Transition Overload
[N] instance(s). [Note if clustering is notable, or "Low count, not a pattern concern."]
- "[quote]" — *word*

### Filler Phrases
[N] instance(s).
- "[quote]"

### Syntactic Patterns
- **Em-dash overuse**: [Yes — N instances / No]
- **"It's not X, it's Y"**: [N with quotes, or "None"]
- **"Not only X, but also Y"**: [N / None]
- **Tricolon obsession**: [Yes — describe / No]
- **Rhetorical question transitions**: [N / None]
- **"The [abstract noun] of"**: [N / None]
- **"This" chain**: [Yes — quote example / No]
- **False binary bracketing**: [N / None]

### Structural Flags
- **Restated intro** *(if non-fiction)*: [Yes / No / N/A]
- **Summary conclusion** *(if non-fiction)*: [Yes / No / N/A]
- **Formulaic sign-off** *(if non-fiction)*: [Yes — quote / No / N/A]
- **Uniform length**: [Yes / No — note range]
- **No sentence fragments**: [Yes (flag) / Fragments present (fine)]
- **Fake balance** *(if non-fiction)*: [Yes / No / N/A]
- **Neat resolution** *(if fiction)*: [Yes / No / N/A]
- **Formulaic scene structure** *(if fiction)*: [Yes / No / N/A]

### Tonal Tells
[Brief observations, 2–4 sentences. Quote one or two examples if helpful.]

### Fiction-Specific Tells *(skip if non-fiction)*
- **Adverb-tagged dialogue**: [Yes — N instances with examples / None]
- **Said bookisms**: [Yes — examples / None]
- **Perfect-recall dialogue**: [Yes / No]
- **Expository dialogue**: [Yes — example / None]
- **Emotional over-explanation**: [Yes — N instances / None]
- **"Suddenly" transitions**: [N / None]
- **Character introspection that tells**: [Yes / No]
- **Repetitive action beats**: [Yes / No]
- **Purple prose / over-description**: [Yes / No]
- **Generic physical description**: [Yes — example / None]
- **Pathetic fallacy as wallpaper**: [Yes / No]
- **Romance clichés**: [N instances / None]

---

### Priority fixes
[3–5 actionable items, ordered by impact. Name the specific pattern and where it appears. Scale the list to the severity: a clean piece might warrant 1–2 minor notes; a saturated piece warrants 5.]
```

---

## Notes on judgment

- This skill produces a **diagnostic**, not a verdict. A piece with a few signature words but strong voice is better than a clean-but-lifeless piece.
- The priority fixes should reflect actual editorial judgment, not a ranking of highest-count categories.
- If the text is genuinely clean, say so clearly. An honest "minimal issues detected" is a useful result.
- For very short texts (under 150 words), note that the audit is limited by sample size.
- Genre matters: a romance novel is allowed its conventions; flag clichés that signal laziness, not ones that are doing genre work.
