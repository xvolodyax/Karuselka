#!/usr/bin/env python3
"""Mechanical Carusel pipeline gate.

Director may orchestrate. Director may not silently do worker steps.
Each worker step needs a Task(...) dispatch record plus artifacts + fragment.
"""

from __future__ import annotations

import argparse
import json
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
SKIP_FLAG_RE = re.compile(r"^skip_(motion|animate):\s*(true|false)\s*$", re.M | re.I)
GEMINI_STEPS = frozenset({"researcher", "copywriter"})
GEMINI_MODEL = "gemini-3.7-flash-high"
GEMINI_WRITERS = frozenset({"gemini", "gemini-3.7-flash-high"})
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
        "Hall/Director: spawn researcher+copywriter on gemini-3.7-flash-high. "
        "Director must not author slides/captions."
    )


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
    return {
        "lang": lang,
        "handle": handle,
        "publish_requested": publish_requested,
        "skip_motion": skip_motion,
        "skip_animate": skip_animate,
        "static_png_only": skip_motion and skip_animate,
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


def step_is_done(state: dict[str, Any]) -> bool:
    return state.get("status") in {"ok", "skipped"}


def require_previous_done(ledger: dict[str, Any], step_id: str) -> None:
    prev = previous_step(step_id)
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


def cmd_init(workspace: Path, repo_root: Path, lang: str, topic: str | None, run_id: str | None) -> int:
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
        if existing.get("steps", {}).get("researcher", {}).get("status") not in {None, "pending"}:
            raise SystemExit(
                "ledger already has a started run. Start a new workspace/run "
                "or delete carusel-memory/pipeline-ledger.json after user OK."
            )
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
                    "face_lock: victoria-sheet.png",
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
    print(f"initialized lang={lang} handle={HANDLES[lang]} run_id={ledger['run_id']}")
    print("next: researcher")
    return 0


def cmd_status(workspace: Path, repo_root: Path) -> int:
    ledger = load_ledger(workspace)
    print(f"run_id={ledger.get('run_id')} lang={ledger.get('lang')} handle={ledger.get('handle')}")
    print(
        f"mode={ledger.get('mode', 'live')} dispatch_mode={ledger.get('dispatch_mode')} "
        f"publish_requested={ledger.get('publish_requested')}"
    )
    for spec in load_steps(repo_root):
        state = ledger["steps"][spec["id"]]
        status = state.get("status") or "pending"
        via = state.get("dispatched_via") or "-"
        model = state.get("model")
        extra = f" model={model}" if model else ""
        print(f"- {spec['id']:18} {status:10} via={via}{extra}")
    nxt = first_pending(ledger)
    print(f"next={nxt or 'done'}")
    return 0


def first_pending(ledger: dict[str, Any]) -> str | None:
    for step_id in STEP_IDS:
        if not step_is_done(ledger["steps"][step_id]):
            return step_id
    return None


def cmd_next(workspace: Path, repo_root: Path) -> int:
    ledger = load_ledger(workspace)
    nxt = first_pending(ledger)
    if nxt is None:
        print("next=done")
        return 0
    spec = step_map(repo_root)[nxt]
    print(f"next={nxt}")
    print(f"role={spec['role']}")
    print(f"plugin_task=Task({spec['task_name']})")
    print("cloud_fallback=Task(generalPurpose)")
    if nxt in GEMINI_STEPS:
        print(f"required_model={GEMINI_MODEL}")
        print("caption_is_copywriter_job=true" if nxt == "copywriter" else "research_only=true")
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
            "inline/parent/self is forbidden."
        )
    if step_id in {"motion-director", "animate"}:
        brief = parse_brief(workspace)
        if brief.get("static_png_only", True):
            raise SystemExit(
                "static PNG lock: skip motion/animate (static-png-only). "
                "Do not dispatch Grok video. Read shared/static-carousel-lock.md."
            )
    ledger = load_ledger(workspace)
    require_previous_done(ledger, step_id)
    state = ledger["steps"][step_id]
    if state.get("status") == "ok":
        raise SystemExit(f"step {step_id} already ok")
    dispatch_id = uuid.uuid4().hex
    resolved_model = model
    if step_id in GEMINI_STEPS:
        resolved_model = (model or GEMINI_MODEL).strip()
        if resolved_model != GEMINI_MODEL:
            raise SystemExit(
                f"{step_id} must spawn with model {GEMINI_MODEL}, got {resolved_model!r}"
            )
    state.update(
        {
            "status": "dispatched",
            "dispatched_via": via,
            "dispatch_id": dispatch_id,
            "started_at": utc_now(),
            "finished_at": None,
            "skip_reason": None,
            "model": resolved_model,
        }
    )
    ledger["dispatch_mode"] = infer_dispatch_mode(via)
    save_ledger(workspace, ledger)
    print(f"recorded {step_id} via={via}")
    print(f"dispatch_id={dispatch_id}")
    if resolved_model:
        print(f"model={resolved_model}")
    print("now call Task, then: pipeline_gate.py verify --step", step_id)
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
    if state.get("model") and state.get("model") != GEMINI_MODEL:
        errors.append(
            f"{step_id} ledger model must be {GEMINI_MODEL}, got {state.get('model')!r}"
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
        if urls and "victoria-sheet.png" not in str(urls[0]):
            errors.append("CAROUSEL_IMAGE_PROMPT.json input_urls[0] must be victoria-sheet.png")
        if len(urls) != 1:
            errors.append("CAROUSEL_IMAGE_PROMPT.json must have exactly one input_url")
        prompt_text = str(prompt.get("prompt") or "")
        count = int(prompt.get("prompt_char_count") or len(prompt_text))
        if len(prompt_text) > 2200 or count > 2200:
            errors.append(
                "CAROUSEL_IMAGE_PROMPT.json prompt too long (>2200) — starves face lock"
            )
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
        maybe_auto_skip_video_steps(workspace, repo_root)
    nxt = spec.get("handoff_next")
    if nxt:
        print(f"HANDOFF_NEXT: {nxt}")
        print("Director: record-dispatch the next step. Do not do it yourself.")
    return 0


def maybe_auto_skip_video_steps(workspace: Path, repo_root: Path) -> None:
    """Owner lock: static PNG carousels. Skip motion/animate unless Hall asks."""
    brief = parse_brief(workspace)
    if not brief.get("static_png_only", True):
        return
    for step_id in ("motion-director", "animate"):
        state = load_ledger(workspace)["steps"][step_id]
        if state.get("status") == "skipped" and state.get("skip_reason") == "static-png-only":
            continue
        cmd_skip(workspace, repo_root, step_id, "static-png-only")


def cmd_skip(workspace: Path, repo_root: Path, step_id: str, reason: str) -> int:
    if step_id not in LEGAL_SKIP:
        raise SystemExit(f"step {step_id} cannot be skipped")
    expected = LEGAL_SKIP[step_id]
    if reason != expected:
        raise SystemExit(f"skip reason for {step_id} must be {expected!r}")
    ledger = load_ledger(workspace)
    require_previous_done(ledger, step_id)
    brief = parse_brief(workspace)
    if step_id == "publish" and brief["publish_requested"]:
        raise SystemExit("publish_requested is true; cannot skip publish")
    if step_id == "fixic" and has_open_incidents(workspace):
        raise SystemExit("open incidents exist; Task(carusel-fixic) is required")
    if step_id in {"motion-director", "animate"} and not brief.get("static_png_only", True):
        raise SystemExit("Hall asked for video; cannot skip motion/animate")

    spec = step_map(repo_root)[step_id]
    fragment_rel = spec["fragment"]
    fragment = workspace / fragment_rel
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text(
        "\n".join(
            [
                f"=== CARUSEL-{step_id.upper().replace('-', '-')} ===",
                "Статус: ⏭️ SKIPPED",
                f"dispatched_via: skip:{reason}",
                f"skip_reason: {reason}",
                f"lang: {brief['lang']}",
                "incident_report: none",
                f"HANDOFF_NEXT: {spec.get('handoff_next') or 'done'}",
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
        "- Read shared/swarm-spawn-contract.md and shared/director-dispatch-contract.md.",
    ]
    if step_id in GEMINI_STEPS:
        extra_hard.append(
            f"- required_model: {GEMINI_MODEL}. Spawn Task(generalPurpose, model={GEMINI_MODEL}) "
            f"or Task({PLUGIN_TASK[step_id]}) with that model. Do not inherit Director model."
        )
        extra_hard.append(f"- Refuse if spawned on any model other than {GEMINI_MODEL}.")
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
            "Prompt SHORT. Face lock FIRST. prompt_char_count <= 2200. "
            "No 3000-char collage/type/wardrobe novel. No face essay."
        )
        extra_hard.append(
            "- Crop ONE left frontal close-up from victoria-sheet.png and upload THAT "
            "as the only input_url, file_name=victoria-sheet.png. Do not i2i the full "
            "12-up grid. Do not send animals-viktoria-style-lock.png."
        )
        extra_hard.append(
            "- Eyes: green + slight hazel/light-brown (Excalibur). Keep passed copy/CTA. "
            "New clothes/poses — not sheet tank+jeans. Read shared/victoria-identity-lock.md "
            "and shared/carousel-seam-slice-contract.md."
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
            "- Pixel FACE_CHECK.md vs victoria-sheet.png close-up (slides 01+09, both langs). "
            "Run scripts/make_face_check_crops.py. Eyes must be green+hazel. "
            "Brown/grey eyes or generic blonde = FAIL, rebuild whole canvas. "
            "Hair-prose only is not a pass. Read shared/victoria-face-pixel-gate.md."
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
            "Read shared/static-carousel-lock.md."
        )
    if step_id == "upload":
        extra_hard.append(
            "- Upload with --static-all-pngs. file1 is slide-01.png. "
            "Do not upload or require slide-01.mp4. Read shared/static-carousel-lock.md."
        )
    extra_hard_block = "\n".join(extra_hard)
    spawn_line = (
        f"Task(generalPurpose, model={GEMINI_MODEL})"
        if step_id in GEMINI_STEPS
        else "Task(generalPurpose) — real Task, not Director inline"
    )
    packet = f"""You are {spec['role']} for the Carusel plugin.

SPAWN
step: {step_id}
via: {state['dispatched_via']}
cloud_fallback: {spawn_line}
required_model: {state.get('model') or (GEMINI_MODEL if step_id in GEMINI_STEPS else 'inherit')}

HARD RULES
- Do only this step ({step_id}). Do not start the next role.
- Read and follow {spec['skill']} and {spec['agent']} verbatim.
- Read shared/taro-seichas-canon.md, shared/animals-viktoria-collage.md,
  shared/agent-pipeline-pitfalls.md and shared/locale-brand-contract.md.
{extra_hard_block}
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
        return 2
    print("✅ PIPELINE COMPLETE (all 12 steps ok or legally skipped)")
    return 0


DRY_RUN_WORKERS = (
    "researcher",
    "copywriter",
    "designer",
    "image-prompter",
    "slice",
    "motion-director",
    "animate",
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
                "face_lock: victoria-sheet.png",
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
        f"# Dry-run design\n\ncarousel_family: {family}\nface_lock: victoria-sheet.png\n"
        "Do not render. New clothes/pose each real carousel.\n",
    )
    write_json(
        mem / "design" / "CAROUSEL_SERIES_CONCEPT.json",
        {"carousel_family": family, "face_lock": "victoria-sheet.png", "dry_run": True},
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
            "face_lock": "victoria-sheet.png",
            "slice_method": "seam",
            "dry_run": True,
            "reference_contract": {"face_lock": "victoria-sheet.png"},
            "input_urls": [
                "https://example.invalid/victoria-sheet.png",
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
            "slides": [{"id": n, "file": None} for n in range(1, 10)],
        },
    )
    write_text_file(
        mem / "design" / "CAROUSEL_MOTION_ANALYSIS.md",
        "# Dry-run motion brief\n\nNo MP4.\n",
    )
    write_json(mem / "design" / "CAROUSEL_VIDEO_PROMPT.json", {"dry_run": True, "clips": []})
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
        model = GEMINI_MODEL if step_id in GEMINI_STEPS else None
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
    print(f"researcher+copywriter+caption model: {GEMINI_MODEL}")
    print(
        "steps recorded: researcher copywriter designer image-prompter slice "
        "motion-director animate design-guardian upload publish(skip) fixic(skip)"
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
    sub.add_parser("status")
    sub.add_parser("next")
    rec = sub.add_parser("record-dispatch")
    rec.add_argument("--step", required=True, choices=STEP_IDS)
    rec.add_argument("--via", required=True)
    rec.add_argument(
        "--model",
        default=None,
        help="Required for researcher/copywriter: gemini-3.7-flash-high",
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = resolve_workspace(args.workspace)
    repo_root = Path(args.repo_root).expanduser().resolve()
    if args.cmd == "init":
        return cmd_init(workspace, repo_root, args.lang, args.topic, args.run_id)
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
    raise SystemExit(f"unknown cmd {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
