#!/usr/bin/env python3
"""Mechanical Carusel pipeline gate.

Director may orchestrate. Director may not silently do worker steps.
Each worker step needs a Task(...) dispatch record plus artifacts + fragment.

CLI, not a novel. Director: run commands. Do not re-read this file in a loop.
Max 2 Reads of this file (or composio_instagram_publish.py) per run.
Third Read of the same gate file = FAIL + hole + EXIT.
After GATE PASS / READY: EXIT immediately. No sleep/poll waiting for a slot.
If status says STALE_LEDGER or next=new-day → run `new-day`, then spawn Task.
If Task is missing or publish auth fails → `hole` and STOP.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cta_canon

STEP_IDS = (
    "director",
    "researcher",
    "copywriter",
    "designer",
    "image-prompter",
    "slice",
    "motion-director",
    "animate",
    "design-guardian",
    "upload",
    "publish",
    "fixic",
)

WORKER_STEPS = STEP_IDS[1:]
ALLOWED_LANG = ("ru", "en")
HANDLES = {"ru": "@todaytaro_ru", "en": "@todaytaro_bot"}
DEFAULT_TOPICS = {"ru": "ТАРО СЕЙЧАС", "en": "Today Tarot"}
PLUGIN_TASK = {
    "director": "director",
    "researcher": "carusel-researcher",
    "copywriter": "carusel-copywriter",
    "designer": "carusel-designer",
    "image-prompter": "carusel-image-prompter",
    "slice": "carusel-slice",
    "motion-director": "carusel-motion-director",
    "animate": "carusel-animate",
    "design-guardian": "carusel-design-guardian",
    "upload": "carusel-upload",
    "publish": "carusel-publish",
    "fixic": "carusel-fixic",
}
LEGAL_SKIP = {
    "publish": "publish-not-requested",
    "fixic": "no-open-incidents",
    "motion-director": "static-png-only",
    "animate": "static-png-only",
}
STATIC_SKIP_STEPS = frozenset({"motion-director", "animate"})
STATIC_REQUIRED_WORKERS = tuple(step_id for step_id in WORKER_STEPS if step_id not in STATIC_SKIP_STEPS)
ARCHIVE_SHORTCODES = ("DcqJGCblQqv", "DcqJS--m0op")
SKIP_FLAG_RE = re.compile(r"^skip_(motion|animate):\s*(true|false)\s*$", re.M | re.I)
GEMINI_STEPS = frozenset({"researcher", "copywriter"})
GEMINI_PARENT_MODEL = "gemini-3.8-flash"
GEMINI_WORKER_MODEL = "inherit"
GEMINI_MODEL = GEMINI_WORKER_MODEL
# Token-burn lock: default is low. high only if Vladimir explicitly overrides
# via KARUSEL_REASONING_EFFORT. Never default workers/parent to high.
_REASONING_OVERRIDE = (os.environ.get("KARUSEL_REASONING_EFFORT") or "").strip().lower()
GEMINI_REASONING_EFFORT = _REASONING_OVERRIDE if _REASONING_OVERRIDE in {"low", "high"} else "low"
MAX_GATE_FILE_READS = 2
GEMINI_MODELS = frozenset({GEMINI_WORKER_MODEL})
GEMINI_SLUG_FORBIDDEN = frozenset({"gemini-3.8-flash", "gemini-3.8-flash-high"})
GEMINI_WRITERS = frozenset(
    {
        "gemini",
        "gemini-3.8-flash",
        "gemini-3.8-flash-high",
        "gemini-3.7-flash-high",
        "gemini-3.7-flash",
    }
)
PIXEL_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov"}
RAW_URL_RE = re.compile(r"https?://|instagram\.com/|t\.me/|telegram\.me/", re.I)
WRITTEN_BY_RE = re.compile(r"written_by[\s:*]*([A-Za-z0-9][A-Za-z0-9._-]*)", re.I)
RESEARCH_MARKERS = (
    "pain",
    "боль",
    "meaning",
    "смысл",
    "hook",
    "хук",
    "topic",
    "тема",
    "audience",
    "аудитор",
)
INCIDENT_RE = re.compile(r"^incident_report:\s+\S+", re.M)
DISPATCH_VIA_RE = re.compile(r"^dispatched_via:\s+(\S+)", re.M)
DISPATCH_ID_RE = re.compile(r"^dispatch_id:\s+(\S+)", re.M)
OPEN_INCIDENT_RE = re.compile(r"^status:\s+open\s*$", re.M | re.I)
LANG_RE = re.compile(r"^lang:\s*(ru|en)\s*$", re.M | re.I)
HANDLE_RE = re.compile(r"^handle:\s*(@\S+)\s*$", re.M | re.I)
PUBLISH_RE = re.compile(r"^publish_requested:\s*(true|false)\s*$", re.M | re.I)
BRIEF_DATE_RE = re.compile(r"^date:\s*(\S+)\s*$", re.M | re.I)
PACK_ID_RE = re.compile(r"^pack_id:\s*(\S+)\s*$", re.M | re.I)
RUN_ID_LINE_RE = re.compile(r"^(?:\*\*)?run_id:(?:\*\*)?\s*(\S+)\s*$", re.M | re.I)
ISO_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
YMD_COMPACT_RE = re.compile(r"(?<!\d)(\d{4})(\d{2})(\d{2})(?!\d)")
DIRECTOR_ONCE = "shared/director-once.md"
NO_REREAD = ("scripts/pipeline_gate.py", "scripts/composio_instagram_publish.py")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def load_steps(repo_root: Path) -> list[dict[str, Any]]:
    path = repo_root / "shared" / "pipeline-steps.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    chain = data["chain"]
    ids = [item["id"] for item in chain]
    if ids != list(STEP_IDS):
        raise SystemExit(f"pipeline-steps.json chain mismatch: {ids}")
    return chain


def step_map(repo_root: Path) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in load_steps(repo_root)}


def resolve_workspace(raw: str | None) -> Path:
    return Path(raw or ".").expanduser().resolve()


def memory_dir(workspace: Path) -> Path:
    return workspace / "carusel-memory"


def pack_root(workspace: Path, date: str) -> Path:
    return memory_dir(workspace) / "packs" / date


def ensure_run_pack(workspace: Path, date: str, run_id: str) -> Path:
    """Create today's dated pack. Never write this run into an older pack."""
    if not date or date.upper() == "PENDING":
        raise SystemExit("pack date missing — run new-day --date YYYY-MM-DD")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise SystemExit(f"pack date must be YYYY-MM-DD, got {date!r}")
    if brief_path(workspace).is_file():
        brief = parse_brief(workspace)
        brief_pack = str(brief.get("pack_id") or "")
        if brief_pack and brief_pack.upper() != "PENDING" and brief_pack != date:
            raise SystemExit(
                f"STALE pack_id={brief_pack}: this run is {date}. "
                "Never write today's slides into an old pack (e.g. 2026-08-30)."
            )
    stale = memory_dir(workspace) / "packs" / "2026-08-30"
    pack = pack_root(workspace, date)
    if date != "2026-08-30" and stale.is_dir() and pack.resolve() == stale.resolve():
        raise SystemExit("Refuse to reuse packs/2026-08-30 for a new run.")
    pack.mkdir(parents=True, exist_ok=True)
    (pack / "ru" / "slides").mkdir(parents=True, exist_ok=True)
    (pack / "en" / "slides").mkdir(parents=True, exist_ok=True)
    manifest_path = pack / "PACK.json"
    manifest = {
        "pack_id": date,
        "date": date,
        "run_id": run_id,
        "face_lock": "none",
        "visual_family": "animals_viktoria_collage",
        "product": "app_audio",
        "langs": ["ru", "en"],
        "slide_01": "static_png",
        "static_png_only": True,
        "already_live": False,
        "already_live_posts": {},
    }
    if manifest_path.is_file():
        existing = load_json(manifest_path)
        existing_id = str(existing.get("pack_id") or existing.get("date") or "")
        if existing_id and existing_id != date:
            raise SystemExit(
                f"STALE pack {existing_id} under packs/{date}. "
                "Refuse to contaminate today's run."
            )
        existing.update(
            {
                "pack_id": date,
                "date": date,
                "run_id": run_id,
                "face_lock": "none",
                "slide_01": "static_png",
                "static_png_only": True,
            }
        )
        if existing.get("visual_family") not in {None, "animals_viktoria_collage"}:
            existing["visual_family"] = "animals_viktoria_collage"
        write_json(manifest_path, existing)
    else:
        write_json(manifest_path, manifest)
    write_text_file(
        pack / "FACE_CHECK.md",
        "\n".join(
            [
                "verdict: ABSENT",
                "face_lock: none",
                "no host portrait",
                "без лица Вики",
                "Do not FACE MATCH. Host portrait is forbidden on every slide.",
                "",
            ]
        ),
    )
    return pack


def ledger_path(workspace: Path) -> Path:
    return memory_dir(workspace) / "pipeline-ledger.json"


def brief_path(workspace: Path) -> Path:
    return memory_dir(workspace) / "00-brief.md"


def queue_path(workspace: Path) -> Path:
    return memory_dir(workspace) / "pipeline-fix-queue.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def is_pixel_rel(rel: str) -> bool:
    return Path(rel).suffix.lower() in PIXEL_SUFFIXES


def is_gemini_writer(value: Any) -> bool:
    return str(value or "").strip().lower() in GEMINI_WRITERS


def written_by_error(rel: str, value: Any) -> str:
    return (
        f"{rel} written_by must be gemini (got {value!r}). "
        "Hall/Director: spawn researcher+copywriter with model=inherit "
        f"(parent is {GEMINI_PARENT_MODEL} + reasoning_effort={GEMINI_REASONING_EFFORT}). "
        "Do NOT pass gemini-3.8-flash slug to Task — it is not in the worker catalog. "
        "Director / default agent must NEVER author slides/captions/CTA. Only FAIL. No default fallback."
    )


