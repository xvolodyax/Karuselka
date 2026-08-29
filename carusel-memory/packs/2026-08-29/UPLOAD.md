# UPLOAD — 2026-08-29 Labels / Статус

status: ok
this_run: static_all_pngs
provider: kie_file_upload_api
file1_kind: png
slide_01: static PNG (not MP4)
published: no
expires: ~24h on Kie tempfile

Pipeline `carusel-memory/output/publish-urls.json` = **RU** (lang=ru).

## Run IDs

| lang | run_id | Kie uploadPath | handle |
|------|--------|----------------|--------|
| ru | `2026-08-29-1110-static-ru` | `carusel/instagram/2026-08-29-1110-static-ru` | @todaytaro_ru |
| en | `2026-08-29-1110-static-en` | `carusel/instagram/2026-08-29-1110-static-en` | @todaytaro_bot |

## RU — 9 HTTPS (file1 = slide-01.png)

1. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-ru/slide-01.png
2. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-ru/slide-02.png
3. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-ru/slide-03.png
4. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-ru/slide-04.png
5. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-ru/slide-05.png
6. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-ru/slide-06.png
7. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-ru/slide-07.png
8. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-ru/slide-08.png
9. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-ru/slide-09.png

JSON: `carusel-memory/packs/2026-08-29/ru/publish-urls.json`  
Pipeline copy: `carusel-memory/output/publish-urls.json`

## EN — 9 HTTPS (file1 = slide-01.png)

1. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-en/slide-01.png
2. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-en/slide-02.png
3. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-en/slide-03.png
4. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-en/slide-04.png
5. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-en/slide-05.png
6. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-en/slide-06.png
7. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-en/slide-07.png
8. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-en/slide-08.png
9. https://tempfile.redpandaai.co/kieai/378019/carusel/instagram/2026-08-29-1110-static-en/slide-09.png

JSON: `carusel-memory/packs/2026-08-29/en/publish-urls.json`

## Command

```
python3 scripts/upload_carousel_assets.py \
  --workspace /workspace \
  --run-id 2026-08-29-1110-static-ru \
  --static-all-pngs \
  --slides-dir carusel-memory/packs/2026-08-29/ru/slides \
  --lang ru

python3 scripts/upload_carousel_assets.py \
  --workspace /workspace \
  --run-id 2026-08-29-1110-static-en \
  --static-all-pngs \
  --slides-dir carusel-memory/packs/2026-08-29/en/slides \
  --lang en \
  --output carusel-memory/packs/2026-08-29/en/publish-urls.json
```

HANDOFF_NEXT: publish via Composio. This pack is already-live — do not republish.
