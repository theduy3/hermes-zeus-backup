# X search enable / verify checklist

## Native `x_search` (preferred public search)

- [ ] xAI creds present (`xai-oauth` in auth pool or `XAI_API_KEY`)
- [ ] `hermes tools enable x_search --platform telegram` (and cli) on default
- [ ] Same enable for each named profile: `hermes -p <name> tools enable x_search --platform telegram`
- [ ] Each profile `config.yaml` has `x_search` under `platform_toolsets.telegram`
- [ ] Gateways restarted; new Telegram session or `/new`
- [ ] Smoke: `x_search_tool(query="…")` returns success JSON (no `limit=` kwarg)

## Agent Reach twitter-cli (session / cookie path)

- [ ] `twitter` on PATH, version ≥ 0.8.5 (`uv tool install twitter-cli`)
- [ ] User Cookie-Editor header from x.com has `auth_token` + `ct0`
- [ ] Imported via `twitter-ar-import-cookies --from-file …` (temp file shredded; no value echo)
- [ ] `~/.agent-reach/secrets/twitter.env` exists mode 600 with `TWITTER_AUTH_TOKEN` + `TWITTER_CT0`
- [ ] Prefer `twitter-ar status` over bare `twitter` when helper exists
- [ ] Live smoke: `twitter-ar status` authenticated + `twitter-ar feed -n 1` (or whoami)
- [ ] Do **not** require `doctor` `active_backend` non-null — doctor often stays warn after good cookies
- [ ] Do not treat `configure twitter-cookies` alone as runtime-ready
- [ ] Keyword search: use `x_search`; if `twitter-ar search` 404s, fall back to feed/user-posts/`x_search`

## Gateway hygiene after tool enable

- [ ] Exactly one python `hermes gateway run` for default
- [ ] Exactly one `hermes -p <name> gateway run` per profile
- [ ] Latest log lines only: `✓ telegram connected` (ignore older timestamps)
- [ ] No duplicate PIDs / polling conflict loops

## User-facing honesty

- [ ] If Agent Reach Twitter is warn/off, say so and use `x_search` for public search
- [ ] Never print cookies, bot tokens, or xAI tokens
