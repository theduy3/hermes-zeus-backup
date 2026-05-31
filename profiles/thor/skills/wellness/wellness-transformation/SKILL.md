---
name: wellness-transformation
description: Build complete body transformation stacks (assessment, training, nutrition, recovery, mindset) for real people with constraints — injuries, high stress, business travel, family obligations. Shoulder-safe protocols, travel adaptations, bookmark triggers for deferred diagnostics.
---

# Wellness Transformation Stack

Build sustainable, integrated transformation plans that survive real life — not just the first perfect week.

## Core Philosophy

- Plans must survive disruption (travel, stress, kids, bad sleep)
- Shoulder safety is default unless user proves overhead tolerance
- Bookmark triggers for stage-gated diagnostics (plateau, maintenance)
- Recovery is the hidden multiplier, not a luxury

## When to Use

User wants a complete transformation plan OR any single pillar (training, nutrition, recovery, mindset) that integrates with an existing stack.

## The 5-Pillar Stack

1. **Full Body Assessment** — honest baseline, realistic 90-day projection, metrics that matter
2. **Training Program** — shoulder-safe by default, double progression, equipment-appropriate
3. **Nutrition Plan** — protein-first, flexible structure, MVP day for chaos, eating-out rules
4. **Recovery Protocol** — sleep optimization, 10-min mobility, stress tactics, weekly audit
5. **Mindset Protocol** — identity shift, never-miss-twice, morning ritual, business trip card

## Stage-Gated Diagnostics (Bookmark Triggers)

Don't pre-build diagnostics for stages the user hasn't reached. Set bookmark triggers instead:

- **Week 4-6:** User says "plateau check" → run full plateau diagnostic with real numbers
- **Day 90+:** User says "maintenance plan" → build forever system from actual habit data

At setup, tell the user these triggers exist. Don't run the diagnostics until triggered.

## Shoulder-Safe Defaults

All training programs assume no overhead work unless user explicitly demonstrates overhead tolerance:
- No OHP, no pull-ups from dead hang, no overhead tricep work
- Lateral raises (to shoulder height only) for shoulder width
- Face pulls and rear delt flyes for posterior shoulder

## Travel Protocol (Monthly/Business)

When user travels regularly:
- **Workouts:** Hotel room bodyweight (see references/travel-workouts.md)
- **Nutrition:** Restaurant protein-first strategy + whey packing
- **Packing list:** Whey (pre-portioned), resistance band, lacrosse ball
- **Home recovery sessions travel perfectly** — no equipment needed
- Set weekly cron check-in for trip schedule updates

## Time Constraints

- **Gym sessions must stay under 60 minutes** — target ~49 min including warmup. If a user says they don't have 75 minutes, don't push it. Move cardio/accessory work to separate days.
- Rowing, mobility, and recovery work belong on non-gym days or evenings — never extend gym beyond the user's stated limit.
- Evening "couch" activities (lymphatic drainage, light stretching) are valid alternatives to dedicated sessions and reduce schedule pressure.

## Pull-Up Progression (Shoulder-Safe)

For users who can dead hang without triggering shoulder issues, integrate a 4-minute pull-up warmup into every gym session:

- **Dead Hang (active, scapula packed):** 2 × 30 sec
- **Scapular Pull-Up:** 8 slow reps (shoulder blades down, no elbow bend)

Progression stages (advance when rep range ceiling hit for 2 consecutive sessions):
1. Active Dead Hang → 3 × 30-45 sec
2. Scapular Pull-Up → 3 × 8-10
3. Negative Pull-Up → 3 × 3-5 (5-sec controlled lower)
4. Band-Assisted Pull-Up → 3 × 5-8
5. Full Pull-Up → 3 × AMRAP
6. Weighted Pull-Up → 3 × 5-8

## Plank Progression (Home-Only)

Planks live in the Saturday home Core session, never in the gym. Progression stages:

1. Forearm Plank → 3 × 45 sec (hips square, no sagging)
2. Shoulder Tap Plank (high plank) → 3 × 8 taps/side (no hip rocking)
3. Plank → Downward Dog transitions → 3 × 6 reps
4. Weighted Plank → 3 × 30-45 sec (2.5-5 kg plate on mid-back)

Advance when 3 consecutive sessions are clean. Full routines in references/home-recovery.md

## Rowing Integration (Strava)

