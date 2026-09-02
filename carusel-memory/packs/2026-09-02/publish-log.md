# publish-log

## 2026-09-02T09:27:40Z
status: fail
reason: composio-error
via: composio
telegram: forbidden
api_key_source: env COMPOSIO_API_KEY
alias_required: instagram-ru / instagram-en (never default)
Composio Instagram alias instagram-ru (@todaytaro_ru) not found. Alias is required; default account is forbidden.

## 2026-09-02T09:33:00Z
status: ok
reason: composio
via: composio MCP (COMPOSIO_MULTI_EXECUTE_TOOL)
telegram: forbidden
browser: forbidden
local_script: skipped (alias field null on REST; MCP aliases used)
session_id: told
alias_required: instagram-ru / instagram-en (never default)
no_blind_retry: true
- ru: alias=instagram-ru handle=@todaytaro_ru connected_id=instagram_inroad-levis ig_user_id=28345168661841021 (from INSTAGRAM_GET_USER_INFO) creation_id=17922247092416739 media_id=17905668447514427 status=published permalink=https://www.instagram.com/p/Dcx7CK1lV0F/ posted_at=2026-09-02T09:32:44+0000 trigger=ПЛАН shortcode=Dcx7CK1lV0F
- en: alias=instagram-en handle=@todaytaro_bot connected_id=instagram_mede-racily ig_user_id=28313136201706513 (from INSTAGRAM_GET_USER_INFO) creation_id=18012423251957836 media_id=18618303673046980 status=published permalink=https://www.instagram.com/p/Dcx7DGam5AN/ posted_at=2026-09-02T09:32:44+0000 trigger=SLOT shortcode=Dcx7DGam5AN

## 2026-09-02T09:39:20Z
status: already-live (no republish)
reason: graph-api-verify
via: composio MCP INSTAGRAM_GET_IG_USER_MEDIA + INSTAGRAM_GET_IG_MEDIA
session_id: hill
browser: forbidden
chrome_instagram: not opened
duplicate: skipped — both 02.09 carousels are the latest CAROUSEL_ALBUM on each alias
gate: PASS
face: ABSENT
- ru: alias=instagram-ru handle=@todaytaro_ru media_id=17905668447514427 permalink=https://www.instagram.com/p/Dcx7CK1lV0F/ timestamp=2026-09-02T09:32:44+0000 trigger=ПЛАН children=9 IMAGE feed_position=1 (above DcvVF5Wm6fM ЗАВТРА)
- en: alias=instagram-en handle=@todaytaro_bot media_id=18618303673046980 permalink=https://www.instagram.com/p/Dcx7DGam5AN/ timestamp=2026-09-02T09:32:44+0000 trigger=SLOT children=9 IMAGE feed_position=1 (above DcvVOcPFe5h TOMORROW)
