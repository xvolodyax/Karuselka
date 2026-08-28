# Victoria face pixel gate

Vladimir 28.08.2026: prose «honey/wheat» is not a face check.
Gate PASS / Guardian DESIGN OK **cannot** override a human who says the woman is not Vika.

## Lock

- Only face: `carusel-memory/references/victoria-sheet.png`
- i2i: crop the **left frontal close-up** (`victoria-sheet-front.png`), upload as `victoria-sheet.png`
- Box copy: `/workspace/cover-refs/victoria-sheet.png` (same official sheet)
- `cover-refs/victoria.png` = **Alena**. Never i2i that file.

## Why the 28.08 pack drifted

Two bugs:

1. Active Kie `prompt` was 3631 chars about collage, cats, type, wardrobe. Face was a one-liner. A long essay starves identity.
2. i2i of the **full 12-up contact sheet** averaged Vika into a generic older stock blonde, often with **brown/grey eyes**.

**Fix:** short prompt, face first. Upload **one** close-up cut from that same sheet. Do not invent a new reference. Do not copy white cami / jeans / pose / jewelry.

## Eyes

Same as Excalibur article covers: **green + slight hazel / light-brown mix**.
Brown or grey = **FAIL face-gate, rebuild the whole canvas**.

## Before DESIGN OK

1. `python3 scripts/make_face_check_crops.py --pack <pack>`
2. Write `FACE_CHECK.md` in the pack. Compare **pixels**, not hair adjectives.
3. Verdict `MATCH` only if eyes (green+hazel), bone, age, and hair pattern are the same woman.
4. Wrong face or wrong eyes on **one** cell → rebuild the **whole** canvas.

`python3 scripts/face_gate.py --pack <pack>` must PASS.
`canon_gate.py` calls this for new packs with real pixels (not live 27.08 legacy).
