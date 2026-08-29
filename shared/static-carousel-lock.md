# Instagram carousels are static PNGs

Owner lock 28.08.2026. Applies to this pack **and going forward** unless Hall
explicitly asks for video.

## Lock

- All 9 RU + 9 EN slides are **PNG**.
- Slide 01 is also a still PNG. Not MP4. Not Grok. Not motion-safe video.
- Skip `carusel-motion-director`, `carusel-animate`, `grok_video_*`, any `ANIMATE.md`.
- Upload with `--static-all-pngs` (file1 = `slide-01.png`).
- Do not generate `slide-01.mp4`.

## Pipeline

```text
researcher → copywriter → designer → image-prompter → slice
  → skip motion-director (static-png-only)
  → skip animate (static-png-only)
  → design-guardian → upload → publish(skip unless asked)
```

Skip reason: `static-png-only`.

`skip_motion: false` / `skip_animate: false` in the brief only if Hall asks for video.
