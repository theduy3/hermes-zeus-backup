---
name: process
description: File loose/unprocessed notes from the theduyvault root and Inbox into their destinations. Scheduled headless job.
version: 1.0.0
metadata:
  hermes:
    requires_toolsets: [terminal, file]
    tags: [vault, process, theduyvault]
---

# process — file unprocessed theduyvault notes (headless)

You are running as a scheduled cron job. Run fully autonomously: no confirmation
prompts, no questions.

## Canonical instructions
Read and follow **`/vault/.claude/skills/process/SKILL.md`** exactly (find loose
notes, analyze each, decide destination + filename + tags + frontmatter, move it).

## Runtime adaptations (this environment)
- Vault is at **`/vault`**. Run helpers as `python3 /vault/System/scripts/<name>.py`
  (e.g. `calculate_dates.py`, `find_today_notes.py --json --inbox`). Scripts
  self-locate the vault, so cwd does not matter.
- Read/write everything under `/vault/...` (destinations: `Notes/`, `Projects/...`,
  `Tasks/tasks|ideas/`, plus `System/wiki-index.md` and `System/wiki-log.md`).
- Conventions: `/vault/CLAUDE.md`.
- **Do NOT invoke the wiki-ingest step here.** The separate `wiki-ingest` scheduled
  job owns wiki integration of notes filed into `Notes/`. Just file the note with
  correct frontmatter/tags and append the `System/wiki-log.md` entry when that file
  is writable.
- If wiki-log/index infrastructure is not writable, finish the filing work anyway
  and report the exact blocker in the run summary rather than retrying endlessly or
  leaving the source note unprocessed.
- If a note contains apparent secrets/credentials, leave it in place and note it in
  your run summary rather than filing it.
- Use the **terminal** tool for python3 and the **file** tool for moves/writes.
