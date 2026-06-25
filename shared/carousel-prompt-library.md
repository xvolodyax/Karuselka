# Carusel Prompt Library

Use these templates inside agent skills. Prompts are written as production briefs, not decorative descriptions.

## 1. Research Prompt

```text
Ты — strategist for Instagram educational carousels.
Topic: {topic}
Audience: {audience}
Goal: saves, shares, profile trust.
Format: 9-panel grid 3x3, row-major.

Deliver:
1. 5-7 hook angles using frameworks: pain, contrarian, mistake, mechanism, specific result, before/after.
2. Audience pains and language.
3. Save-worthy promise: why this carousel deserves a bookmark.
4. 9-panel story arc: 01 hook, 02 problem, 03 hidden cost, 04 mechanism, 05 proof, 06 flow, 07 checklist, 08 recap/rule, 09 CTA.
5. Design translation notes from reference: preserve / change / do_not_borrow.
6. Prompt risks: text rendering, wrong panel count, style drift, extra logos.
```

## 2. Hook Lab Prompt

```text
Generate 7 hooks for {topic}.
Each hook must:
- be readable in <2 seconds
- create an information gap
- promise a concrete payoff
- avoid generic "tips for..."
- fit one panel headline

Return:
framework, headline, why_it_swipes, risk, score/10.
Pick the best hook and explain why.
```

## 3. Copywriter Prompt

```text
Write a 9-panel Instagram carousel in Russian.
Topic: {topic}
Top hook: {selected_hook}
Audience: {audience}
Tone: direct, useful, not hype.
Format: grid 3x3, row-major.

Rules:
- One idea per panel.
- Slide 1 is hook only, motion-friendly.
- Slides 7-8 must be save-worthy.
- Slide 9 has one CTA.
- Headline max 45-50 chars; body max 1-2 short lines.

Return JSON:
hook_options[], hook_rationale, slide_count=9, grid, slides[1..9], save_value[], caption.
```

## 4. Reference Decomposition Prompt

```text
Analyze the reference design as a professional art director.

Output:
reference_role:
  style:
  layout:
  typography:
  mood:

preserve:
- grid and reading order
- palette
- type hierarchy
- spacing/gutters
- panel archetypes
- recurring marks/motifs

change:
- topic
- characters/icons
- copy
- CTA
- domain metaphors

do_not_borrow:
- original logo/brand
- people/mascot
- accidental text
- institution names

panel_archetype_map:
01 -> ...
...
09 -> ...
```

## 5. Kie Image Prompt

```text
Reference role: use input image as style + layout reference.
Preserve: {palette}, {grid}, {type hierarchy}, {spacing}, {panel archetypes}, {contrast}.
Change: adapt content to {topic}; replace original subjects with {new metaphors}.
Do not borrow: original logo, brand name, people, mascot, accidental text.

Output:
One Instagram carousel master image, grid 3 columns x 3 rows, 9 equal panels.
Aspect ratio: 3:4.
Resolution: 4K.
Row-major order: 01 02 03 / 04 05 06 / 07 08 09.

Typography:
Render exact quoted text only.
Verbatim text; no substitutions; no extra labels; no duplicate text.
Headline > short body > pill hierarchy.
High contrast, generous margins, no text crossing gutters.
Keep all text and pills 10–12% away from every grid line and cell edge.

Panels:
01: exact headline "{headline_01}", visual zones...
...
09: exact headline "{headline_09}", exact CTA "{cta}", visual zones...

Negative:
wrong number of panels, 2x3 grid, horizontal strip, random text, watermark, original logo,
style drift, clutter, unreadable Cyrillic, duplicate labels, cropped text.
```

## 6. Motion Prompt

```text
Сохрани исходный slide-01 один в один: композиция, стиль, цвета, текст, логотипы.
5 секунд, seamless loop, первый и последний кадр совпадают.

Двигать только:
- мягкий дрейф фона
- glow экранов/света
- лёгкий parallax декоративных элементов
- subtle particles/shimmer

Не двигать:
- headline
- body text
- numbers/pills
- logos/wordmark

Запреты:
без новых объектов, без смены сцены, без morph текста, без glitch текста,
без camera whip, без hard cuts, без искажения лиц.
```

## 7. Design Guardian Prompt

```text
Review carousel as a strict design guardian.

Check:
1. 9 panels exist, row-major grid.
2. Reference fidelity: preserve/change/do_not_borrow followed.
3. Slide 1 hook readable in <2 seconds.
4. Typography exact enough; no random labels.
5. Brand consistency: palette, type, spacing, image treatment.
6. Slides 7-8 are save-worthy.
7. Slide 9 has one CTA.
8. Video slide 1 keeps text static and loop clean.

Output: score, P0 blockers, warnings, per-slide notes, publish verdict.
```