Rowing machine = full-body + cardio + lymph pump, shoulder-safe. Schedule: 2 × 30 min/week on non-gym days (e.g., Thu + Sun). Never extend gym beyond the user's stated time limit.

### Strava OAuth Setup
When user has a Concept2 rower connected to Strava:
1. User generates tokens at strava.com/settings/api (Client ID + Client Secret)
2. User visits OAuth authorize URL to get an authorization code
3. Exchange code for refresh token via POST to /oauth/token
4. Save credentials to `~/.hermes/profiles/thor/secrets/strava.json`
5. Run `scripts/strava_refresh.py` to auto-refresh — it caches active token and renews before expiry
6. Pull activities via GET /api/v3/athlete/activities
7. Include weekly rowing stats (sessions, total distance, avg pace, watts) in the Sunday measurement audit

Token storage: `secrets/strava.json` (permanent) + `cache/strava_active.json` (ephemeral). Refresh script: `scripts/strava_refresh.py`.

If user prefers manual, accept photos of the rowing display and read stats from them.

### Rowing Metrics Tracked
- Sessions per week, total distance (meters), total time
- Average pace per 500m, average watts
- Heart rate (if strap connected to Concept2)

## Intake Tracking ("Log" Command)

The user only wants food, water, measurements, and activity data recorded when they explicitly say **"Log"** or **"Log this"**. 

- Cron job water/sitz bath/meditation pings are **nudges**, not tracked events. Don't record them as intake.
- If the user says "Log my morning breakfast" but already described it earlier in the conversation, don't re-ask for details — use what was already provided.
- When logging, include time, item, and estimated protein. Keep a running daily total.
- For voice-message food/water logs, first echo a clear **"What I heard"** list before or alongside totals so the user can catch transcription errors. If any phrase is ambiguous (e.g., "three 50 grams" could mean 350g or 3×50g), state the interpretation explicitly in the assumptions.

### Log File Convention

