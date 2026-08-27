# Hall — secretary handoff

## Swarm (plain language)

The pack is not one agent wearing 11 hats.

1. Director only starts the run and calls the next Task.
2. Cloud cannot see `Task(carusel-*)`. Use `Task(generalPurpose)` **once per step** (`pipeline_gate.py dispatch-prompt`).
3. Researcher + copywriter (slides **and** caption) must run on **Gemini**. Artifacts must say `written_by: gemini`. Other models = gate FAIL.
4. Designer locks layout. Image-prompter writes Kie prompts from that copy + `victoria-sheet.png`. Do not invent new slogans.
5. Publish is **skip** unless Vladimir asked Hall. Never Instagram/Make/Composio from the swarm.

Today’s empty pretty posts happened because Director skipped researcher+copywriter and jumped to vibe pixels. Do not do that.

See `shared/swarm-spawn-contract.md`.

## Do not auto-publish

This pack is for **human review**, then you publish via Composio.

- Do **not** call Instagram / Make / Composio from Karuselka director.
- Do **not** delete or edit live posts:
  - RU @todaytaro_ru https://www.instagram.com/p/Dci-EP1ErI-/ «Пауза или конец?»
  - EN @todaytaro_bot https://www.instagram.com/p/Dci-ozwAH4l/ «Pause or over?»
- New posts only, after Vladimir reviews slide text in the PR.

## Product / CTA (one each)

| lang | Handle | Trigger comment | Product |
|------|--------|-----------------|---------|
| ru | @todaytaro_ru | ПАУЗА | 3 бесплатных расклада в боте, ответ в Direct |
| en | @todaytaro_bot | PAUSE | 3 free spreads in the bot, reply in Direct |

No raw URLs in captions. No app mix. No Academy on EN.

## Refs on the box

See `carusel-memory/references/BOX-PATHS.md`:

- `/workspace/cover-refs/victoria-sheet.png` — ONLY Victoria face lock (commit as `carusel-memory/references/victoria-sheet.png`)
- `/workspace/cover-refs/victoria.png` — **ALENA, forbidden**
- `/workspace/karusel-old/image-851e.png` — style only
- `/workspace/karusel-old/cover-old.png` — RETIRED studio-blazer
- `/workspace/karusel-old/slide-04.png` — depth example only

## Pack path

`carusel-memory/packs/2026-08-27-v2/{ru,en}/slides/slide-01.png` … `slide-09.png`

Captions: `CAROUSEL_CAPTION.md` next to slides.
Gate: `GATE.md` — PASS before you publish.
