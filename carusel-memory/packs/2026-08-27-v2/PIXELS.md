# PIXELS

## What was generated

Cloud VM **had** `KIE_API_KEY`, but box originals (`/workspace/karusel-old/image-851e.png`, `/workspace/cover-refs/victoria.png`) were **not** in this checkout.

Pixels in this pack were rendered with Cursor GenerateImage, then converted with ffmpeg to real PNG **864×1152 (3:4)**:

- Face lock stand-in: `carusel-memory/references/victoria-hair-lock.png` (honey/wheat + darker roots)
- Style sheet stand-in: `carusel-memory/references/animals-viktoria-style-lock.png` (no Portuguese, no foreign faces)
- RU `slide-01.png` … `slide-09.png`
- EN `slide-01.png` … `slide-09.png`

Kie i2i JSON is ready in each lang folder (`CAROUSEL_IMAGE_PROMPT.json`, model `gpt-image-2-image-to-image`).

## Hall: re-render with box originals (preferred)

If `/workspace/cover-refs/victoria.png` and `/workspace/karusel-old/image-851e.png` exist on your box:

1. Upload both via `scripts/kie_file_upload.py` (stream).
2. Put HTTPS URLs into `input_urls` of RU and EN `CAROUSEL_IMAGE_PROMPT.json`.
3. Run `python scripts/kie_run_prompt.py --workspace <pack-lang-workspace>`.
4. Or keep these PNGs if human review already likes them.

Do **not** publish from this agent. Do **not** touch live posts 27.08.
