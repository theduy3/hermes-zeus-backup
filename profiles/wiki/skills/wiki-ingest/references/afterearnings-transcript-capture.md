# After Earnings transcript capture

Use this when the user asks to ingest or monitor transcripts from <https://www.afterearnings.com/blog/>.

## Workflow

1. Fetch the transcript listing page: `https://www.afterearnings.com/blog/`.
2. Parse the first non-navigation transcript link under `/blog/<slug>/` as the latest transcript.
3. Fetch the transcript page and extract the `.blog-post` body. Fallback selectors: `article`, then `main`.
4. Write a Markdown source to `/vault/Inbox/`:
   - basename pattern: `YYYY-MM-DD-HHMM-afterearnings-<slug>.md`
   - frontmatter: `type: transcript`, `source: <post URL>`, `site: After Earnings`, `captured`, `published`
   - sections: `# <title>`, `Source: <url>`, `## Description`, `## Transcript`
5. Track the last captured URL/fingerprint in a profile state file so repeat runs stay silent.
6. Let the normal `vault-wiki-ingest` cron convert the Inbox source into typed wiki notes/MOCs.

## Current runtime implementation

The wiki profile uses a no-agent cron script at:

`/home/hermes/.hermes/profiles/wiki/scripts/afterearnings_latest_capture.py`

Cron job name:

`afterearnings-latest-transcript-capture`

Schedule: every 14 days (`every 14d` / `every 20160m`).

## Verification pattern

After editing the capture script, run an ad-hoc verifier from `/tmp` with a `hermes-verify-` filename prefix. Mock `requests.get`, redirect `STATE_PATH` and `INBOX_DIR` to a `tempfile.TemporaryDirectory`, and assert:

- the fake latest transcript is captured exactly once;
- source URL, title, description, and transcript text appear in the Markdown;
- state JSON records the latest URL/fingerprint;
- a second run creates no second file and prints nothing.

Report this as **ad-hoc verification**, not as a full suite-green result.

## Pitfalls

- Podpage pages expose the transcript body in `.blog-post`; do not rely only on generic metadata.
- Keep no-agent cron scripts silent when there is no new transcript. Non-empty stdout is delivered to Telegram.
- Do not create a new wiki note directly from the capture script; capture to `/vault/Inbox/` and let `wiki-ingest` handle dedup, notes, MOCs, index, and log.
- `cronjob` script paths must be relative to the wiki profile scripts directory, e.g. `afterearnings_latest_capture.py`, not an absolute path.
