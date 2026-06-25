# Carusel — Master aspect ratio (grid 3×3)

## Default: 9 slides from one 3:4 master

| Параметр | Значение |
|----------|----------|
| Kie `aspect_ratio` | **`3:4`** |
| Kie `resolution` | **`4K`** |
| Сетка | **3×3** |
| Панелей | **9** |
| Соотношение панели | **3:4** (master 3:4 ÷ 3×3 → каждая ячейка 3:4) |

Математика: для сетки `cols×rows` с равными ячейками aspect `A`:

```text
master_aspect = (cols × panel_w) / (rows × panel_h)
Для cols=rows=3 и panel 3:4 → master = 3:4
```

## Устаревший режим (6-slide seamless)

| Master | 6480×1350 (4.8:1) | Kie max wide 3:1 — не рекомендуется |
|--------|-------------------|-------------------------------------|

См. `carousel-grid-design.md` для текущего пайплайна.

## Polling

`KIE_POLL_TIMEOUT_SEC=1200`, `KIE_POLL_INTERVAL_SEC=5`  
Опционально `KIE_CALLBACK_URL` + `callBackUrl` в createTask.
