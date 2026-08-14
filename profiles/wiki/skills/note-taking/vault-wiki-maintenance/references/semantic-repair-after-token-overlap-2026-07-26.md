# Semantic repair after token-overlap autolinks (2026-07-26)

A cron lint run selected 20 mostly Economist pages and initially used token/title overlap to satisfy low-outbound counts. The first pass created weak links such as ecology ↔ tennis, Myanmar secrecy ↔ Trump DOJ, and Cambodia scams ↔ Democrats crime because broad publication/date context and incidental vocabulary outweighed subject relevance.

## Durable workflow lesson

After any automated link fill, freeze the selected titles and run a separate semantic repair pass before final reporting:

1. Print each touched page's actual `## Related` lines and body-level `## Links`/MOC entries.
2. Remove all MOC links from `## Related`; MOC placement is navigation, not a subject neighbor.
3. Remove broad-token or same-issue-only neighbors even if the numeric verifier reports two outbound links.
4. Search by distinctive domain terms from the page title/body, not generic tags or issue/date context.
5. Add a replacement only when the target is a close subject companion:
   - climate/ecology → climate/ecology pages, not same-issue sports pages.
   - sports/game theory → sports/performance/event-economics pages.
   - management/Bartleby → management/operational judgment pages.
   - China AI companion → AI companion/AI product-risk pages, not unrelated China politics.
6. If no close neighbor exists, leave the page honestly low-outbound and report it.
7. Regenerate the index, rewrite exactly one same-day maintenance log entry, and rerun exact-batch verification against the frozen list.

## Verification cautions

- A page can pass structural checks while still having bad Related semantics; final verification must include human-readable Related output for all touched pages.
- Count MOC links for navigation/MOC membership, but exclude them when deciding whether `## Related` is semantically healthy.
- It is acceptable for semantic cleanup to increase selected low-outbound count when removed links were weak.
