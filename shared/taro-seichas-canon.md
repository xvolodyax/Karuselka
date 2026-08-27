# ТАРО СЕЙЧАС / Today Tarot — always-on carousel canon

Читать **до** research / copy / design / prompt / guardian на каждом daily run (в т.ч. 11:10).
Пустой красивый вайб без урока = FAIL. Семья `animals_viktoria_collage` не опция, а дефолт.

Контракты рядом: `shared/locale-brand-contract.md`, `shared/animals-viktoria-collage.md`,
`shared/caption-format-contract.md`. Проверка: `python scripts/canon_gate.py --pack <pack>`.

## Почему этот файл существует

27.08.2026 две карусели уже вышли и **остаются live** (не удалять, не править):

| lang | Handle | Post | Hook |
|------|--------|------|------|
| ru | @todaytaro_ru | https://www.instagram.com/p/Dci-EP1ErI-/ | «Пауза или конец?» |
| en | @todaytaro_bot | https://www.instagram.com/p/Dci-ozwAH4l/ | «Pause or over?» |

Владелец: посты пустые / красивые / глупые относительно OLD Karuselka.
Причина (проверено 27.08): в plugin-scaffold не было visual family + meaning lock.
Locale-контракт фиксировал handle и «без URL», но не сцену, не животных, не Викторию,
не framework на save-слайдах. Copywriter skill писал generic vibe-arc.

Этот канон закрывает дрейф. Новая пара по той же теме — pack `2026-08-27-v2`.

## Профили

| | RU | EN |
|---|----|----|
| Бренд | ТАРО СЕЙЧАС | Today Tarot |
| Handle | @todaytaro_ru | @todaytaro_bot |
| Слоган | Ясность сейчас | Clarity now |
| Лицо | Victoria (один face lock) | та же Victoria |
| Academy | можно не трогать | **NO Academy** |

Клиент: женщины 20–50, ~78% отношения. Не целиться в 13–17.
Не хайпить войну/медицину. Не читать мысли. Не пугать одиночеством.

## Visual family (всегда)

`carousel_family`: **`animals_viktoria_collage`**

Полный spec: `shared/animals-viktoria-collage.md`.

Коротко:

- charcoal/black + magenta `#ff006e` + white + soft gold
- Victoria cutout на hook (1) и CTA (9). Волосы = warm honey/wheat + darker roots.
  Platinum / white-blonde / сильно светлее `victoria.png` = FAIL, regen.
- Других женских лиц нет.
- Животные = метафоры, не мемы: кот = «чуешь», пёс = верность вопросу, сова = ночные мысли.
- Минимум **3** слайда с животным-метафорой.
- 9 слайдов, каждый 3:4, hook читается за 2 секунды.
- Нет horror / крови / черепов / тёмного стола со свечами.
- Нет подписи Victoria на слайдах.
- Лёгкий tarot-декор можно, если не закрывает headline.
- Опционально золотой медальон ТАРО/СЕЙЧАС, если садится нативно.

## Meaning / copy (то, чего не хватило 27.08 live)

9-slide teaching arc:

```text
01 hook SCENE     — первая строка = сцена, не название механики
02 pain           — что болит в этой сцене
03 mistake        — как клиентка слышит приговор вместо процесса
04 mechanism      — чем пауза является на самом деле
05–07 save        — 2–3 слайда с рамкой / вопросами / «говорит vs слышишь»
08 recap / rule   — правило, которое можно сохранить
09 CTA            — одно действие, одно слово-триггер
```

Первая строка — СЦЕНА. Энергия:

> Он смотрит твои истории. Третью неделю. Сообщения нет.

Не: «5 признаков паузы», «Что такое пауза в таро», «Pause vs ending».

Простой разговорный русский / English. Без поэзии, которую надо объяснять.
Глубина как в OLD `slide-04`: «Говорит: … / Слышишь: …» + конструктивный урок.
Не список вайб-слов.

Запреты в тексте:

- «личный аудиоразбор» — только «аудиоразбор», если вообще выбран app-продукт
- мешать bot и app в одном CTA
- сырые URL в слайдах и caption
- пугать одиночеством, войной, болезнью
- EN: Academy

## Caption + продукт

Один пост = один продукт = одно слово-триггер. Команда отвечает в Direct.

| lang | Trigger | Продукт (выбрать один на карусель) |
|------|---------|-------------------------------------|
| ru | пример: `ПАУЗА` | 3 бесплатных расклада в боте **или** аудиоразбор в приложении |
| en | пример: `PAUSE` | то же, один продукт, без Academy |

В pack `2026-08-27-v2` выбран **бот / 3 бесплатных расклада**, не приложение.

Не писать сырые `https://`, `instagram.com`, `t.me`. Handle как `@todaytaro_ru`.

## Референсы

В репо: `carusel-memory/references/` (описания + сгенерированный hair lock, если исходник не в git).

На боксе Hall (не всегда в cloud checkout):

- `/workspace/karusel-old/image-851e.png` — STYLE LOCK (владелец выбрал)
- `/workspace/cover-refs/victoria.png` — CURRENT hair/face lock
- `/workspace/karusel-old/cover-old.png` — old face lock (структура лица, не цвет волос)
- `/workspace/karusel-old/slide-04.png` — DEPTH example, не visual family

Португальский текст и чужие лица из style collage **не заимствовать**.

## Gate (PASS только если все true)

- (a) Victoria face = hair lock (honey/wheat + darker roots; не platinum)
- (b) ≥3 слайда с животным как метафорой
- (c) ≥2 save-слайда с настоящей рамкой или вопросами
- (d) hook = сцена
- (e) нет platinum
- (f) нет пустых vibe-only слайдов

## Пайплайн

Не изобретать новый рой. Цепочка та же:

`director → researcher → copywriter → designer → image-prompter → slice
 → motion-director → animate → design-guardian → upload → publish → fixic`

`Task(carusel-*)` если plugin types есть. Иначе отдельный `Task(generalPurpose)` на шаг
(`shared/director-dispatch-contract.md` + `scripts/pipeline_gate.py`).

Если Task недоступен и brief явно разрешает parent remake (этот тип задачи) —
директор делает шаг сам и пишет это в `GATE.md`. Publish / Composio / Instagram —
только Hall после human review. `publish_requested: false` по умолчанию.

## Live posts

Не удалять и не редактировать посты 27.08. Новая пара = новый pack / новый пост.
