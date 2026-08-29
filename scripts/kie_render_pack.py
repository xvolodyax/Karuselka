#!/usr/bin/env python3
"""Upload viktoriaref.png only, Kie i2i both langs, copy 18 slides.

The file is one frontal photo of Victoria. Never i2i виктория.png (Alena).
Never upload victoria-sheet, victoria.png, alena*, or the style collage as a face.
Does not publish Instagram. Does not rewrite slide copy.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from kie_carousel_gen import run_grid_3x3  # noqa: E402
from kie_client import KieImageClient  # noqa: E402
from kie_file_upload import KieFileUploadClient  # noqa: E402

FACE = REPO / "carusel-memory" / "references" / "viktoriaref.png"
FACE_LOCK = "viktoriaref.png"
UPLOAD_NAME = "viktoriaref.png"
STYLE_LOCK = REPO / "carusel-memory" / "references" / "animals-viktoria-style-lock.png"
DEFAULT_PACK = REPO / "carusel-memory" / "packs" / "2026-08-29"
EYES_RE = re.compile(r"зелён.*карим|green.*hazel|green.*light-brown|green.*hazel-brown", re.I)
ONE_WOMAN_RE = re.compile(r"one woman|одна женщин|same face|одно(го)? лиц|viktoriaref", re.I)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require_face() -> Path:
    if not FACE.is_file() or FACE.stat().st_size < 100_000:
        raise SystemExit(
            "STOP: carusel-memory/references/viktoriaref.png is missing. "
            "git pull — Vladimir already committed it."
        )
    im = Image.open(FACE)
    if im.size[0] < 400 or im.size[1] < 400:
        raise SystemExit(f"viktoriaref.png looks too small for a face lock: {im.size}")
    return FACE


def render_lang(
    pack: Path,
    lang: str,
    face_url: str,
    workspace: Path,
) -> int:
    prompt = load_json(pack / lang / "CAROUSEL_IMAGE_PROMPT.json")
    if FACE_LOCK not in str(prompt.get("face_lock") or ""):
        raise SystemExit(f"{lang}: face_lock must be {FACE_LOCK}")
    active = str(prompt.get("prompt") or "")
    count = int(prompt.get("prompt_char_count") or len(active))
    if len(active) > 2200 or count > 2200:
        raise SystemExit(
            f"{lang}: prompt too long ({max(count, len(active))} chars). "
            "Rewrite short, face first. Do not generate."
        )
    head = active[:500]
    if FACE_LOCK not in head or not EYES_RE.search(head) or not ONE_WOMAN_RE.search(head):
        raise SystemExit(
            f"{lang}: prompt must start with same woman as {FACE_LOCK} + "
            "green/hazel / зелёные с лёгким карим"
        )
    prompt["slice_method"] = "seam"
    prompt["input_urls"] = [face_url]
    prompt["i2i_source"] = "carusel-memory/references/viktoriaref.png"
    prompt["i2i_file_name"] = UPLOAD_NAME
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
        [face_url],
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
    parser = argparse.ArgumentParser(description="Kie i2i pack render from viktoriaref.png only")
    parser.add_argument("--pack", default=str(DEFAULT_PACK))
    parser.add_argument("--langs", default="ru,en")
    args = parser.parse_args(argv)
    face = require_face()
    pack = Path(args.pack).expanduser().resolve()
    uploader = KieFileUploadClient()
    print(f"Uploading identity sheet {face} as {UPLOAD_NAME} ...")
    print(f"Style collage not uploaded ({STYLE_LOCK.name} is palette only).")
    face_url = uploader.upload_local(
        face, upload_path="carusel-face-lock", file_name=UPLOAD_NAME
    )
    print(f"face_url={face_url}")

    for lang in [x.strip() for x in args.langs.split(",") if x.strip()]:
        workspace = Path(f"/tmp/kie-pack-{lang}")
        if workspace.exists():
            shutil.rmtree(workspace)
        workspace.mkdir(parents=True)
        print(f"=== Kie i2i {lang} from {FACE_LOCK} ===")
        rc = render_lang(pack, lang, face_url, workspace)
        if rc != 0:
            return rc
    print("18 slides written from viktoriaref.png. Do not publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
