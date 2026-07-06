# After Earnings transcript monitoring

Use when the user asks to pull transcripts from <https://www.afterearnings.com/blog/> into the vault and/or keep checking for new ones.

## Pattern

- Treat the site as a transcript feed, not a generic blog.
- Fetch `https://www.afterearnings.com/blog/` and select the first substantive `/blog/<slug>/` link that is not navigation and not `View more` text.
- Fetch that post page and extract the transcript from `.blog-post` first, falling back to `article` or `main` only if needed.
- Preserve provenance in the Inbox Markdown frontmatter:
  - `type: transcript`
  - `source: <post URL>`
  - `site: "After Earnings"`
  - `captured: <UTC timestamp>`
  - `published: <date if visible>`
- Body structure:
  - `# <title>`
  - `Source: <url>`
  - `## Description`
  - `## Transcript`
- Write to `/vault/Inbox/YYYY-MM-DD-HHMM-afterearnings-<slug>.md`, then let `wiki-ingest` create/update durable notes and MOCs.

## Cron/check-latest pattern

For biweekly monitoring, use a no-agent cron script that:

1. Stores state outside the vault product, e.g. `~/.hermes/profiles/wiki/state/afterearnings_latest.json`.
2. Compares the latest URL/fingerprint against state.
3. Prints nothing when there is no new transcript, so cron delivery stays silent.
4. Writes the latest transcript to `/vault/Inbox/` only when new.
5. Updates state only after the Inbox file was written.

Schedule example: `every 14d` (Hermes normalizes this to `every 20160m`).

## Verification

After writing or changing a capture script, create a temporary ad-hoc verifier under `/tmp/hermes-verify-*` that monkeypatches HTTP responses, asserts:

- latest link discovery works,
- one Markdown file is written,
- state records the URL,
- a second run is silent and does not create a duplicate.

Report this as ad-hoc verification, not as a full test-suite pass.
