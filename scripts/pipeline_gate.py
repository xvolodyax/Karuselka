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
}
RAW_URL_RE = re.compile(r"https?://|instagram\.com/|t\.me/|telegram\.me/", re.I)
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
    return {
        "lang": lang,
        "handle": handle,
        "publish_requested": publish_requested,
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
                    "cta_style: header_link",
                    "bot_vs_app: @todaytaro_bot is a Telegram bot, not an app",
                    "slides: 9",
                    "grid: 3x3",
                    "slide_01: mp4_allowed",
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
    print(f"dispatch_mode={ledger.get('dispatch_mode')} publish_requested={ledger.get('publish_requested')}")
    for spec in load_steps(repo_root):
        state = ledger["steps"][spec["id"]]
        status = state.get("status") or "pending"
        via = state.get("dispatched_via") or "-"
        print(f"- {spec['id']:18} {status:10} via={via}")
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
    print(f"skill={spec['skill']}")
    print(f"agent={spec['agent']}")
    print("STOP if you were about to write these artifacts in the parent chat:")
    for rel in spec["required_artifacts"]:
        print(f"  - {rel}")
    return 0


def cmd_record_dispatch(workspace: Path, repo_root: Path, step_id: str, via: str) -> int:
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
    ledger = load_ledger(workspace)
    require_previous_done(ledger, step_id)
    state = ledger["steps"][step_id]
    if state.get("status") == "ok":
        raise SystemExit(f"step {step_id} already ok")
    dispatch_id = uuid.uuid4().hex
    state.update(
        {
            "status": "dispatched",
            "dispatched_via": via,
            "dispatch_id": dispatch_id,
            "started_at": utc_now(),
            "finished_at": None,
            "skip_reason": None,
        }
    )
    ledger["dispatch_mode"] = infer_dispatch_mode(via)
    save_ledger(workspace, ledger)
    print(f"recorded {step_id} via={via}")
    print(f"dispatch_id={dispatch_id}")
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
        if lang == "en" and re.search(r"\bapp\b", blob, re.I) and "bot" not in blob.lower():
            errors.append(f"{caption_rel} looks like it confuses the Telegram bot with an app")
        if lang == "en" and re.search(r"academy", blob, re.I):
            errors.append(f"{caption_rel} Academy is forbidden on EN")
        if "личный аудиоразбор" in blob:
            errors.append(f"{caption_rel} forbidden phrase личный аудиоразбор")
        if caption.get("trigger_word") in {None, ""} and data.get("trigger_word") in {None, ""}:
            errors.append(f"{caption_rel} missing trigger_word (comment CTA)")
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
    for rel in spec["required_artifacts"]:
        if not file_ok(workspace, rel):
            errors.append(f"missing artifact {rel}")
    errors.extend(verify_fragment(workspace, spec, state))
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
        if "PLACEHOLDER" in json.dumps(prompt):
            errors.append("CAROUSEL_IMAGE_PROMPT.json still contains PLACEHOLDER")
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
    nxt = spec.get("handoff_next")
    if nxt:
        print(f"HANDOFF_NEXT: {nxt}")
        print("Director: record-dispatch the next step. Do not do it yourself.")
    return 0


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
    packet = f"""You are {spec['role']} for the Carusel plugin.

HARD RULES
- Do only this step ({step_id}). Do not start the next role.
- Read and follow {spec['skill']} and {spec['agent']} verbatim.
- Read shared/taro-seichas-canon.md, shared/animals-viktoria-collage.md,
  shared/agent-pipeline-pitfalls.md and shared/locale-brand-contract.md.
- lang={brief['lang']}. Brand handle={brief['handle']}.
- Write artifacts only to the paths listed below.
- End with fragment {spec['fragment']}.
- Fragment MUST contain:
  dispatched_via: {state['dispatched_via']}
  dispatch_id: {state['dispatch_id']}
  incident_report: none
  HANDOFF_NEXT: {spec.get('handoff_next')}
- Instagram: no raw URLs; CTA is one comment trigger word; team answers in Direct.
- @todaytaro_bot is a Telegram bot, not an app.
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
        return cmd_record_dispatch(workspace, repo_root, args.step, args.via)
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
    raise SystemExit(f"unknown cmd {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