Primary target is the user's Obsidian vault. When it's unreachable (e.g., VPS can't access macOS paths), fall back to a local markdown log:

```
~/.hermes/profiles/thor/logs/food-log-YYYY-MM.md
```

One file per month. Each day is an `## MMM DD, YYYY (Day)` section containing:

- **Body Measurements** — waist, hips, chest, arms, waist-to-hip ratio (when provided)
- **Food Log** — table: Time | Item | Cal | Protein | Carbs | Fat
- **Hydration** — each 500ml round with time of day, running total vs 3,000ml target. If the user says “glass” or “cup” of water, count it as 500ml unless they specify another amount; keep the displayed label if useful (e.g., `Water — 2 glasses | 1,000ml`).
- **Activity** — steps, distance, move minutes, heart points (when user shares screenshot or numbers)
- **Daily totals** — running cal/protein consumed + remaining vs 1,950/150g targets

### Estimating Unspecified Foods

When logging a food item the user hasn't fully specified:
1. Ask for the critical missing detail (milk type, size, sweetener) — it often swings calories by 200+
2. If user confirms "just estimate it," use common defaults (e.g., 2% milk, medium=14oz, unsweetened)
3. Always state what you assumed so the user can correct

### Activity Screenshots

When the user sends a screenshot of their activity tracker, extract steps/distance/move minutes via OCR (see `references/activity-screenshots.md` for layouts and workflow) and log under the daily Activity section.

### Smoothie Brunch (Summer/IF-Adapted)

Each targets 40-50g protein via whey + Greek yogurt + fruit + greens. Juicing limited to 150ml accent shots, not meal replacements. See references/summer-smoothies.md

## Medical Condition Protocols

When a user has an active medical condition that interacts with training or nutrition, build an evidence-based protocol that integrates with the existing stack. Never replace medical advice — always include a "see a doctor if" trigger.

### Anal Fissures
Fiber ramp (20→30g over 2 weeks), 3L water minimum, 2 kiwis + 2-3 prunes + 1-2 tbsp flaxseed daily. Sitz baths 2x/day. See `references/fissure-recovery.md` for full protocol and integration with existing nutrition plan.

## Meditation Stack

For users adding meditation to a wellness stack:
- Start with breath awareness at the nostrils — one technique, no complexity
- Current beginner target: 10 min daily, keep it easy enough to do consistently (see `references/meditation-progression.md`)
- Add body scanning or noting only after the base habit is stable and sessions lengthen
- Never add duration after a missed day — return to the current easy target
- Set a daily cron reminder at a fixed morning time

## Daily Reminder Infrastructure

Maintain a `references/daily-reminders.md` with all active cron job IDs, times, purposes, and button callback conventions. When the user adds or removes a daily practice, update this reference and the corresponding cron jobs in sync.

### Reminder Button UX

For Thor Telegram wellness reminders, prefer the compact Water-log pattern:
- One short check-in line (e.g., `💧 Water check`, `🧘 Meditation check`)
- One inline button with an explicit logging action (e.g., `✅ Log 500ml`, `✅ Log 20 min`)
- `no_agent=true` cron job runs a `send_<habit>_button.py` script that sends directly via Telegram Bot API and prints nothing on success
- Button callback uses the stable `wl:<kind>:<amount>` convention and dispatches to `log_<habit>_button.py`
- After editing a reminder script, run a syntax check and trigger the cron job once so the user can verify the button format
- When the same habit needs different copy/media by time of day, keep the shared sender generic and add thin wrapper scripts (e.g., `send_morning_meditation_button.py`, `send_evening_meditation_button.py`) that set `THOR_MEDITATION_REMINDER_TEXT` / `THOR_MEDITATION_MINUTES` before running the base sender. Then update each cron job to the appropriate wrapper script instead of hardcoding time-specific text in the generic sender.
- If the user adds a link to a recurring reminder, update **all requested variants** (morning + evening, etc.) and record the link/button details in `references/daily-reminders.md` so later changes don't silently drop it.

## Reference Files

- `references/home-recovery.md` — Full routines for Spine & Posture (Tue), Lymphatic Flow (Thu), Core & Release (Sat)
- `references/travel-workouts.md` — Hotel room bodyweight session, packing list, travel nutrition rules
- `references/summer-smoothies.md` — 5 smoothie brunch recipes + 2 juice accents for IF users
- `references/fissure-recovery.md` — Anal fissure dietary/hydration protocol, sitz baths, integration with nutrition plan
- `references/meditation-progression.md` — Breath awareness technique, 20→60 min ramp, daily practice rules
- `references/daily-reminders.md` — Cron job schedule: water, sitz baths, meditation, weekly trip check

## Key Mental Models

- **"Never miss twice"** — one slip is math (meaningless), two is the spiral
- **"Done beats perfect"** — 20-min partial workout > skipped 45-min plan
- **"MVP day"** — 150g protein is the entire floor. Hit that and the day counts.
- **Bookmark triggers** — defer stage-gated diagnostics, don't pre-build them

## Cheat Day Protocol

One meal per week, not one day. Rules:
- Still hit 150g protein
- Enjoy it socially (family dinner, not solo binge)
- Never miss twice — the very next meal is back on plan
- Skip the scale the next morning (water weight spike is normal, not fat)
- Recovery: extra liter of water + 15-20 min walk. No fasting punishment, no cardio punishment.

## Pitfalls

- Don't pre-run plateau or maintenance diagnostics before the user reaches those stages
- Don't build plans that only work in perfect conditions — every plan needs a survival mode
- For IF users, ensure protein targets are achievable in the eating window (two meals = ~75g each)
- Shoulder limitations aren't always overhead — verify ROM with the user for each exercise class
- **Never log cron job responses as intake** unless the user explicitly says "Log." Cron pings are nudges, not tracked events. Only record food/water when commanded.
- **Audit wellness button/manual date bugs actively.** If the user says water/food logs were marked for yesterday/today incorrectly, inspect the actual daily log and callback/audit trail before answering. If the user says they are “completing” a specific prior date, log/correct entries under that date even if the current clock has rolled past midnight. Delayed clicks on old reminder buttons should count for the day the user pressed the button, not the original reminder message date. Correct the affected day totals and patch the button handler/script so the same date drift cannot recur.
- Respect gym time limits — never suggest extending sessions beyond the user's stated ceiling
- **Planks are home-only** unless the user explicitly wants them in the gym
- When a user requests a "today plan," give only that day's schedule — not the full week
- **Don't re-ask for information already provided.** If the user says "I already gave it to you" or "look back at what I said," scan the conversation before asking again. This wastes patience.
- **Voice logs need a transcript echo.** Before finalizing a voice-message intake log, write a concise "What I heard" list of foods/water and any assumptions; do not only give totals. This is especially important for speech-to-text ambiguities around quantities.
