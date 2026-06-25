#!/usr/bin/env python3
"""Pre-flight publish checks — duplicate URL detection vs publish-log.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

URL_KEYS = ("file1", "file2", "File3", "file4", "file5", "file6", "file7", "file8", "file9")
URL_PATTERN = re.compile(r"https://[^\s`|)]+")
BASENAME_PATTERN = re.compile(r"(slide-\d{2}\.(?:png|mp4))")


def load_publish_urls(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    urls: dict[str, str] = {}
    for key in URL_KEYS:
        val = data.get(key)
        if isinstance(val, str) and val.startswith("http"):
            urls[key] = val
    files = data.get("files")
    if isinstance(files, dict):
        for key, meta in files.items():
            if key in urls:
                continue
            if isinstance(meta, dict):
                u = meta.get("url")
                if isinstance(u, str) and u.startswith("http"):
                    urls[key] = u
    return urls


def url_basenames(urls: dict[str, str] | set[str]) -> set[str]:
    items = urls.values() if isinstance(urls, dict) else urls
    names: set[str] = set()
    for url in items:
        if isinstance(url, str):
            names.add(url.rsplit("/", 1)[-1])
    return names


def basenames_from_log_line(line: str) -> set[str]:
    names = set(BASENAME_PATTERN.findall(line))
    for url in URL_PATTERN.findall(line):
        names.add(url.rsplit("/", 1)[-1])
    return names


def urls_from_log(log_text: str) -> list[dict[str, str | set[str]]]:
    """Extract run blocks with URL and basename sets from publish-log.md."""
    runs: list[dict[str, str | set[str]]] = []
    current_run = ""
    current_urls: set[str] = set()
    current_basenames: set[str] = set()

    for line in log_text.splitlines():
        m_run = re.match(r"^## Run `([^`]+)`", line)
        if m_run:
            if current_run and (current_urls or current_basenames):
                runs.append(
                    {
                        "run_id": current_run,
                        "urls": set(current_urls),
                        "basenames": set(current_basenames),
                    }
                )
            current_run = m_run.group(1)
            current_urls = set()
            current_basenames = set()
            continue
        if "https://" in line or "…/" in line or "slide-" in line:
            for url in URL_PATTERN.findall(line):
                current_urls.add(url.rstrip(".,;"))
            current_basenames |= basenames_from_log_line(line)

    if current_run and (current_urls or current_basenames):
        runs.append(
            {
                "run_id": current_run,
                "urls": set(current_urls),
                "basenames": set(current_basenames),
            }
        )
    return runs


def check_duplicates(
    publish_urls: dict[str, str],
    log_path: Path,
    *,
    current_run_id: str | None,
) -> list[dict[str, str | int]]:
    """Return list of conflicts with prior runs."""
    if not log_path.exists():
        return []

    log_text = log_path.read_text(encoding="utf-8")
    our_urls = set(publish_urls.values())
    our_basenames = url_basenames(publish_urls)
    conflicts: list[dict[str, str | int]] = []

    for entry in urls_from_log(log_text):
        prior_run = str(entry["run_id"])
        if current_run_id and prior_run == current_run_id:
            continue
        prior_urls = entry["urls"]
        prior_basenames = entry["basenames"]
        if not isinstance(prior_urls, set):
            prior_urls = set()
        if not isinstance(prior_basenames, set):
            prior_basenames = set()

        url_overlap = our_urls & prior_urls
        basename_overlap = our_basenames & prior_basenames
        # Block on identical HTTPS URLs. Basename-only overlap is OK when upload_path is run-scoped.
        if len(url_overlap) >= 1:
            sample = next(iter(url_overlap), None) or next(iter(basename_overlap), "")
            conflicts.append(
                {
                    "prior_run_id": prior_run,
                    "overlap_count": max(len(url_overlap), len(basename_overlap)),
                    "sample_url": str(sample),
                }
            )
    return conflicts


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


def main() -> int:
    p = argparse.ArgumentParser(description="Publish pre-flight: duplicate URL check")
    p.add_argument("--workspace", default=".")
    p.add_argument(
        "--publish-urls",
        default="carusel-memory/output/publish-urls.json",
    )
    p.add_argument(
        "--publish-log",
        default="carusel-memory/output/publish-log.md",
    )
    p.add_argument("--run-id", help="Current run_id (default: from caption/brief)")
    args = p.parse_args()

    workspace = Path(args.workspace).resolve()
    urls_path = Path(args.publish_urls)
    if not urls_path.is_absolute():
        urls_path = workspace / urls_path
    log_path = Path(args.publish_log)
    if not log_path.is_absolute():
        log_path = workspace / log_path

    if not urls_path.exists():
        print(f"ERROR: {urls_path} not found", file=sys.stderr)
        return 1

    run_id = args.run_id or resolve_run_id(workspace)
    publish_urls = load_publish_urls(urls_path)
    if len(publish_urls) < 9:
        print(f"ERROR: expected 9 URLs, got {len(publish_urls)}", file=sys.stderr)
        return 1

    data = json.loads(urls_path.read_text(encoding="utf-8"))
    upload_path = data.get("upload_path") or ""
    if run_id and not data.get("run_id"):
        print(
            f"WARN: publish-urls.json missing run_id; upload_path={upload_path!r}. "
            "Re-upload with --run-id for unique URLs.",
            file=sys.stderr,
        )

    conflicts = check_duplicates(publish_urls, log_path, current_run_id=run_id)
    if conflicts:
        for c in conflicts:
            print(
                f"BLOCKED: {c['overlap_count']} URLs overlap with run "
                f"`{c['prior_run_id']}` (e.g. {c['sample_url'][:60]}...)"
            )
        print(
            "Fix: re-run upload with --run-id for unique Kie paths, or wait for prior publish confirmation.",
            file=sys.stderr,
        )
        return 2

    print(f"OK: {len(publish_urls)} URLs, no duplicate conflict (run_id={run_id or 'unknown'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
