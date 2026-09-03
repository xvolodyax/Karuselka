# publish-log

## 2026-08-30T09:03:48Z
status: ok
reason: composio
via: composio MCP (COMPOSIO_MULTI_EXECUTE_TOOL)
telegram: forbidden
browser: forbidden
local_script: skipped (alias field null on REST; MCP aliases used)
session_id: feet
alias_required: instagram-ru / instagram-en (never default)
no_blind_retry: true
- ru: alias=instagram-ru handle=@todaytaro_ru connected_id=instagram_inroad-levis ig_user_id=28345168661841021 (from INSTAGRAM_GET_USER_INFO) creation_id=17921802750416739 media_id=18109887448855475 status=published permalink=https://www.instagram.com/p/DcqJGCblQqv/ posted_at=2026-08-30T09:01:31+0000 trigger=СУББОТА
- en: alias=instagram-en handle=@todaytaro_bot connected_id=instagram_mede-racily ig_user_id=28313136201706513 (from INSTAGRAM_GET_USER_INFO) creation_id=18011985128957836 media_id=18113257384788858 status=published permalink=https://www.instagram.com/p/DcqJS--m0op/ posted_at=2026-08-30T09:03:12+0000 trigger=WEEKEND

## 2026-09-01T09:16:00Z
status: fail
reason: composio-error
via: composio REST script
telegram: forbidden
api_key_source: env COMPOSIO_API_KEY
alias_required: instagram-ru / instagram-en (never default)
Composio Instagram alias instagram-ru (@todaytaro_ru) not found. Alias is required; default account is forbidden.
local_script: failed (alias field null on REST /connected_accounts)

## 2026-09-01T09:23:43Z
status: ok
reason: composio
via: composio MCP (COMPOSIO_MULTI_EXECUTE_TOOL)
telegram: forbidden
browser: forbidden
local_script: skipped (alias field null on REST; MCP aliases used)
session_id: nuts
dispatch_id: f907744288624261b6f8a3ffdede5b3a
dispatched_via: Task(generalPurpose)
alias_required: instagram-ru / instagram-en (never default)
no_blind_retry: true
file1_kind: png
this_run: static_all_pngs
duplicate_check: GET_IG_USER_MEDIA limit=3
- ru live top before post: https://www.instagram.com/p/DcvUJFqmz0R/ IMAGE 01.09 trigger=ЕХАТЬ (not ЗАВТРА) — not a duplicate, published
- en live top before post: https://www.instagram.com/p/DcszQubG-bl/ MONDAY 31.08 — not a duplicate, published
- ru: alias=instagram-ru handle=@todaytaro_ru connected_id=instagram_inroad-levis ig_user_id=28345168661841021 (from INSTAGRAM_GET_USER_INFO) creation_id=17922092973416739 media_id=17968814088137847 status=published permalink=https://www.instagram.com/p/DcvVF5Wm6fM/ posted_at=2026-09-01T09:22:28+0000 trigger=ЗАВТРА
- en: alias=instagram-en handle=@todaytaro_bot connected_id=instagram_mede-racily ig_user_id=28313136201706513 (from INSTAGRAM_GET_USER_INFO) creation_id=18012278483957836 media_id=18385449295203014 status=published permalink=https://www.instagram.com/p/DcvVOcPFe5h/ posted_at=2026-09-01T09:23:43+0000 trigger=TOMORROW
telegram: not sent
