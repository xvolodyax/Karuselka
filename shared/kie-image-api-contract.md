# Carusel — Kie.ai Image API (без MCP)

Генерация изображений **только через скрипты**, не через `user-mcp-kv/gpt-image-2`.

## API Key

Файл с ключом (создан, вставь ключ сам):

```
<WORKSPACE>\.env
```

Шаблон: `<WORKSPACE>\.env.example`

```env
KIE_API_KEY=твой_ключ_с_https://kie.ai/api-key
```

`.env` в `.gitignore` — ключ не попадёт в git.

## Endpoints

| Шаг | Method | URL |
|-----|--------|-----|
| Create task | POST | `https://api.kie.ai/api/v1/jobs/createTask` |
| Poll status | GET | `https://api.kie.ai/api/v1/jobs/recordInfo?taskId=...` |

- **model:** `gpt-image-2-image-to-image`
- **Auth:** `Authorization: Bearer KIE_API_KEY`

## Скрипты

| Файл | Назначение |
|------|------------|
| `scripts/kie_client.py` | API client (create, poll, download) |
| `scripts/kie_run_prompt.py` | main CLI: prompt JSON → grid generation |
| `scripts/kie_carousel_gen.py` | grid_3x3 create/poll/download + fallback |
| `scripts/slice_grid.py` | master → 3×3 → 9 slides |
| `scripts/kie_image_gen.py` | legacy wide CLI |
| `scripts/slice_carousel.py` | legacy 6-slide horizontal |

## Рекомендуемые параметры карусели (grid 3×3)

| Param | Value | Почему |
|-------|-------|--------|
| `generation_mode` | `grid_3x3` | 1 Kie task → 9 панелей |
| aspect_ratio | **`3:4`** | master = сетка 3×3 панелей 3:4 |
| resolution | **`4K`** | Kie 4K-supported portrait mode |
| input_urls | HTTPS референс | i2i style lock |

После скачивания: `slice_grid.py --cols 3 --rows 3` → **9 slides**.

`3:4` — основной режим для grid_3x3. Не просить `4:5` в 4K, если API его не поддерживает.

Legacy wide: `slice_carousel.py` (6-slide horizontal) — deprecated.

## Пример (агент / терминал)

```bash
python <CURSOR_PLUGIN_DIR>/carusel\scripts\kie_run_prompt.py \
  --workspace <WORKSPACE> \
  --prompt-json carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json
```

## Логи

- `carusel-memory/output/kie-task-log.json` — taskId, resultUrls
- `carusel-memory/design/CAROUSEL_IMAGE_GEN_STATUS.md` — статус генерации
- `CAROUSEL_ASSET_REGISTRY.json` — local_path + source URL

## Ошибки

| code | Действие |
|------|----------|
| 401 | Проверить `KIE_API_KEY` в `.env` |
| 402 | Баланс Kie.ai |
| 429 | Подождать, повторить poll |

## Video

Видео для slide 1 — **отдельный скрипт** (когда пришлёшь), тоже без MCP.
