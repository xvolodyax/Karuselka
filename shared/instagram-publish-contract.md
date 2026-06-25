# Carusel — Instagram Publish Contract (MCP)

## Server

```text
server: user-instagram carusel
tool: t4528_carrusel_instagram
```

## Carousel format (default)

- **9 slides** from grid 3×3
- **slide-01** = Grok video → MCP `file1`
- **slide-02 … slide-09** = PNG → `file2` … `file9`

## Arguments (schema)

| Param | Slide | Type | Note |
|-------|-------|------|------|
| `file1` | 1 | HTTPS URL | **video** mp4 (Grok) |
| `file2` | 2 | string | |
| `File3` | 3 | string | **Capital F** |
| `file4` | 4 | string | |
| `file5` | 5 | string | |
| `file6` | 6 | string | |
| `file7` | 7 | string | required by Make for 9-slide grid |
| `file8` | 8 | string | required by Make for 9-slide grid |
| `file9` | 9 | string | required by Make for 9-slide grid |
| `caption` | — | string | max 2200 chars |

### MCP descriptor drift (2026-06)

Исторически локальный descriptor MCP содержал только `file1`–`file6`, но Make-сценарий уже валидирует **9** входов.  
Если отправить только 6 файлов, Make возвращает:

```json
{"message":"Validation failed for 3 parameter(s).","name":"BundleValidationError"}
```

Root cause: отсутствуют `file7`, `file8`, `file9`.

**Canonical payload:** всегда передавать `file1`, `file2`, `File3`, `file4`, `file5`, `file6`, `file7`, `file8`, `file9`, `caption`.

## Idempotency / no blind retry

Instagram publish is not idempotent.

- Делай **ровно один** MCP call на один `run_id` / набор media URLs.
- После вызова **жди 3–5 минут** — Make часто отвечает async (`started but did not complete yet`); это норма.
- Async **не** означает «сделай второй call» — дождись выполнения сценария или проверки пользователем.
- Повторный publish-call только после явного OK пользователя и fresh upload (новые URL).

## Pre-publish validation

1. `carusel-memory/output/slides/slide-01.png` … `slide-09.png` (9 PNG после slice).
2. `carusel-memory/output/video/slide-01.mp4` после animate.
3. **HTTPS** URLs в `publish-urls.json` (Kie File Upload, scoped by `run_id`).
4. `caption` из `CAROUSEL_CAPTION.json`.
5. `python scripts/publish_preflight.py` — no URL overlap with prior runs in `publish-log.md`.

## Video slide 1

- `file1` = HTTPS `slide-01.mp4` — Grok, 5s loop
- `file2`–`file9` = PNG slides 2–9
- Still `slide-01.png` используется motion-director + Grok input

## Log

`carusel-memory/output/publish-log.md`
