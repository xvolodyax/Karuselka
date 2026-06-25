# Carusel — Image Generation (Kie.ai)

> Генерация через **скрипт** `kie_image_gen.py`, ключ в **`.env`**. MCP не используем.

## API Key — вставь сюда

**Файл:**

`<WORKSPACE>\.env`

```env
KIE_API_KEY=твой_ключ
```

Получить ключ: https://kie.ai/api-key

## Поток

```text
CAROUSEL_IMAGE_PROMPT.json + HTTPS reference
        ↓
kie_run_prompt.py / kie_carousel_gen.py (grid_3x3, 4K, 3:4)
        ↓
source.png -> slice_grid.py -> 9 slides (3×3)
```

## Размеры

| Этап | Размер |
|------|--------|
| Kie output (4K) | `3:4` |
| Grid | **3×3** |
| Слайды | **9 equal cells** |

## Команда для `carusel-designer` / `carusel-slice`

См. `shared/kie-image-api-contract.md`

## Статус

`carusel-memory/design/CAROUSEL_IMAGE_GEN_STATUS.md`
