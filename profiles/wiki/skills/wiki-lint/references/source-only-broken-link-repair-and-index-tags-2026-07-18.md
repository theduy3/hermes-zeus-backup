# Source-only broken-link repair and index tag regeneration (2026-07-18)

Context: an exact-20 cron lint batch targeted pages whose only structural issue was dangling source/provenance wikilinks, mostly inside `sources:` frontmatter or source-reference prose. The canonical health scan counted these as broken outbound links, but many targets were raw captures or legacy source titles with no real wiki page.

## Durable workflow

1. For each selected page, classify every broken `[[target]]` before editing:
   - **Close note alias exists** → repoint to the real note basename, e.g. an old punctuation-free alias to an existing `*.md` note.
   - **Source/provenance-only target with no page** → preserve the provenance as plain text (or URL if present) and remove only the wikilink brackets. Do **not** create dummy Notes pages just to satisfy link counts.
   - **Attachment path target** → if a real attachment exists by basename/name, prefer the correct attachment link; otherwise treat as provenance text rather than inventing a page.
2. After bracket removal, re-run broken-link verification on the same 20 pages, not only the global count. Empty or malformed targets (`[[]]`) in the verifier usually mean the checker did not skip blank captures; fix the verifier before treating it as a page defect.
3. Run a semantic pass over the touched pages' `## Related` sections:
   - Remove `[[... MOC]]` entries from Related sections.
   - Remove source/provenance-only Related bullets.
   - Keep low-context pages honestly low-outbound rather than adding broad MOC/tag substitutions.
4. Regenerate `System/wiki-index.md` after semantic cleanup and rewrite/append exactly one same-day lint log entry with post-run counts.

## Index regeneration pitfall

When rebuilding `wiki-index.md`, parse YAML list fields correctly. For `tags:` blocks like:

```yaml
tags:
  - ai
  - engineering
```

the index row should contain `ai engineering`, **not** `- ai ai engineering` or duplicated inline/list values. Only collect indented `- value` entries as tag values; strip the dash and quotes.

## Verification checklist

- Canonical `System/scripts/wiki-health.py` succeeds after edits.
- Each of the 20 touched pages has `updated: <run-date>`, required frontmatter, no conflict markers, and no broken links.
- `## Related` sections contain no MOC-substitute links.
- `wiki-index.md` header `page_count` equals the number of direct `/vault/Notes/*.md` pages and sample rows do not contain literal YAML dashes in the Tags column.
- `wiki-log.md` has exactly one same-day lint entry for the run, updated after semantic cleanup.
