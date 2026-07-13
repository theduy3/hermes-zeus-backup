# 2026-07-08 multi-profile evening recap pattern

Session-specific recap lessons from a cron-heavy day with default + named-profile activity.

## What worked

- Resolve the user's local reporting date first. In this run the host was already `2026-07-09 UTC`, while the user-local day was still `2026-07-08 EDT`; the recap correctly used the local day.
- Scan both default-profile outputs and named-profile outputs. The meaningful work was mostly under `~/.hermes/profiles/{wiki,zeus,catthew,thor,charles}/cron/output/`, not default.
- Use `hermes --profile <profile> cron list` for profiles that show many outputs. This identifies job names behind opaque IDs such as:
  - wiki: `vault-today`, `vault-wiki-lint`, `vault-wiki-ingest`, `vault-tonight`, `newsletter-imap-capture`
  - zeus/catthew: daily briefings and task-button drips
  - thor: wellness reminders
  - charles: daily stock watchlist
- Re-scan near the end. A co-scheduled evening job appeared after the first aggregation (`vault-tonight`), and the total changed from 206 to 208 output files.
- Treat script/no-agent silent files as successful no-alert runs when they contain only a header with `Status: silent (empty output)` and no `## Error`.
- Read final response sections of representative outputs, not the loaded skill/prompt text. Grepping whole files for strings like `Permission denied`, `not writable`, or `[SILENT]` can hit boilerplate in the prompt/skill body rather than the actual result.

## Classification guidance

- Count and classify first, then sample. A compact Python script over output files can count by job/profile, detect `## Error`, and extract the last `## Response` section.
- For blocker searches, prefer final response extraction over raw `grep -R`; raw grep is useful only as a lead because loaded skill text frequently contains historical pitfalls that are not current failures.
- For backup jobs with explicit time self-checks, report a skipped run as a real blocker only when the final response says the job intentionally stopped before side effects. In this run, the backup fired at 03:00 EDT and skipped because the self-check required 00:00.
- For wiki-ingest/lint, include durable backlog counts from the final response (broken links, duplicate basenames, untriaged sources, low-outbound pages) as next-action material.

## Final recap style that worked

- Keep the delivered recap concise and split into exactly: `What got done`, `Failures / blockers`, `Top next actions`.
- Aggregate repetitive monitoring/reminder jobs instead of listing every run.
- Include concrete file paths only for important artifacts (daily briefings, evening digest), not every cron output path.
