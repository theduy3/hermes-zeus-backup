---
name: agent-reach-platform-auth
description: "Use when importing Agent Reach Reddit/Twitter VPS cookies."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent-reach, reddit, twitter, cookies, rdt, twitter-ar, telegram, vps]
    related_skills: [agent-reach, x-twitter-search-routing, social-platform-workflows]
---

# Agent Reach platform auth (VPS / Telegram)

Class-level workflow for **login-state platforms** on a headless Hermes host: user exports Cookie-Editor headers on desktop; agent imports safely; smoke-tests before claiming live.

Companion skills (may be user-owned/protected — recommend `hermes curator adopt` if they drift):
- `agent-reach` — platform routing table
- `x-twitter-search-routing` — X keyword search prefers native `x_search`
- Host doc: `~/.agent-reach/docs/telegram-platforms.md`

## When to Use

- User wants to finish Reddit (`rdt`) or Twitter Agent Reach (`twitter-ar`) setup
- User pastes a Cookie-Editor header from reddit.com or x.com
- User asks which search platforms work on Telegram bots
- Doctor shows warn and you need the correct readiness rule

## Decision tree

1. **Public web / GitHub / YouTube / V2EX / RSS** — no cookies; use Exa, `gh`, yt-dlp, V2EX API, feedparser.
2. **Public X keyword search** — Hermes native **`x_search`** (no cookies).
3. **Reddit** — `rdt` after cookie import (`reddit_session` required).
4. **X session reads (feed / whoami / user / user-posts / tweet)** — `twitter-ar` after cookie import (`auth_token` + `ct0`).
5. **Facebook / Instagram** — OpenCLI desktop only; **not** available on this VPS Telegram path.
6. **Skipped unless user asks** (this host): bilibili, xueqiu, linkedin, xiaohongshu, xiaoyuzhou.

## User export steps

### Reddit (reddit.com)
1. Log into https://www.reddit.com fully.
2. Cookie-Editor (Moustachauve) → Export → **Header String**.
3. Must include `reddit_session=…`.
4. Paste as `rdt cookies:` + full string (JSON name/value also accepted by importer).

### Twitter (x.com)
1. Log into https://x.com fully.
2. Cookie-Editor → Export → **Header String**.
3. Must include both `auth_token=…` and `ct0=…`.
4. Paste as `twitter cookies:` + full string.

## Agent import (never print values)

```bash
umask 077
f=$(mktemp /tmp/cookie-XXXXXX.txt)
# write user paste into $f (heredoc), then:
rdt-import-cookies --from-file "$f"            # Reddit
twitter-ar-import-cookies --from-file "$f"     # Twitter
shred -u "$f" 2>/dev/null || rm -f "$f"
```

Prefer `--from-file` over shell argv so secrets stay out of process lists / history.

| Platform | Helper | Path | Mode | Required keys |
|----------|--------|------|------|---------------|
| Reddit | `rdt-import-cookies` | `~/.config/rdt-cli/credential.json` | 600 | `reddit_session` |
| Twitter | `twitter-ar-import-cookies` | `~/.agent-reach/secrets/twitter.env` | 600 | `TWITTER_AUTH_TOKEN`, `TWITTER_CT0` |

`twitter-ar-import-cookies` also runs `agent-reach configure twitter-cookies … --sync-legacy-twitter` for doctor completeness. That alone does **not** export shell env for bare `twitter` — always use **`twitter-ar`**.

## Smoke tests (only claim live after these)

```bash
# Reddit
rdt status                    # authenticated true, username, capabilities include read
rdt search "LocalLLaMA" --limit 3

# Twitter — status/feed/user first; keyword search last
twitter-ar status
twitter-ar whoami
twitter-ar feed -n 3
twitter-ar user-posts @OpenAI -n 2
# twitter-ar search "…" often HTTP 404 even when auth is good
```

## Doctor warn ≠ broken

`agent-reach doctor --json` deliberately skips live `rdt status` / `twitter status` and often leaves those platforms at `warn` with `active_backend: null` **after a successful import**. Never re-ask for cookies solely because doctor is warn. Smoke-test the real CLI.

## X search routing

| Intent | Use |
|--------|-----|
| Public keyword/topic search on CLI or Telegram | native **`x_search`** |
| Home feed, profile, user posts, single tweet | **`twitter-ar`** |
| `twitter-ar search` returns 404 | fall back to `x_search` or `feed` / `user-posts` |

`ClientTransaction` warnings from twitter-cli can appear on successful calls — ignore unless the command fails.

## Safety

- Never echo cookie headers, `credential.json`, or `twitter.env` values.
- Suggest user delete the chat paste after successful import.
- Cookies = full account access; re-import when status flips to not_authenticated / login walls.
- Write actions (post/like/comment) need explicit user intent — default is read-only.

## Detail

See `references/import-and-smoke.md` for a short checklist.
