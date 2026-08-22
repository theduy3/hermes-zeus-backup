---
name: voice-call-reminders
description: "Trigger a spoken call reminder via CallMeBot."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [hermes, reminders, voice-call, phone, telegram, callmebot, cron, notifications]
---

# Voice-Call Reminders (free, via CallMeBot)

Use this when the user wants Hermes to **call them with a spoken message** at a
scheduled time — a real phone call or an in-app Telegram voice call. The free
provider for this is **CallMeBot**.

## Key constraint (why a third party is required)

> **Telegram bots (including Hermes' own bot) cannot initiate a normal phone
> call or even a Telegram voice call on their own.** Only a human-initiated
> call is possible from a bot. To make an automated outbound call you must route
> through a service that places the call *for* you. CallMeBot is the free
> option that works here.

Two free CallMeBot modes, both verified live this session:

| Mode | Endpoint | Rings | Key needed? | Works w/o app/data |
|------|----------|-------|-------------|--------------------|
| **Telegram voice call** (in-app) | `https://api.callmebot.com/start.php` | Telegram app (bot calls you inside Telegram) | **No** (only @username authorization) | ❌ needs Telegram + data |
| **Real PSTN phone call** | `https://api.callmebot.com/call.php` | your actual phone (cellular) | **Yes** (one-time API key) | ✅ yes (uses cellular) |

**Recommendation:** Telegram in-app voice call is the simplest (no key) and the
user chose it this session. Real PSTN is the better "feels like a normal call"
option. The bundled `callmebot_reminder.sh` supports both via the same config.

## One-time setup (user action — agent cannot do this)

1. **Tell the agent your Telegram @username** (e.g. `@theduy`) → written into
   `callmebot.conf`.
2. **Authorize CallMeBot once** to contact that @username:
   - Open `https://api2.callmebot.com/txt/auth.php`, OR
   - message **@CallMeBot** / **@CallMeBot_API** on Telegram and follow its
     authorize prompt.
   - Without this, calls bounce as "not authorized". (The script surfaces this
     exact auth URL on failure.)
3. For **PSTN** mode only: get the API key from the **@CallMeBot_phone** bot,
   set `CALLMEBOT_KEY=` in `callmebot.conf`, and change `USER=` to your
   `+CCphonenumber` (e.g. `+16045551234`).

## How the agent wires a reminder

When the user says e.g. *"remind me at 3:45pm — call me to pick up Victoria"*:

1. Create a **one-off cron job**:
   ```bash
   cronjob action=create \
     name="Call: pick up Victoria" \
     schedule="2026-08-22T15:45:00" \
     no_agent=true \
     script="~/.hermes/scripts/callmebot_reminder.sh" \
     prompt="Pick up Victoria"
   ```
   - `no_agent=true` → the `script` IS the job; its stdout is delivered as the
     message. No LLM, no model/credits spent.
   - `script` receives the reminder text as `$1` (and optional `$2` lang).
2. The default gateway (must be healthy) fires it at the scheduled time → the
   spoken Telegram call rings the user.
3. Optionally also deliver a Telegram text message as a written record.

The reusable script lives at `scripts/callmebot_reminder.sh`; copy it to
`~/.hermes/scripts/` and pair with `templates/callmebot.conf` (mode 600). Both
are in this skill for re-deployment.

## Verification pattern (no real call needed)

Dry-run against a **fake** @username to prove the HTTP path is correct:
```bash
CALLMEBOT_CONF=./callmebot.conf USER=@nonexistentxyz ./callmebot_reminder.sh "test"
# Expect: "...User not authorized... Authorize CallMeBot once: <url>" + exit 1
```
A clean "not authorized" (NOT a 404/connection error) confirms the endpoint,
URL-encoding, and dispatch logic all work. Only the one-time authorization step
remains.

## Limits / caveats

- **Free tier is fair-use**: a handful of calls/day and a short cooldown
  between calls to the same user. Fine for personal reminders (Victoria pickup)
  — not for high-volume blasting.
- TTS voices are **Standard** only (Wavenet/premium voices unsupported).
- `lang` param uses Google "Voice Name" format, e.g. `en-US-Standard-B`,
  `en-GB-Standard-A`. See CallMeBot voice list.
- Telegram in-app call requires the Telegram app running + data connection at
  call time; PSTN mode does not.

## Pitfalls

1. **Don't try to make Hermes' own Telegram bot call the user.** It can't
   initiate calls. Route through CallMeBot (or another telephony provider).
2. **`start.php` (Telegram) needs NO key** — only @username authorization.
   Only `call.php` (PSTN) needs the API key. Confusing the two wastes a setup
   step.
3. **Authorization is per @username**, one-time, anti-spam. Until done, every
   call returns "not authorized" — that is expected, not a bug.
4. **`web_search`/`web_extract` are unavailable here** (no FIRECRAWL_API_KEY),
   so verify CallMeBot endpoints by `curl` probing the live API (e.g. a key-less
   probe of `call.php` returns "Wrong APIkey" → correct endpoint) rather than
   scraping docs. Doc URLs on callmebot.com often 404; the API itself is stable.
5. **One-off cron with `no_agent=true` + `script=`** is the right vehicle: it
   runs the call with zero LLM cost. Don't spin up an agent cron for a fixed
   message.
6. **Conf perms:** `callmebot.conf` holds identity/key → `chmod 600`; script
   `chmod 700`.

## Files in this skill

- `scripts/callmebot_reminder.sh` — the dispatcher (copy to `~/.hermes/scripts/`)
- `templates/callmebot.conf` — config template (copy, fill, `chmod 600`)
- `references/callmebot-endpoints.md` — endpoint/activation/voice details
