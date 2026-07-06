# Recurring website transcript capture into Inbox

Use this when the user wants transcripts from a website/blog periodically pulled into the vault.

## Pattern

1. Inspect the listing page and identify the latest transcript URL.
2. Write a small no-agent cron script under the active profile's `scripts/` directory.
3. The script should:
   - fetch the listing page with a clear User-Agent
   - select the latest transcript link deterministically
   - fetch the transcript page
   - extract title, description, publication date, source URL, and transcript body
   - write a timestamped Markdown capture to `/vault/Inbox/`
   - persist a state file under the profile, e.g. `state/<source>_latest.json`
   - print a message only when a new transcript is captured
   - print nothing when the latest transcript is already captured, so no-agent cron stays silent
4. Create a `cronjob` with `no_agent=True`, `script=<relative script name>`, and the requested schedule.
5. Rely on the existing `vault-wiki-ingest` cron to turn the Inbox capture into wiki notes, unless the user asks for immediate ingest.

## Verification

After writing or changing the script, run an ad-hoc verification script under `/tmp/hermes-verify-*` that monkeypatches network fetches with fixture HTML and verifies:

- latest link selection
- Markdown capture content
- state-file write
- duplicate/same-latest run creates no second file and stays silent

Report this as ad-hoc verification, not as a full suite pass.

## Pitfalls

- Do not fabricate transcript text from titles or snippets; capture only extracted page text.
- Do not assume listing-page links are already absolute; normalize with `urljoin`.
- If the source has many historical transcripts, clarify whether the user wants only latest going forward or a backfill. For “check latest every N weeks,” capture latest now and schedule future latest checks.
