# Visual family: `animals_viktoria_collage`

Default family for every ТАРО СЕЙЧАС / Today Tarot daily carousel.
Slug must appear in `CAROUSEL_SERIES_CONCEPT.json` → `carousel_family`.

## Palette

| Role | Hex | Use |
|------|-----|-----|
| background | `#111111`–`#1a1a1a` charcoal / matte black | full-bleed |
| accent | `#ff006e` hot magenta | script, pills, tape, lips |
| type | `#ffffff` | heavy sans headlines |
| metal | soft gold | medallion, buttons, light foil |

No pastel rainbow. No beige lifestyle wash. No horror red/black candle table.

## Typography

- **Heavy sans, white** — primary keywords, scene, numbers
- **Thin script / handwritten, magenta** — secondary word («или конец?», Pause)
- Layer type behind and in front of subjects in the scene
- Magenta torn-tape / pill blocks for short labels
- Hook readable in 2 seconds at thumbnail size
- Verbatim copy from `CAROUSEL_SLIDE_COPY.json`. No extra labels, no watermarks, no Victoria signature

## Subjects

### No host portrait

- Slides have **no presenter**. Do not draw Vika. Do not i2i `Виктория.png`.
- Hook (1) and CTA (9) = scene + type + animal / object. Not a woman.
- GATE FAIL if Vika's face or any recognizable host portrait is on a slide.
- Do not FACE MATCH «похожа на Виктория.png».
- `viktoriaref.png`, `victoria-sheet.png`, `victoria.png` stay deleted. Never i2i.
- No women's faces. No doubles. Portuguese models are `do_not_borrow`.

### Animals (metaphor, not meme)

Use the animal as the emotion of the slide:

| Animal | Meaning | Typical slides |
|--------|---------|----------------|
| Cat | «чуешь» / you sense it | hook, intuition |
| Dog | loyalty to the unanswered question | pain / mistake / waiting |
| Owl | night thoughts, worst-case loop | mechanism or says/hears |

Minimum **3** slides with an animal used as metaphor.
Cute random pets without a job = FAIL.

### Decor

- Sunglasses, coffee cup, magenta lips, gold medallion — fashion-lifestyle, sparingly
- Light tarot card OK if it does **not** cover the headline
- Optional gold medallion logo ТАРО / СЕЙЧАС if it sits natively
- No skulls, blood, horror, dripping candles, ouija, demon faces

## Layout (9 × 3:4)

- Instagram portrait 3:4 each. Not 4:5 mixed, not 1:1 publish assets
- Hook: large scene line + one animal / object (no host)
- Internal: 50–60% type, smaller subject at bottom or side
- CTA: huge magenta script trigger word + object / animal (no host)
- Safe area ≥10–12% from edges if generated as a 3×3 master

## Reference roles

| File | Role |
|------|------|
| `image-851e.png` / `animals-viktoria-style-lock.png` | style + layout + palette — never i2i as a face |
| `Виктория.png` | NOT used by carousel generation |
| Alena (`victoria.png` / `alena.png` / `victoria_ref.jpg`) | DELETED / forbidden. Never i2i. |
| `viktoriaref.png` / `victoria-sheet.png` | DELETED. Never restore. |
| `cover-old.png` / studio-blazer | RETIRED |
| `slide-04.png` | meaning depth only, not the visual family |

`preserve`: dark field, magenta + white type mix, torn-paper pills, animals-as-metaphor, seam slice, no host portrait.
`change`: topic objects, exact copy, which animal on which slide.
`do_not_borrow`: Portuguese text, foreign faces, other brands, horror table.
