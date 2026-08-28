# Victoria identity lock — copied from taro-excalibur i2i

Excalibur locks a host face by putting the **appearance reference first** in
`input_urls` and keeping the prompt short (`cover_mode=host_reference`).
A long MUST/face essay starves the model. Wrong face or platinum hair →
**new canvas**, not a patched cell.

## Karuselka lock

| Rule | Value |
|------|--------|
| Official sheet | `carusel-memory/references/victoria-sheet.png` (box: `/workspace/cover-refs/victoria-sheet.png`) |
| i2i file | **ONE cropped close-up** of the large left frontal portrait — not the 12-up grid |
| `input_urls` | exactly one URL; upload the crop as `file_name=victoria-sheet.png` |
| Eyes | green with a slight hazel / light-brown mix (same as Excalibur articles) |
| Hair | warm honey / wheat blonde with darker roots |
| Fail | platinum, white-blonde, Alena, brown/grey eyes, any other woman |
| Clothes | **new every carousel** — never the sheet white cami + jeans |

`cover-refs/victoria.png` is **Alena**. Never upload it. There is no second face file.

Style lock (`animals-viktoria-style-lock.png`) is **palette / type described in text**.
Do **not** send it as an i2i input — the plate is a sticker collage and the model
copies those outlines. Face crop is the only `input_url`.

## Crop, do not send the grid

i2i of the full 12-up sheet averages many angles into a generic blonde.

```bash
python3 scripts/crop_victoria_sheet_tight.py
# writes carusel-memory/references/victoria-sheet-front.png
```

Upload **that crop** only. Keep the official 12-up in the repo for FACE_CHECK.

## Prompt

Face lock **first**, then grid + verbatim copy. `prompt_char_count` ≤ 2200.
No 3000-char collage / type / wardrobe novel. No face essay.
