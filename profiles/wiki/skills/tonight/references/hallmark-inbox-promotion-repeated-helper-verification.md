# Hallmark Inbox promotion + repeated deleted-helper verification

Session pattern captured from the 2026-07-18 evening run where a single GitHub Inbox capture (`Nutlope/hallmark`) was promoted into a wiki page and the harness repeatedly flagged the already-deleted one-off helper under `/vault/System/scripts/`.

## What worked

1. Treat `find_today_notes.py --json --inbox` as the live queue; if it returns one Markdown capture, read the source, dedupe by distinctive title/source URL/content, then promote it into a normal `Notes/` page.
2. For a GitHub/repo capture with enough substance, create:
   - an atomic `Notes/<Title>.md` page with full wiki frontmatter (`type`, `created`, `updated`, quoted `sources`, `wiki_status`), at least two relevant wikilinks, and a concise operating-model summary;
   - a `Sources/YYYY-MM-DD - <Source Title>.md` archive preserving the original URL and raw capture text;
   - idempotent MOC, `System/wiki-index.md`, and `System/wiki-log.md` entries.
3. Only remove the Inbox original after the Note and Source archive both read back as non-empty.
4. Overwrite `/vault/Daily/<date>-tonight.md` with `notes_processed` equal to the current-run filed/folded source count, not the final queue count. Then rerun `find_today_notes.py --json --inbox` and expect queue `0`.
5. Remove any one-off helper under `/vault/System/scripts/` after successful digest + queue verification.

## Repeated harness warning pattern

If the harness repeatedly reports the removed helper path as an unverified changed path (for example `/vault/System/scripts/tonight_one_off_20260718_hallmark.py`), do not cite prior verifier output. Run a **fresh** `/tmp/hermes-verify-*.py` verifier in the current response and explicitly assert:

- digest exists and is non-empty;
- digest `date`/`day` match `calculate_dates.py`;
- digest `notes_processed` matches the current-run count;
- post-run Inbox queue is `0`;
- promoted Note and Source archive exist and are non-empty;
- Inbox original is absent;
- MOCs, index, and log link the promoted page;
- exact flagged helper path is absent;
- same-directory atomic digest temp path is absent;
- verifier removed itself in `finally`.

Keep the final reply concise and label it **ad-hoc verification**, not suite-green/canonical tests.
