# Import + smoke checklist

## Reddit
- [ ] Header from reddit.com includes `reddit_session`
- [ ] `rdt-import-cookies --from-file …` exit 0
- [ ] `~/.config/rdt-cli/credential.json` mode 600
- [ ] `rdt status` → authenticated true
- [ ] `rdt search "…" --limit 3` returns posts
- [ ] Temp file shredded; values not printed

## Twitter Agent Reach
- [ ] Header from x.com includes `auth_token` + `ct0`
- [ ] `twitter-ar-import-cookies --from-file …` exit 0
- [ ] `~/.agent-reach/secrets/twitter.env` mode 600
- [ ] `twitter-ar status` → authenticated true
- [ ] `twitter-ar feed -n 1` (or whoami) OK
- [ ] Do not fail the setup if `twitter-ar search` is HTTP 404
- [ ] Keyword search path documented as native `x_search`
- [ ] Temp file shredded; values not printed

## Telegram “what can I search?” answer shape
Live (typical this host after cookie setup): web/Exa, X via `x_search`, Reddit via `rdt`, GitHub `gh`, YouTube, V2EX, RSS.
Not on VPS Telegram: Facebook, Instagram (OpenCLI desktop).
Skipped unless asked: bilibili, 小红书, LinkedIn, 雪球, 小宇宙.
