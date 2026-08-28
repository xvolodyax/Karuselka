#!/usr/bin/env python3
"""Upload cropped victoria-sheet close-up, Kie i2i both langs, copy 18 slides.

Refuses the full 12-up grid and Alena. Will not invent a face.
Does not publish Instagram.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from crop_victoria_sheet_tight import crop_front_closeup  # noqa: E402
from kie_carousel_gen import run_grid_3x3  # noqa: E402
from kie_client import KieImageClient  # noqa: E402
from kie_file_upload import KieFileUploadClient  # noqa: E402

SHEET = REPO / "carusel-memory" / "references" / "victoria-sheet.png"
FRONT = REPO / "carusel-memory" / "references" / "victoria-sheet-front.png"
ALENA = Path("/workspace/cover-refs/victoria.png")
DEFAULT_PACK = REPO / "carusel-memory" / "packs" / "2026-08-28"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require_front_crop() -> Path:
    if ALENA.is_file():
        print(
            "NOTE: /workspace/cover-refs/victoria.png is Alena — will not upload it.",
            file=sys.stderr,
        )
    if not SHEET.is_file() or SHEET.stat().st_size < 10_000:
        raise SystemExit(
            "STOP: carusel-memory/references/victoria-sheet.png is missing. "
            "That file is the ONLY Victoria face lock. "
            "Do not invent a stand-in. Do not use cover-refs/victoria.png (Alena)."
        )
    if not FRONT.is_file() or FRONT.stat().st_size < 1000:
        crop_front_closeup(SHEET, FRONT)
    im = Image.open(FRONT)
    if im.size[0] > 500 or im.size[1] > 400:
        raise SystemExit(f"i2i crop is still a grid: {im.size}. Crop the left frontal close-up only.")
    return FRONT


def render_lang(
    pack: Path,
    lang: str,
    sheet_url: str,
    workspace: Path,
) -> int:
    prompt = load_json(pack / lang / "CAROUSEL_IMAGE_PROMPT.json")
    if prompt.get("face_lock") != "victoria-sheet.png":
        raise SystemExit(f"{lang}: face_lock must be victoria-sheet.png")
    active = str(prompt.get("prompt") or "")
    count = int(prompt.get("prompt_char_count") or len(active))
    if len(active) > 2200 or count > 2200:
        raise SystemExit(
            f"{lang}: prompt too long ({max(count, len(active))} chars). "
            "Rewrite short, face first. Do not generate."
        )
    prompt["slice_method"] = "seam"
    # Excalibur: cropped close-up first and only. Style plate teaches stickers.
    prompt["input_urls"] = [sheet_url]
    copy_src = pack / lang / "CAROUSEL_SLIDE_COPY.json"
    design = workspace / "carusel-memory" / "design"
    design.mkdir(parents=True, exist_ok=True)
    shutil.copy2(copy_src, design / "CAROUSEL_SLIDE_COPY.json")
    write_json(design / "CAROUSEL_IMAGE_PROMPT.json", prompt)

    client = KieImageClient()
    task_log = workspace / "carusel-memory" / "output" / "kie-task-log.json"
    rc = run_grid_3x3(
        client,
        prompt,
        workspace,
        task_log,
        prompt.get("resolution") or "4K",
        [sheet_url],
        None,
    )
    if rc != 0:
        return rc

    dest = pack / lang / "slides"
    dest.mkdir(parents=True, exist_ok=True)
    src_slides = workspace / "carusel-memory" / "output" / "slides"
    for i in range(1, 10):
        src = src_slides / f"slide-{i:02d}.png"
        if not src.is_file():
            print(f"ERROR: {lang} missing {src}", file=sys.stderr)
            return 1
        shutil.copy2(src, dest / f"slide-{i:02d}.png")
    master = workspace / "carusel-memory" / "output" / "master" / "master.png"
    if master.is_file():
        shutil.copy2(master, pack / lang / "master.png")
    if task_log.is_file():
        shutil.copy2(task_log, pack / lang / "kie-task-log.json")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Kie i2i pack render from victoria-sheet close-up")
    parser.add_argument("--pack", default=str(DEFAULT_PACK))
    parser.add_argument("--langs", default="ru,en")
    args = parser.parse_args(argv)
    front = require_front_crop()
    pack = Path(args.pack).expanduser().resolve()
    uploader = KieFileUploadClient()
    print(f"Uploading face close-up {front} as victoria-sheet.png ...")
    sheet_url = uploader.upload_local(
        front, upload_path="carusel-face-lock", file_name="victoria-sheet.png"
    )
    print(f"sheet_url={sheet_url}")
    print("Style lock not uploaded for i2i (sticker plate). Palette is in the prompt.")

    for lang in [x.strip() for x in args.langs.split(",") if x.strip()]:
        workspace = Path(f"/tmp/kie-pack-{lang}")
        if workspace.exists():
            shutil.rmtree(workspace)
        workspace.mkdir(parents=True)
        print(f"=== Kie i2i {lang} ===")
        rc = render_lang(pack, lang, sheet_url, workspace)
        if rc != 0:
            return rc
    print("18 slides written. Do not publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
