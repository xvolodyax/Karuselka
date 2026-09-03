# CAROUSEL_IMAGE_PROMPT — RU 2026-09-03

**Шаг:** image-prompter. Пикселей нет. Kie не запускался. Slice не стартовал.

## Lock

| Поле | Значение |
|------|----------|
| pack_id | 2026-09-03 |
| topic | Он пишет только после полуночи — днём тебя нет |
| trigger | ПОЛНОЧЬ |
| product | app_audio |
| face_lock | none |
| host_portrait | false |
| generation_mode | grid_3x3 |
| aspect / res | 3:4 @ 4K |
| slice_method | seam — thin white gutters at 1/3 and 2/3 (Excalibur) |
| output | static PNG, slide-01 still |
| prompt_char_count | 1879 (gate ≤2200, target 1600–2000) |

## Style ref

- HTTPS (upload_stream): `https://tempfile.redpandaai.co/kieai/378019/carusel-style-lock/animals-viktoria-style-lock.png`
- Local: `carusel-memory/references/animals-viktoria-style-lock.png`
- Роль: палитра / ритм коллажа. **Не лицо.** Не i2i как портрет.
- **Не** в `input_urls`: `Виктория.png`, `viktoriaref.png`, `victoria-sheet.png`, `victoria.png`.

## Prompt logic

Промпт короткий, на русском, с verbatim-цитатами из `CAROUSEL_SLIDE_COPY.json` этого прогона (не СУББОТА). Старт: no host / no woman / без лица / без портрет.

9 панелей row-major:

| # | Animal | Role | Headline |
|---|--------|------|----------|
| 01 | owl | hook | 00:47 голосовое. 14:20 — нет галочек. |
| 02 | dog | problem | Ночью выбранная. Днём — пустое место. |
| 03 | dog | mistake | Ошибка — двигать сон под его 01:12 |
| 04 | owl | mechanism | Полночь — часы без свидетелей |
| 05 | cat | save_decoder | Говорит / Слышишь / Есть |
| 06 | cat | save_checklist | 3 дневные проверки |
| 07 | dog | save_questions | 3 вопроса до его полуночи |
| 08 | owl | recap | Ночь без дня — окно, не выбор |
| 09 | owl | cta | Напиши ПОЛНОЧЬ + Аудиоразбор в моём приложении. + Суть – Тень – Вектор |

Панель 09 = app_audio. Не бот. Не 3 бесплатных расклада. Не Academy.

## Preserve / change / do_not_borrow

- **Preserve:** charcoal #111111, magenta #ff006e, white heavy sans, torn pills, seam gutters, animals-as-metaphor, no host.
- **Change:** midnight-window objects + verbatim ПОЛНОЧЬ copy. Hook/CTA = owl + object + type.
- **Do not borrow:** Portuguese lettering, host face, weekend suitcase, horror/skulls, bot prize, prior triggers (СУББОТА / WEEKEND / …).

## Typography

Verbatim only. Headline > body > magenta script trigger. Safe 12% from seams and edges. No extra labels. No Victoria signature. No word «Сцена».

## Handoff

`HANDOFF_NEXT: slice` — один master 3:4@4K, seam cut. Не motion. Не publish.
