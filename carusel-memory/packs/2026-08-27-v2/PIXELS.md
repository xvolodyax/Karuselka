# PIXELS

## Face lock (ONLY)

`carusel-memory/references/victoria-sheet.png` — appearance card confirmed by Vladimir.
Box path if present: `/workspace/cover-refs/victoria-sheet.png`.

**NOT Victoria:** `/workspace/cover-refs/victoria.png` (Alena). Do not upload. Do not i2i.

Eyes: green with a slight hazel mix. Hair: warm honey/wheat + darker roots as on the sheet. No platinum.
Clothes/pose: **new every carousel**. Do not copy the sheet outfit (white cami + jeans) or the old ivory studio blazer.

## How to render (Kie i2i)

```bash
python3 scripts/kie_render_pack.py --pack carusel-memory/packs/2026-08-27-v2
```

Uploads the SHEET + style lock, runs `gpt-image-2-image-to-image` 3×3 @ 4K for RU then EN, writes 18 PNGs. Does **not** publish.

Copy stays the existing Пауза / PAUSE teaching arc.

## Current pixels in this checkout

Older GenerateImage slides (studio-blazer stand-in) may still sit under `{ru,en}/slides/` until the sheet binary lands on this VM and Kie is run. Gate **FAIL**s while `victoria-sheet.png` is missing or Alena/platinum/sheet-clothes appear in prompts.

Do **not** publish. Do **not** touch live posts 27.08.
