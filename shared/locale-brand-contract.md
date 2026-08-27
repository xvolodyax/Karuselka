# Locale + brand contract (ТАРО СЕЙЧАС / Today Tarot)

`lang` обязателен в `carusel-memory/00-brief.md` и `carusel-memory/pipeline-ledger.json`.

Допустимо только: `ru` | `en`.

## Аккаунты

| lang | Handle | Что это | Чем это не является |
|------|--------|---------|---------------------|
| `ru` | `@todaytaro_ru` | Публичный бренд-аккаунт русской линии **ТАРО СЕЙЧАС** | Не EN-бот, не приложение |
| `en` | `@todaytaro_bot` | Telegram-бот английской линии **Today Tarot** | Не мобильное приложение, не Instagram app, не `@todaytaro_ru` |

Не путать **бот** и **приложение**:

- `@todaytaro_bot` — Telegram bot. В EN-копирайте: bot / Telegram bot.
- Запрещено: «скачай приложение», «open the app», «the Today Tarot app», если речь про этот handle.
- Instagram — канал публикации карусели. Telegram-бот — CTA/продукт EN-линии. Это разные вещи.

## Instagram: без сырых URL

В слайдах и caption **нельзя** сырые ссылки:

- `https://`, `http://`
- `instagram.com/...`, `t.me/...`, `telegram.me/...`

CTA в посте:

- RU: «ссылка в шапке»
- EN: «link in bio»

Handle писать как `@todaytaro_ru` / `@todaytaro_bot`, не как URL.

Ссылки живут в шапке / bio Instagram, не в теле карусели.

## Язык артефактов

| Артефакт | `lang=ru` | `lang=en` |
|----------|-----------|-----------|
| Слайды (headline/body/CTA) | русский | English |
| Caption | русский | English |
| Research dossier | русский | English |
| Design docs (человеческие) | русский | English |
| Текст **на** картинке в Kie prompt | русские строки из copy | English strings from copy |
| Промпт Kie/Grok (инструкции модели) | русский (как в каноне пайплайна) | русский; цитаты текста — на английском |

Директор с пользователем говорит по-русски. Язык **контента** задаёт `lang`.

## Формат (оба языка)

- Ровно **9** слайдов, сетка **3×3**, панель **3:4**
- Master Kie: **3:4 @ 4K**
- slide-01 **может** быть MP4 (Grok, 5s loop) → Instagram `file1`
- slide-02 … slide-09 — PNG

## Brief — обязательные поля

```markdown
lang: ru
topic: ТАРО СЕЙЧАС
handle: @todaytaro_ru
publish_requested: false
cta_style: header_link
bot_vs_app: @todaytaro_bot is a Telegram bot, not an app
```

EN-пример:

```markdown
lang: en
topic: Today Tarot
handle: @todaytaro_bot
publish_requested: false
cta_style: header_link
bot_vs_app: @todaytaro_bot is a Telegram bot, not an app
```

`publish_requested: true` только после явной просьбы пользователя опубликовать live-пост.
