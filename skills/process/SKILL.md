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
  job owns deep wiki integration of notes filed into `Notes/`. For any page filed to
  `Notes/`, do only the lightweight manual integration required for a clean wiki page:
  correct frontmatter/tags, at least 2 related wikilinks, relevant MOC link,
  `System/wiki-index.md` row/page count update when writable, and a
  `System/wiki-log.md` ingest entry when writable.
- If wiki-log/index infrastructure is not writable, finish the filing work anyway
  and report the exact blocker in the run summary rather than retrying endlessly or
  leaving the source note unprocessed.
- If a note contains apparent secrets/credentials, leave it in place and note it in
  your run summary rather than filing it.
- If an Inbox/root markdown capture is zero bytes or contains no meaningful content,
  remove it during processing so it does not recur in future scheduled runs; mention
  the cleanup in the run summary.
- Use the **terminal** tool for python3 and the **file** tool for moves/writes. Keep
  scheduled-run changes auditable as normal tool calls rather than bundling filing,
  index edits, and source cleanup into an ad hoc Python helper.
- Verify completion by rerunning `python3 /vault/System/scripts/find_today_notes.py --json --inbox`
  and only report success when the processable note count is zero or remaining notes
  are intentionally left in place (for example, because they contain credentials).
