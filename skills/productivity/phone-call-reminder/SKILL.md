---
name: phone-call-reminder
description: "Spoken Telegram call reminders via CallMeBot + Hermes cron."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [reminder, phone-call, telegram, callmebot, voice, cron]
---

# Phone-call reminder via CallMeBot

Fire a spoken reminder to the user by phone, for free, using CallMeBot. Verified
working 2026-08-21 with `USER=@theduynguyen`.

## When to use

The user says something like *"call me at HH:MM [to X]"* or *"remind me at
HH:MM — call me [to do X]"*. This is a **spoken** reminder: at the due time the
Telegram bot rings the user (in-app voice call) and speaks the message via TTS.

## Architecture (already built)

- `~/.hermes/scripts/callmebot_reminder.sh` — fires the CallMeBot request.
  - Telegram voice call (default, no key): `https://api.callmebot.com/start.php?source=hermes&user=@USER&text=MSG&lang=LANG`
  - Optional real PSTN call (needs `CALLMEBOT_KEY` + `USER=+CC…`): `https://api.callmebot.com/call.php?phone=USER&text=MSG&lang=LANG&key=KEY`
- `~/.hermes/scripts/callmebot.conf` — `600` perms; holds `USER=@handle` and
  optional `CALLMEBOT_KEY`. No secrets other than the username/key live here.
- The dispatch is a one-off Hermes **cron job** (`no_agent: true`,
  `script: callmebot_reminder.sh "MESSAGE"`) so it runs inside the gateway
  even with no user present. The default gateway (healthy) runs it.

The script strips HTML from the CallMeBot response and surfaces the one-time
authorize link on failure; exits non-zero on rejected dispatch.

## Setup (one-time, user does most of it)

1. **Hermes side (already done):** scripts + conf exist. `USER` is the user's
   real Telegram `@username` (case-sensitive, copy from Telegram → Settings →
   Username). Do NOT guess it; the API rejects unknown handles as
   "not authorized".
2. **User authorizes CallMeBot (browser OAuth, required):**
   - Open `https://api2.callmebot.com/txt/auth.php` in a browser.
   - Click **Login** → completes Telegram OAuth for the `@username` account.
   - Must reach a success/"authorized" screen, not just message a bot.
   - Telegram → Settings → Privacy & Security → **Voice Calls** must allow calls
     (Everybody, or add `@CallMeBot_API` as a contact), else the call is silently blocked.
3. **Test once:** `cd ~/.hermes/scripts && CALLMEBOT_CONF=./callmebot.conf ./callmebot_reminder.sh "Test from Hermes"`. Expected: `Autorization OK … Starting Telegram Audio Call … Call answered and ended by the user`. The user must **answer** to hear the TTS.

## Creating a reminder job

When the user names a time + message, create a one-off cron via the `cronjob`
tool with:

- `action=create`
- `schedule` = ISO local timestamp OR cron expr, e.g. `2026-08-22T15:45:00` or `0 15 * * *`
- `prompt` = empty/short note (the script does the work)
- `no_agent=true`
- `script` = **basename only** (relative to `~/.hermes/scripts/`), e.g.
  `callmebot_reminder.sh "Pick up Victoria at 3:45pm"`
  — the tool REJECTS absolute paths; use the filename, not `/home/hermes/...`.
