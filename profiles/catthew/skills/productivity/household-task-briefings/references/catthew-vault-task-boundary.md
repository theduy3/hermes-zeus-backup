# Catthew vault task boundary and history reconciliation

Use this reference when Sir asks to create, list, remember, migrate, or brief household tasks.

## Current rule

- `/vault/Tasks` is the source of truth for tasks across profiles.
- Catthew may read `/vault/Tasks`, but the Catthew morning briefing and household task lists must include only tasks explicitly tagged `#catthew`.
- A task counts as Catthew if either:
  - frontmatter contains `catthew` in `tags: [...]` or block `tags:`; or
  - the body contains literal `#catthew`.
- Do not include untagged tasks or other-profile tasks unless they also have `#catthew`.

## Creating Catthew tasks

When Sir or Madam creates a household task in the Catthew chat/profile:

```md
---
type: task
due_date: YYYY-MM-DD
tags: [catthew, family]
status: pending
---
# Title

- [ ] Task text
```

Use `/vault/Tasks/tasks/` for dated tasks, `/vault/Tasks/ideas/` for ideas/no-date items, and `/vault/Tasks/bugs/` for bugs.

## Reconciling historical tasks

When asked to “remember all tasks from history”:

1. Search prior Catthew sessions for user task phrases such as `Task for`, `to do`, `remind`, `created tasks`, `/vault/Tasks/tasks`, and known household names like Victoria, Sea Star, Costco, NEXUS.
2. Cross-check `/vault/Tasks/{tasks,ideas,bugs}` for matching files.
3. Add `catthew` to matching vault task frontmatter only when the task was clearly created in Catthew chat/profile.
4. Keep separate categories in the reply:
   - active/pending `#catthew` vault tasks;
   - completed `#catthew` vault tasks;
   - historical local/chat tasks without matching vault files;
   - recurring cron reminders.
5. Do not silently retag unrelated business, finance, or personal tasks.

## Briefing behavior

Daily Morning Briefing should:

- show pending/overdue and next-7-day `/vault/Tasks` items only when tagged `#catthew`;
- keep grocery list separate, sourced from Catthew grocery file;
- include household events from Catthew events file and available Google Calendar events;
- avoid cross-profile leakage even when global task memory mentions theduyvault as source of truth.
