# Newsletter Design/Themed Sunday Special Routing

Session pattern from 2026-07-19 Morning Brew "Design Brew" ingest.

## Trigger
Use this when a Morning Brew Sunday special or other newsletter issue is theme-led (design, culture, public lands, etc.) rather than a normal market/news digest, and the issue contains several reusable ideas but little day-to-day market data.

## Routing pattern
1. Archive the newsletter under `Sources/Newsletter/YYYY-MM-DD - <Issue Title>.md` with `original_filename`, `ingested`, and a `## Pages Updated` section.
2. Create one issue-level synthesis note in `Notes/` (e.g. `Design Brew Sunday Special`) that lists the distilled pages and records source-only blocks skipped.
3. Distill 4-8 durable concept/entity notes when the theme yields reusable patterns, not just one monolithic newsletter note.
4. Update `Morning Brew Newsletter Network` with a date-specific routing paragraph and add the source to its frontmatter.
5. Route each atomic note to semantic MOCs, not only the newsletter hub. For the Design Brew issue:
   - Business/brand/platform notes -> `14 Business MOC`
   - Culture/design/status/information-design notes -> `17 Culture MOC`
   - AI-specific design/branding notes -> `AI Development MOC`
6. Leave sponsor copy, referrals, product recommendations, social links, generic boilerplate, and most ICYMI recommendation lists source-only unless they connect to an existing durable page.

## Example distilled pages
The July 19 2026 Design Brew issue created:
- `Design Brew Sunday Special` — issue-level synthesis and routing note.
- `Successful Brand Redesign Patterns` — rebrands as continuity plus modernization.
- `Typography Semantic Risk` — fonts as meaning, reputational risk, and forensic evidence.
- `AI Logo Convergence` — AI logos converging on circular/hexagonal abstraction.
- `Algorithmic Cafe Aesthetic` — platform discovery incentives homogenizing physical retail design.
- `Schematic Transit Map Design` — useful topological distortion beats literal geography.
- `Quiet Luxury Aesthetic Cycle` — luxury status signaling between stealth and display.

## Verification checklist
- Inbox empty.
- Source exists in `Sources/Newsletter/` with `## Pages Updated`.
- Every created note exists and cites the source archive.
- `Morning Brew Newsletter Network` contains the new issue routing paragraph and source wikilink.
- Relevant semantic MOCs contain exact links to the created notes.
- `System/wiki-index.md` rows exist for all created notes and any updated hub.
- `System/wiki-log.md` contains an ingest entry for the issue.
