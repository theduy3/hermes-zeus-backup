# Telegram inline Done buttons for Obsidian tasks

Use this pattern when the user wants task-reminder buttons that behave like Thor's wellness buttons, but backed by Obsidian task files.

## Shape

- Script-only cron job (`no_agent: true`) sends Telegram messages directly via Bot API.
- Source of truth is `/vault/Tasks/tasks/*.md`, not a generated sidecar, unless the user explicitly wants a staging layer.
- Each Markdown task file has YAML frontmatter with `type: task`, `due_date`, and `status`.
- The sender scans tasks and emits one Telegram card per actionable task:
  - include `status: pending` and `status: in_progress`
  - exclude `completed`, `done`, `cancelled`, `canceled`
  - include only `due_date <= today` for daily cards
- Button callback data should be compact and stable, e.g. `zt:<digest>`.
- Persist a registry mapping digest → `{title, file_path, due_date, status, message_id}` so callback handlers can resolve the original file.

## Callback behavior

Gateway callback handler should:

1. Authorize the clicking user.
2. Load the registry entry for the callback ID.
3. Verify `file_path` is inside `/vault/Tasks/tasks/`.
4. Update the source task file's YAML frontmatter to `status: completed`.
5. Update the registry entry to `status: done` with `done_at` and `done_by`.
6. Edit the Telegram message to `✅ Done — <title>` and remove the keyboard.

## Important pitfall

Do not depend on an LLM-generated `today_tasks.json` sidecar when the user's stated goal is "generate each individual task directly from Obsidian vault." A sidecar can be useful for curated lists, but it adds a failure point and makes the button flow stale. For the direct-vault pattern, the sender itself should parse `/vault/Tasks/tasks/*.md` every run.

## Verification

Before enabling or running the cron job:

```bash
python3 -m py_compile /path/to/send_task_buttons.py
python3 - <<'PY'
import importlib.util
p='/path/to/send_task_buttons.py'
spec=importlib.util.spec_from_file_location('task_buttons', p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
today=m.today_local()
tasks=m.load_vault_tasks(today)
print(today.isoformat(), len(tasks))
for t in tasks[:10]:
    print(t['due_date'], t['title'], t['file_path'])
PY
```

Avoid manually running the sender if it would spam many task cards; verify with a dry scan first.