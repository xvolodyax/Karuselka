# Каруселька

![Каруселька — плагин для Cursor](assets/cover.png)

[![Telegram](https://img.shields.io/badge/Telegram-Maya%20Pro-ff006e?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/maya_pro)

**Каруселька** — локальный плагин для Cursor, который собирает Instagram-карусели через цепочку специализированных AI-агентов: от ресерча и текста до дизайна, генерации изображения, анимации первого слайда, QA, загрузки ассетов и публикации через MCP.

Плагин сделан для формата **9 слайдов сеткой 3×3**: один большой master-image генерируется в едином стиле, затем режется на 9 вертикальных карточек. Первый слайд может быть заменён коротким MP4 loop-видео, а остальные остаются PNG.

## Что умеет

- Делает ресерч темы и конкурентов перед созданием карусели.
- Пишет текст для 9 слайдов и caption для Instagram.
- Раскладывает визуальную концепцию по панелям сетки 3×3.
- Готовит компактный prompt для Kie.ai / GPT Image 2.
- Генерирует master image и режет его на 9 одинаковых слайдов.
- Анимирует первый слайд через Grok Video.
- Проверяет дизайн, bleed, текст, размер и соответствие референсу.
- Загружает финальные ассеты на HTTPS-хранилище Kie.
- Публикует карусель через Instagram MCP / Make-сценарий.
- Ведёт incident queue и фиксирует повторяющиеся проблемы через Fixic.

## Карта функционала

| Зона | Компоненты | Назначение |
| --- | --- | --- |
| Оркестрация | `rules/`, `agents/director.md`, `skills/director-carusel/` | Управляет пайплайном и handoff между агентами |
| Ресерч | `agents/carusel-researcher.md`, `skills/carusel-researcher/` | Анализ темы, аудитории, конкурентов и углов подачи |
| Текст | `agents/carusel-copywriter.md`, `skills/carusel-copywriter/` | 9 слайдов, caption, CTA и структура сторителлинга |
| Дизайн | `agents/carusel-designer.md`, `skills/carusel-designer/`, `shared/CAROUSELDESIGN_SPEC.md` | Визуальная система, композиция, style lock |
| Image prompt | `agents/carusel-image-prompter.md`, `skills/carusel-image-prompter/` | JSON/MD prompt для Kie, 9 panel briefs, compact prompt policy |
| Генерация и slice | `agents/carusel-slice.md`, `scripts/kie_carousel_gen.py`, `scripts/slice_grid.py` | Master image 3:4 @ 4K и нарезка 3×3 |
| Motion | `agents/carusel-motion-director.md`, `agents/carusel-animate.md`, `scripts/grok_video_gen.py` | Сценарий анимации и MP4 для первого слайда |
| QA | `agents/carusel-design-guardian.md`, `scripts/video_frame_qa.py` | Проверка дизайна, bleed, aspect ratio, frame0 fidelity |
| Upload | `agents/carusel-upload.md`, `scripts/upload_carousel_assets.py` | HTTPS upload, run-scoped paths, MP4 normalization |
| Publish | `agents/carusel-publish.md`, `scripts/publish_preflight.py` | MCP publish без blind retry и дублей |
| Fixic | `agents/carusel-fixic.md`, `skills/carusel-fixic/` | Разбор инцидентов и durable fixes |
| Общие контракты | `shared/` | Playbook, API contracts, pitfalls, publish rules |

## Структура репозитория

```text
.
├── .cursor-plugin/          # metadata плагина Cursor
├── agents/                  # описания subagents
├── commands/                # команды Cursor
├── rules/                   # workspace rules
├── skills/                  # skill-контракты агентов
├── scripts/                 # Python utilities для Kie/Grok/slice/upload/QA
├── shared/                  # playbooks, contracts, pitfalls
├── assets/cover.png         # обложка репозитория
└── .env.example             # шаблон переменных окружения без ключей
```

## Установка

1. Склонируйте репозиторий:

```bash
git clone https://github.com/Horosheff/Karuselka.git
```

2. Установите плагин как локальный Cursor plugin: скопируйте папку репозитория в директорию локальных плагинов Cursor или подключите её как local plugin.

3. Установите зависимости Python:

```bash
pip install -r scripts/requirements.txt
```

4. Создайте `.env` рядом с рабочей папкой карусели:

```env
KIE_API_KEY=your_kie_api_key_here
COMPOSIO_API_KEY=
```

Публичный репозиторий содержит только `.env.example`. Реальные ключи, run-логи, изображения, видео и результаты публикаций не входят в поставку. Значение `COMPOSIO_API_KEY` в git, лог и отчёт не писать.

## Публикация Instagram (Composio)

После GATE PASS + сверки лица рой сам кладёт карусели RU+EN. Холл не публикует и слайды не пересматривает.

```bash
python scripts/composio_instagram_publish.py --pack carusel-memory/packs/YYYY-MM-DD
```

| Env | Зачем |
|---|---|
| `COMPOSIO_API_KEY` | единственный источник ключа |
| `COMPOSIO_API_BASE` | опционально, дефолт `https://backend.composio.dev/api/v3` |

Alias обязателен, не default: `instagram-ru` = `@todaytaro_ru`, `instagram-en` = `@todaytaro_bot`. Telegram не слать.

Без ключа процесс **не падает**: GATE PASS + `publish: SKIP нет COMPOSIO_API_KEY`.
GATE FAIL / чужое лицо / CTA бота — не публиковать. Уже live карусели не перезаливать.

Контракт: `shared/composio-instagram-publish-contract.md`.

## Базовый пайплайн

```text
director
  -> researcher
  -> copywriter
  -> designer
  -> image-prompter
  -> slice
  -> motion-director
  -> animate
  -> design-guardian
  -> upload
  -> publish
  -> fixic
```

Рабочие артефакты по умолчанию создаются в `carusel-memory/` внутри проекта пользователя. Эта папка считается runtime-memory и не должна попадать в публичные коммиты.

## Безопасность

- Не коммитьте `.env`, API keys, OAuth tokens, MCP payloads, временные CDN URL и publish logs.
- Не публикуйте `carusel-memory/`, `output/`, `fragments/`, `research/`, `design/` с реальными прогонами.
- Перед публикацией запускайте secret-scan по ключевым словам: `KIE_API_KEY`, `COMPOSIO_API_KEY`, `Bearer`, `token`, `secret`, `password`, `tempfile`.
- Публикация в Instagram идемпотентна по pack: already-live не перезаливать. Ключ Composio только из env.

## Требования

- Cursor с поддержкой local plugins, rules, skills и agents.
- Python 3.10+.
- Kie.ai API key для image/video generation и file upload.
- `ffmpeg` и `ffprobe` для проверки/нормализации MP4.
- `COMPOSIO_API_KEY` и alias `instagram-ru` / `instagram-en` для автопубликации. Без ключа publish = SKIP, не FAIL.

## Статус

Версия `0.1.0`: рабочий public scaffold плагина с контрактами, агентами и утилитами. Репозиторий очищен от приватной памяти прогонов и поставляется как база для установки, доработки и командной работы.
