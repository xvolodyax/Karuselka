# CAROUSEL_IMAGE_PROMPT — Пинг vs шаг

written_by: carusel-image-prompter  
lang: ru  
visual_family / carousel_family: `animals_viktoria_collage`  
generation_mode: `grid_3x3`  
model: `gpt-image-2-image-to-image`  
aspect_ratio: `3:4`  
resolution: `4K`  
face_lock: `victoria-sheet.png`  
slice_method: `seam`  
prompt_compacted: true  
prompt_char_count: 4030  
Kie: rebuild with Excalibur i2i + seam slice

Machine JSON: `carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json`  
Copy source: `carusel-memory/design/CAROUSEL_SLIDE_COPY.json` — verbatim only. No invented slogans.

## Style lock

Night-fashion collage, not occult horror and not beige lifestyle.

| Role | Hex |
|------|-----|
| background | `#111111`–`#1a1a1a` |
| type | `#ffffff` |
| accent | `#ff006e` |
| metal | `#c4a35a` |

Heavy white grotesque headlines. Thin magenta script / torn-tape pills only for words already in the slide copy. Type layers behind and in front of subjects in the scene. Safe margin ≥10–12% from every white seam and from every cell edge.

## Reference contract

| File | Role |
|------|------|
| `carusel-memory/references/animals-viktoria-style-lock.png` | style + layout + palette |
| `carusel-memory/references/victoria-sheet.png` | ONLY face + hair lock |

**Preserve:** charcoal field, magenta + white type, torn-paper pills, animals-as-metaphor, Victoria on 1+9, 3×3 seamed canvas (thin white gutters).

**Change:** topic objects and exact copy (night ping at 23:42, leash/hook, ПИНГ vs ШАГ table, three-layer decode, three-question checklist), this-pack wardrobe, animal seats cat/dog/owl.

**Do not borrow:** Portuguese, foreign faces, Alena, ivory-blazer studio, sheet outfit/pose, platinum hair, horror table, slogans not in the copy JSON, raw URLs.

## Face + wardrobe (this pack)

Victoria **only** on slides 1 and 9. Same woman. Eyes green with a slight hazel mix. Warm honey / wheat blonde with darker roots as on the sheet. Never lighten.

- **Slide 1 (NEW):** deep burgundy satin blouse, open collar, black high-waist trousers. Seated on a dark bed edge, 3/4, looking down at a phone in her left hand. Screen glow. Hair loose over one shoulder.
- **Slide 9 (NEW, different pose):** black leather jacket over a fitted charcoal turtleneck, dark chocolate wide-leg trousers. Standing 3/4, chin slightly lifted, looking at camera, right hand relaxed at her side.

Banned looks live in `negative_prompt` only (platinum, Alena, white cami, jeans from sheet, ivory blazer, other women's faces).

## Animals

| Slide | Animal | Job |
|-------|--------|-----|
| 1 | cat | stares at the notification — «чуешь» |
| 2 | dog | sits by the glowing screen — loyalty to the unanswered question |
| 4 | owl | night watch — cold scan / night thoughts |

No animals on 3, 5–9. No Victoria on 2–8.

## Verbatim panel copy

Quoted from `CAROUSEL_SLIDE_COPY.json`. Do not substitute.

1. hook — «Он молчал 24 дня. В 23:42: «Спишь?»» / «Ровно в тот вечер, когда ты перестала проверять его страницу.»
2. problem — «Сердце колотится, как месяц назад» / «Снова бессонная ночь и скриншоты подругам: «Он скучал? Он всё понял?»»
3. mistake — «Ловушка: принять импульс за любовь» / «Ты ищешь знаки судьбы там, где человек просто проверяет длину поводка.»
4. mechanism — «Это не шаг. Это обычный пинг» / «Нулевые затраты. Он почуял потерю контроля и бросил крючок: «Ты ещё ждёшь?»»
5. save A — «Разница: пустой пинг vs шаг» / «ПИНГ: ночные смс, реакции на сторис, ноль действий.» / «ШАГ: звонок днём, конкретное место и время встречи.»
6. save B — «Что он пишет vs что ты слышишь» / «Пишет: «Вспоминаю нас».» / «Слышишь: «Хочет вернуть».» / «В реальности: «Ищу бесплатное подтверждение своей важности».»
7. save C — «3 вопроса перед тем, как ответить» / «1. Есть ли в сообщении действие?» / «2. Изменилось ли что-то в его отношении?» / «3. Готова ли снова ждать 3 недели?»
8. recap — «Правило, которое бережёт тебя» / «Тот, кто хочет быть рядом — делает шаг. Тот, кому скучно — шлёт пинг. Не соглашайся на проверку связи.»
9. cta — «Что на самом деле за его смс?» / «Напиши ШАГ в комментариях» / «Напиши в комментариях слово ШАГ. Пришлём в Direct 3 бесплатных расклада в боте.» Huge magenta script **ШАГ**.

## Grid

Master one image, 3:4 @ 4K, `generation_mode: grid_3x3`, `slice_method: seam`. Row-major 01 02 03 / 04 05 06 / 07 08 09. Thin white gutters at 1/3 and 2/3; code cuts on those seams. Each cell is a standalone 3:4 panel. Slide 1 is motion-friendly (phone glow, cat micro-move; type stays still).

## Negative (Kie)

platinum, Alena, white cami, jeans from sheet, ivory blazer, other women's faces, Portuguese, horror — plus strip/gutter/watermark extras in JSON.

## Handoff

Prompt ready. Do **not** invent copy. Next: **slice** (Kie i2i + 3×3 cut). Image-prompter does not generate pixels.
