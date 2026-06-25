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
- For queued Markdown captures that become wiki pages, follow
  `references/idempotent-wiki-filing-and-digest.md`: write/verify the `Notes/` page,
  update MOCs/index/log idempotently, remove the source only after readback, recheck
  the Inbox queue, and make `notes_processed` reflect the verified current-run count.

## Headless robustness notes
- Detailed checklist: see `references/robust-headless-processing.md`.
- For non-trivial multi-file promotions during the evening run, use the deterministic helper pattern in `references/one-off-helper-pattern.md`: idempotent writes, compact JSON summary, ordinary-tool verification, then remove the temporary helper.
- Treat the output of `find_today_notes.py` as a work queue, not proof that the source still exists. In scheduled runs another process may have already filed a note between discovery and digest generation; before creating duplicates, verify the source path and, if it is gone or empty, search the vault for distinctive title/source URL/content to identify an existing filed page and summarize that page in the digest instead of creating a duplicate.
- Use `calculate_dates.py` as the source of truth for the digest date/day. The server clock may be UTC while the vault scripts use America/Vancouver; do not name the digest from `date` output or from the `date` field in `find_today_notes.py` if it disagrees with `calculate_dates.py`.
- After filing notes, rerun `find_today_notes.py --json --inbox` and verify the queue is empty. This catches root originals that were copied into `Notes/` but not removed.
- If a digest already exists but `find_today_notes.py` still returns work, do **not** treat the existing digest as proof the routine is done. Process the current queue, match residual captures to existing filed Notes pages when possible, archive/remove the residual originals, then overwrite the digest with the verified current-run counts.
- When promoting a root capture into a wiki page, remove the original root file after verifying the new page was written and non-empty. For low-content captures such as image-only notes, empty GitHub clippings, YouTube shells, or metadata pages, create a clearly labeled stub with the original source URL/attachment path and a transcript/manual-summary follow-up rather than inventing content.
- If a digest path already exists or cannot be overwritten directly while the `Daily/` directory is writable, write the desired content to a same-directory temporary file and atomically `mv -f`/`os.replace` it into place. Verify by reading the final digest back before reporting success.
- In cron/headless runs, prefer ordinary file + terminal operations for multi-step vault mutations. Do **not** use `execute_code` for this routine: cron profiles may block arbitrary local Python/subprocess execution, and the normal file + terminal path is the durable workflow. If a Python helper is useful, write it as a temporary script with the file tool and run it via `terminal` from `/vault`, rather than relying on interactive-only execution paths. Keep the script deterministic, print a compact JSON summary, and verify each written/removed file afterward with normal tools. After the digest and queue verification succeed, remove any one-off helper script you created under `/vault/System/scripts/` unless it is intentionally reusable.
- When creating wiki pages from low-content captures, preserve the source URL in quoted YAML/frontmatter or body text, write explicit follow-up bullets, add at least two relevant `[[wikilinks]]`/MOC links where possible, then only delete the original Inbox/root capture after the new page is non-empty and readable.
- When `/vault/System/wiki-index.md` or `/vault/System/wiki-log.md` are unreadable/unwritable in a cron run, do not fail the digest. Continue the routine, report the infrastructure limitation succinctly, and avoid claiming wiki-index/log updates were made.
- Make any temporary helper script resumable/idempotent around partial mutations. A crash can happen after files are promoted and the Inbox queue is emptied but before the digest/log is written; on recovery, do not recreate notes or assume there is no work. Verify the already-written `Notes/` pages, append any missing log entries idempotently, rerun the queue check, then always write/overwrite the digest with the verified current-run count. If the helper is no longer needed after recovery, remove it.
- Final cron output should not be `[SILENT]` just because zero notes were processed; creating and verifying the nightly digest is itself reportable.
