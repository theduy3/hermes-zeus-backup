# Idempotent wiki filing during evening digest runs

Use this reference when the evening routine finds processable Markdown captures that should become `Notes/` wiki pages.

## Pattern

1. Use `System/scripts/calculate_dates.py` as the digest date source of truth.
2. Treat `find_today_notes.py --json --inbox` as a work queue, not proof that the source still exists later.
3. Before writing, choose a stable destination page title and check whether the page already exists.
4. Write or verify the destination `Notes/<Title>.md` with normal wiki frontmatter:
   - `tags`
   - `type`
   - `created`
   - `updated`
   - `sources`
   - `wiki_status`
5. Add at least two meaningful outbound wikilinks in the body, plus relevant MOC links.
6. Only remove the original Inbox/root capture after the destination page is readable and non-empty.
7. Update MOCs, `System/wiki-index.md`, and `System/wiki-log.md` idempotently: search for the target link/header first, then insert only if absent.
8. Re-run `find_today_notes.py --json --inbox`; the post-run queue must be empty unless a source is intentionally left for human review.
9. Write the digest atomically in `Daily/<YYYY-MM-DD>-tonight.md` and read it back before reporting success.
10. Remove any temporary helper script after digest and queue verification succeed.

## Counting rule

`notes_processed` in the digest should reflect the verified current run outcome:

- Increment when this run successfully files/removes a live queued source.
- Use `0` only when the queue was empty, the source was already filed by another process, or no live source was actually consumed.
- If a source disappeared between discovery and filing, search for an existing filed page and summarize it, but do not count it as newly processed unless this run performed the filing/removal.

## Digest verification block

Include a compact verification section in the digest:

```markdown
## Verification

- Date source: `System/scripts/calculate_dates.py` returned `<Day>, <YYYY-MM-DD>`.
- Inbox queue was rechecked after filing.
- Digest was written atomically and read back for verification.
- Mini wiki-lint was skipped because this is a scheduled headless run.
```
