# Daily Reminders — Cron Job Inventory

Cron schedules are interpreted in Pacific local clock time by the scheduler. Names should match the user-visible phone time. If user is in Quebec, switch wellness reminders to Eastern local time when requested.

## Daily

- 🧘 Meditation - 7:15AM Pacific
  - Job ID: `2616b50dddac`
  - Schedule: `15 7 * * *`
  - Script: `send_morning_meditation_button.py`
  - Message includes YouTube Music link: `https://music.youtube.com/watch?v=ThyQNMZZH-E&si=D-8kcTEkkpHdVKUV`
  - Button: `✅ Log 20 min`

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

- 🏃 Exercise - 3PM Pacific
  - Job ID: `5d9328231c7d`
  - Schedule: `0 15 * * *`
  - Script: `send_exercise_link.py`
  - Message includes YouTube link: `https://youtu.be/Jo1eWJ0YNnA?si=xnAMcODqvYy1oyde`
  - Button: `▶️ Start exercise` URL button

- 💧 Water - 4PM Pacific
  - Job ID: `2934304ac770`
  - Schedule: `0 16 * * *`

- 💧 Water - 7PM Pacific
  - Job ID: `eea7a86f64fe`
  - Schedule: `0 19 * * *`

- 🛁 Sitz Bath - 9PM Pacific
  - Job ID: `7c74587c2e68`
  - Schedule: `0 21 * * *`

- 🧘 Evening Stretch - 9PM Pacific
  - Job ID: `b20602062ff4`
  - Schedule: `0 21 * * *`
  - Script: `send_evening_stretch_link.py`
  - Message includes YouTube guide link: `https://youtu.be/g_tea8ZNk5A?si=O5hDX974GhelN6iT`
  - Button: `▶️ Start stretch` URL button

- 💧 Water - 10PM Pacific
  - Job ID: `0dd08e4e07da`
  - Schedule: `0 22 * * *`

- 🧘 Meditation - 10:15PM Pacific
  - Job ID: `3e512762661c`
  - Schedule: `15 22 * * *`
  - Script: `send_evening_meditation_button.py`
  - Message includes YouTube Music link: `https://music.youtube.com/watch?v=ThyQNMZZH-E&si=D-8kcTEkkpHdVKUV`
  - Button: `✅ Log 20 min`

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
- Meditation reminders use time-specific wrapper scripts with `no_agent=true`:
  - Morning: `send_morning_meditation_button.py` → `🧘 Morning meditation — 20 min.` + YouTube Music link + `✅ Log 20 min`
  - Evening: `send_evening_meditation_button.py` → `🧘 Evening meditation — 20 min.` + same YouTube Music link + `✅ Log 20 min`
  - Both wrappers set `THOR_MEDITATION_REMINDER_TEXT` and `THOR_MEDITATION_MINUTES=20`, then run the shared `send_meditation_button.py` sender. Button callbacks use `wl:meditation:20` and `log_meditation_button.py`.
- Meditation: current daily target/reminder button is 20 min.
- Intake logging: user must explicitly say “Log” / “Log this” or tap a Telegram Log button. Cron pings are nudges only, not tracked unless user confirms logging.
