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

## Verification discipline
- Detailed harness-response pattern: see `references/ad-hoc-verification-harness-handshake.md`.
- After writing or patching the digest, perform fresh verification before the final report: read the final digest back, rerun `find_today_notes.py --json --inbox`, and confirm the digest is non-empty and its `notes_processed` value matches the verified current-run count.
- Because the evening routine changes a Markdown file and usually has no canonical test/lint/build command, proactively run a focused **ad-hoc verification** script before the first final report whenever the digest was created or overwritten. Create it under `/tmp` using Python `tempfile.NamedTemporaryFile(..., prefix="hermes-verify-", suffix=".py", dir="/tmp", delete=False)` (not a deterministic filename), verify digest existence/non-empty status, date/day from `calculate_dates.py`, current queue counts from `find_today_notes.py --json --inbox`, and that `notes_processed` matches the verified queue count; then remove the verifier and report cleanup status.
- If the surrounding harness reports that changed files lack canonical verification, create a focused temporary verifier under `/tmp` using a **new OS-safe tempfile path** with prefix `hermes-verify-`, run it against the digest/date/queue behavior, remove it afterward, and describe the result explicitly as **ad-hoc verification** rather than a suite-green result. Do not reuse a prior verifier path or cite prior evidence; the harness expects fresh evidence in the current response.
- If the harness repeats the same unverified changed-path warning after an ad-hoc check, treat it as a **new verification request**, not as a dispute about earlier evidence. Do not argue from or cite the previous verifier as sufficient. Run a **fresh** `/tmp/hermes-verify-*` verifier, remove it, and report the new verifier path/result/cleanup status concisely.
- If the repeated changed path is the same-directory atomic-write temp digest file (for example `/vault/Daily/.YYYY-MM-DD-tonight.md.tmp`), the fresh verifier must explicitly assert that exact temp path is absent as well as verifying the final digest. Name that check in the final report (for example `changed_tmp_path_absent: true`) so the harness/user can see the flagged path was covered. Re-run this exact absence check on every repeated harness warning because the harness may only consider fresh current-turn evidence.
- Avoid leaving temporary verifier files behind. If a previous `/tmp/hermes-verify-*` path appears in the changed-path list, include its absence/removal in the next ad-hoc verification output.
- When generating the temporary verifier script from a shell/Python wrapper, keep parsing deliberately simple and robust: parse `calculate_dates.py` output with `splitlines()`/`startswith()` rather than nested raw-string regexes that are easy to over-escape inside generated code. Structure the verifier so cleanup of `Path(__file__).unlink()` happens in a `finally` block even when parsing or validation fails, then rerun with a fresh `/tmp/hermes-verify-*` path if the first verifier fails because of verifier-script logic.
- Avoid creating durable wrapper/helper scripts for verification under `/tmp` with `write_file` (for example `/tmp/hermes-create-tonight-verifier*.py`): the harness may flag those wrapper paths as unverified changes even after the real verifier passes. Prefer a single `terminal` heredoc/`python3 - <<'PY'` that creates an OS-safe `tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', dir='/tmp', delete=False)`, runs it, prints JSON, and lets the verifier unlink itself in `finally`. If wrapper paths were already created or flagged, the next fresh verifier must explicitly remove/assert absence of those exact wrapper paths plus the same-directory atomic digest temp path; see `references/fresh-ad-hoc-verification-with-flagged-temp-paths.md`.
- If the harness repeatedly reports a one-off evening helper under `/vault/System/scripts/` as an unverified changed path even after the helper was removed, treat it as a fresh verification request each time. Run a new `/tmp/hermes-verify-*` verifier and explicitly assert the flagged helper path is absent, the atomic digest temp path is absent, the digest/date/queue/`notes_processed` checks still pass, and previous verifier paths are absent when known; see `references/repeated-harness-verification-for-deleted-helpers.md`. Do not cite earlier verifier output as sufficient.

## Skill bundle references
- The `references/*.md` files named above are bundled with this Hermes skill, not necessarily present under `/vault/.claude/skills/tonight/`. If their content is needed during a maintenance/update pass, load them with `skill_view(name='tonight', file_path='references/<file>.md')`; during the cron routine, follow the already-loaded instructions and do not fail just because the vault copy lacks those reference files.
- `references/single-inbox-wiki-promotion-verification.md` captures a successful single-Inbox Markdown promotion pattern: idempotent helper writes, ordinary-tool readbacks/searches, fresh `/tmp/hermes-verify-*` ad-hoc verification, correct `notes_processed` semantics, and cleanup of both verifier and one-off helper.
