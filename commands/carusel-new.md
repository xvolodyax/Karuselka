# Carusel — новая карусель

Сбрось handoff и запусти **полную** 12-шаговую цепочку. Не делай worker-шаги в этом чате.

## 0. Язык

Пользователь должен дать `lang=ru` или `lang=en`.

| lang | Тема по умолчанию | Handle | Что не путать |
|------|-------------------|--------|----------------|
| ru | ТАРО СЕЙЧАС | `@todaytaro_ru` | не EN-бот |
| en | Today Tarot | `@todaytaro_bot` | это Telegram **bot**, не приложение |

Instagram: без сырых URL, CTA «ссылка в шапке» / «link in bio».  
9 слайдов, сетка 3×3, slide-01 может быть MP4.  
`publish_requested: false`, пока нет явного «опубликуй».

## 1. Init

```bash
python scripts/pipeline_gate.py --workspace . init --lang ru --topic "ТАРО СЕЙЧАС"
# или
python scripts/pipeline_gate.py --workspace . init --lang en --topic "Today Tarot"
```

Допиши intake в `carusel-memory/00-brief.md`.

## 2. Каждый worker — отдельный Task

Повтори для: researcher, copywriter, designer, image-prompter, slice, motion-director, animate, design-guardian, upload, publish, fixic.

```bash
python scripts/pipeline_gate.py --workspace . next
python scripts/pipeline_gate.py --workspace . record-dispatch --step <id> --via 'Task(carusel-<role>)'
python scripts/pipeline_gate.py --workspace . dispatch-prompt --step <id>
```

Cloud: `--via 'Task(generalPurpose)'`, затем один `Task(generalPurpose)` с пакетом.  
После Task: `verify --step <id>`. Нет verify → стоп.

Нельзя сокращать цепочку до copywriter → publish.

## 3. Publish / Fixic

По умолчанию:

```bash
python scripts/pipeline_gate.py --workspace . skip --step publish --reason publish-not-requested
python scripts/pipeline_gate.py --workspace . skip --step fixic --reason no-open-incidents
```

Live-пост — только отдельная команда / явный запрос + `carusel-publish`.

```bash
python scripts/pipeline_gate.py --workspace . assert-complete
```
