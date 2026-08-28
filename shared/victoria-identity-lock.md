# Victoria identity lock — viktoriaref.png only

Excalibur locks a host face by putting the **appearance reference first** in
`input_urls` and keeping the prompt short (`cover_mode=host_reference`).
A long MUST/face essay starves the model. Wrong face or platinum hair →
**new canvas**, not a patched cell.

## Karuselka lock

| Rule | Value |
|------|--------|
| Official face | `carusel-memory/references/viktoriaref.png` (~1.5MB frontal) |
| Box copy | `/workspace/cover-refs/viktoriaref.png` (same bytes) |
| `input_urls` | exactly one URL; upload `file_name=viktoriaref.png` |
| Eyes (first line after identity) | green with a slight hazel / light-brown tint around the pupil; **зелёные с лёгким карим** |
| Hair | warm honey / wheat blonde with darker roots, not platinum |
| Fail | 12-up sheet, sheet crop, Alena, brown-only / grey / blue eyes, platinum, any other woman |
| Clothes | **new every carousel** — never the reference white cami |

Deleted (do not restore, do not i2i):

- `victoria-sheet.png` (12-up contact sheet)
- `victoria-sheet-front.png` (crop of that sheet)
- `victoria-face.png`
- `victoria.png` / `alena.png` / `*_ref.jpg`

Style lock (`animals-viktoria-style-lock.png`) is **palette / type described in text**.
Do **not** send it as an i2i input — the plate is a sticker collage.

## Prompt

First lines must name `viktoriaref.png` and the eyes lock. Then grid + verbatim copy.
`prompt_char_count` ≤ 2200. No 3000-char collage / type / wardrobe novel.
