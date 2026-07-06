# Semantic review and log rewrite notes — 2026-07-05

Use this reference when a wiki-lint run uses automated related-link or MOC fill, especially on mixed finance/AI/business batches.

## What happened
- A bounded 20-page lint pass selected finance/trading, market-update, quant-agent, and nail-salon payroll pages.
- The automated same-tag linker made structurally valid but semantically weak choices:
  - `[[17 Agentic AI Design Patterns]]` was added to some finance/quant pages only because of broad `ai`/`ai-agents` overlap.
  - `[[Finance MOC]]` appeared as a Related link on some pages; MOCs can be navigation context, but should not substitute for close subject-neighbor page links.
  - `Nail Salon W-2 Payroll Process` was initially placed in `AI Development MOC` because it had an inherited `ai` tag, even though the page belongs with finance/small-business/payroll notes.
- After manual semantic review, weak generic links were removed and the nail-salon payroll page was moved to `Finance & Economics MOC` near `Nail Salon W2 Commission Economics`.
- The same-day wiki-log entry was rewritten after cleanup so remaining counts reflected the post-cleanup state.

## Durable workflow lesson
1. After any automated linking/MOC fill, inspect every touched page's `## Related` section, not only link counts.
2. Treat MOC links in Related sections as suspect. Keep them only when the page explicitly discusses the MOC as an object; otherwise prefer subject-neighbor notes or leave the page honestly low-outbound.
3. Broad tags (`ai`, `ai-agents`, `finance`, `tools`, `research`, `developer-tools`, `source`, `github`, `video`) are not enough to justify a link. Require a close domain relationship visible in the title/body.
4. Review MOC placement semantically. If a page has inherited/broad tags, choose the MOC matching its actual topic and user intent, not the highest tag-overlap score.
5. If cleanup happens after the initial run, regenerate `System/wiki-index.md`, rewrite (not append) the same-day lint log entry, and rerun the exact-20 verification.

## Verification pattern
- Verify each touched page has:
  - `updated` equal to the run date
  - valid `type`, `wiki_status`, and non-empty `tags`
  - no `>> NEW >>` / `<< OLD <<` artifacts in frontmatter
  - an index row in `System/wiki-index.md`
  - either two semantically close outbound note links or an honest low-outbound count
- Verify exactly one same-day `## [YYYY-MM-DD] lint | Wiki health check` entry remains in `wiki-log.md`.
