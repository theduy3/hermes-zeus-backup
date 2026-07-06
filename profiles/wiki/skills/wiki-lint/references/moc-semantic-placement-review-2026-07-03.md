# MOC semantic placement review after automated wiki-lint (2026-07-03)

## What happened
A cron-safe wiki-lint automation correctly enhanced 20 direct `Notes/*.md` pages and added missing MOC memberships, but the heuristic placed a few pages in broad or misleading MOCs:

- `Credit Card Churning Strategy for Travel` was initially added to `AI Development MOC.md`; semantic review moved it to `Personal MOC.md` under `## Travel`.
- `European Workers Job Switching` was initially added to `Home.md`; semantic review moved it to `Europe MOC.md` under `## Economy & Labor`.
- `THE FUTURE OF EVERYTHING - The Wall Street Journal Thu, Jun 13, 2024` was initially added to `Finance & Economics MOC.md`; semantic review moved it to `Science & Technology MOC.md` under `## Energy & Climate Technology` because the article was about green steel / climate technology.

## Durable workflow lesson
After automated MOC fill, semantic review must inspect MOC destinations, not only `## Related` sections and outbound link counts.

Use this guard:

1. For every touched page that was newly added to a MOC, read the page title/body and the target MOC section.
2. Treat broad/generic tags (`ai`, `business`, `finance`, `research`, `personal-development`) as insufficient for MOC placement.
3. Prefer the narrowest domain MOC and section that matches the page's actual subject:
   - geography/politics/labor articles → regional Economist MOCs (`Europe MOC`, `Asia MOC`, etc.) when applicable;
   - finance mechanics/personal finance/travel rewards → `Finance MOC` or `Personal MOC` sections, not AI MOCs;
   - energy/climate/materials technology → `Science & Technology MOC`, not finance by default;
   - company/industry strategy articles → `Business MOC` when the firm/industry is central.
4. If the best MOC does not have a suitable section, create a concise domain section rather than dropping the page into `Home.md` or an unrelated existing section.
5. After moving MOC entries, rerun final verification: all 20 pages still have at least one MOC membership, index header/page count remains valid, and there is still exactly one same-day lint log entry.

## Implementation pattern
A small repair script can remove a line from the wrong MOC and add it under the right section, then touch the MOC frontmatter `updated` field. This is an infrastructure repair within the same lint run and should not append a second `wiki-log.md` entry unless page/index/log contents changed in a way the existing entry no longer describes.
