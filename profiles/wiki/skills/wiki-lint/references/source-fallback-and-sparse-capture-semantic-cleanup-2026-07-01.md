# Source fallback pages and sparse-capture semantic cleanup (2026-07-01)

## Context
A wiki-lint cron run processed exactly 20 pages and initially used automated `## Related` fill to satisfy the numeric two-outbound-link target. Several sparse captures and imported article/channel notes received weak links because their broad tags overlapped with popular pages.

## Durable lessons

### 1. Source fallback pages often already have the correct semantic link
Notes that are archived source fallbacks under `/vault/Notes` commonly include a `## Pages Updated` section. Treat those links as first-class outbound semantic links. Do **not** add unrelated `## Related` entries just because the page has fewer than two note-to-note links.

Good repairs from this run:
- `AIClient-2-API GitHub Source` should link to `[[AIClient2API Free LLM Proxy Tool]]` and, if a second link is justified, a close AI router/proxy neighbor such as `[[9Router AI Model Router Setup]]`.
- `ByteDance DeerFlow GitHub Source` should link to `[[ByteDance DeerFlow Super Agent Harness]]` and close agent-harness neighbors such as `[[Agent Harness Engineering for Coding Agents]]`.
- `SEOMachine GitHub Source` should link to `[[SEOMachine Claude Code Content Platform]]` and close SEO neighbors such as `[[Advanced SEO GEO Audit Rank Checker]]`.

### 2. Sparse captures should remain honestly low-outbound
For low-content captures like one-line legal notes, channel URL stubs, language phrase snippets, or unclear product captures, remove weak related links instead of forcing generic neighbors. It is better to report them as low-outbound pending human/source clarification.

Examples where weak links were removed:
- `Legal Reserve Note` — removed unrelated astrology/date-week links.
- `Canada’s Conservative leader echoes Reagan as his party regroups` — removed unrelated marketing/video-tool links.
- `Grace Leung YouTube Channel` — removed unrelated Claude Code/course links.
- `Korean Greeting Phrases` — removed unrelated personal-development/course links.
- `MYLE GoalAccess Capture` — removed unrelated AI guide/agent harness links.

### 3. Verification must inspect the actual rendered related sections
A heuristic `weak_added_links` check can miss bad links if broad tags overlap. After automated link fill, re-read the touched pages and inspect every `## Related` section, especially source fallback pages and sparse captures. Then regenerate the index and rewrite the same-day log entry to match the honest low-outbound count.

### 4. Log/index consistency after semantic cleanup
After removing weak links:
- regenerate `/vault/System/wiki-index.md`;
- rewrite the same-day `wiki-log.md` lint entry rather than appending a second entry;
- verify exactly one same-day lint entry;
- report non-zero low-outbound counts honestly.
