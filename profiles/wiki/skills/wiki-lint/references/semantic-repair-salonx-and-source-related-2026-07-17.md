# Semantic repair: SalonX/source Related cleanup — 2026-07-17

## Context
An exact-20 cron `wiki-lint` pass selected a newly indexed direct note, `salonx-first-100-customers`, plus several older tool/source-derived pages. The first automated pass satisfied numeric outbound counts but added weak SalonX links via broad `ai`/business overlap and left source/provenance-only entries in `## Related` sections after broken-link cleanup.

## Durable lesson
When a selected page is a real business/operational note, do not let broad tags such as `ai`, `business`, `marketing`, or `startup` dominate related-link selection. Search distinctive body/title terms first (`SalonX`, `salon`, `nail`, `payroll`, `commission`, `customers`, etc.) and prefer direct subject neighbors even if they are not high-inbound pages.

## Repair pattern
1. After the automated exact-20 pass, print/re-read every touched page's `## Related` section.
2. For newly indexed or low-context pages, search by distinctive terms from the title/body rather than broad tags.
3. Replace weak generic links with close domain neighbors. Example for SalonX first-customer planning:
   - `[[Salon SOP Coaching Package]]`
   - `[[AI Ontology First Approach for Salon Business]]`
   - `[[Nail Salon W-2 Payroll Process]]`
   - `[[Nail Salon W2 Commission Economics]]`
4. Remove source/provenance-only Related entries created by broken-link cleanup (plain text like `2026-04-18 - Awesome Generative AI Guide — related wiki context`) unless the source itself is an actual page and close semantic neighbor.
5. Move MOC placement to the narrowest existing section. For SalonX/nail-salon operating notes, use `Personal MOC` → `Business & Salon` rather than a generic date bucket.
6. Regenerate `System/wiki-index.md`, rewrite exactly one same-day lint log entry, rerun canonical `System/scripts/wiki-health.py`, and verify all 20 touched pages again.

## Guardrails
- It is better to leave a page honestly low-outbound than to add generic AI/business links.
- Do not create dummy source pages to satisfy broken source/provenance links.
- Keep active/high-value sources directly under `/vault/Sources`; `_cold` remains legacy/low-browse bulk only.
