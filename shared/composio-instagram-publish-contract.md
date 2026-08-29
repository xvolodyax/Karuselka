# Composio Instagram publish

После **GATE PASS** + **FACE_CHECK MATCH** vs `viktoriaref.png` рой **сам** кладёт карусели RU+EN в Instagram через Composio.

Холл **не** публикует и **слайды не пересматривает**.

## Как вызывать

```bash
# после guardian / face / upload
python scripts/composio_instagram_publish.py --pack carusel-memory/packs/YYYY-MM-DD

# только сверка (без Instagram call)
python scripts/composio_instagram_publish.py --pack carusel-memory/packs/YYYY-MM-DD --check-only
```

Director: после сверки лица — `Task(carusel-publish)`, **не SKIP**.
Worker читает этот файл и skill `skills/carusel-publish/SKILL.md`.

Dry-run пайплайна (без пикселей) publish не зовёт:

```bash
python scripts/pipeline_gate.py --workspace /tmp/carusel-dry-run dry-run --lang ru
```

## Env

| Переменная | Обязательно | Назначение |
|---|---|---|
| `COMPOSIO_API_KEY` | для live-поста | ключ **только** из env. В git / лог / отчёт / fragment не писать |
| `COMPOSIO_API_BASE` | нет | дефолт `https://backend.composio.dev/api/v3` |

В `.env.example` ключ пустой. Реальный ключ — только локальный `.env` (в `.gitignore`).

## Alias (обязательно, не default)

| Alias | Handle | Язык |
|---|---|---|
| `instagram-ru` | `@todaytaro_ru` | RU |
| `instagram-en` | `@todaytaro_bot` | EN |

Default-аккаунт Composio запрещён. Если alias нет — **не** публиковать на «первый попавшийся» Instagram.

Telegram не вызывать.

## Что без ключа

GATE PASS + нет `COMPOSIO_API_KEY` → **не падать**:

```text
GATE PASS
publish: SKIP нет COMPOSIO_API_KEY
```

exit 0. Пакет остаётся готовым. Холл слайды не ревьюит.

## Когда не публиковать (жёсткий отказ, exit 2)

- GATE FAIL
- чужое лицо / FACE_CHECK не MATCH / не `viktoriaref.png`
- CTA бота (`3 free readings` / три бесплатных расклада / `product != app_audio`)
- сырой URL в подписи

## Уже live — не перезаливать

Сегодняшние (и прошлые) live-посты записаны в `carusel-memory/canon/live-posts.json`.
Скрипт делает **SKIP already-live**, Instagram не дергает.

29.08 СТАТУС / LABELS уже в ленте:

- RU https://www.instagram.com/p/Dcnrh0nm7pp/
- EN https://www.instagram.com/p/Dcnrht_lVca/

## Канон пакета (не ломать)

- лицо только `viktoriaref.png`
- глаза зелёные с лёгким карим
- 9+9 статичные PNG, slide-01 тоже PNG
- CTA = кодовое слово → аудиоразбор в приложении, не бот
- в подписи нет сырых URL
