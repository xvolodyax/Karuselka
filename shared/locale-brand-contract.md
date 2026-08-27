# Locale + brand contract (ТАРО СЕЙЧАС / Today Tarot)

`lang` обязателен в `carusel-memory/00-brief.md` и `carusel-memory/pipeline-ledger.json`.

Допустимо только: `ru` | `en`.

Всегда читать вместе с `shared/taro-seichas-canon.md`.

## Аккаунты

| lang | Handle | Что это | Чем это не является |
|------|--------|---------|---------------------|
| `ru` | `@todaytaro_ru` | Публичный бренд-аккаунт русской линии **ТАРО СЕЙЧАС** | Не EN-бот, не приложение |
| `en` | `@todaytaro_bot` | Telegram-бот английской линии **Today Tarot** | Не мобильное приложение, не Instagram app, не `@todaytaro_ru` |

Не путать **бот** и **приложение**:

- `@todaytaro_bot` — Telegram bot. В EN-копирайте: bot / Telegram bot.
- Запрещено мешать bot и app в одном CTA.
- Запрещено: «личный аудиоразбор». Если продукт — приложение, писать только «аудиоразбор».
- Instagram — канал публикации. Продукт в CTA — один на карусель.

## Продукт и триггер (один пост = один продукт)

В caption **одно** слово-триггер. Команда отвечает в Direct.

| lang | Пример триггера | Продукт (выбрать один) |
|------|-----------------|------------------------|
| ru | `ПАУЗА` | 3 бесплатных расклада в боте **или** аудиоразбор в приложении |
| en | `PAUSE` | то же; **NO Academy** на EN |

Не писать сырые ссылки. Не делать CTA «подпишись + сохрани + перейди по ссылке».

Вторично можно «ссылка в шапке» / «link in bio», если триггер уже есть.
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
publish_requested: false
visual_family: animals_viktoria_collage
cta_style: comment_trigger
trigger_word: ПАУЗА
product: bot_three_spreads
bot_vs_app: pick ONE product; do not mix bot and app
```

EN-пример:

```markdown
lang: en
topic: Today Tarot
handle: @todaytaro_bot
publish_requested: false
visual_family: animals_viktoria_collage
cta_style: comment_trigger
trigger_word: PAUSE
product: bot_three_spreads
bot_vs_app: pick ONE product; do not mix bot and app
```

`publish_requested: true` только после явной просьбы опубликовать live-пост.
Hall публикует через Composio после human review. Агент карусели сам не публикует.
