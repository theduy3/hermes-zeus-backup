# Index tag normalization + Related-section bounds (2026-06-24)

## What happened
A cron wiki-lint run successfully processed exactly 20 pages and passed batch verification, but the regenerated `System/wiki-index.md` initially included `None` as a tag in many rows. The cause was a lightweight frontmatter parser that converted empty list headers such as `tags:` to `None`, then later included that sentinel when rendering the index.

The same run also printed overly broad `Related` inspection output for some pages because the inspection collector entered at `## Related` and did not stop at a horizontal rule (`---`). Several imported notes place a `---` separator after the Related block before source/body content, so the semantic-review printout accidentally included the whole body.

## Durable fix
When regenerating the index or verifying batch tags:

```python
def norm_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v
                if x is not None and str(x).strip() and str(x).strip().lower() != 'none']
    s = str(v).strip()
    if not s or s.lower() == 'none':
        return []
    return [x.strip() for x in re.split(r'[,;]', s)
            if x.strip() and x.strip().lower() != 'none']
```

After regenerating `wiki-index.md`, explicitly verify:

```python
none_rows = [r for r in index_text.splitlines() if ' None,' in r or '| None' in r]
assert not none_rows
```

When collecting `## Related` lines for semantic review, stop at any next section heading **or** horizontal rule:

```python
if capture and (line.startswith('## ') or line.strip() == '---'):
    capture = False
```

## Verification pattern
After any index repair or semantic cleanup:
1. Re-read all 20 batch pages.
2. Verify `updated == run_date`, required frontmatter fields, and no conflict markers.
3. Verify `wiki-index.md` header date/page_count and all 20 rows.
4. Verify no `None` tags appear in index rows.
5. Verify exactly one same-day lint log entry.
6. Reprint bounded Related lines only; do not let source-body content masquerade as Related links.
