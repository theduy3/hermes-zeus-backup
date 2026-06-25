# One-off helper pattern for headless evening runs

Use this when the evening routine has a non-trivial Inbox/root capture to promote and the changes span several files (new `Notes/` page, MOC, wiki-index, wiki-log, digest, source removal). The goal is deterministic, resumable mutation with compact verification output.

## Pattern

1. Get the canonical date/day first from `python3 System/scripts/calculate_dates.py`; hard-code or pass that result into the helper so digest naming never depends on UTC server time.
2. Read the source capture with normal file tools first, then write a temporary helper under `/vault/System/scripts/` only if it reduces error-prone repeated edits.
3. In the helper, make each mutation idempotent:
   - If the source is gone but the destination page exists and is non-empty, treat the note as already filed rather than recreating a duplicate.
   - Write new/updated Markdown through a same-directory temp file and `os.replace`.
   - Add MOC, `System/wiki-index.md`, and `System/wiki-log.md` entries only if the target link/heading/row is not already present.
   - Delete the source only after the destination page exists and is non-empty.
4. Print one compact JSON summary with: `date`, `day`, `notes_processed`, `created`, `updated`, `removed`, `digest`, `digest_verified`, `queue_remaining`, and `errors`.
5. After the helper succeeds, verify with ordinary tools: read the digest, read the top of the filed note, confirm the source is gone, rerun `find_today_notes.py --json --inbox`, and spot-check MOC/log/index entries.
6. Remove the one-off helper after verification unless it is intentionally reusable.

## Pitfalls

- Do not let an existing digest short-circuit processing. If the queue has work, process it and overwrite the digest with current verified counts.
- Do not report success based only on the helper's self-report; read back the final digest and rerun the queue check.
- Do not invent content for low-content captures. For substantive captures, summarize and preserve the original capture in a fenced `Original Capture` section when useful for later review.
