---
name: household-task-briefings
description: Manage Catthew household task lists, grocery lists, daily briefings, and reminder formatting for the family Telegram chat.
version: 1.0.0
---

# Household Task Briefings

Use this skill whenever Sir asks Catthew to add, display, revise, schedule, or summarize household tasks, chores, grocery items, or daily morning briefings.

## Core workflow

1. **Separate storage format from chat format.**
   - Obsidian/task files use real Markdown task syntax: `- [ ] Task`.
   - Telegram chat confirmations use the household-friendly display format below.

2. **For Telegram chat task/chores lists, use square checkbox + quick number.**
   - Format: `☐ Task name (1)`
   - Continue numbering sequentially within the task/chores section.
   - Do not use `- [ ]` or hyphen bullets in chat task/chores confirmations unless Sir explicitly asks.

3. **For Telegram grocery lists, use simple bullets unless Sir requests otherwise.**
   - Example:
     - `- Korean pear`
     - `- Ghee`
   - Do not add `[Bought 1]` buttons/labels unless Sir re-requests that format.

4. **Task delivery preference.**
   - Send household task reminders and task-containing briefings to the family Telegram group (`telegram:-5249331607`, “Catthew - the Butler”), not Sir’s private DM.
   - List today and overdue household tasks inside the Daily Morning Briefing under **Pending tasks & chores**.
   - **Strict Catthew boundary:** morning briefings pull from `/vault/Tasks`, but show only files explicitly tagged `#catthew` — either `catthew` in frontmatter `tags: [...]` or literal body tag `#catthew`. Never include untagged tasks or other-profile tasks unless they also have `#catthew`.
   - When creating any task/bug/idea from this Catthew chat/profile, write it under `/vault/Tasks/{tasks,bugs,ideas}` and include `catthew` in the frontmatter tags list.
   - When a Catthew task has a due date or due time, also create the matching Google Calendar event on **Kittyggup Family** (`05a625d510ad884bcedf222735efe0ab5926b8b43f20e4b80493d84309466802@group.calendar.google.com`) using America/Vancouver time. Store the calendar event ID in the task note when possible. Creating a calendar event is expected when Sir explicitly creates a new dated/timed task; confirm before deleting or modifying calendar events.
   - **Calendar verification rule:** When Google Calendar authentication is available, it is the sole source of truth for the briefing’s **Today’s events** and **Upcoming** sections. Query the exact Vancouver-local date range before drafting; report only returned events whose start falls in that range. An empty result means no verified events—never substitute, infer, or carry forward entries from `events.md`, old briefing output, task-button registry, memory, or a weekly pattern. If the query fails, say calendar events could not be verified rather than present local entries as scheduled.
   - For Google Calendar sync setup, prefer calendar read-only OAuth for Catthew briefings and full calendar OAuth for task writes. If full Workspace consent hangs or errors, reduce scope to Calendar-only, use the OAuth JSON’s exact redirect URI (often `http://localhost`), and have Sir open the link in Safari/Chrome rather than Telegram’s in-app browser. See `references/google-calendar-sync.md` and `references/google-calendar-task-sync.md`.
   - If individual Telegram Done-button cards are also enabled, treat them as supplemental; do not remove today/overdue tasks from the briefing.
   - Create or keep a separate reminder only when Sir gives a specific time/date-time, e.g. “9 AM,” “tonight at 6,” or “May 25 at 9:00.”

5. **Update existing scheduled briefing prompts when the formatting rule changes.**
   - If Sir corrects the Daily Morning Briefing format, update the `Daily Morning Briefing` cron prompt, then verify the cron job content reflects the correction.
   - Keep the prompt concise and explicit about grocery vs task formatting.

## Household product extraction and shopping research

Use this when Sir sends a reel/video/photo and asks to identify products, build a grocery list, or find purchase links/prices.

- First identify products from the source: extract public page metadata where possible, then inspect video frames/key frames if labels are visible.
- For shopping research, default to **Vancouver, BC** retailers and delivery availability unless Sir explicitly asks for another city. Travel context should not override household shopping location.
- Prefer exact product matches; if only substitutes are available, label them clearly as “closest match” or “substitute.”
- Include retailer, verified price, size, direct URL, and availability/shipping caveat. Do not invent prices when a page is blocked or unavailable.
- For Instacart Vancouver checks, include a Vancouver postal code such as `zipcode=V6B1A1`; otherwise it may silently use a stale/default location.
- Session reference: `references/product-video-shopping-research.md` captures the Facebook reel → product extraction → Vancouver price lookup workflow.

## Recurring household routines/checks

Use this when Sir asks to “create this routine,” “every Sunday,” or similar recurring household checks.

