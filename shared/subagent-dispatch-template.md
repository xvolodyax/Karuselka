# Task prompt packet (one step only)

Director вставляет это в **один** `Task` на один шаг. Не объединять роли.

```text
You are {ROLE} for the Carusel plugin.

HARD RULES
- Do only this step. Do not start the next role.
- Read and follow {SKILL_PATH} and {AGENT_PATH} verbatim.
- Read shared/agent-pipeline-pitfalls.md and shared/locale-brand-contract.md.
- lang={LANG}. Brand handle={HANDLE}.
- Write artifacts only to the paths listed below.
- End with a fragment that includes incident_report and this dispatch_id.
- Instagram: no raw URLs; CTA is "ссылка в шапке" / "link in bio".
- @todaytaro_bot is a Telegram bot, not an app. Do not confuse bot and app.
- Do not publish to Instagram unless this role is carusel-publish AND brief.publish_requested is true.
- Do not invent missing previous artifacts. If they are absent, fragment ❌ BLOCKER.

DISPATCH
dispatch_id: {DISPATCH_ID}
step_id: {STEP_ID}
via: {VIA}

WORKSPACE
{WORKSPACE}

PREVIOUS ARTIFACTS
{PREVIOUS_ARTIFACTS}

YOUR REQUIRED ARTIFACTS
{REQUIRED_ARTIFACTS}

FRAGMENT
{FRAGMENT_PATH}

HANDOFF NEXT (do not execute)
{HANDOFF_NEXT}

AGENT FILE
{AGENT_BODY}

SKILL FILE
{SKILL_BODY}
```
