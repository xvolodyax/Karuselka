# Locale + brand contract (ТАРО СЕЙЧАС / Today Tarot)

`lang` обязателен в `carusel-memory/00-brief.md` и `carusel-memory/pipeline-ledger.json`.

Допустимо только: `ru` | `en`.

Всегда читать вместе с `shared/taro-seichas-canon.md`.

## Аккаунты

| lang | Handle | Что это | Чем это не является |
|------|--------|---------|---------------------|
| `ru` | `@todaytaro_ru` | Публичный бренд-аккаунт русской линии **ТАРО СЕЙЧАС** | Не EN-бот, не приложение |
| `en` | `@todaytaro_bot` | Имя EN Instagram-аккаунта **Today Tarot** | Не приз за комментарий, не `@todaytaro_ru` |

Не путать **handle** и **продукт**:

- `@todaytaro_bot` — имя EN Instagram-аккаунта. Это **не** приз за комментарий.
- Продукт CTA = **аудиоразбор в приложении** (`app_audio`). Не 3 бесплатных расклада в боте.
- Запрещено: «личный аудиоразбор». Писать «аудиоразбор» / «audio reading».
- Instagram — канал. Ссылки — в профиле / шапке. Сырых URL нет.
- Контракт: `shared/cta-app-audio-contract.md`.

## Продукт и триггер (один пост = один продукт)

В caption **одно** слово-триггер. Команда отвечает в Direct.

| lang | Триггер | Продукт | Рамка темы |
|------|---------|---------|------------|
| ru | новое слово каждый день, по теме | `app_audio` — аудиоразбор в приложении | Суть – Тень – Вектор |
| en | своё слово, не копия RU | то же; **NO Academy** | Essence–Shadow–Vector |

Не писать сырые ссылки. Не делать CTA «подпишись + сохрани + перейди по ссылке».
Обязательно «ссылка в шапке» / «links are in the profile».
Сырые URL запрещены всегда:

- `https://`, `http://`
- `instagram.com/...`, `t.me/...`, `telegram.me/...`

Handle писать как `@todaytaro_ru` / `@todaytaro_bot`.

## Язык артефактов

| Артефакт | `lang=ru` | `lang=en` |
|----------|-----------|-----------|
| Слайды (headline/body/CTA) | русский | English |
| Caption | русский | English |
| Research dossier | русский | English |
| Design docs (человеческие) | русский | English |
| Текст **на** картинке в Kie prompt | русские строки из copy | English strings from copy |
| Промпт Kie/Grok (инструкции модели) | русский | русский; цитаты текста — на английском |

Директор с пользователем говорит по-русски. Язык **контента** задаёт `lang`.

## Формат (оба языка)

- Ровно **9** слайдов, сетка **3×3**, панель **3:4**
- Master Kie: **3:4 @ 4K** (или 9 отдельных 3:4, если i2i per-slide)
- Visual family: **`animals_viktoria_collage`**
- slide-01 **может** быть MP4 (Grok, 5s loop) → Instagram `file1`
- slide-02 … slide-09 — PNG
- Hook = сцена. ≥2 save-слайда с рамкой/вопросами. ≥3 слайда с животным-метафорой.

## Brief — обязательные поля

```markdown
lang: ru
topic: ТАРО СЕЙЧАС
handle: @todaytaro_ru
publish_requested: true
visual_family: animals_viktoria_collage
cta_style: comment_trigger
trigger_word: ПАУЗА
product: app_audio
cta_offer: comment trigger → Direct audio reading in the APP (Суть – Тень – Вектор)
```

EN-пример:

```markdown
lang: en
topic: Today Tarot
handle: @todaytaro_bot
publish_requested: true
visual_family: animals_viktoria_collage
cta_style: comment_trigger
trigger_word: PAUSE
product: app_audio
cta_offer: comment trigger → Direct audio reading in the APP (Essence–Shadow–Vector)
```

`publish_requested: true` по умолчанию: после GATE PASS рой сам кладёт RU+EN в Instagram через Composio.
Холл не публикует и слайды не пересматривает. Нет `COMPOSIO_API_KEY` → SKIP «нет COMPOSIO_API_KEY».
Alias обязателен: `instagram-ru` / `instagram-en`. Telegram запрещён.
