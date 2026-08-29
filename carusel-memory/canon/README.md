# Canon pointer

Always-on rules live in the committed plugin contracts (so daily 11:10 cannot drift):

- `shared/taro-seichas-canon.md`
- `shared/animals-viktoria-collage.md`
- `shared/locale-brand-contract.md`
- `shared/caption-format-contract.md`
- `scripts/canon_gate.py`
- `scripts/pipeline_gate.py`
- `shared/swarm-spawn-contract.md` — Director orchestrates only; all human text = Gemini (`written_by: gemini`); after GATE+face the swarm publishes via Composio; `dry-run` = 11 records, no PNG
- `shared/composio-instagram-publish-contract.md` — aliases instagram-ru / instagram-en; env `COMPOSIO_API_KEY`; no key = SKIP
- `carusel-memory/canon/live-posts.json` — already-live posts; do not republish

References: `carusel-memory/references/`.
Dated packs: `carusel-memory/packs/`.