- If the routine content is missing, ask for the routine name, time, and task list before scheduling.
- If Sir provides enough intent and cadence, create both a durable `/vault/Tasks/tasks/` note (tagged `catthew`, `household`, and `recurring`) and a self-contained cron reminder rather than merely describing the plan.
- For recurring task notes, calculate the *actual next scheduled occurrence* in America/Vancouver before setting `due_date`. Do not assume the next named weekday if today's scheduled time has not yet passed (for example, a Thursday 8 PM reminder created Thursday morning is due that same evening).
- Interpret household recurring checks in Pacific time unless Sir says otherwise; verify the `next_run_at` in the cron response before confirming.
- Cron prompts must be self-contained because future runs have no chat context. Include the target source, decision criteria, desired output format, and “do not create or modify cron jobs.”
- For store/app sale checks that may be blocked by Cloudflare or app-only access, instruct the cron job to try the official website first, then web search, and report `Active / Not active / Unable to verify` with source URLs.
- Session reference: `references/recurring-sale-checks.md` captures the Save-On-Foods “1.49 Day Tuesday” pattern.

## Google Calendar sync for household briefings

When Sir asks to sync Catthew with Google Calendar:

- Use the `google-workspace` OAuth flow for the active Catthew profile, then verify with `setup.py --check` and a small calendar list command before saying it is connected.
- If Sir provides a macOS path like `/Users/theduy/Downloads/...`, first check whether it exists from the Linux/container runtime. If missing, ask him to upload the JSON to the chat; use the uploaded document path instead.
- For Google Cloud apps in Testing mode, if OAuth returns `Error 403: access_denied`, direct Sir to add `duynt1989@gmail.com` as a test user in Google Cloud Console → OAuth consent screen/Audience → Test users, then generate a fresh auth URL.
- If Google shows “Google hasn’t verified this app,” tell Sir to use **Advanced → Go to Hermes-Catthew (unsafe)** and paste the final `http://localhost:1/?code=...` redirected URL back.
- Session detail: see `references/google-calendar-oauth-catthew.md`.

## Daily Morning Briefing formatting

Preferred sections:

- Date & greeting
- Today's events
- Grocery list
- Pending tasks & chores (list today and overdue tasks)
- Upcoming (next 7 days)
- Closing

In the **Pending tasks & chores** section, format items like:

```text
☐ Collapse the baby crib (1)
☐ Build the cabinet (2)
☐ Move current cabinet from dining room to master bedroom (3)
```

In the **Grocery list** section, use ordinary simple bullets:

```text
- Korean pear
- Ghee
```

## Pitfalls

- **Catthew task boundary correction:** do not solve cross-profile task leakage by ignoring `/vault/Tasks` entirely. Sir wants `/vault/Tasks` as source of truth, but Catthew briefings must include only tasks explicitly tagged `#catthew`; all tasks created from this Catthew chat/profile must add `catthew` to frontmatter tags.
- When Sir asks for task Done buttons, use the established Catthew task-card drip: `scripts/send_household_task_buttons.py`, callback prefix `ct:`, and registry `~/.hermes/profiles/catthew/task_buttons/registry.json`. Ensure `/home/hermes/.hermes/profiles/catthew/.env` has `TASK_BUTTON_CHAT_ID=-5249331607` so cards go to the Catthew group, not Sir's private `TELEGRAM_HOME_CHANNEL`.
- **Recurring-event safety:** An `events.md` recurrence without an explicit end date must not be treated as a verified future appointment. Before using it for a Done-button card, verify the current occurrence against the authoritative calendar or obtain confirmation. A weekday mismatch or an expired date range means do not send the event/card.
- Victoria's same-day household events count as tasks for the individual Done-button drip, so recurring events in `events.md` (e.g. music class or Playgym) should be sent as Done-button task cards on their day. Date-limited recurring events may use `from YYYY-MM-DD through YYYY-MM-DD`; the drip ignores them outside that range.
- Do not put `[Done 1]` or `[Bought 1]` labels in the final briefing unless Sir asks again.
- Do not forget to persist durable formatting corrections in both memory and this skill when Sir corrects task/list display.
- Prefer the individual Done-button task card style for household tasks and same-day household events, even when they have a time. Do not create standalone cron-style reminder messages for these unless Sir explicitly asks for a separate reminder.

## Reference

- See `references/telegram-task-formatting.md` for the correction sequence that established these household display rules.
- See `references/catthew-vault-task-boundary.md` for the `/vault/Tasks` + `#catthew` boundary, creation rules, and historical task reconciliation workflow.
- See `references/google-calendar-task-sync.md` for the Kittyggup Family calendar ID, Catthew task → calendar write workflow, and backfill procedure.
