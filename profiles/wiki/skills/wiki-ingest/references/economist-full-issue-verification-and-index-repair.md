# Economist full-issue verification and index-repair pitfalls

Use this when ingesting full *The Economist* issue PDFs with article folders, article-level Notes, MOC routing, and wiki-index/wiki-log updates.

## Lessons from July 11 2026 full-issue ingest

### Article counts: exclude `00-index.md`
When verifying the article folder, count only numbered article extracts and explicitly exclude `00-index.md`:

```python
arts = sorted(p for p in folder.glob('[0-9][0-9]-*.md') if p.name != '00-index.md')
```

Pitfall: a glob like `[0-9][0-9]-*.md` matches `00-index.md`, so naive counts overstate the article count by one and can leak a wrong count into `wiki-log.md` or summaries.

### Template compliance: do not test `00-index.md` as an article
Template-heading checks (`# Type of post`, `# Rapid fire thoughts`, etc.) should run only against article extract files, not `00-index.md`. If the only missing-template file is `00-index.md`, the article extracts may still be compliant.

### wiki-index row generation: parse only frontmatter keys intended as tags
When generating `System/wiki-index.md` rows from note frontmatter, do not collect every YAML list item after the first `tags:` block. A naive parser can accidentally include `sources:` wikilinks as tags, producing rows like:

```text
| [[Note]] | concept | complete | economist finance "[[Source]]" "[[Article Extract]]" | 2026-07-12 |
```

Safer pattern:
- parse the frontmatter with a YAML parser when available; or
- if using a small manual parser, only collect list items while the current key is exactly `tags`.

After any bulk index update, exact-search representative rows and verify that the Tags column contains only tags, not source wikilinks.

### Mapping/MOC verification checklist
After creating article extracts and semantic Notes, verify these facts from actual files:

```python
maps = re.findall(r'\[\[([0-9][0-9]-[^\]]+)\]\] → \[\[([^\]]+)\]\]', index_text)
missing_notes = [note for stem, note in maps if not (vault/'Notes'/f'{note}.md').exists()]
missing_moc = [note for stem, note in maps if f'[[{note}]]' not in all_moc_text]
raw_moc_links = re.findall(r'\[\[([0-9][0-9]-[^\]]+)\]\]', all_moc_text)
```

Success criteria:
- `len(maps)` equals the true article-extract count;
- `missing_notes == []`;
- `missing_moc == []`;
- `raw_moc_links == []`.

### Canonical numbered MOCs
If a manifest entry routes to a legacy unnumbered MOC name (for example `International MOC`), also verify the canonical numbered MOC receives the link when that section has a numbered filename (for example `08 International MOC.md`). The user expects canonical section numbers in actual MOC filenames.
