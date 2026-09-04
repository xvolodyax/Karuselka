# Director — один проход (читать ОДИН раз)

Не открывай `scripts/pipeline_gate.py` и `scripts/composio_instagram_publish.py` повторно.
Это CLI. После первого `status` только команды + Task.

## Канон

- Parent Cloud Agent: `gemini-3.8-flash` + `reasoning_effort=high`
- Текстовые Task (`researcher`, `copywriter`): **только** `model="inherit"`
- Не передавать slug `gemini-3.8-flash` в Task (его нет в каталоге воркеров)
- Нет fallback на Claude / GPT / Composer / Grok. Нет Gemini → **FAIL + HOLE**
- Нет лица Вики. 9+9 static PNG. CTA = аудиоразбор в приложении, не бот

## Ритуал

```bash
python scripts/pipeline_gate.py --workspace . status
# если STALE_LEDGER / next=new-day:
python scripts/pipeline_gate.py --workspace . new-day --date YYYY-MM-DD --lang ru
python scripts/pipeline_gate.py --workspace . record-dispatch --step researcher --via 'Task(generalPurpose)' --model inherit
python scripts/pipeline_gate.py --workspace . dispatch-prompt --step researcher
# Task(generalPurpose, model="inherit") с пакетом из carusel-memory/dispatches/researcher.md
python scripts/pipeline_gate.py --workspace . verify --step researcher
# дальше тот же цикл по next=
```

## Стоп (не loop)

- Нет инструмента Task → `python scripts/pipeline_gate.py --workspace . hole --reason 'Task tool missing'` и выход
- Publish 403 / нет `tool_execution` / нет alias → FAIL + `HOLE.md`, выход
- Запрещено подставлять archive permalinks (`DcqJGCblQqv`, `DcqJS--m0op` и любые URL из `live-posts.json` с чужой датой)

## Запреты

- Не писать dossier / slides / caption / CTA в родительском чате
- Не крутить один и тот же файл Read-ом
- Не считать вчерашний ledger `next=done` сегодняшней каруселью
