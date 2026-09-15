# 2026-07-29 multi-profile evening recap

A scheduled weekday recap at 18:00 America/Vancouver needed a tool-only fallback because Python aggregation paths were blocked or approval-gated.

## Durable workflow lessons

- When `execute_code` is denied and terminal heredoc Python returns `pending_approval`, continue with ordinary tools: `search_files`, `read_file`, `session_search`, and `hermes --profile <name> cron list`.
- Always inspect named profiles, not just the default profile. On this run, the substantive work lived across `wiki`, `zeus`, `thor`, `catthew`, and `charles` outputs.
- If `search_files` over profile outputs truncates, paginate with `offset` and use profile cron lists to choose representative output files instead of trying to read everything.
- Re-scan near the end. A co-scheduled `wiki/vault-tonight` output appeared after the first pass and materially changed the recap.
- Search hits for failure words inside skill/prompt boilerplate are noisy. Confirm blockers from final `## Response`, `## Error`, or no-agent `**Status:**` sections.

## Representative outputs worth checking in similar recaps

- Default profile:
  - health-check for gateway/provider/tool warnings.
  - backup job for disaster-recovery push status.
  - graph/refresh jobs for local non-agent script failures.
- `wiki` profile:
  - `vault-today` for daily/investment notes generated.
  - `vault-wiki-lint` for exact batch counts and canonical wiki-health next actions.
  - `vault-wiki-ingest` for sources processed/pages created/pages updated/MOCs touched.
  - `vault-tonight` for evening digest and final queue status.
- `zeus`, `catthew`, `thor`, `charles` profiles: morning briefings, time-block plans, reminders, watchlist/finance reports.

## Reporting cautions

- Do not classify the current recap job as missing while it is running; its output file is written only after the final response.
- Treat current setup failures as blockers for tomorrow, but do not save them as permanent tool capability claims.
