# Exactly-20 batch and log consistency repair

Use this when a wiki-lint cron pass finds fewer than 20 structural issue-bearing pages but the schedule still requires a 20-page run.

## Lesson

The batch-size requirement is literal: process exactly 20 readable pages. If the structural issue queue has fewer than 20 pages, fill the remainder from the oldest `updated` readable pages as a rolling refresh batch. Do not stop after the smaller issue-bearing set.

## Correct workflow

1. Build the primary candidate list from pages with structural issues: sparse frontmatter, MOC gaps, stale pages, diff markers, orphan candidates, or semantically repairable low-outbound pages.
2. If that list has fewer than 20 pages, append oldest-`updated` readable pages not already selected until the batch has exactly 20.
3. Keep semantic integrity above numeric link targets:
   - Remove unrelated forced `## Related` links even if that leaves a page with fewer than 2 Note-to-Note outbound links.
   - MOC links are useful navigation but do not make a sparse capture substantively cross-linked.
   - Log these as “semantically unresolved low-outbound sparse captures,” not as a failed frontmatter/MOC run.
4. After semantic cleanup, rewrite the same-day wiki-log entry rather than appending another entry.
5. Ensure log language matches verification counts. Never report `Remaining: 0` if post-run `low_outbound` is non-zero; say how many low-outbound pages remain and why.
6. Rerun final verification after any log/index/page repair:
   - batch size is exactly 20
   - all pages have required frontmatter and today’s `updated`
   - index header date/page_count are current
   - all 20 titles are in the index
   - exactly one same-day lint log entry exists

## Pitfall

A structurally successful script can still violate the skill if it only processes the issue-bearing subset. Treat “5 pages enhanced” with a requested batch size of 20 as incomplete, then immediately run a fill-to-20 repair pass before reporting success.