#!/usr/bin/env python3
"""Animate slide-01 via Grok Imagine Video 1.5 Preview (Kie.ai).

Output: loop-ready 5s MP4 for Instagram carousel file1.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

from grok_video_client import (
    DEFAULT_LOOP_PROMPT_RU,
    GrokVideoClient,
    map_aspect_ratio_for_kie,
)
from kie_common import find_env_file

SCRIPT_DIR = Path(__file__).resolve().parent


def is_transient_kie_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return (
        "server exception" in message
        or "failcode') — 500" in message
        or "failcode') - 500" in message
        or " 500" in message
        or "rate limit" in message
        or "temporarily" in message
    )


def trim_or_loop_video(src: Path, dest: Path, duration: int) -> Path:
    """Trim to duration; if ffmpeg missing, copy as-is."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("WARN: ffmpeg not found — saving raw download without trim/loop", file=sys.stderr)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.resolve() != dest.resolve():
            dest.write_bytes(src.read_bytes())
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    # Trim to exact duration; stream_loop helps short clips feel continuous
    cmd = [
        ffmpeg,
        "-y",
        "-stream_loop",
        "2",
        "-i",
        str(src),
        "-t",
        str(duration),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(dest),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return dest


def resolve_image_url(args: argparse.Namespace, workspace: Path) -> str:
    if args.image_url:
        return args.image_url.strip()

    if args.prompt_json:
        p = Path(args.prompt_json)
        if not p.is_absolute():
            p = workspace / p
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            urls = data.get("image_urls") or []
            if urls:
                return urls[0]

    url_file = workspace / "carusel-memory/output/slide-01-url.txt"
    if url_file.exists():
        text = url_file.read_text(encoding="utf-8").strip()
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("http"):
                return line

    local_png = workspace / "carusel-memory/output/slides/slide-01.png"
    raise ValueError(
        "HTTPS image URL required for Grok video API.\n"
        "Use --image-url, or set image_urls in CAROUSEL_VIDEO_PROMPT.json,\n"
        "or upload slide-01.png to Kie and write URL to carusel-memory/output/slide-01-url.txt\n"
        f"Local PNG exists: {local_png.exists()} — upload before animate, do NOT reuse publish-urls file1 (video)."
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Grok video for carousel slide 1")
    p.add_argument("--image-url", help="HTTPS URL of slide-01.png")
    p.add_argument(
        "--prompt-json",
        default="carusel-memory/design/CAROUSEL_VIDEO_PROMPT.json",
        help="Video prompt JSON",
    )
    p.add_argument("--prompt", help="Override motion prompt (English)")
    p.add_argument("--duration", type=int, default=5, help="Seconds (1-15, default 5)")
    p.add_argument(
        "--aspect-ratio",
        default="3:4",
        help="Carousel contract aspect (3:4 maps to Kie auto before createTask)",
    )
    p.add_argument("--resolution", default="720p", choices=["480p", "720p"])
    p.add_argument(
        "--output",
        "-o",
        default="carusel-memory/output/video/slide-01.mp4",
        help="Output MP4 path",
    )
    p.add_argument("--workspace", default=".", help="Workspace root")
    p.add_argument("--task-log", default="carusel-memory/output/grok-video-task-log.json")
    p.add_argument("--raw-out", help="Save raw download before ffmpeg trim")
    p.add_argument("--api-key", help="Override KIE_API_KEY")
    p.add_argument("--no-nsfw-checker", action="store_true")
    p.add_argument("--max-retries", type=int, default=2, help="Retry transient Kie 500/temporary failures")
    p.add_argument(
        "--verify-png",
        default="carusel-memory/output/slides/slide-01.png",
        help="Local PNG for post-animate frame-0 MAE check (empty to skip)",
    )
    p.add_argument(
        "--qa-mae-threshold",
        type=float,
        default=35.0,
        help="Fail if frame-0 MAE vs verify-png exceeds threshold",
    )
    p.add_argument("--skip-qa", action="store_true", help="Skip post-animate frame QA")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    env_file = find_env_file()
    if env_file:
        print(f"Env: {env_file}")

    try:
        image_url = resolve_image_url(args, workspace)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    prompt = args.prompt
    duration = args.duration
    aspect_ratio = args.aspect_ratio
    resolution = args.resolution

    prompt_path = Path(args.prompt_json)
    if not prompt_path.is_absolute():
        prompt_path = workspace / prompt_path
    if prompt_path.exists():
        data = json.loads(prompt_path.read_text(encoding="utf-8"))
        prompt = prompt or data.get("prompt")
        duration = data.get("duration", duration)
        aspect_ratio = data.get("aspect_ratio", aspect_ratio)
        resolution = data.get("resolution", resolution)
    if not prompt:
        print(
            "ERROR: Пустой prompt. Сначала запусти carusel-motion-director.",
            file=sys.stderr,
        )
        return 1

    client = GrokVideoClient(api_key=args.api_key)
    requested_aspect = aspect_ratio
    kie_aspect = map_aspect_ratio_for_kie(aspect_ratio)
    print(
        f"Grok video: duration={duration}s, aspect={requested_aspect} "
        f"(Kie {kie_aspect}), res={resolution}"
    )
    print(f"Image URL: {image_url[:80]}...")

    attempts: list[dict[str, str | int]] = []
    task_id = ""
    data: dict = {}
    max_attempts = max(1, args.max_retries + 1)
    for attempt in range(1, max_attempts + 1):
        try:
            task_id = client.create_task(
                image_urls=[image_url],
                prompt=prompt,
                aspect_ratio=kie_aspect,
                resolution=resolution,
                duration=duration,
                nsfw_checker=not args.no_nsfw_checker,
            )
            print(f"taskId: {task_id} (attempt {attempt}/{max_attempts})")
            data = client.wait_for_task(task_id)
            attempts.append({"attempt": attempt, "taskId": task_id, "status": "success"})
            break
        except RuntimeError as exc:
            attempts.append(
                {"attempt": attempt, "taskId": task_id or "createTask_failed", "status": "failed", "error": str(exc)}
            )
            if attempt >= max_attempts or not is_transient_kie_error(exc):
                raise
            delay = min(15, 3 * attempt)
            print(f"WARN: transient Grok/Kie failure; retrying in {delay}s ({exc})", file=sys.stderr)
            time.sleep(delay)

    urls = client.extract_result_urls(data)
    if not urls:
        print("ERROR: No resultUrls in video task", file=sys.stderr)
        return 1

    output = Path(args.output)
    if not output.is_absolute():
        output = workspace / output

    raw_path = Path(args.raw_out) if args.raw_out else workspace / "carusel-memory/output/video/slide-01-raw.mp4"
    if not raw_path.is_absolute():
        raw_path = workspace / raw_path

    client.download(urls[0], raw_path)
    print(f"Downloaded raw: {raw_path}")

    trim_or_loop_video(raw_path, output, duration)
    print(f"Output: {output} ({duration}s target)")

    qa_result: dict | None = None
    if not args.skip_qa and args.verify_png:
        verify_png = Path(args.verify_png)
        if not verify_png.is_absolute():
            verify_png = workspace / verify_png
        if verify_png.exists():
            try:
                from video_frame_qa import compare_video_to_png

                qa_result = compare_video_to_png(
                    output,
                    verify_png,
                    mae_threshold=args.qa_mae_threshold,
                )
                status = "PASS" if qa_result["pass"] else "FAIL"
                print(f"QA frame0 vs {verify_png.name}: MAE={qa_result['mae']} ({status})")
                if not qa_result["pass"]:
                    print(
                        f"ERROR: video frame 0 does not match source PNG "
                        f"(MAE {qa_result['mae']} > {args.qa_mae_threshold}). "
                        "Re-upload slide-01.png and re-animate.",
                        file=sys.stderr,
                    )
                    return 1
            except Exception as exc:
                print(f"WARN: video QA skipped: {exc}", file=sys.stderr)

    log_path = Path(args.task_log)
    if not log_path.is_absolute():
        log_path = workspace / log_path
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        json.dumps(
            {
                "taskId": task_id,
                "attempts": attempts,
                "model": "grok-imagine-video-1-5-preview",
                "resultUrls": urls,
                "image_url": image_url,
                "duration": duration,
                "aspect_ratio_requested": requested_aspect,
                "aspect_ratio": kie_aspect,
                "local_raw": str(raw_path.resolve()),
                "local_output": str(output.resolve()),
                "prompt": prompt,
                "qa_frame0": qa_result,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Task log: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
