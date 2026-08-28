# CAROUSEL_MOTION_ANALYSIS — 2026-08-28 / Тепло – холодно

**Решение этого run: SKIP. Slide-01 остаётся статичным PNG. 5-секундный loop не снимаем. Grok не вызываем.**

- brief: `skip_motion: true`, `skip_animate: true`, `slide_01: static_png`
- concept: `this_run.slide_01: static_png`
- pack: `carusel-memory/packs/2026-08-28` — `skip_motion: true`, `skip_animate: true`

Это не live-промпт для `grok-imagine-video-1-5-preview`. Никакого motion we will actually shoot.

## Копипак / пути артефактов

Рабочие (gate):

- `carusel-memory/design/CAROUSEL_MOTION_ANALYSIS.md`
- `carusel-memory/design/CAROUSEL_VIDEO_PROMPT.json`
- `carusel-memory/design/CAROUSEL_VIDEO_PROMPT.md`

Копия в pack RU (gitignore-safe):

- `carusel-memory/packs/2026-08-28/ru/CAROUSEL_MOTION_ANALYSIS.md`
- `carusel-memory/packs/2026-08-28/ru/CAROUSEL_VIDEO_PROMPT.json`
- `carusel-memory/packs/2026-08-28/ru/CAROUSEL_VIDEO_PROMPT.md`

Исходный кадр (статичный PNG, не input для Grok в этом run):

- `carusel-memory/output/slides/slide-01.png`
- `carusel-memory/packs/2026-08-28/ru/slides/slide-01.png`

Копипак слайдов (hook / смысл):

- `carusel-memory/design/CAROUSEL_SLIDE_COPY.json` → slide 1
- `carusel-memory/packs/2026-08-28/ru/CAROUSEL_SLIDE_COPY.json`

## 1. Что на кадре

Slide-01 — портрет 3:4, семья `animals_viktoria_collage`.

- **Виктория** слева, тёплые медово-пшеничные волосы с более тёмными корнями, бордовый рубчатый водолаз, золотые кольца. Смотрит вниз в телефон, лицо в холодном свете экрана.
- **Кот** (табби) справа снизу смотрит в тот же экран.
- **Телефон** внизу по центру — источник света, чёрный фон.
- **Текст (lock):** «В субботу он смотрел в глаза» / «и строил планы на осень.» + иконка термометра / «Во вторник — сухое «занят» и три дня тишины.» + снежинка / script «Тепло — холодно» малиновой кистью.

Кадр читается. В этом run он **не оживляется**.

## 2. Роль hook

Сцена контраста суббота→вторник останавливает скролл сама по себе. Motion не нужен: brief явно просит static 9 slides, slide-01 = PNG.

## 3. Стратегия motion

**Нет стратегии съёмки.** `this_run_asset: static_png`. Ни parallax, ни glow, ни loop.

Что остаётся навсегда статичным (и так бы lock'алось, если бы снимали): headline, body, script, иконки, лицо, логотипы, CTA следующих слайдов.

## 4. Речь

Нет. `speech_recommended: false`. Grok не запускается — линии речи нет.

## 5. Звук / атмосфера

Нет. Статичный PNG без аудиодорожки.

## 6. Loop

**Нет 5-секундного loop в этом run.** Первый кадр = единственный кадр = PNG. Seamless loop не проектируем и не снимаем.

## 7. Риски

- Единственный риск — если animate проигнорирует skip и вызовет Grok. Не делать этого: `skip_animate: true`, промпт помечен `"skipped": true`.
- HTTPS URL slide-01 для Grok не нужен и не запрашивался (`slide-01-url.txt` отсутствует — это не BLOCKER при skip).

## 8. Readability lock

Весь текст, иконки, script «Тепло — холодно», лицо Виктории — не двигать, не морфить. В этом run lock выполняется автоматически: файл не анимируется.

## Handoff

Следующий шаг пайплайна: `animate` (тоже skip / static, не Grok). Затем design-guardian.
