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

### Victoria (hero, only woman's face)

- Slides **1 (hook)** and **9 (CTA)** in-scene (no sticker halo)
- Face lock: **`carusel-memory/references/виктория.png`** only
  (box: `/workspace/cover-refs/виктория.png`)
- One woman, twelve angles of ONE person. Not 12 people.
- Eyes: green with a slight hazel-brown tint (зелёные с лёгким карим)
- Hair: warm honey / wheat blonde with darker roots **as on виктория.png**. Never lighten.
- Platinum / white-blonde / Alena / studio-blazer = FAIL. Vika = `виктория.png` only.
- **Clothes and pose MUST change** every carousel. Do not copy the reference outfit
  (white cami) or a frozen reference pose. Slide 1 vs 9 may differ; same woman.
- No other women's faces. No doubles. Portuguese models are `do_not_borrow`

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
- Hook: large scene line + Victoria + one animal
- Internal: 50–60% type, smaller subject at bottom or side
- CTA: Victoria + huge magenta script trigger word
- Safe area ≥10–12% from edges if generated as a 3×3 master

## Reference roles

| File | Role |
|------|------|
| `image-851e.png` / `animals-viktoria-style-lock.png` | style + layout + palette — never i2i as a face |
| `виктория.png` | ONLY face + hair lock (one woman, 12 angles) |
| Alena (`victoria.png` / `alena.png`) | DELETED. Never i2i. |
| `cover-old.png` / studio-blazer | RETIRED |
| `slide-04.png` | meaning depth only, not the visual family |

`preserve`: dark field, magenta + white type mix, torn-paper pills, animals-as-metaphor, Victoria on 1+9, seam slice.
`change`: topic objects, exact copy, which animal on which slide.
`do_not_borrow`: Portuguese text, foreign faces, other brands, horror table.
