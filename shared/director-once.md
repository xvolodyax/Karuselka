# Director — один проход (читать ОДИН раз)

Не открывай `scripts/pipeline_gate.py` и `scripts/composio_instagram_publish.py` **Read-ом**.
Это CLI. Запусти `status` / `next` / `verify` **один раз** через shell (или Task), потом только команды + Task.
Запрещён Read-loop исходников гейта и publish-скрипта.
После **GATE PASS / READY** — **EXIT сразу**. Не ждать слот. Нет `sleep` / poll.
Один и тот же gate-файл — максимум **2 Read** за run. Третий = FAIL + `hole` + EXIT.

## Канон

- Parent Cloud Agent: `gemini-3.8-flash` + `reasoning_effort=low`
- high только если Владимир явно переопределил (`KARUSEL_REASONING_EFFORT`)
- Текстовые Task (`researcher`, `copywriter`): **только** `model="inherit"`
- Не передавать slug `gemini-3.8-flash` в Task (его нет в каталоге воркеров)
- Нет fallback на Claude / GPT / Composer / Grok. Нет Gemini → **FAIL + HOLE**
- Нет лица Вики. 9+9 static PNG. CTA = аудиоразбор в приложении, не бот
- `motion-director` и `animate` уже skipped (`static-png-only`). Не диспатчить.

## Ритуал

```bash
python scripts/pipeline_gate.py --workspace . status
# если STALE_LEDGER / next=new-day:
python scripts/pipeline_gate.py --workspace . new-day --date YYYY-MM-DD --lang ru
# new-day создаёт carusel-memory/packs/YYYY-MM-DD/ (сегодняшний pack, не 2026-08-30)
python scripts/pipeline_gate.py --workspace . record-dispatch --step researcher --via 'Task(generalPurpose)' --model inherit
python scripts/pipeline_gate.py --workspace . dispatch-prompt --step researcher
# Task(generalPurpose, model="inherit") с пакетом из carusel-memory/dispatches/researcher.md
python scripts/pipeline_gate.py --workspace . verify --step researcher
# дальше тот же цикл по next=
```

Цепочка: `researcher → copywriter → designer → image-prompter → slice → design-guardian → upload → publish`.

После **slice** `HANDOFF_NEXT` = **design-guardian** (или upload, если guardian уже ok).
НИКОГДА `motion-director` / `animate` / Grok / mp4 / ANIMATE.md.

## Стоп (не loop)

- Нет инструмента Task → `python scripts/pipeline_gate.py --workspace . hole --reason 'Task tool missing'` и выход
- Publish 403 / нет `tool_execution` / нет alias → FAIL + `HOLE.md`, выход
- GATE PASS / READY → EXIT. Не ждать слот. Нет sleep/poll
- Третий Read `scripts/pipeline_gate.py` или `scripts/composio_instagram_publish.py` → FAIL + hole + EXIT
- Запрещено подставлять archive permalinks (`DcqJGCblQqv`, `DcqJS--m0op` и любые URL из `live-posts.json` с чужой датой)
- `publish-urls.json` только от **этого** `run_id`

## Запреты

- Не писать dossier / slides / caption / CTA в родительском чате
- Не крутить один и тот же файл Read-ом (max 2, потом FAIL)
- Не sleep/poll в ожидании слота
- Не считать вчерашний ledger `next=done` сегодняшней каруселью
- Не писать сегодняшние слайды в старый pack (`2026-08-30` и любые чужие даты)
