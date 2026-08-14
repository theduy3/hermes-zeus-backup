# Rolling refresh + semantic cleanup when few structural issues remain (2026-07-22)

Context: scheduled `/wiki-lint` exact-20 run where canonical health showed no orphans, no MOC gaps, no sparse direct Notes pages, and only a few issue-bearing low-outbound pages remained.

Reusable pattern:

1. **Freeze the batch after the first selector.** If fewer than 20 structural issue-bearing direct pages remain, select those first, then fill to exactly 20 from the oldest `updated` direct `Notes/*.md` rolling-refresh queue. Freeze that title list and use it for every subsequent mutation, repair, verification, index regeneration, and log rewrite.
2. **Do not rerun a mutating selector after semantic repair.** Lower issue counts can cause a second set of pages to be touched in the same cron run. Reuse the frozen list.
3. **Normalize frontmatter without inventing links.** Set `updated` to the run date, ensure required fields (`tags`, `type`, `created`, `updated`, `wiki_status`), remove conflict-marker artifacts from selected frontmatter, and strip polluted tag values such as URLs, `[[wikilinks]]`, or `none`.
4. **Run semantic Related cleanup after any automated pass.** Re-read all 20 touched pages and inspect actual `## Related` sections. Remove MOC links, broad/generic tag-overlap links, source/provenance-only links, and token-collision links. Examples of weak links removed in this run: generic marketing links from an AI video workflow; unrelated MCP server links from Context7; generic self-hosted-tool links from Drawbridge; broad browser/security links from CloakBrowser; broad infrastructure examples from a DevOps guidelines page.
5. **Leave honest low-outbound pages low.** Sparse captures, metadata-only source pages, and niche pages with only one close neighbor should remain low-outbound rather than receiving unrelated replacements. Report them as honest low-outbound after semantic cleanup.
6. **Regenerate infrastructure once repairs are done.** Regenerate `System/wiki-index.md` with list-aware tag parsing, then rewrite exactly one same-day `wiki-log.md` lint entry with canonical `System/scripts/wiki-health.py` counts plus frozen-batch verification.
7. **Final verification should combine canonical + frozen-batch checks.** Use `wiki-health.py` for vault-wide canonical health, and a frozen-batch verifier for: exactly 20 touched pages, frontmatter parses/has required fields, `updated` is today, no conflict artifacts, all 20 have index rows, all 20 are in some readable MOC, exactly one same-day lint log entry, and low-outbound pages are explicitly listed.

Report canonical health separately from honest selected-batch low-outbound counts. A higher low-outbound count after semantic cleanup is acceptable when weak links were removed.