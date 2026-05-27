---
name: tonight
description: theduyvault evening routine — process notes, then write the evening digest. Scheduled headless job.
version: 1.0.0
metadata:
  hermes:
    requires_toolsets: [terminal, file]
    tags: [vault, evening, theduyvault]
---

# tonight — theduyvault evening routine (headless)

You are running as a scheduled cron job. Run fully autonomously: no confirmation
prompts, no questions.

## Order of work
1. **Process notes first.** Follow `/vault/.claude/skills/process/SKILL.md` (same
   adaptations as the `process` skill: vault at `/vault`, helpers at
   `python3 /vault/System/scripts/...`, skip the wiki-ingest hop).
2. **Always write the digest.** Follow `/vault/.claude/skills/tonight/SKILL.md` for the
   evening digest content and format, but override its stale "no notes -> stop" rule:
   even when `/process` finds 0 notes, still create `/vault/Daily/<YYYY-MM-DD>-tonight.md`
   with a short "No notes processed" digest and verification details.

## Runtime adaptations (this environment)
- Vault is at **`/vault`**. Write the digest to
  **`/vault/Daily/<YYYY-MM-DD>-tonight.md`**. Append any lint entry to
  `/vault/System/wiki-log.md`.
- **Skip** the interactive mini wiki-lint pass (the canonical skill already skips it in
  headless mode); the dedicated `wiki-lint` job covers enhancement.
- Conventions: `/vault/CLAUDE.md`. Use terminal + file tools.

## Headless robustness notes
- Treat the output of `find_today_notes.py` as a work queue, not proof that the source still exists. In scheduled runs another process may have already filed a note between discovery and digest generation; before creating duplicates, verify the source path and, if it is gone, search the vault for distinctive title/content to identify the filed note and summarize that existing page in the digest.
- Use `calculate_dates.py` as the source of truth for the digest date/day. The server clock may be UTC while the vault scripts use America/Vancouver; do not name the digest from `date` output or from the `date` field in `find_today_notes.py` if it disagrees with `calculate_dates.py`.
- After filing notes, rerun `find_today_notes.py --json --inbox` and verify the queue is empty. This catches root originals that were copied into `Notes/` but not removed.
- When promoting a root capture into a wiki page, remove the original root file after verifying the new page was written. For low-content captures such as YouTube shell/metadata pages, create a clearly labeled stub with the original source URL and a transcript/manual-summary follow-up rather than inventing content.
- If a digest path already exists but cannot be overwritten directly while the `Daily/` directory is writable, write the desired content to a same-directory temporary file and atomically `mv -f` it into place. Verify by reading the final digest back before reporting success.
- When `/vault/System/wiki-index.md` or `/vault/System/wiki-log.md` are unreadable/unwritable in a cron run, do not fail the digest. Continue the routine, report the infrastructure limitation succinctly, and avoid claiming wiki-index/log updates were made.
