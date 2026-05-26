# Daily Reminders — Cron Job Inventory

Cron schedules are interpreted in Pacific local clock time by the scheduler. Names should match the user-visible phone time. If user is in Quebec, switch wellness reminders to Eastern local time when requested.

## Daily

- 🧘 Meditation - 7:15AM Pacific
  - Job ID: `2616b50dddac`
  - Schedule: `15 7 * * *`

- 💧 Water - 7AM Pacific
  - Job ID: `caabc02dabc9`
  - Schedule: `0 7 * * *`

- 🛁 Sitz Bath - 9AM Pacific
  - Job ID: `b7db2ca9de46`
  - Schedule: `0 9 * * *`

- 💧 Water - 10AM Pacific
  - Job ID: `b76341d71354`
  - Schedule: `0 10 * * *`

- 🥤 Protein Drink - 2PM Pacific
  - Job ID: `4ab656b26552`
  - Schedule: `0 14 * * *`

- 💧 Water - 1PM Pacific
  - Job ID: `2e5b3af69398`
  - Schedule: `0 13 * * *`

- 💧 Water - 4PM Pacific
  - Job ID: `2934304ac770`
  - Schedule: `0 16 * * *`

- 💧 Water - 7PM Pacific
  - Job ID: `eea7a86f64fe`
  - Schedule: `0 19 * * *`

- 🛁 Sitz Bath - 9PM Pacific
  - Job ID: `7c74587c2e68`
  - Schedule: `0 21 * * *`

- 💧 Water - 10PM Pacific
  - Job ID: `0dd08e4e07da`
  - Schedule: `0 22 * * *`

- 🧘 Meditation - 10:15PM Pacific
  - Job ID: `3e512762661c`
  - Schedule: `15 22 * * *`

## Weekly

- 📏 Weekly Measurements
  - Job ID: `9a296fe6c2aa`
  - Schedule: `0 17 * * 0`
  - Current meaning: Sunday 5PM if interpreted as Pacific local; verify with user if this should be Sunday morning.

## Notes

- Water reminders target 3L/day: 6 × 500ml.
- Water reminder cron jobs run `send_water_button.py` with `no_agent=true`, sending a Telegram inline “✅ Log 500ml” button. Button callbacks use `wl:water:500` and `log_water_button.py` to update the daily hydration total.
- Protein reminder runs `send_protein_button.py` with `no_agent=true`, sending a Telegram inline “✅ Log protein drink” button. Button callbacks use `wl:protein:50` and `log_protein_button.py` to add a 50g protein drink to the food log and daily totals.
- Sitz baths: 10–15 min warm water.
- Meditation: start at 20 min, ramp toward 60 min over time.
- Intake logging: user must explicitly say “Log” / “Log this” or tap a Telegram Log button. Cron pings are nudges only, not tracked unless user confirms logging.
