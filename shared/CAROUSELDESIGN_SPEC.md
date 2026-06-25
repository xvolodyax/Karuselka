# CarouselDesign Contract — Спецификация формата

**CarouselDesign Contract (`CAROUSELDESIGN.md`)** — дизайн-контракт для Instagram-карусели grid 3×3: 9 панелей из одного master.

Формат аналогичен AURA `AURADESIGN.md`: YAML frontmatter + markdown prose.

---

## 1. Двухслойная архитектура

```md
---
# Слой 1: машиночитаемые токены
name: Brand Carousel Series
format:
  generation_mode: "grid_3x3"
  slide_count: 9
  grid:
    cols: 3
    rows: 3
    order: "row-major"
  master_aspect: "3:4"
  resolution: "4K"
  panel_aspect: "3:4"
colors:
  primary: "#..."
...
---

# Слой 2: логика и правила
## Source Replication Doctrine
...
```

---

## 2. Обязательные YAML-группы

### format

```yaml
format:
  generation_mode: "grid_3x3"
  slide_count: 9
  grid:
    cols: 3
    rows: 3
    order: "row-major"
  master_aspect: "3:4"
  resolution: "4K"
  panel_aspect: "3:4"
```

### colors

Семантические роли: `primary`, `background`, `on-background`, `accent`, `surface`, `outline`.

### typography

Роли для карусели:

- `slide-headline` — заголовок слайда (крупный, hook на slide 1)
- `slide-body` — основной текст
- `slide-cta` — кнопка/призыв на slide 9
- `slide-number` — нумерация (pill bottom-right)

### grid

```yaml
grid:
  cols: 3
  rows: 3
  order: "row-major"
  gutters_px: 3
  cell_is_self_contained: true
  animate_slide: 1
```

### carousel_system

```yaml
carousel_system:
  carousel_family: "brand_collage"
  narrative: "hook-value-cta"
  slide_roles:
    - hook
    - value
    - value
    - value
    - value
    - value
    - save
    - save
    - cta
```

---

## 3. Markdown prose (слой 2)

Обязательные секции:

- `## Source Replication Doctrine` — референс = закон
- `## Composition Lock` — что фиксировано на всех 9 панелях
- `## Philosophy & Vibe` — конкретно, без «premium/modern»
- `## Grid Rules` — 3×3, gutters, row-major order, self-contained cells
- `## Color Guidance`
- `## Typography & Readability` — лимиты символов, контраст
- `## Slide Rhythm` — hook → value → CTA
- `## Do's and Don'ts`

---

## 4. Связанные артефакты

| Файл | Назначение |
|------|------------|
| `CAROUSEL_SERIES_CONCEPT.md` + `.json` | Series lock: family, palette, prompts |
| `CAROUSEL_SLIDE_BLUEPRINTS.json` | Per-slide layout + copy zones |
| `CAROUSEL_SOURCE_DECOMPOSITION.json` | Разбор референса |
| `CAROUSEL_VISUAL_INVENTORY.json` | Зоны и assets |
| `CAROUSEL_ASSET_REGISTRY.json` | MCP URLs |
| `CAROUSEL_STYLE_MATCH_SCORECARD.md` | Fidelity score |

---

## 5. Linter (carusel-designer)

- YAML валиден
- `generation_mode` = `grid_3x3`
- `slide_count` = 9
- `grid.cols` = 3, `grid.rows` = 3
- Все token refs закрыты
- `carousel_family` ∈ `carousel-family-registry.json`
- WCAG contrast для текста на фоне
