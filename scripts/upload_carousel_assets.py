#!/usr/bin/env python3
"""Upload carousel assets via Kie.ai File Upload API → publish-urls.json.

- file1 (video, default): URL Upload from Grok result URL, or Stream Upload local mp4
- file2–file9: Stream Upload local PNG slides 2–9 (slide-01 = video)
- --static-all-pngs: stream-upload ALL 9 PNGs; slide-01.png is file1 (no video)

Docs: https://docs.kie.ai/file-upload-api/quickstart
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from kie_file_upload import KieFileUploadClient

UPLOAD_PATH = "carusel/instagram"


def resolve_run_id(workspace: Path) -> str | None:
    caption = workspace / "carusel-memory/design/CAROUSEL_CAPTION.json"
    if caption.exists():
        data = json.loads(caption.read_text(encoding="utf-8"))
        rid = data.get("run_id")
        if isinstance(rid, str) and rid.strip():
            return rid.strip()
    brief = workspace / "carusel-memory/00-brief.md"
    if brief.exists():
        m = re.search(r"\*\*run_id:\*\*\s*(\S+)", brief.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    return None


def resolve_video(
    workspace: Path,
    client: KieFileUploadClient,
    upload_path: str,
    force_stream: bool,
    video_path: Path | None = None,
) -> tuple[str, str, dict | None]:
    if video_path:
        if not video_path.exists():
            raise FileNotFoundError(f"video path not found: {video_path}")
        print(f"Video: stream upload explicit local mp4 {video_path.name}")
        meta = client.upload_stream(video_path, upload_path=upload_path, file_name="slide-01.mp4")
        return meta["publicUrl"], "kie_stream_upload_local_video", meta

    grok_log = workspace / "carusel-memory/output/grok-video-task-log.json"
    if grok_log.exists() and not force_stream:
        data = json.loads(grok_log.read_text(encoding="utf-8"))
        grok_urls = data.get("resultUrls") or []
        if grok_urls and str(grok_urls[0]).startswith("http"):
            grok_url = str(grok_urls[0])
            print(f"Video: URL upload from Grok -> Kie ({grok_url[:70]}...)")
            meta = client.upload_from_url(
                grok_url,
                upload_path=upload_path,
                file_name="slide-01.mp4",
            )
            return meta["publicUrl"], "kie_url_upload_from_grok", meta

    local_mp4 = workspace / "carusel-memory/output/video/slide-01.mp4"
    if local_mp4.exists():
        print(f"Video: stream upload {local_mp4.name}")
        meta = client.upload_stream(local_mp4, upload_path=upload_path, file_name="slide-01.mp4")
        return meta["publicUrl"], "kie_stream_upload", meta

    raise FileNotFoundError(
        "Нет видео: grok-video-task-log.json без resultUrls и slide-01.mp4 не найден"
    )


def image_size(path: Path) -> tuple[int, int]:
    from PIL import Image

    with Image.open(path) as img:
        return img.size


def video_size(path: Path) -> tuple[int, int] | None:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "json",
        str(path),
    ]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    data = json.loads(proc.stdout or "{}")
    streams = data.get("streams") or []
    if not streams:
        return None
    return int(streams[0]["width"]), int(streams[0]["height"])


def normalize_video_to_slide_size(workspace: Path, video_path: Path, slides_dir: Path) -> tuple[Path, dict]:
    slide_ref = slides_dir / "slide-02.png"
    if not slide_ref.exists():
        slide_ref = slides_dir / "slide-01.png"
    if not slide_ref.exists():
        raise FileNotFoundError("cannot normalize video: no slide PNG found for target size")

    target_w, target_h = image_size(slide_ref)
    source_size = video_size(video_path)
    if source_size == (target_w, target_h):
        return video_path, {
            "applied": False,
            "source_size": source_size,
            "target_size": (target_w, target_h),
            "reason": "already matches slide PNG size",
        }

    out = workspace / f"carusel-memory/output/video/slide-01-publish-{target_w}x{target_h}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = (
        f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
        f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2,setsar=1"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "copy",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    return out, {
        "applied": True,
        "source_size": source_size,
        "target_size": (target_w, target_h),
        "output": str(out),
        "method": "fit+pad, no crop",
    }


def resolve_workspace_path(workspace: Path, raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    path = Path(raw_path)
    if not path.is_absolute():
        path = workspace / path
    return path.resolve()


def main() -> int:
    p = argparse.ArgumentParser(description="Kie.ai upload → publish-urls.json")
    p.add_argument("--workspace", default=".")
    p.add_argument("--upload-path", default=UPLOAD_PATH, help="Kie uploadPath folder")
    p.add_argument(
        "--method",
        choices=["auto", "stream", "url", "base64"],
        default="auto",
        help="auto: stream для PNG, url для Grok video",
    )
    p.add_argument(
        "--reupload-video-stream",
        action="store_true",
        help="Не использовать URL upload для Grok — залить локальный mp4 stream",
    )
    p.add_argument(
        "--video-path",
        help="Локальный mp4 для file1; stream upload вместо Grok URL",
    )
    p.add_argument(
        "--normalized-video-path",
        help="Alias для --video-path: уже нормализованный локальный mp4 для file1",
    )
    p.add_argument(
        "--normalize-video-to-slides",
        action="store_true",
        help="Fit+pad локальный mp4 к размеру PNG slides перед stream upload (requires ffmpeg)",
    )
    p.add_argument(
        "--output",
        default="carusel-memory/output/publish-urls.json",
    )
    p.add_argument(
        "--run-id",
        help="Scope Kie uploadPath (carusel/instagram/{run_id}) — unique URLs per run",
    )
    p.add_argument(
        "--upload-path-suffix",
        help="Append suffix to run-scoped Kie path, e.g. final-YYYYMMDD-HHMMSS",
    )
    p.add_argument(
        "--static-all-pngs",
        action="store_true",
        help="Stream-upload all 9 PNGs; slide-01.png is file1 (no video). Video path stays default.",
    )
    p.add_argument(
        "--slides-dir",
        help="Directory with slide-01.png ... slide-09.png (default: carusel-memory/output/slides)",
    )
    p.add_argument(
        "--lang",
        help="Optional language tag written into publish-urls.json (ru/en)",
    )
    args = p.parse_args()

    workspace = Path(args.workspace).resolve()
    run_id = args.run_id or resolve_run_id(workspace)
    upload_base = args.upload_path.rstrip("/")
    upload_path = upload_base
    if run_id:
        upload_path = f"{upload_base}/{run_id}"
    if args.upload_path_suffix:
        upload_path = f"{upload_path}-{args.upload_path_suffix.strip('/')}"
    slides_dir = resolve_workspace_path(workspace, args.slides_dir) or (
        workspace / "carusel-memory/output/slides"
    )
    client = KieFileUploadClient()
    video_path_arg = args.normalized_video_path or args.video_path
    explicit_video_path = resolve_workspace_path(workspace, video_path_arg)
    video_normalization: dict | None = None
    if args.normalize_video_to_slides and not args.static_all_pngs:
        source_video = explicit_video_path or (workspace / "carusel-memory/output/video/slide-01.mp4")
        explicit_video_path, video_normalization = normalize_video_to_slide_size(
            workspace,
            source_video,
            slides_dir,
        )

    result: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "provider": "kie_file_upload_api",
        "upload_path": upload_path,
        "docs": "https://docs.kie.ai/file-upload-api/quickstart",
        "note": "Файлы на Kie временные (~24ч). Публикуй в Instagram сразу после upload.",
        "files": {},
    }
    if args.lang:
        result["lang"] = args.lang
    if args.static_all_pngs:
        result["file1_kind"] = "png"
        result["this_run"] = "static_all_pngs"

    slide_count = 9

    if args.static_all_pngs:
        for i in range(1, slide_count + 1):
            slide_path = slides_dir / f"slide-{i:02d}.png"
            if not slide_path.exists():
                print(f"ERROR: missing {slide_path}", file=sys.stderr)
                return 1
            if args.method == "base64":
                meta = client.upload_base64(slide_path, upload_path=upload_path)
            else:
                meta = client.upload_stream(
                    slide_path,
                    upload_path=upload_path,
                    file_name=slide_path.name,
                )
            url = meta["publicUrl"]
            if not url.startswith("https://"):
                print(f"ERROR: non-https URL for slide-{i:02d}: {url}", file=sys.stderr)
                return 1
            key = "File3" if i == 3 else f"file{i}"
            result[key] = url
            result[f"slide_{i:02d}"] = url
            result["files"][key] = {
                "local": str(slide_path),
                "url": url,
                "kind": "png",
                "kie_file_id": meta.get("data", {}).get("fileId"),
                "expires_at": meta.get("data", {}).get("expiresAt"),
            }
            print(f"{key}: {url}")
        result["video_source"] = "kie_stream_upload_static_png"
    else:
        try:
            video_url, video_source, video_meta = resolve_video(
                workspace,
                client,
                upload_path,
                force_stream=args.reupload_video_stream or bool(explicit_video_path),
                video_path=explicit_video_path,
            )
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        except subprocess.CalledProcessError as e:
            print(f"ERROR: ffmpeg normalization failed: {e}", file=sys.stderr)
            return 1

        result["file1"] = video_url
        result["slide_01"] = video_url
        result["video_source"] = video_source
        if video_normalization:
            result["video_normalization"] = video_normalization
        if video_meta:
            result["files"]["file1"] = {
                "kie_file_id": video_meta.get("data", {}).get("fileId"),
                "expires_at": video_meta.get("data", {}).get("expiresAt"),
                "url": video_url,
                "local": str(explicit_video_path) if explicit_video_path else None,
            }
        print(f"file1: {video_url}")

        for i in range(2, slide_count + 1):
            slide_path = slides_dir / f"slide-{i:02d}.png"
            if not slide_path.exists():
                print(f"ERROR: missing {slide_path}", file=sys.stderr)
                return 1

            if args.method == "base64":
                meta = client.upload_base64(slide_path, upload_path=upload_path)
            else:
                meta = client.upload_stream(
                    slide_path,
                    upload_path=upload_path,
                    file_name=slide_path.name,
                )

            url = meta["publicUrl"]
            key = "File3" if i == 3 else f"file{i}"
            # file7-file9 are required by the Make scenario; see instagram-publish-contract.md.
            result[key] = url
            result[f"slide_{i:02d}"] = url
            result["files"][key] = {
                "local": str(slide_path),
                "url": url,
                "kie_file_id": meta.get("data", {}).get("fileId"),
                "expires_at": meta.get("data", {}).get("expiresAt"),
            }
            print(f"{key}: {url}")

    out = Path(args.output)
    if not out.is_absolute():
        out = workspace / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
