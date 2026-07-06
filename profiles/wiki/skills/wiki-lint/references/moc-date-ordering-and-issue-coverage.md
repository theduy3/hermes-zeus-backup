# MOC date ordering and full-issue article coverage

Use this when the user asks whether MOCs are sorted newest-first, whether a full magazine/newspaper issue is represented in MOCs, or points at an MOC screenshot where issue dates appear out of order.

## Newest-first date sections

1. Scan `/vault/MOCs/*.md` for adjacent date headings such as `### July 4th 2026`, `### June 27th 2026`, and `### 2026-07-04`.
2. Sort only contiguous runs of date headings at the same heading level, newest first.
3. Preserve all content inside each date section; do not alphabetize article bullets unless the user asks.
4. Verify after editing by re-scanning every readable MOC and asserting each contiguous date-heading run is descending.

## Full-issue article coverage

For issue article folders such as `/vault/Sources/The Economist July 4 2026 Articles/`:

1. Treat `00-index.md` as the article inventory of record.
2. Parse every article wikilink from `## Articles`.
3. Route article-extract links into the relevant section MOCs using the section labels in `00-index.md`:
   - `The world this week`, `Leaders`, `Letters`, `By Invitation`, `Essay`, `Obituary` → `The Economist MOC`
   - `United States`, `America at 250` → `US Politics & Society MOC`
   - `The Americas` → `The Americas MOC`
   - `Asia` → `Asia MOC`
   - `China` → `China MOC`
   - `Middle East & Africa` → `Middle East & Africa MOC`
   - `Europe` → `Europe MOC`
   - `Britain` → `Britain MOC`
   - `International` → `International MOC`
   - `Business` → `Business MOC`
   - `Finance & economics`, `Economic & financial indicators` → `Finance & Economics MOC`
   - `Science & technology` → `Science & Technology MOC`
   - `Culture` → `Culture MOC`
4. Add cross-listing only when it is semantically useful, e.g. AI-governance/legal-AI articles into `AI Development MOC` or `AI Agent Tooling MOC`.
5. Verify coverage by checking that every `00-index.md` article link appears in at least one readable MOC. Report `article_count`, `covered_count`, and `missing_count`.

## Pitfalls

- Do not assume an issue synthesis page in a MOC means all article extracts are represented. Verify the article-level folder separately.
- Root-owned MOCs may become unreadable after prior edits. Treat them file-by-file. If the relevant domain MOC is blocked, report the exact `chown` command rather than silently skipping coverage.
- For The Economist finance articles, prefer `Finance & Economics MOC` for section coverage; `Finance MOC` may be a separate/root-owned hub and should not block section-level Economist coverage.
- Append a `wiki-log.md` maintenance entry after bulk MOC routing or date-order fixes.
