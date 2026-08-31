# publish-log

## 2026-08-31T09:42:46Z
status: fail
reason: composio-error
via: composio REST script
telegram: forbidden
api_key_source: env COMPOSIO_API_KEY
alias_required: instagram-ru / instagram-en (never default)
Composio Instagram alias instagram-ru (@todaytaro_ru) not found. Alias is required; default account is forbidden.
local_script: failed (alias field null on REST /connected_accounts)

## 2026-08-31T09:48:21Z
status: ok
reason: composio
via: composio MCP (COMPOSIO_MULTI_EXECUTE_TOOL)
telegram: forbidden
browser: forbidden
local_script: skipped (alias field null on REST; MCP aliases used)
session_id: film
dispatch_id: 2aca33c30e994f319302ad24cfdb6aa3
dispatched_via: Task(generalPurpose)
alias_required: instagram-ru / instagram-en (never default)
no_blind_retry: true
duplicate_check: GET_IG_USER_MEDIA limit=3
- ru live top before post: https://www.instagram.com/p/DcsytNnmwuv/ IMAGE 31.08 trigger=ПОЗВОНИТЬ (not ПОНЕДЕЛЬНИК) — not a duplicate, published
- en live top before post: https://www.instagram.com/p/DcqJS--m0op/ WEEKEND 30.08 — not a duplicate, published
- ru: alias=instagram-ru handle=@todaytaro_ru connected_id=instagram_inroad-levis ig_user_id=me creation_id=17921952438416739 media_id=18009334409955562 status=published permalink=https://www.instagram.com/p/DcszHTWIHS5/ posted_at=2026-08-31T09:47:10+0000 trigger=ПОНЕДЕЛЬНИК
- en: alias=instagram-en handle=@todaytaro_bot connected_id=instagram_mede-racily ig_user_id=me creation_id=18012132380957836 media_id=18093108425438526 status=published permalink=https://www.instagram.com/p/DcszQubG-bl/ posted_at=2026-08-31T09:48:21+0000 trigger=MONDAY
telegram: not sent