- `deliver=origin` (or the user's telegram) so they also get a written log.

Confirm the job id back to the user. The gateway fires it at the due time.

## Multi-reminder architecture (wrapping existing reminders)

To make existing cron reminders also ring the phone, use TWO patterns:

### A) Fixed recurring reminder (known cron time)
Wrap the original reminder with a pair of call jobs: one at the exact time, one
30 min before. Each is its own `no_agent` cron job pointing at a small wrapper
script that calls `callmebot_reminder.sh "<spoken text>"`. Example wrappers
(built 2026-08-21 for Catthew):
- `callmebot_c7_vehicle.sh` / `callmebot_c7_vehicle_at.sh` — Vehicle odometer
  (cron `30 8 30 6,12 *` + `0 9 30 6,12 *`).
- `callmebot_c9_humidifier.sh` / `callmebot_c9_humidifier_at.sh` — Weekly
  humidifier (cron `30 20 * * 3` + `0 20 * * 3`).
If the user wants ONLY an at-time call (no 30-min-before), create just the
at-time job — e.g. Thor water-intake reminders (6/day, 7AM/10AM/1PM/4PM/7PM/10PM)
use a single `callmebot_reminder.sh "Time to drink water. Hydration reminder."`
cron job per time, no before-call.

### B) Dynamic "tasks & events with a specific time" digest
A daily generator (`callmebot_tasks_events.sh`, cron `15 5 * * *`) scans
`/vault/Tasks/tasks/*.md` (tasks with BOTH `due_date` + `due_time`, status not
completed/cancelled, NOT tagged `catthew`) and `/vault/Tasks/calendar/*.md`
(events with a real `start` time, `allDay: false`, not completed), and for each
item DATED TODAY creates two one-off call jobs via
`hermes cron create "<ISO>" "name" --no-agent --script "callmebot_reminder.sh '<msg>'"`:
one 30 min before and one at the time. Emits output only if it scheduled something.

**Scheduling inside a script:** `at` is NOT installed. To schedule future
calls from a script, shell out to `hermes cron create "<ISO-timestamp>"
"name" --no-agent --script "callmebot_reminder.sh '<msg>'"`. Verified: it
accepts ISO `YYYY-MM-DDTHH:MM:SS` and returns `once at ...`.

**Frontmatter parse gotchas (callmebot_tasks_events.sh):**
- Use `local` only inside functions; top-level loop vars must be plain.
- Calendar times are messy: `earnings-*` use `"Aftermarketclose"` / `"Timenotconfirmed"`
  and flights use `"8:35PMEDT"` — none parse as `HH:MM`, so they're safely
  skipped (no false schedule). Only clean `HH:MM`/`HH:MM:SS` times schedule.
- Pass the message as a single shell-quoted arg to the script inside the
  `--script` string (use a `_q` helper that single-quotes safely).

## Behavior notes

- **Answer to hear it:** the bot speaks only after the user picks up. No-answer
  = ring nudge only, no voicemail drop. Tell the user: pick up to hear the words.
- **Fair-use limits:** free CallMeBot is a few calls/day with a short cooldown
  between calls to the same user. Fine for personal reminders (Victoria pickup);
  not for high-volume blasting.
- **Rate limit:** repeated API hits trip `"Too many requests"`. If seen, **stop
  calling the API** and wait ~3 min before retrying. Do not loop/retry rapidly.
- **`source=hermes`** in the URL is an arbitrary tag; safe to keep.
- Voice: default `lang=en-US-Standard-B`. Other `en-*`/regional Standard voices
  are valid (Wavenet/premium voices are NOT supported by the API).

## Pitfalls (learned this session)

- A plain `/start` message to the bot is NOT sufficient — the **browser OAuth**
  at `txt/auth.php` is what registers the username for the call bot
  (`@CallMeBot_API`).
- The wrong `@username` is the #1 failure: "not authorized" usually means the
  handle in `callmebot.conf` doesn't match the account that did the OAuth. The
  user's display name is NOT their @username.
- The real PSTN `call.php` endpoint needs an `API key` from the `@CallMeBot_phone`
  bot; `start.php` (Telegram in-app) needs none. Keep both paths in the script
  but default to the keyless in-app call unless the user supplies a key.
- Repeated authorization checks during setup tripped the global rate limit and
  blocked the real test — batch verification, then wait before the live call.

## Verification

After setup, run the script once and confirm `Autorization OK` + `Call answered`
in the output before promising the user it works. Keep the conf at `600` and the
script at `700`.

**End-to-end proof (after wiring call-reminder cronjobs):** a manual dry-run is
NOT sufficient. Prove the cron-executed path actually reaches the phone:
1. Run the wrapper directly:
   `cd ~/.hermes/scripts && CALLMEBOT_CONF=./callmebot.conf ./callmebot_reminder.sh "verify test"`
   — expect `CallMeBot voice call dispatched to @user`.
2. For the dynamic generator, temporarily drop a throwaway today-task
   (`due_date`+`due_time` today, `status: pending`) and a today-calendar event
   with a clean `start: HH:MM`, run the generator, confirm it creates the
   30-min-before + at-time call jobs, then delete the temp files AND the 4
   created call jobs. Or just `cronjob run <generator_id>` and confirm clean
   execution (0 scheduled is the correct result on a day with no timed items).
3. Do NOT trust a dry-run that intercepts `hermes` with a fake PATH — that only
   proves frontmatter parsing, not that CallMeBot accepts the real call.

**Reusable dry-run for the generator (no real calls):** prepend a fake `hermes`
shell script on PATH that appends each `hermes cron create` invocation to a log
file, then run the generator. Confirms which items WOULD schedule without
creating jobs. See `references/wrapped-reminders-current.md` for the live
wiring as of the build date.
