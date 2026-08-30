#!/usr/bin/env python3
"""Kie render: style lock only. No host face ref.

Do not upload Виктория.png / viktoriaref / victoria-sheet.
Style collage is palette / rhythm only.
Does not publish Instagram. Does not rewrite slide copy.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from face_gate import FACE_FILE_RE, NO_FACE, is_live_host_face_pack  # noqa: E402
from kie_carousel_gen import run_grid_3x3  # noqa: E402
from kie_client import KieImageClient  # noqa: E402
from kie_file_upload import KieFileUploadClient  # noqa: E402

STYLE_LOCK = REPO / "carusel-memory" / "references" / "animals-viktoria-style-lock.png"
DEFAULT_PACK = REPO / "carusel-memory" / "packs" / "2026-08-30-ru-noface"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require_style() -> Path:
    if not STYLE_LOCK.is_file() or STYLE_LOCK.stat().st_size < 10_000:
        raise SystemExit(
            "STOP: carusel-memory/references/animals-viktoria-style-lock.png is missing."
        )
    return STYLE_LOCK


def render_lang(
    pack: Path,
    lang: str,
    style_url: str,
    workspace: Path,
) -> int:
    prompt = load_json(pack / lang / "CAROUSEL_IMAGE_PROMPT.json")
    lock = str(prompt.get("face_lock") or "")
    if lock not in {NO_FACE, "no_host", "absent", ""}:
        raise SystemExit(f"{lang}: face_lock must be {NO_FACE} (no host portrait)")
    active = str(prompt.get("prompt") or "")
    count = int(prompt.get("prompt_char_count") or len(active))
    if len(active) > 2200 or count > 2200:
        raise SystemExit(
            f"{lang}: prompt too long ({max(count, len(active))} chars). "
            "Rewrite short. Do not generate."
        )
    if FACE_FILE_RE.search(active) and "не " not in active.lower() and "no " not in active.lower():
        raise SystemExit(f"{lang}: prompt still treats a face file as a lock")
    if FACE_FILE_RE.search(json.dumps(prompt.get("input_urls") or [])):
        raise SystemExit(f"{lang}: do not put a face ref in input_urls")
    prompt["slice_method"] = "seam"
    prompt["face_lock"] = NO_FACE
    prompt["input_urls"] = [style_url]
    prompt["i2i_source"] = "carusel-memory/references/animals-viktoria-style-lock.png"
    prompt["i2i_file_name"] = STYLE_LOCK.name
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
        [style_url],
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
    parser = argparse.ArgumentParser(description="Kie render without host face ref")
    parser.add_argument("--pack", default=str(DEFAULT_PACK))
    parser.add_argument("--langs", default="ru")
    args = parser.parse_args(argv)
    pack = Path(args.pack).expanduser().resolve()
    manifest = load_json(pack / "PACK.json") if (pack / "PACK.json").is_file() else {}
    pack_id = str(manifest.get("pack_id") or pack.name)
    if is_live_host_face_pack(pack_id):
        raise SystemExit(
            f"STOP: {pack_id} is a live host-face pack. Do not rebuild it."
        )
    style = require_style()
    uploader = KieFileUploadClient()
    print(f"Uploading style lock {style.name} (palette only, not a face) ...")
    style_url = uploader.upload_local(
        style, upload_path="carusel-style-lock", file_name=style.name
    )
    print(f"style_url={style_url}")

    for lang in [x.strip() for x in args.langs.split(",") if x.strip()]:
        if lang == "en":
            print("EN skipped by contract (do not rebuild WEEKEND).", file=sys.stderr)
            continue
        workspace = Path(f"/tmp/kie-pack-{lang}")
        if workspace.exists():
            shutil.rmtree(workspace)
        workspace.mkdir(parents=True)
        print(f"=== Kie i2i {lang} style-only, no host face ===")
        rc = render_lang(pack, lang, style_url, workspace)
        if rc != 0:
            return rc
    print("RU slides written with no host face ref. Do not touch EN. Do not delete old СУББОТА.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
