# Carusel Professional Playbook

Use this before writing research, copy, design, image prompts, motion prompts, or QA.

## 2026 Carousel Principles

- Slide 1 does one job: stop the scroll in ~2 seconds.
- Hook must create an information gap: relevance + tension + payoff.
- Each slide has one idea. If a slide needs two ideas, split it.
- 7-10 slides work well for educational/saveable content; Carusel default is **9 panels** in grid 3x3.
- Final slide asks for one action only. Prefer a save-worthy CTA over generic "follow".
- Design for saves: checklists, frameworks, before/after, mistakes, process, reference cards.
- Brand recognition beats variety: locked palette, type stack, spacing, image treatment.
- Use high contrast and thumbnail readability. The cover must work when small.

## 9-Panel Story Arc

```text
01 hook / pattern interrupt / motion-friendly
02 problem / why it matters
03 hidden cost / common mistake
04 mechanism / framework
05 proof / numbers / credibility
06 flow / step-by-step
07 save card A / checklist
08 save card B / decision rule / recap
09 CTA / save + follow + one-liner payoff
```

Row-major reading order:

```text
01 02 03
04 05 06
07 08 09
```

## Hook Frameworks

Generate at least 5 hooks before choosing one:

| Framework | Formula |
|-----------|---------|
| Pain | "Still doing X? That is why Y keeps happening" |
| Contrarian | "X is not the problem. Y is." |
| Specific result | "N steps / N checks before you do X" |
| Mistake | "The mistake that breaks X before Y" |
| Mechanism | "The hidden loop behind X" |
| Before/after | "Before: X. After: Y." |

Choose the hook with the strongest information gap and easiest thumbnail read.

## Reference-Based Design Replication

Never say only "in this style". Decompose the reference into:

- layout grid and reading order
- palette with hex guesses
- typography hierarchy (headline/body/badge/mono)
- image treatment (photo, cutout, 3D, flat, grain, blur)
- composition archetypes per panel
- spacing/margins/gutters
- brand marks and recurring motifs
- what must NOT be copied literally

Use the preserve/change/do-not-borrow structure:

```text
Reference role: style + layout reference.
Preserve: palette, grid, hierarchy, spacing, brand rhythm, contrast.
Change: topic, characters, icons, copy, domain metaphors.
Do not borrow: original logo, people, mascot, institution name, accidental text.
Output: 3x3 grid master, 9 panels, panel 1 motion-safe.
```

## Image Prompt Anatomy

Every Kie image prompt must contain these blocks:

1. **Reference role** - why the input image exists.
2. **Output format** - grid 3x3, aspect, resolution, row-major order.
3. **Style lock** - palette, typography style, spacing, panel archetypes.
4. **Preserve** - exact design traits to carry over.
5. **Change** - new topic and visual metaphors.
6. **Panel plan** - panel 1..9 with exact headline + visual zones.
7. **Typography rules** - quoted text, hierarchy, placement, no extra words.
8. **Negative constraints** - wrong grid, wrong count, extra text, watermark, drift.

Typography rules:

- Put exact text in quotes.
- State "verbatim text, no substitutions, no extra labels".
- Describe text zone, hierarchy, color, and alignment.
- Avoid dense body text in generated image. Prefer short headings + pills.

## Motion Prompt Anatomy

Slide 1 motion must preserve readability:

- headline, CTA, logos, and small text stay static
- animate background, glow, particles, parallax, screen light, subtle object drift
- no scene change, no new objects, no camera whip, no text morph
- first and last frames should match
- 5 seconds, calm loop, not a trailer

## QA Gates

P0 blockers:

- wrong number of panels
- wrong grid order
- unreadable hook
- style does not resemble reference
- random extra text/logos
- slide 9 CTA missing
- file1/video missing before publish
- publish would retry an already-started MCP call

Warnings:

- mixed aspect/size across publish assets
- minor copy paraphrase
- weak save card
- inconsistent icon style

## Research Sources Used

- 2026 carousel best practice synthesis: hooks create information gap, 7-10 slides, saves as primary value metric.
- Reference image prompting synthesis: assign reference roles, separate preserve/change/do-not-borrow, use explicit output format.
- Typography-heavy prompt synthesis: quoted exact text, spatial zones, hierarchy ratios, negative constraints.