def extract_iso_date(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text or text.upper() == "PENDING":
        return None
    iso = ISO_DATE_RE.search(text)
    if iso:
        return iso.group(1)
    compact = YMD_COMPACT_RE.search(text)
    if compact:
        return f"{compact.group(1)}-{compact.group(2)}-{compact.group(3)}"
    return None


def today_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def director_watch(ledger: dict[str, Any]) -> dict[str, Any]:
    watch = ledger.get("director_watch")
    if not isinstance(watch, dict):
        watch = {}
        ledger["director_watch"] = watch
    return watch


def bump_director_watch(workspace: Path, key: str, step_id: str | None = None) -> int:
    ledger = load_ledger(workspace)
    watch = director_watch(ledger)
    if step_id:
        bucket = watch.get(key)
        if not isinstance(bucket, dict):
            bucket = {}
            watch[key] = bucket
        count = int(bucket.get(step_id) or 0) + 1
        bucket[step_id] = count
    else:
        count = int(watch.get(key) or 0) + 1
        watch[key] = count
    save_ledger(workspace, ledger)
    return count


def fail_gate_reread(workspace: Path, rel: str, count: int) -> int:
    cmd_hole(
        workspace,
        f"{rel} read {count} times this run (max {MAX_GATE_FILE_READS}). "
        "Token-burn lock: FAIL and EXIT. Do not sleep/poll for a slot.",
    )
    print(f"FAIL: {rel} counted {count} times (max {MAX_GATE_FILE_READS}). EXIT now.")
    return 2


def note_gate_file_read(workspace: Path, rel: str) -> int:
    """Count a Director Read of a gate source file. Third Read = FAIL + hole."""
    if rel not in NO_REREAD:
        raise SystemExit(f"unknown gate file {rel}")
    count = bump_director_watch(workspace, "gate_file_reads", rel)
    print(f"gate_file_read={rel} count={count} max={MAX_GATE_FILE_READS}")
    if count > MAX_GATE_FILE_READS:
        return fail_gate_reread(workspace, rel, count)
    return 0


def print_exit_now(reason: str) -> None:
    print("READY")
    print("GATE PASS")
    print("EXIT=1")
    print(f"Director EXIT now. {reason}")
    print("Do not re-read scripts/pipeline_gate.py or scripts/composio_instagram_publish.py.")
    print("Do not sleep/poll waiting for a slot. Token-burn lock.")


def print_director_banner() -> None:
    print(f"DIRECTOR_ONCE={DIRECTOR_ONCE}")
    print("DO_NOT_REREAD=" + " ".join(NO_REREAD))
    print(f"MAX_GATE_FILE_READS={MAX_GATE_FILE_READS}")
    print("AFTER_READY_OR_GATE_PASS=EXIT")
    print("NO_SLEEP_POLL=1")
    print("CLI_ONLY=1")
    print(f"parent_canon={GEMINI_PARENT_MODEL} reasoning_effort={GEMINI_REASONING_EFFORT}")
    print(f"worker_model={GEMINI_WORKER_MODEL}")


def archive_file(src: Path, dest: Path) -> None:
    if not src.is_file():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def stamp_brief_dates(text: str, date: str, run_id: str, pack_id: str) -> str:
    replacements = (
        (BRIEF_DATE_RE, f"date: {date}"),
        (PACK_ID_RE, f"pack_id: {pack_id}"),
        (re.compile(r"^\*\*run_id:\*\*\s*\S+\s*$", re.M | re.I), f"**run_id:** {run_id}"),
        (re.compile(r"^run_id:\s*\S+\s*$", re.M | re.I), f"run_id: {run_id}"),
    )
    out = text
    for pattern, repl in replacements:
        if pattern.search(out):
            out = pattern.sub(repl, out, count=1)
    if not BRIEF_DATE_RE.search(out):
        out = out.rstrip() + f"\n\ndate: {date}\npack_id: {pack_id}\nrun_id: {run_id}\n"
    return out


def pending_handoff_text(date: str) -> str:
    return "\n".join(
        [
            "# Carusel — новая сессия",
            "",
            f"Slot: {date} (pending new-day)",
            "Pair: RU @todaytaro_ru + EN @todaytaro_bot",
            "Face lock: none (без лица Вики)",
            "Static PNG only (9+9). CTA = app audio, not bot.",
            f"Model policy: parent {GEMINI_PARENT_MODEL} + reasoning_effort={GEMINI_REASONING_EFFORT};",
            f"text Task workers model={GEMINI_WORKER_MODEL}. NO slug gemini-3.8-flash. NO Claude/GPT fallback.",
            "Archive Instagram permalinks are FORBIDDEN as today's report.",
            "",
            "=== CARUSEL-RESEARCHER ===",
            "Статус: pending",
            "",
        ]
    )


def stale_reason(workspace: Path, ledger: dict[str, Any], today: str | None = None) -> str | None:
    today = today or today_iso()
    ledger_date = extract_iso_date(ledger.get("run_id"))
    brief_date = None
    brief_path_ok = brief_path(workspace).is_file()
    if brief_path_ok:
        brief_text = brief_path(workspace).read_text(encoding="utf-8")
        date_m = BRIEF_DATE_RE.search(brief_text)
        if date_m:
            raw = date_m.group(1)
            brief_date = None if raw.upper() == "PENDING" else extract_iso_date(raw)
    all_done = first_pending(ledger) is None
    if brief_date and ledger_date and brief_date != ledger_date:
        return f"brief date {brief_date} != ledger run_id date {ledger_date}"
    if all_done and ledger_date and ledger_date != today:
        return f"ledger {ledger.get('run_id')} is complete for {ledger_date}, today={today}"
    if all_done and brief_date is None and ledger_date:
        return f"ledger {ledger.get('run_id')} is complete; brief date is PENDING — run new-day"
    if all_done and ledger_date:
        pack_dir = memory_dir(workspace) / "packs" / ledger_date
        if not pack_dir.is_dir():
            return f"ledger claims done for {ledger_date} but pack dir missing"
    return None


def empty_step_state(step_id: str) -> dict[str, Any]:
    return {
        "id": step_id,
        "status": "pending",
        "dispatched_via": None,
        "dispatch_id": None,
        "started_at": None,
        "finished_at": None,
        "skip_reason": None,
        "artifacts": [],
        "fragment": None,
        "incident_report": None,
        "model": None,
    }


def new_ledger(lang: str, topic: str, run_id: str | None = None) -> dict[str, Any]:
    if lang not in ALLOWED_LANG:
        raise SystemExit(f"lang must be ru|en, got {lang!r}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return {
        "schema_version": 1,
        "run_id": run_id or f"{stamp}-{lang}",
        "lang": lang,
        "topic": topic,
        "handle": HANDLES[lang],
        "created_at": utc_now(),
        "dispatch_mode": "unknown",
        "publish_requested": False,
        "mode": "live",
        "pixels": "allowed",
        "steps": {step_id: empty_step_state(step_id) for step_id in STEP_IDS},
    }


def load_ledger(workspace: Path) -> dict[str, Any]:
    path = ledger_path(workspace)
    if not path.is_file():
        raise SystemExit(
            "pipeline-ledger.json missing. Run: "
            "python scripts/pipeline_gate.py --workspace . init --lang ru|en"
        )
    data = load_json(path)
    if "steps" not in data:
        raise SystemExit("pipeline-ledger.json has no steps")
    for step_id in STEP_IDS:
        data["steps"].setdefault(step_id, empty_step_state(step_id))
    return data


def save_ledger(workspace: Path, ledger: dict[str, Any]) -> None:
    write_json(ledger_path(workspace), ledger)


def parse_brief(workspace: Path) -> dict[str, Any]:
    path = brief_path(workspace)
    if not path.is_file():
        raise SystemExit("carusel-memory/00-brief.md missing")
    text = path.read_text(encoding="utf-8")
    lang_m = LANG_RE.search(text)
    if not lang_m:
        raise SystemExit("00-brief.md must contain a line: lang: ru|en")
    lang = lang_m.group(1).lower()
    handle_m = HANDLE_RE.search(text)
    handle = handle_m.group(1) if handle_m else HANDLES[lang]
    expected = HANDLES[lang]
    if handle != expected:
        raise SystemExit(f"handle for lang={lang} must be {expected}, got {handle}")
    pub_m = PUBLISH_RE.search(text)
    publish_requested = bool(pub_m and pub_m.group(1).lower() == "true")
    skip_flags = {m.group(1).lower(): m.group(2).lower() == "true" for m in SKIP_FLAG_RE.finditer(text)}
    # Owner lock: Instagram carousels are static PNGs unless Hall asks for video.
    skip_motion = skip_flags.get("motion", True)
    skip_animate = skip_flags.get("animate", True)
    date_m = BRIEF_DATE_RE.search(text)
    pack_m = PACK_ID_RE.search(text)
    run_m = RUN_ID_LINE_RE.search(text)
    raw_date = date_m.group(1) if date_m else None
    return {
        "lang": lang,
        "handle": handle,
        "publish_requested": publish_requested,
        "skip_motion": skip_motion,
        "skip_animate": skip_animate,
        "static_png_only": skip_motion and skip_animate,
        "date": None if not raw_date or raw_date.upper() == "PENDING" else extract_iso_date(raw_date),
        "pack_id": pack_m.group(1) if pack_m else None,
        "run_id": run_m.group(1) if run_m else None,
        "text": text,
    }


def has_open_incidents(workspace: Path) -> bool:
    path = queue_path(workspace)
    if not path.is_file():
        return False
    return bool(OPEN_INCIDENT_RE.search(path.read_text(encoding="utf-8")))


def file_ok(workspace: Path, rel: str) -> bool:
    path = workspace / rel
    return path.is_file() and path.stat().st_size > 0


def previous_step(step_id: str) -> str | None:
    idx = STEP_IDS.index(step_id)
    if idx == 0:
        return None
    return STEP_IDS[idx - 1]


def is_static_skip_state(step_id: str, state: dict[str, Any]) -> bool:
    return (
        step_id in STATIC_SKIP_STEPS
        and state.get("status") == "skipped"
        and state.get("skip_reason") == LEGAL_SKIP.get(step_id)
    )


def previous_gate_step(ledger: dict[str, Any], step_id: str) -> str | None:
    """Walk back past motion/animate when they are already static-png-only skipped."""
    idx = STEP_IDS.index(step_id)
    while idx > 0:
        idx -= 1
        prev = STEP_IDS[idx]
        if is_static_skip_state(prev, ledger["steps"][prev]):
            continue
        return prev
    return None


def step_is_done(state: dict[str, Any]) -> bool:
    return state.get("status") in {"ok", "skipped"}


def require_previous_done(ledger: dict[str, Any], step_id: str) -> None:
    prev = previous_gate_step(ledger, step_id)
    if prev is None:
        return
    state = ledger["steps"][prev]
    if not step_is_done(state):
        raise SystemExit(
            f"STOP: previous step {prev!r} is {state.get('status')!r}. "
            f"Do not start {step_id}. Do not do {step_id} in the parent chat."
        )


def allowed_via(step_id: str, via: str) -> bool:
    if step_id == "director":
        return via in {"parent", "self"}
    if via in {"inline", "parent", "self", ""}:
        return False
    plugin = f"Task({PLUGIN_TASK[step_id]})"
    return via in {plugin, "Task(generalPurpose)"}


def infer_dispatch_mode(via: str) -> str:
    if via.startswith("Task(carusel-") or via == "Task(director)":
        return "plugin-agents"
    if via == "Task(generalPurpose)":
        return "generalPurpose-fallback"
    if via in {"parent", "self"}:
        return "parent-intake"
    return "unknown"


def cmd_init(
    workspace: Path,
    repo_root: Path,
    lang: str,
    topic: str | None,
    run_id: str | None,
    force: bool = False,
) -> int:
    if lang not in ALLOWED_LANG:
        raise SystemExit("lang must be ru|en")
    topic = topic or DEFAULT_TOPICS[lang]
    mem = memory_dir(workspace)
    mem.mkdir(parents=True, exist_ok=True)
    (mem / "fragments").mkdir(exist_ok=True)
    (mem / "research").mkdir(exist_ok=True)
    (mem / "design").mkdir(exist_ok=True)
    (mem / "output" / "slides").mkdir(parents=True, exist_ok=True)
    (mem / "output" / "video").mkdir(parents=True, exist_ok=True)
    (mem / "output" / "master").mkdir(parents=True, exist_ok=True)

    ledger = new_ledger(lang, topic, run_id)
    if ledger_path(workspace).is_file():
        existing = load_ledger(workspace)
        started = existing.get("steps", {}).get("researcher", {}).get("status") not in {
            None,
            "pending",
        }
        if started and not force:
            raise SystemExit(
                "ledger already has a started run. Run: "
                "python scripts/pipeline_gate.py --workspace . new-day --date YYYY-MM-DD --lang ru "
                "or init --force. Do not re-read this file."
            )
        if started and force:
            stamp = utc_now().replace(":", "")
            old_id = existing.get("run_id") or "prev"
            archive_file(
                ledger_path(workspace),
                mem / "archive" / f"ledger-{old_id}-{stamp}.json",
            )
            ledger_path(workspace).unlink()
    save_ledger(workspace, ledger)

    if not brief_path(workspace).is_file():
        brief_path(workspace).write_text(
            "\n".join(
                [
                    f"# Carusel brief — {topic}",
                    "",
                    f"lang: {lang}",
                    f"topic: {topic}",
                    f"handle: {HANDLES[lang]}",
                    "publish_requested: false",
                    "visual_family: animals_viktoria_collage",
                    "face_lock: none",
                    "slice_method: seam",
                    "cta_style: comment_trigger",
                    "product: app_audio",
                    "cta_offer: comment trigger → Direct audio reading in the APP",
                    "bot_vs_app: sell the APP audio reading, not 3 free bot spreads",
                    "slides: 9",
                    "grid: 3x3",
                    "slide_01: static_png",
                    "skip_motion: true",
                    "skip_animate: true",
                    "date: PENDING",
                    "pack_id: PENDING",
                    "run_id: PENDING",
                    "",
                    "## Intake",
                    "- audience:",
                    "- goal:",
                    "- reference_carousel:",
                    "- cta_target: header_link",
                    "- brand:",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    if not queue_path(workspace).is_file():
        queue_path(workspace).write_text("# pipeline-fix-queue\n\n", encoding="utf-8")

    handoff = workspace / ".cursor" / "carusel-handoff.md"
    handoff.parent.mkdir(parents=True, exist_ok=True)
    if not handoff.is_file():
        handoff.write_text("# Carusel — новая сессия\n", encoding="utf-8")

    director_fragment = mem / "fragments" / "director.md"
    director_fragment.write_text(
        "\n".join(
            [
                "=== CARUSEL-DIRECTOR ===",
                "Статус: ✅ OK",
                "dispatched_via: parent",
                f"lang: {lang}",
                f"handle: {HANDLES[lang]}",
                "skill: skills/director-carusel/SKILL.md",
                "Кратко: intake + ledger init. Worker steps not started.",
                "Артефакты:",
                "- carusel-memory/00-brief.md",
                "- carusel-memory/pipeline-ledger.json",
                "incident_report: none",
                "HANDOFF_NEXT: researcher",
                "",
            ]
        ),
        encoding="utf-8",
    )
    ledger["steps"]["director"] = {
        "id": "director",
        "status": "ok",
        "dispatched_via": "parent",
        "dispatch_id": None,
        "started_at": utc_now(),
        "finished_at": utc_now(),
        "skip_reason": None,
        "artifacts": [
            "carusel-memory/00-brief.md",
            "carusel-memory/pipeline-ledger.json",
        ],
        "fragment": "carusel-memory/fragments/director.md",
        "incident_report": "none",
    }
    save_ledger(workspace, ledger)
    apply_static_video_skips(workspace, repo_root)
    print(f"initialized lang={lang} handle={HANDLES[lang]} run_id={ledger['run_id']}")
    print("next: researcher")
    print("static_png_only: motion-director+animate skipped (static-png-only)")
    return 0


def cmd_status(workspace: Path, repo_root: Path) -> int:
    apply_static_video_skips(workspace, repo_root)
    ledger = load_ledger(workspace)
    print_director_banner()
    print(f"run_id={ledger.get('run_id')} lang={ledger.get('lang')} handle={ledger.get('handle')}")
    print(
        f"mode={ledger.get('mode', 'live')} dispatch_mode={ledger.get('dispatch_mode')} "
        f"publish_requested={ledger.get('publish_requested')}"
    )
    stale = stale_reason(workspace, ledger)
    if stale:
        print("STALE_LEDGER=1")
        print(f"stale_reason={stale}")
        print("next=new-day")
        print(
            "command: python scripts/pipeline_gate.py --workspace . new-day "
            f"--date {today_iso()} --lang {ledger.get('lang') or 'ru'}"
        )
        print("STOP. Do not re-read this file. Do not sleep/poll for a slot.")
        print("Run new-day, then Task researcher model=inherit. Or EXIT if this run is cancelled.")
        return 0
    for spec in load_steps(repo_root):
        state = ledger["steps"][spec["id"]]
        status = state.get("status") or "pending"
        via = state.get("dispatched_via") or "-"
        model = state.get("model")
        extra = f" model={model}" if model else ""
        print(f"- {spec['id']:18} {status:10} via={via}{extra}")
    nxt = first_pending(ledger)
    print(f"next={nxt or 'done'}")
    if nxt is None:
        print_exit_now("Pipeline is READY / GATE PASS.")
        hits = bump_director_watch(workspace, "ready_status_hits")
        print(f"ready_status_hits={hits} max={MAX_GATE_FILE_READS}")
        if hits > MAX_GATE_FILE_READS:
            return fail_gate_reread(workspace, "status-after-ready", hits)
        return 0
    if nxt in GEMINI_STEPS:
        print(f"spawn=Task(generalPurpose, model={GEMINI_WORKER_MODEL})")
        print("IF_NO_TASK: python scripts/pipeline_gate.py --workspace . hole --reason 'Task tool missing'")
    print("Do not Read scripts/pipeline_gate.py. CLI only. No sleep/poll for a slot.")
    return 0


def first_pending(ledger: dict[str, Any]) -> str | None:
    for step_id in STEP_IDS:
        if not step_is_done(ledger["steps"][step_id]):
            return step_id
    return None


def cmd_next(workspace: Path, repo_root: Path) -> int:
    apply_static_video_skips(workspace, repo_root)
    ledger = load_ledger(workspace)
    stale = stale_reason(workspace, ledger)
    if stale:
        print_director_banner()
        print("STALE_LEDGER=1")
        print(f"stale_reason={stale}")
        print("next=new-day")
        print(
            "command: python scripts/pipeline_gate.py --workspace . new-day "
            f"--date {today_iso()} --lang {ledger.get('lang') or 'ru'}"
        )
        print("STOP. Do not re-read this file. Do not sleep/poll for a slot.")
        print("Do not treat archive Instagram URLs as today.")
        return 0
    nxt = first_pending(ledger)
    if nxt is None:
        print("next=done")
        print_exit_now("Pipeline is READY / GATE PASS.")
        hits = bump_director_watch(workspace, "ready_status_hits")
        print(f"ready_status_hits={hits} max={MAX_GATE_FILE_READS}")
        if hits > MAX_GATE_FILE_READS:
            return fail_gate_reread(workspace, "next-after-ready", hits)
        return 0
    spec = step_map(repo_root)[nxt]
    print(f"next={nxt}")
    print(f"role={spec['role']}")
    print(f"plugin_task=Task({spec['task_name']})")
    if nxt in GEMINI_STEPS:
        print(f"required_model={GEMINI_WORKER_MODEL}")
        print(f"parent_canon={GEMINI_PARENT_MODEL}")
        print(f"reasoning_effort={GEMINI_REASONING_EFFORT}")
        print("caption_is_copywriter_job=true" if nxt == "copywriter" else "research_only=true")
        print("default_fallback=FAIL (director/default agent must NEVER write text)")
        print(f"spawn=Task(generalPurpose, model={GEMINI_WORKER_MODEL})")
        print("IF_NO_TASK: python scripts/pipeline_gate.py --workspace . hole --reason 'Task tool missing'")
    else:
        print("cloud_fallback=Task(generalPurpose)")
    print(f"skill={spec['skill']}")
    print(f"agent={spec['agent']}")
    print("STOP if you were about to write these artifacts in the parent chat:")
    for rel in spec["required_artifacts"]:
        print(f"  - {rel}")
    return 0


def cmd_record_dispatch(
    workspace: Path, repo_root: Path, step_id: str, via: str, model: str | None = None
) -> int:
    if step_id not in STEP_IDS:
        raise SystemExit(f"unknown step {step_id}")
    if step_id == "director":
        raise SystemExit("director is intake-only; use init")
    if not allowed_via(step_id, via):
        raise SystemExit(
            f"illegal dispatched_via={via!r} for {step_id}. "
            f"Use Task({PLUGIN_TASK[step_id]}) or Task(generalPurpose). "
            "inline/parent/self is forbidden. Default agent / director must never write text."
        )
    ledger = load_ledger(workspace)
    if step_id in {"motion-director", "animate"}:
        if ledger.get("mode") != "dry-run":
            brief = parse_brief(workspace)
            if brief.get("static_png_only", True):
                raise SystemExit(
                    "static PNG lock: skip motion/animate (static-png-only). "
                    "Do not dispatch Grok video. Read shared/static-carousel-lock.md."
                )
    require_previous_done(ledger, step_id)
    state = ledger["steps"][step_id]
    if state.get("status") == "ok":
        raise SystemExit(f"step {step_id} already ok")
    dispatch_id = uuid.uuid4().hex
    resolved_model = model
    if step_id in GEMINI_STEPS:
        resolved_model = (model or GEMINI_WORKER_MODEL).strip()
        if resolved_model in GEMINI_SLUG_FORBIDDEN:
            raise SystemExit(
                f"{step_id} must spawn with model={GEMINI_WORKER_MODEL} (parent {GEMINI_PARENT_MODEL}). "
                f"Slug {resolved_model!r} is not in the Task worker catalog. "
                "Default agent / director fallback is forbidden. Only FAIL."
            )
        if resolved_model not in GEMINI_MODELS:
            raise SystemExit(
                f"{step_id} must spawn with model={GEMINI_WORKER_MODEL} (inheriting parent Gemini "
                f"{GEMINI_PARENT_MODEL} + reasoning_effort={GEMINI_REASONING_EFFORT}), got {resolved_model!r}. "
                "Default agent / director fallback is forbidden. Only FAIL."
            )
    step_data: dict[str, Any] = {
        "status": "dispatched",
        "dispatched_via": via,
        "dispatch_id": dispatch_id,
        "started_at": utc_now(),
        "finished_at": None,
        "skip_reason": None,
        "model": resolved_model,
    }
    if step_id in GEMINI_STEPS:
        step_data["reasoning_effort"] = GEMINI_REASONING_EFFORT
    state.update(step_data)
    ledger["dispatch_mode"] = infer_dispatch_mode(via)
    save_ledger(workspace, ledger)
    print(f"recorded {step_id} via={via}")
    print(f"dispatch_id={dispatch_id}")
    if resolved_model:
        print(f"model={resolved_model}")
        if step_id in GEMINI_STEPS:
            print(f"reasoning_effort={GEMINI_REASONING_EFFORT}")
    print(f"now call Task(generalPurpose, model={resolved_model or GEMINI_WORKER_MODEL})")
    print("IF_NO_TASK: python scripts/pipeline_gate.py --workspace . hole --reason 'Task tool missing'")
    print("then: pipeline_gate.py verify --step", step_id)
    print("DO_NOT_REREAD this file. Packet is in carusel-memory/dispatches/ after dispatch-prompt.")
    print("After GATE PASS / READY: EXIT. Max 2 Reads of this file per run.")
    return 0


def read_text(workspace: Path, rel: str) -> str:
    return (workspace / rel).read_text(encoding="utf-8")


def verify_fragment(workspace: Path, spec: dict[str, Any], state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rel = spec["fragment"]
    if not file_ok(workspace, rel):
        return [f"missing fragment {rel}"]
    text = read_text(workspace, rel)
    if not INCIDENT_RE.search(text):
        errors.append(f"{rel} has no incident_report: line")
    if spec["id"] != "director":
        via_m = DISPATCH_VIA_RE.search(text)
        if not via_m:
            errors.append(f"{rel} has no dispatched_via: Task(...) line")
        elif not allowed_via(spec["id"], via_m.group(1)):
            errors.append(f"{rel} illegal dispatched_via={via_m.group(1)}")
        expected_via = state.get("dispatched_via")
        if expected_via and via_m and via_m.group(1) != expected_via:
            errors.append(
                f"{rel} dispatched_via mismatch: fragment={via_m.group(1)} ledger={expected_via}"
            )
        id_m = DISPATCH_ID_RE.search(text)
        expected_id = state.get("dispatch_id")
        if expected_id and (not id_m or id_m.group(1) != expected_id):
            errors.append(f"{rel} must repeat dispatch_id {expected_id}")
        role_token = spec["role"].split("-", 1)[-1].upper()
        if f"CARUSEL-{role_token}" not in text.upper() and spec["role"].upper() not in text.upper():
            errors.append(f"{rel} must name role {spec['role']}")
        if spec["id"] in GEMINI_STEPS:
            by_m = WRITTEN_BY_RE.search(text)
            if not by_m or not is_gemini_writer(by_m.group(1)):
                errors.append(written_by_error(rel, by_m.group(1) if by_m else None))
    return errors


def verify_gemini_artifacts(workspace: Path, step_id: str, state: dict[str, Any]) -> list[str]:
    """Human-readable text (research brief, slides, caption) must be Gemini-stamped."""
    errors: list[str] = []
    if step_id not in GEMINI_STEPS:
        return errors
    if state.get("model") and state.get("model") not in GEMINI_MODELS:
        errors.append(
            f"{step_id} ledger model must be in {sorted(GEMINI_MODELS)}, got {state.get('model')!r}"
        )
    if step_id == "researcher":
        rel = "carusel-memory/research/carousel-research-dossier.md"
        if not file_ok(workspace, rel):
            return errors
        text = read_text(workspace, rel)
        by_m = WRITTEN_BY_RE.search(text)
        if not by_m or not is_gemini_writer(by_m.group(1)):
            errors.append(written_by_error(rel, by_m.group(1) if by_m else None))
        low = text.lower()
        if not any(marker in low for marker in RESEARCH_MARKERS):
            errors.append(
                f"{rel} is not a research brief (need topic/pain/meaning/hook). "
                "Do not write a caption here."
            )
        if re.search(r"^comment (the word )?(пауза|pause)\s*$", text.strip(), re.I):
            errors.append(f"{rel} looks like a caption, not research")
    if step_id == "copywriter":
        copy_rel = "carusel-memory/design/CAROUSEL_SLIDE_COPY.json"
        if file_ok(workspace, copy_rel):
            data = load_json(workspace / copy_rel)
            if not is_gemini_writer(data.get("written_by")):
                errors.append(written_by_error(copy_rel, data.get("written_by")))
        cap_rel = "carusel-memory/design/CAROUSEL_CAPTION.json"
        if file_ok(workspace, cap_rel):
            caption = load_json(workspace / cap_rel)
            if not is_gemini_writer(caption.get("written_by")):
                errors.append(written_by_error(cap_rel, caption.get("written_by")))
        cap_md = "carusel-memory/design/CAROUSEL_CAPTION.md"
        if file_ok(workspace, cap_md):
            text = read_text(workspace, cap_md)
            by_m = WRITTEN_BY_RE.search(text)
            if not by_m or not is_gemini_writer(by_m.group(1)):
                errors.append(written_by_error(cap_md, by_m.group(1) if by_m else None))
    return errors


def verify_copy_locale(workspace: Path, lang: str) -> list[str]:
    errors: list[str] = []
    copy_rel = "carusel-memory/design/CAROUSEL_SLIDE_COPY.json"
    if not file_ok(workspace, copy_rel):
        return errors
    try:
        data = load_json(workspace / copy_rel)
    except json.JSONDecodeError as exc:
        return [f"{copy_rel} invalid JSON: {exc}"]
    if data.get("slide_count") != 9:
        errors.append(f"{copy_rel} slide_count must be 9")
    slides = data.get("slides") or []
    if len(slides) != 9:
        errors.append(f"{copy_rel} must contain 9 slides")
    if data.get("visual_family") not in {None, "animals_viktoria_collage"}:
        errors.append(f"{copy_rel} visual_family must be animals_viktoria_collage")
    if data.get("hook_is_scene") is False:
        errors.append(f"{copy_rel} hook_is_scene cannot be false")
    handle = HANDLES[lang]
    caption_rel = "carusel-memory/design/CAROUSEL_CAPTION.json"
    if file_ok(workspace, caption_rel):
        try:
            caption = load_json(workspace / caption_rel)
        except json.JSONDecodeError as exc:
            return [f"{caption_rel} invalid JSON: {exc}"]
        blob = json.dumps(caption, ensure_ascii=False)
        if RAW_URL_RE.search(blob):
            errors.append(f"{caption_rel} contains raw URL; use handle + comment trigger")
        mentions = caption.get("mentions") or []
        if handle not in mentions and handle not in blob:
            errors.append(f"{caption_rel} must mention {handle}")
        if lang == "en" and re.search(r"academy", blob, re.I):
            errors.append(f"{caption_rel} Academy is forbidden on EN")
        if caption.get("trigger_word") in {None, ""} and data.get("trigger_word") in {None, ""}:
            errors.append(f"{caption_rel} missing trigger_word (comment CTA)")
        slide9 = next((s for s in slides if int(s.get("index") or 0) == 9), {})
        slide9_blob = " ".join(
            str(slide9.get(k) or "") for k in ("headline", "body", "cta", "notes")
        )
        errors.extend(
            cta_canon.check_cta_offer(
                lang=lang,
                product=caption.get("product") or data.get("product"),
                caption_blob=blob,
                slide9_blob=slide9_blob,
                prefix=caption_rel,
            )
        )
    return errors


def cmd_verify(workspace: Path, repo_root: Path, step_id: str) -> int:
    if step_id not in STEP_IDS:
        raise SystemExit(f"unknown step {step_id}")
    apply_static_video_skips(workspace, repo_root)
    if step_id in STATIC_SKIP_STEPS:
        brief = parse_brief(workspace) if brief_path(workspace).is_file() else {}
        if brief.get("static_png_only", True):
            print(f"✅ VERIFY SKIP {step_id} reason=static-png-only")
            print("HANDOFF_NEXT: design-guardian")
            print("Director: do not dispatch motion/animate. Next is design-guardian.")
            return 0
    ledger = load_ledger(workspace)
    spec = step_map(repo_root)[step_id]
    state = ledger["steps"][step_id]
    require_previous_done(ledger, step_id)

    if step_id != "director" and state.get("status") != "dispatched":
        raise SystemExit(
            f"STOP: {step_id} was not dispatched via Task. "
            "Run record-dispatch, then Task(...). "
            "Do not write this step in the parent chat."
        )

    errors: list[str] = []
    dry = ledger.get("mode") == "dry-run"
    for rel in spec["required_artifacts"]:
        if dry and is_pixel_rel(rel):
            continue
        if not file_ok(workspace, rel):
            errors.append(f"missing artifact {rel}")
    errors.extend(verify_fragment(workspace, spec, state))
    errors.extend(verify_gemini_artifacts(workspace, step_id, state))
    if step_id == "copywriter":
        brief = parse_brief(workspace)
        errors.extend(verify_copy_locale(workspace, brief["lang"]))
    if step_id == "designer" and file_ok(workspace, "carusel-memory/design/CAROUSEL_SERIES_CONCEPT.json"):
        concept = load_json(workspace / "carusel-memory/design/CAROUSEL_SERIES_CONCEPT.json")
        family = concept.get("carousel_family") or concept.get("family")
        if family and family != "animals_viktoria_collage":
            errors.append("CAROUSEL_SERIES_CONCEPT.json carousel_family must be animals_viktoria_collage")
    if step_id == "image-prompter" and file_ok(workspace, spec["required_artifacts"][0]):
        prompt = load_json(workspace / spec["required_artifacts"][0])
        if prompt.get("generation_mode") != "grid_3x3":
            errors.append("CAROUSEL_IMAGE_PROMPT.json generation_mode must be grid_3x3")
        if prompt.get("slice_method") != "seam":
            errors.append("CAROUSEL_IMAGE_PROMPT.json slice_method must be seam")
        urls = prompt.get("input_urls") or []
        if any(re.search(r"Виктория\.png|viktoriaref|victoria-sheet", str(u), re.I) for u in urls):
            errors.append("CAROUSEL_IMAGE_PROMPT.json must not put a face ref in input_urls")
        if str(prompt.get("face_lock") or "none") not in {"none", "no_host", "absent", ""}:
            errors.append("CAROUSEL_IMAGE_PROMPT.json face_lock must be none")
        prompt_text = str(prompt.get("prompt") or "")
        count = int(prompt.get("prompt_char_count") or len(prompt_text))
        if len(prompt_text) > 2200 or count > 2200:
            errors.append("CAROUSEL_IMAGE_PROMPT.json prompt too long (>2200)")
        if not re.search(r"no host|no woman|без (лица|портрет)|без Вик", prompt_text, re.I):
            errors.append("CAROUSEL_IMAGE_PROMPT.json must forbid host portrait")
        if "PLACEHOLDER" in json.dumps(prompt):
            errors.append("CAROUSEL_IMAGE_PROMPT.json still has PLACEHOLDER")
        briefs = prompt.get("panel_visual_brief") or []
        if len(briefs) != 9:
            errors.append("CAROUSEL_IMAGE_PROMPT.json needs 9 panel_visual_brief")
    if step_id == "design-guardian" and file_ok(workspace, spec["required_artifacts"][0]):
        report = read_text(workspace, spec["required_artifacts"][0])
        ok = "✅ DESIGN OK" in report or re.search(r"Score:\s*(9\d|100)\b", report)
        if not ok and "❌" in report:
            errors.append("guardian report is not DESIGN OK / score>=90")
    if step_id == "slice":
        errors.extend(verify_slice_pack(workspace))
    if step_id == "upload" and file_ok(workspace, "carusel-memory/output/publish-urls.json"):
        errors.extend(verify_publish_urls_this_run(workspace, ledger))

    if errors:
        print("❌ VERIFY FAIL", step_id)
        for err in errors:
            print(f"- {err}")
        print("STOP. Re-run the same Task. Do not complete this step as Director.")
        return 2

    fragment_text = read_text(workspace, spec["fragment"])
    inc = INCIDENT_RE.search(fragment_text)
    state.update(
        {
            "status": "ok",
            "finished_at": utc_now(),
            "artifacts": list(spec["required_artifacts"]),
            "fragment": spec["fragment"],
            "incident_report": inc.group(0).split(":", 1)[1].strip() if inc else "none",
        }
    )
    save_ledger(workspace, ledger)
    print(f"✅ VERIFY OK {step_id}")
    if step_id == "slice":
        apply_static_video_skips(workspace, repo_root)
        nxt = "design-guardian"
    else:
        nxt = spec.get("handoff_next")
        if nxt in STATIC_SKIP_STEPS:
            brief = parse_brief(workspace) if brief_path(workspace).is_file() else {}
            if brief.get("static_png_only", True):
                nxt = "design-guardian"
    if nxt:
        print(f"HANDOFF_NEXT: {nxt}")
        print("Director: record-dispatch the next step. Do not do it yourself.")
    return 0


def verify_slice_pack(workspace: Path) -> list[str]:
    errors: list[str] = []
    if not brief_path(workspace).is_file():
        return errors
    brief = parse_brief(workspace)
    date = brief.get("date")
    if not date:
        return errors
    pack = pack_root(workspace, date)
    if not pack.is_dir():
        errors.append(
            f"missing pack dir carusel-memory/packs/{date} — "
            "never write today's slides into an older pack"
        )
        return errors
    manifest_path = pack / "PACK.json"
    if manifest_path.is_file():
        data = load_json(manifest_path)
        if str(data.get("pack_id") or "") != date:
            errors.append(f"PACK.json pack_id must be {date}, not an archive pack")
        if str(data.get("face_lock") or "none") not in {"none", "no_host", "absent", ""}:
            errors.append("PACK.json face_lock must be none (no host portrait)")
        want_run = brief.get("run_id")
        got_run = data.get("run_id")
        if want_run and want_run != "PENDING" and got_run and got_run != want_run:
            errors.append(f"PACK.json run_id={got_run} is not this run {want_run}")
    face_path = pack / "FACE_CHECK.md"
    if face_path.is_file():
        text = face_path.read_text(encoding="utf-8")
        if re.search(r"verdict:\s*MATCH", text, re.I):
            errors.append("FACE_CHECK MATCH is retired; verdict must be ABSENT")
        if re.search(r"compared:\s*Виктория|face ref.*Виктория|face_lock:\s*Виктория", text, re.I):
            errors.append("FACE_CHECK must not treat Виктория.png as a face ref")
        if not re.search(r"verdict:\s*ABSENT", text, re.I):
            errors.append("FACE_CHECK.md needs verdict: ABSENT")
    return errors


def verify_publish_urls_this_run(workspace: Path, ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rel = "carusel-memory/output/publish-urls.json"
    data = load_json(workspace / rel)
    brief = parse_brief(workspace) if brief_path(workspace).is_file() else {}
    want = brief.get("run_id") or ledger.get("run_id")
    got = data.get("run_id")
    if want and str(want).upper() != "PENDING" and not got:
        errors.append(f"{rel} missing run_id — URLs must come from this run only")
    if want and str(want).upper() != "PENDING" and got and got != want:
        errors.append(f"{rel} run_id={got} is not this run {want}. Refuse archive URLs.")
    blob = json.dumps(data, ensure_ascii=False)
    for code in ARCHIVE_SHORTCODES:
        if code in blob:
            errors.append(f"{rel} contains archive permalink {code}")
    if brief.get("static_png_only", True):
        file1 = str(data.get("file1") or "")
        if file1.endswith(".mp4") or data.get("file1_kind") == "mp4":
            errors.append("static lock: file1 must be PNG (--static-all-pngs), not mp4")
    return errors


def apply_static_video_skips(workspace: Path, repo_root: Path) -> None:
    """Owner lock: skip motion/animate on init so Director never dispatches them."""
    if not brief_path(workspace).is_file() or not ledger_path(workspace).is_file():
        return
    brief = parse_brief(workspace)
    if not brief.get("static_png_only", True):
        return
    for step_id in STATIC_SKIP_STEPS:
        state = load_ledger(workspace)["steps"][step_id]
        if is_static_skip_state(step_id, state):
            continue
        if state.get("status") == "ok":
            continue
        mark_step_skipped(workspace, repo_root, step_id, "static-png-only", check_previous=False)


def maybe_auto_skip_video_steps(workspace: Path, repo_root: Path) -> None:
    apply_static_video_skips(workspace, repo_root)


def mark_step_skipped(
    workspace: Path,
    repo_root: Path,
    step_id: str,
    reason: str,
    check_previous: bool = True,
) -> int:
    if step_id not in LEGAL_SKIP:
        raise SystemExit(f"step {step_id} cannot be skipped")
    expected = LEGAL_SKIP[step_id]
    if reason != expected:
        raise SystemExit(f"skip reason for {step_id} must be {expected!r}")
    ledger = load_ledger(workspace)
    if check_previous:
        require_previous_done(ledger, step_id)
    brief = parse_brief(workspace)
    if step_id == "publish" and brief["publish_requested"]:
        raise SystemExit("publish_requested is true; cannot skip publish")
    if step_id == "fixic" and has_open_incidents(workspace):
        raise SystemExit("open incidents exist; Task(carusel-fixic) is required")
    if step_id in STATIC_SKIP_STEPS and not brief.get("static_png_only", True):
        raise SystemExit("Hall asked for video; cannot skip motion/animate")

    spec = step_map(repo_root)[step_id]
    fragment_rel = spec["fragment"]
    fragment = workspace / fragment_rel
    fragment.parent.mkdir(parents=True, exist_ok=True)
    handoff = spec.get("handoff_next") or "done"
    if step_id in STATIC_SKIP_STEPS and brief.get("static_png_only", True):
        if step_id == "motion-director":
            handoff = "design-guardian"
        elif step_id == "animate":
            handoff = "design-guardian"
    fragment.write_text(
        "\n".join(
            [
                f"=== CARUSEL-{step_id.upper().replace('-', '-')} ===",
                "Статус: ⏭️ SKIPPED",
                f"dispatched_via: skip:{reason}",
                f"skip_reason: {reason}",
                f"lang: {brief['lang']}",
                "incident_report: none",
                f"HANDOFF_NEXT: {handoff}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    ledger["steps"][step_id].update(
        {
            "status": "skipped",
            "dispatched_via": f"skip:{reason}",
            "dispatch_id": None,
            "finished_at": utc_now(),
            "skip_reason": reason,
            "fragment": fragment_rel,
            "incident_report": "none",
        }
    )
    if step_id == "publish":
        log = workspace / "carusel-memory" / "output" / "publish-log.md"
        log.parent.mkdir(parents=True, exist_ok=True)
        if not log.is_file():
            log.write_text(
                f"# publish-log\n\nstatus: skipped\nreason: {reason}\n",
                encoding="utf-8",
            )
    save_ledger(workspace, ledger)
    print(f"skipped {step_id} reason={reason}")
    return 0


def cmd_skip(workspace: Path, repo_root: Path, step_id: str, reason: str) -> int:
    return mark_step_skipped(workspace, repo_root, step_id, reason, check_previous=True)


def cmd_assert_ready(workspace: Path, step_id: str) -> int:
    ledger = load_ledger(workspace)
    require_previous_done(ledger, step_id)
    nxt = first_pending(ledger)
    if nxt != step_id:
        raise SystemExit(f"STOP: next step is {nxt}, not {step_id}")
    print(f"ready {step_id}")
    return 0


def cmd_dispatch_prompt(workspace: Path, repo_root: Path, step_id: str) -> int:
    if step_id not in WORKER_STEPS:
        raise SystemExit("dispatch-prompt is for worker steps only")
    ledger = load_ledger(workspace)
    spec = step_map(repo_root)[step_id]
    state = ledger["steps"][step_id]
    if state.get("status") != "dispatched" or not state.get("dispatch_id"):
        raise SystemExit("run record-dispatch before dispatch-prompt")
    brief = parse_brief(workspace)
    agent_body = (repo_root / spec["agent"]).read_text(encoding="utf-8")
    skill_body = (repo_root / spec["skill"]).read_text(encoding="utf-8")
    prev_artifacts: list[str] = []
    for item in load_steps(repo_root):
        if item["id"] == step_id:
            break
        prev_artifacts.extend(item.get("required_artifacts") or [])
    extra_hard: list[str] = [
        "- Already-read: execute THIS step only. Do not re-read scripts/pipeline_gate.py.",
        "- Do not re-read scripts/composio_instagram_publish.py.",
        "- After GATE PASS / READY: Director EXIT immediately. No sleep/poll waiting for a slot.",
        f"- Max {MAX_GATE_FILE_READS} Reads of scripts/pipeline_gate.py or "
        "scripts/composio_instagram_publish.py per run. Third Read = FAIL + hole + EXIT.",
    ]
    prompt_hits = bump_director_watch(workspace, "dispatch_prompt_hits", step_id)
    print(f"dispatch_prompt_hits={step_id} count={prompt_hits} max={MAX_GATE_FILE_READS}", file=sys.stderr)
    if prompt_hits > MAX_GATE_FILE_READS:
        return fail_gate_reread(workspace, f"dispatch-prompt:{step_id}", prompt_hits)
    if step_id in GEMINI_STEPS:
        extra_hard.append(
            f"- required_model: inherit (parent Gemini {GEMINI_PARENT_MODEL} + "
            f"reasoning_effort={GEMINI_REASONING_EFFORT}; default low — high only if "
            "Vladimir explicitly overrides KARUSEL_REASONING_EFFORT). "
            f"Spawn Task(generalPurpose, model={GEMINI_WORKER_MODEL}). "
            "Do NOT pass gemini-3.8-flash slug to worker. Inherit Gemini from parent."
        )
        extra_hard.append(
            "- Refuse if spawned on Claude/GPT/Composer/Grok or any non-Gemini inherit. "
            "NO DEFAULT FALLBACK: if Gemini is unavailable, FAIL immediately. "
            "Director/default agent must NEVER write slides/caption/CTA himself."
        )
    if step_id == "copywriter":
        extra_hard.append(
            "- Caption is THIS step. Write Instagram caption here. There is no separate caption worker."
        )
        extra_hard.append(
            "- Stamp written_by: gemini on CAROUSEL_SLIDE_COPY.json, CAROUSEL_CAPTION.json, "
            "CAROUSEL_CAPTION.md, and the fragment. Director must not write these files."
        )
        extra_hard.append(
            "- CTA canon: product=app_audio. Comment a topic-tied trigger (new each day, "
            "RU ≠ EN). Direct = audio reading in the APP (RU Суть–Тень–Вектор / "
            "EN Essence–Shadow–Vector). FAIL if you sell 3 free bot spreads. "
            "No raw URLs; links in the profile. Read shared/cta-app-audio-contract.md."
        )
    if step_id == "researcher":
        extra_hard.append(
            "- Write a research brief (topic, client pain, one meaning, why this hook). "
            "Not a caption. Stamp written_by: gemini on the dossier and fragment."
        )
        extra_hard.append(
            "- Product is app audio reading, not 3 free bot spreads. Recommend a "
            "topic-tied comment trigger (different RU vs EN)."
        )
    if step_id == "image-prompter":
        extra_hard.append(
            "- slice_method: seam. Prompt thin white gutters at 1/3 and 2/3 (Excalibur). "
            "Prompt SHORT. No host portrait. prompt_char_count <= 2200. "
            "No 3000-char collage/type/wardrobe novel. No face essay."
        )
        extra_hard.append(
            "- Do NOT upload or i2i Виктория.png / viktoriaref.png / victoria-sheet.png / "
            "victoria.png. Style collage is palette only. No face ref in generation."
        )
        extra_hard.append(
            "- Prompt FIRST: no host, no woman, no Victoria, no presenter portrait. "
            "Animals + objects + type. Keep copy/CTA verbatim."
        )
        extra_hard.append(
            "- Panel 9 verbatim text = app audio CTA from copy (аудиоразбор / audio reading). "
            "Never paint 3 free bot spreads as the comment prize."
        )
    if step_id == "design-guardian":
        extra_hard.append(
            "- CTA test: slide 9 + caption sell the app audio reading "
            "(Суть–Тень–Вектор / Essence–Shadow–Vector). FAIL if they sell "
            "3 free bot readings / три бесплатных расклада. "
            "Read shared/cta-app-audio-contract.md."
        )
        extra_hard.append(
            "- FACE_CHECK.md verdict ABSENT. GATE FAIL if Vika or any host portrait "
            "is on a slide. Do not FACE MATCH Виктория.png. "
            "Read shared/victoria-face-pixel-gate.md."
        )
        extra_hard.append(
            "- STATIC PNG ONLY. Do not require slide-01.mp4 or video_frame_qa. "
            "Missing video is not a blocker. Read shared/static-carousel-lock.md."
        )
    if step_id == "slice":
        extra_hard.append(
            "- Cut with scripts/seam_slice_grid.py --split-mode gutter. "
            "CROOKED CANVAS (exit 2) = rebuild the whole master. Never patch one cell. "
            "Do not use remove_grid_gutters.py as the primary path."
        )
        extra_hard.append(
            "- STATIC PNG ONLY. Slide 01 is a still PNG. Do not generate mp4, "
            "do not run grok_video_*, do not write ANIMATE.md. "
            "HANDOFF_NEXT is design-guardian. Never motion-director or animate."
        )
        extra_hard.append(
            "- Write 9 PNG into carusel-memory/output/slides AND copy into "
            f"carusel-memory/packs/{brief.get('date') or 'YYYY-MM-DD'}/{{lang}}/slides/. "
            "Never write today's slides into packs/2026-08-30 or any other old pack."
        )
        extra_hard.append(
            "- FACE_CHECK.md verdict ABSENT. face_lock none. "
            "Do not require or mention Виктория.png as a face ref."
        )
    if step_id == "upload":
        extra_hard.append(
            "- Upload with --static-all-pngs. file1 is slide-01.png. "
            "Do not upload or require slide-01.mp4. Read shared/static-carousel-lock.md."
        )
        extra_hard.append(
            "- publish-urls.json must carry THIS run_id only. "
            "Refuse archive permalinks (DcqJGCblQqv, DcqJS--m0op, live-posts.json of another date)."
        )
    extra_hard_block = "\n".join(extra_hard)
    spawn_line = (
        f"Task(generalPurpose, model={GEMINI_WORKER_MODEL}) [NO DEFAULT FALLBACK - inherit parent Gemini]"
        if step_id in GEMINI_STEPS
        else "Task(generalPurpose) — real Task, not Director inline"
    )
    packet = f"""You are {spec['role']} for the Carusel plugin.

SPAWN
step: {step_id}
via: {state['dispatched_via']}
cloud_fallback: {spawn_line}
required_model: {state.get('model') or GEMINI_WORKER_MODEL}
reasoning_effort: {state.get('reasoning_effort') or (GEMINI_REASONING_EFFORT if step_id in GEMINI_STEPS else 'none')}

HARD RULES
- Do only this step ({step_id}). Do not start the next role.
- Follow {spec['skill']} and {spec['agent']} (inlined below). Do not re-open pipeline_gate.py.
- Canon already inlined: no host portrait, 9+9 static PNG, CTA = app audio not bot.
{extra_hard_block}
- NO DEFAULT FALLBACK: if Gemini is unavailable, FAIL immediately. Director/default agent must NEVER write slides/caption/CTA himself.
- lang={brief['lang']}. Brand handle={brief['handle']}.
- Write artifacts only to the paths listed below.
- End with fragment {spec['fragment']}.
- Fragment MUST contain:
  dispatched_via: {state['dispatched_via']}
  dispatch_id: {state['dispatch_id']}
  incident_report: none
  HANDOFF_NEXT: {spec.get('handoff_next')}
- Instagram: no raw URLs; say links are in the profile. CTA is one comment trigger word.
- Product is app_audio: Direct = audio reading in the APP (not 3 free bot spreads).
- @todaytaro_bot is the EN Instagram handle name, not the comment prize.
- Read shared/cta-app-audio-contract.md.
- Do not publish to Instagram unless this role is carusel-publish AND brief.publish_requested is true.
- If previous artifacts are missing: fragment ❌ BLOCKER and stop.

DISPATCH
dispatch_id: {state['dispatch_id']}
step_id: {step_id}
via: {state['dispatched_via']}
workspace: {workspace}

PREVIOUS ARTIFACTS
{chr(10).join(f'- {p}' for p in prev_artifacts) or '- (none)'}

YOUR REQUIRED ARTIFACTS
{chr(10).join(f'- {p}' for p in spec['required_artifacts']) or '- (fragment only)'}

HANDOFF NEXT (do not execute)
{spec.get('handoff_next')}

===== AGENT FILE {spec['agent']} =====
{agent_body}

===== SKILL FILE {spec['skill']} =====
{skill_body}
"""
    out = memory_dir(workspace) / "dispatches" / f"{step_id}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(packet, encoding="utf-8")
    print(packet)
    print(f"\n# also wrote {out.as_posix()}", file=sys.stderr)
    return 0


def cmd_assert_complete(workspace: Path) -> int:
    ledger = load_ledger(workspace)
    pending = [step_id for step_id in STEP_IDS if not step_is_done(ledger["steps"][step_id])]
    if pending:
        print("❌ PIPELINE INCOMPLETE")
        for step_id in pending:
            print(f"- missing {step_id} status={ledger['steps'][step_id].get('status')}")
        print("STOP. Dispatch the missing step. Do not finish the carousel yourself.")
        print("Do not sleep/poll. Do not re-read scripts/pipeline_gate.py.")
        return 2
    print("✅ PIPELINE COMPLETE (all 12 steps ok or legally skipped)")
    print_exit_now("assert-complete is READY / GATE PASS.")
    return 0


DRY_RUN_WORKERS = (
    "researcher",
    "copywriter",
    "designer",
    "image-prompter",
    "slice",
    "design-guardian",
    "upload",
)


def write_dry_run_artifacts(workspace: Path, lang: str) -> None:
    """Text stubs only. No PNG/MP4. Satisfies verify in mode=dry-run."""
    trigger = "ПАУЗА" if lang == "ru" else "PAUSE"
    handle = HANDLES[lang]
    mem = memory_dir(workspace)
    family = "animals_viktoria_collage"

    write_text_file(
        mem / "research" / "carousel-research-dossier.md",
        "\n".join(
            [
                "# Dry-run research",
                "",
                "No pixels. Teaching-arc notes only.",
                f"lang: {lang}",
                f"visual_family: {family}",
                "face_lock: none",
                "written_by: gemini",
                "",
                "## Topic",
                "- dry-run topic",
                "",
                "## Client pain",
                "- dry-run pain",
                "",
                "## One meaning",
                "- dry-run meaning",
                "",
                "## Why this hook",
                "- dry-run hook (scene)",
                "",
                "## Hook lab",
                "- dry-run hook (scene)",
                "",
                "## 9-panel arc",
                "- 01-09 text-only stubs",
                "",
            ]
        ),
    )

    copy = {
        "hook_options": [
            {"framework": "pain", "headline": "dry-run scene", "why_it_swipes": "gap"}
        ],
        "hook_rationale": "dry-run: no live copy",
        "hook_is_scene": True,
        "visual_family": family,
        "trigger_word": trigger,
        "product": "app_audio",
        "written_by": "gemini",
        "slide_count": 9,
        "grid": {"cols": 3, "rows": 3},
        "slides": [
            {"index": i, "role": "stub", "headline": f"dry-run slide {i:02d}"}
            for i in range(1, 9)
        ]
        + [
            {
                "index": 9,
                "role": "cta",
                "headline": f"Напиши {trigger}" if lang == "ru" else f"Comment {trigger}",
                "body": (
                    "Аудиоразбор в приложении. Суть – Тень – Вектор."
                    if lang == "ru"
                    else "Audio reading in the app. Essence–Shadow–Vector."
                ),
            }
        ],
    }
    write_json(mem / "design" / "CAROUSEL_SLIDE_COPY.json", copy)
    offer = (
        "В Direct пришлём аудиоразбор в приложении: Суть – Тень – Вектор. Ссылки в профиле."
        if lang == "ru"
        else "We'll DM an audio reading in the app: Essence–Shadow–Vector. Links are in the profile."
    )
    write_json(
        mem / "design" / "CAROUSEL_CAPTION.json",
        {
            "full_caption": f"Dry-run caption. Comment {trigger}. {offer} {handle}",
            "mentions": [handle],
            "cta": f"Comment the word {trigger}. {offer}",
            "trigger_word": trigger,
            "product": "app_audio",
            "has_url": False,
            "written_by": "gemini",
        },
    )
    write_text_file(
        mem / "design" / "CAROUSEL_CAPTION.md",
        f"written_by: gemini\nDry-run caption. Comment {trigger}. No URL. {handle}\n",
    )

    write_text_file(
        mem / "design" / "CAROUSELDESIGN.md",
        f"# Dry-run design\n\ncarousel_family: {family}\nface_lock: none\n"
        "Do not render. No host portrait.\n",
    )
    write_json(
        mem / "design" / "CAROUSEL_SERIES_CONCEPT.json",
        {"carousel_family": family, "face_lock": "none", "dry_run": True},
    )
    write_json(
        mem / "design" / "CAROUSEL_SOURCE_DECOMPOSITION.json",
        {"dry_run": True, "preserve": ["family"], "change": ["topic"], "do_not_borrow": ["Alena"]},
    )
    write_json(
        mem / "design" / "CAROUSEL_SLIDE_BLUEPRINTS.json",
        {"dry_run": True, "slides": [{"index": i} for i in range(1, 10)]},
    )

    write_json(
        mem / "design" / "CAROUSEL_IMAGE_PROMPT.json",
        {
            "generation_mode": "grid_3x3",
            "carousel_family": family,
            "face_lock": "none",
            "slice_method": "seam",
            "dry_run": True,
            "prompt": "No host portrait. No woman. Thin white gutters at 1/3 and 2/3. Dry-run only.",
            "prompt_char_count": 78,
            "reference_contract": {"face_lock": "none", "host_portrait": False},
            "input_urls": [
                "https://example.invalid/animals-viktoria-style-lock.png",
            ],
            "typography_rules": {"dry_run": True},
            "panel_visual_brief": [
                {"slide": i, "prompt": f"dry-run text brief {i:02d} — no image generation"}
                for i in range(1, 10)
            ],
        },
    )
    write_text_file(
        mem / "design" / "CAROUSEL_IMAGE_PROMPT.md",
        "# Dry-run prompts\n\nNo Kie. No GenerateImage. Text only.\n",
    )

    write_json(
        mem / "output" / "slice-manifest.json",
        {
            "dry_run": True,
            "pixels": "forbidden",
            "face_lock": "none",
            "slides": [{"id": n, "file": None} for n in range(1, 10)],
        },
    )
    write_text_file(
        mem / "design" / "CAROUSEL_DESIGN_GUARDIAN_REPORT.md",
        "✅ DESIGN OK\n\nDry-run: no pixels to review.\n",
    )
    write_json(
        mem / "output" / "publish-urls.json",
        {"dry_run": True, "published": False},
    )


def write_dry_run_fragment(
    workspace: Path, spec: dict[str, Any], state: dict[str, Any], lang: str
) -> None:
    role = spec["role"]
    rel = spec["fragment"]
    write_text_file(
        workspace / rel,
        "\n".join(
            [
                f"=== {role.upper()} ===",
                "Статус: ✅ OK",
                f"dispatched_via: {state['dispatched_via']}",
                f"dispatch_id: {state['dispatch_id']}",
                f"lang: {lang}",
                *(
                    ["written_by: gemini"]
                    if spec["id"] in GEMINI_STEPS
                    else []
                ),
                "incident_report: none",
                f"HANDOFF_NEXT: {spec.get('handoff_next') or 'done'}",
                "note: dry-run text stub — no pixels",
                "",
            ]
        ),
    )


def leaked_output_pixels(workspace: Path) -> list[Path]:
    output = memory_dir(workspace) / "output"
    if not output.is_dir():
        return []
    return [p for p in output.rglob("*") if p.is_file() and p.suffix.lower() in PIXEL_SUFFIXES]


def cmd_dry_run(
    workspace: Path, repo_root: Path, lang: str, topic: str | None, force: bool
) -> int:
    """Record 11 worker steps with text stubs only. No PNG/MP4. Skip publish+fixic."""
    if ledger_path(workspace).is_file():
        existing = load_json(ledger_path(workspace))
        started = existing.get("steps", {}).get("researcher", {}).get("status") not in {
            None,
            "pending",
        }
        if started and not force:
            print(
                f"dry-run refused: {workspace} already has a started run (pass --force)",
                file=sys.stderr,
            )
            return 1
        if force:
            ledger_path(workspace).unlink(missing_ok=True)
            if brief_path(workspace).is_file():
                brief_path(workspace).unlink()

    rc = cmd_init(workspace, repo_root, lang, topic, run_id=f"dry-run-{lang}")
    if rc != 0:
        return rc

    ledger = load_ledger(workspace)
    ledger["mode"] = "dry-run"
    ledger["pixels"] = "forbidden"
    ledger["publish_requested"] = False
    save_ledger(workspace, ledger)

    write_dry_run_artifacts(workspace, lang)
    specs = step_map(repo_root)

    for step_id in DRY_RUN_WORKERS:
        via = "Task(generalPurpose)"
        model = GEMINI_WORKER_MODEL if step_id in GEMINI_STEPS else None
        rc = cmd_record_dispatch(workspace, repo_root, step_id, via, model=model)
        if rc != 0:
            return rc
        ledger = load_ledger(workspace)
        write_dry_run_fragment(workspace, specs[step_id], ledger["steps"][step_id], lang)
        rc = cmd_verify(workspace, repo_root, step_id)
        if rc != 0:
            return rc

    rc = cmd_skip(workspace, repo_root, "publish", "publish-not-requested")
    if rc != 0:
        return rc
    rc = cmd_skip(workspace, repo_root, "fixic", "no-open-incidents")
    if rc != 0:
        return rc

    leaked = leaked_output_pixels(workspace)
    if leaked:
        print("dry-run leaked pixels:", *[str(p) for p in leaked], sep="\n", file=sys.stderr)
        return 1

    print("=== DRY-RUN 11 WORKER RECORDS ===")
    print(f"workspace: {workspace}")
    print("pixels: none")
    print("publish: skipped (publish-not-requested)")
    print("fixic: skipped (no-open-incidents)")
    print(
        f"researcher+copywriter+caption model: {GEMINI_WORKER_MODEL} "
        f"(parent {GEMINI_PARENT_MODEL} + reasoning_effort={GEMINI_REASONING_EFFORT}; "
        "no slug, no default fallback)"
    )
    print(
        "steps recorded: researcher copywriter designer image-prompter slice "
        "motion-director(skip static-png-only) animate(skip static-png-only) "
        "design-guardian upload publish(skip) fixic(skip)"
    )
    cmd_status(workspace, repo_root)
    return cmd_assert_complete(workspace)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Carusel pipeline gate")
    parser.add_argument("--workspace", default=".", help="carousel workspace root")
    parser.add_argument(
        "--repo-root",
        default=str(repo_root_from_script()),
        help="plugin repo root (agents/skills/shared)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    init = sub.add_parser("init")
    init.add_argument("--lang", required=True, choices=ALLOWED_LANG)
    init.add_argument("--topic", default=None)
    init.add_argument("--run-id", default=None)
    init.add_argument(
        "--force",
        action="store_true",
        help="Archive a started ledger and start a fresh run (prefer new-day)",
    )
    sub.add_parser("status")
    sub.add_parser("next")
    rec = sub.add_parser("record-dispatch")
    rec.add_argument("--step", required=True, choices=STEP_IDS)
    rec.add_argument("--via", required=True)
    rec.add_argument(
        "--model",
        default=None,
        help="researcher/copywriter: inherit only (parent Gemini). Slug gemini-3.8-flash is forbidden.",
    )
    ver = sub.add_parser("verify")
    ver.add_argument("--step", required=True, choices=STEP_IDS)
    sk = sub.add_parser("skip")
    sk.add_argument("--step", required=True, choices=list(LEGAL_SKIP))
    sk.add_argument("--reason", required=True)
    ready = sub.add_parser("assert-ready")
    ready.add_argument("--step", required=True, choices=STEP_IDS)
    prompt = sub.add_parser("dispatch-prompt")
    prompt.add_argument("--step", required=True, choices=STEP_IDS)
    sub.add_parser("assert-complete")
    dry = sub.add_parser(
        "dry-run",
        help="11 worker records, text stubs only, no PNG, skip publish",
    )
    dry.add_argument("--lang", required=True, choices=ALLOWED_LANG)
    dry.add_argument("--topic", default=None)
    dry.add_argument("--force", action="store_true")
    new_day = sub.add_parser(
        "new-day",
        help="Archive a completed/stale ledger and start a pending run for --date",
    )
    new_day.add_argument("--date", required=True, help="YYYY-MM-DD slot date")
    new_day.add_argument("--lang", default="ru", choices=ALLOWED_LANG)
    new_day.add_argument("--topic", default=None)
    hole = sub.add_parser(
        "hole",
        help="Write FAIL+HOLE and stop. Use when Task is missing or publish auth fails.",
    )
    hole.add_argument("--reason", required=True)
    note = sub.add_parser(
        "note-read",
        help="Count a Director Read of a gate source file. Third Read = FAIL + EXIT.",
    )
    note.add_argument(
        "--file",
        required=True,
        choices=list(NO_REREAD),
        help="scripts/pipeline_gate.py or scripts/composio_instagram_publish.py",
    )
    return parser


def cmd_new_day(
    workspace: Path,
    repo_root: Path,
    date: str,
    lang: str,
    topic: str | None,
) -> int:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise SystemExit("new-day --date must be YYYY-MM-DD")
    if lang not in ALLOWED_LANG:
        raise SystemExit("lang must be ru|en")
    topic = topic or DEFAULT_TOPICS[lang]
    run_id = f"{date}-1110"
    stamp = utc_now().replace(":", "")
    mem = memory_dir(workspace)
    mem.mkdir(parents=True, exist_ok=True)
    if ledger_path(workspace).is_file():
        existing = load_json(ledger_path(workspace))
        old_id = existing.get("run_id") or "prev"
        archive_file(ledger_path(workspace), mem / "archive" / f"ledger-{old_id}-{stamp}.json")
        ledger_path(workspace).unlink()
    if brief_path(workspace).is_file():
        archive_file(brief_path(workspace), mem / "archive" / f"brief-{stamp}.md")
    handoff = workspace / ".cursor" / "carusel-handoff.md"
    if handoff.is_file():
        archive_file(handoff, mem / "archive" / f"handoff-{stamp}.md")
    rc = cmd_init(workspace, repo_root, lang, topic, run_id, force=True)
    if rc != 0:
        return rc
    if brief_path(workspace).is_file():
        stamped = stamp_brief_dates(
            brief_path(workspace).read_text(encoding="utf-8"),
            date=date,
            run_id=run_id,
            pack_id=date,
        )
        write_text_file(brief_path(workspace), stamped)
    apply_static_video_skips(workspace, repo_root)
    pack = ensure_run_pack(workspace, date, run_id)
    write_text_file(handoff, pending_handoff_text(date))
    hole = mem / "HOLE.md"
    if hole.is_file():
        hole.unlink()
    print_director_banner()
    print(f"new-day date={date} run_id={run_id} lang={lang}")
    print(f"pack={pack.as_posix()}")
    print("face_lock=none FACE_CHECK=ABSENT")
    print("static_png_only: motion-director+animate skipped")
    print("next=researcher")
    print(f"spawn=Task(generalPurpose, model={GEMINI_WORKER_MODEL})")
    print("IF_NO_TASK: python scripts/pipeline_gate.py --workspace . hole --reason 'Task tool missing'")
    print("DO_NOT_REREAD scripts. Run record-dispatch then dispatch-prompt then Task.")
    print("After GATE PASS / READY: EXIT. No sleep/poll for a slot.")
    return 0


def cmd_hole(workspace: Path, reason: str) -> int:
    path = memory_dir(workspace) / "HOLE.md"
    write_text_file(
        path,
        "\n".join(
            [
                "# HOLE",
                "status: FAIL",
                f"reason: {reason}",
                f"created_at: {utc_now()}",
                "permalink: FORBIDDEN — do not copy live-posts.json or handoff archive URLs",
                "loop: STOP. Do not re-read scripts/pipeline_gate.py or scripts/composio_instagram_publish.py.",
                "",
            ]
        ),
    )
    print("FAIL")
    print(f"HOLE={path.as_posix()}")
    print(f"reason={reason}")
    print("STOP. EXIT now. Do not reread scripts. Do not sleep/poll for a slot.")
    print("Do not substitute archive Instagram URLs.")
    return 2


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = resolve_workspace(args.workspace)
    repo_root = Path(args.repo_root).expanduser().resolve()
    if args.cmd == "init":
        return cmd_init(
            workspace, repo_root, args.lang, args.topic, args.run_id, force=args.force
        )
    if args.cmd == "status":
        return cmd_status(workspace, repo_root)
    if args.cmd == "next":
        return cmd_next(workspace, repo_root)
    if args.cmd == "record-dispatch":
        return cmd_record_dispatch(
            workspace, repo_root, args.step, args.via, model=args.model
        )
    if args.cmd == "verify":
        return cmd_verify(workspace, repo_root, args.step)
    if args.cmd == "skip":
        return cmd_skip(workspace, repo_root, args.step, args.reason)
    if args.cmd == "assert-ready":
        return cmd_assert_ready(workspace, args.step)
    if args.cmd == "dispatch-prompt":
        return cmd_dispatch_prompt(workspace, repo_root, args.step)
    if args.cmd == "assert-complete":
        return cmd_assert_complete(workspace)
    if args.cmd == "dry-run":
        return cmd_dry_run(workspace, repo_root, args.lang, args.topic, args.force)
    if args.cmd == "new-day":
        return cmd_new_day(workspace, repo_root, args.date, args.lang, args.topic)
    if args.cmd == "hole":
        return cmd_hole(workspace, args.reason)
    if args.cmd == "note-read":
        return note_gate_file_read(workspace, args.file)
    raise SystemExit(f"unknown cmd {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
