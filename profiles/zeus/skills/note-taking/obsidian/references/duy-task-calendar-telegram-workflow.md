# Duy task workflow: Telegram ↔ Obsidian ↔ Google Calendar

## Source of truth

`/vault/Tasks/tasks/*.md` is the durable task database.

- Telegram is the on-the-go capture/input layer.
- Obsidian/theduyvault is the planning/editing layer.
- Google Calendar `theduy calendar` (`duynt1989@gmail.com`) is the dated-task visual layer and appointment layer.
- Thor stays separate for wellness reminders.
- Catthew/family items tagged or mentioning `#catthew`/`catthew` must not sync to theduy calendar.

## Active sync directions

```text
Telegram task request -> Obsidian task file
Telegram Done button -> Obsidian task status completed
Obsidian dated task -> Google Calendar all-day event
Google Calendar title `Task:`/`TODO:` -> Obsidian task file
```

## Google Calendar import rule

Only import events from `theduy calendar` whose title starts with:

```text
Task: ...
TODO: ...
```

Normal appointments must stay calendar-only. This prevents birthdays, flights, dentist visits, family events, and meetings from becoming tasks.

Implementation:
- Importer: `/home/hermes/.hermes/profiles/zeus/scripts/import_theduy_calendar_tasks.py`
- Mirror: `/home/hermes/.hermes/profiles/zeus/scripts/sync_obsidian_tasks_to_theduy_calendar.py`
- Import cron: `Import theduy Calendar Task Events to Obsidian`
- Mirror cron: `Sync Obsidian Tasks to theduy Calendar`

## User-facing explanation pattern

When Duy asks how to create tasks:

| Context | Recommended input |
|---|---|
| On the go | Telegram to Zeus |
| At computer planning | Obsidian task file |
| Fixed appointment/meeting | Google Calendar/Outlook event |
| Calendar-created task | Prefix event title with `Task:` or `TODO:` |
| Wellness | Thor reminders, not tasks |

Keep the explanation short and operational. Do not over-explain implementation unless asked.