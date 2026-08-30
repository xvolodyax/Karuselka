# Host portrait — pixel gate (ABSENT)

Guardian compares **pixels**. Old FACE MATCH vs `Виктория.png` is retired.

## Lock (new packs)

- No host portrait on any slide.
- Do not i2i `Виктория.png` / `viktoriaref.png` / `victoria-sheet.png` / `victoria.png`.
- `animals-viktoria-style-lock.png` is palette only — never a face ref.
- Do not restore deleted face files.

## FACE_CHECK.md

Must say `verdict: ABSENT` (not `MATCH`).
Must say the rule is **no host portrait**, not “похожа на Виктория.png”.
GATE **FAIL** if:

- slide shows Vika / any recognizable presenter portrait
- `verdict: MATCH`
- prompt or `input_urls` still carry a face file

Live packs `2026-08-27-*` … `2026-08-30` keep their historical FACE MATCH notes.
Do not rewrite those pixels.
