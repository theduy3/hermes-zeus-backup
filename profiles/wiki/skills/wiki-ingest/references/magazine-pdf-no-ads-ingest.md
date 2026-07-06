# Magazine / Newspaper PDF ingest with ads removed

Use this pattern when the user uploads a full magazine/newspaper issue PDF and asks to ingest it while deleting ads.

## Workflow
1. **Inspect the PDF locally first** with PyMuPDF (`fitz`) rather than vision/large OCR when the PDF has embedded text.
   - Print file size, page count, metadata, and a per-page preview: page number, character count, first 6-10 non-empty lines.
   - Use the preview to identify ad pages, blank pages, cover/contents/subscription-service pages, and other non-editorial front/back matter.
2. **Create a cleaned PDF attachment** under `/vault/Attachments/` containing only retained pages.
   - Do not keep an uncleaned copy in the vault when the user explicitly asked to delete ads/content.
   - Use a clear basename such as `The Economist 2026-06-06 Issue Cleaned No Ads.pdf`.
3. **Create cleaned Markdown source** in `/vault/Inbox/` from the same retained pages.
   - Frontmatter should include `tags: [source, magazine]`, `type: article`, `source: telegram-upload`, `title`, `created`, `attachment`, and a field listing removed pages (for example `ad_and_noneditorial_pages_removed: "1-4, 11, 13, 31, 40, 72, 91, 92"`).
   - Add a short note that ad/blank/non-editorial pages were removed before ingest.
   - Footer should embed/link the cleaned PDF, not the original uncleaned PDF.
4. **Ingest at issue + atomic-page levels.** For dense issues, create a synthesis page for the whole issue and 2-5 atomic notes for the strongest durable themes. Do not make one page per article unless the user asks.
5. **Archive and verify.** Move the cleaned Markdown source to `Sources/`, update `wiki-index.md`, `wiki-log.md`, relevant MOC(s), and verify:
   - Inbox is empty.
   - Cleaned PDF exists and uncleaned PDF is absent from the vault.
   - Cleaned PDF page count equals original pages minus removed pages.
   - Searches for obvious ad text / known removed page headings return no matches in the source archive.
   - Created pages, index rows, MOC links, and log entry exist.

### Telegram full-issue shortcut
When a Telegram-uploaded full issue is only described as “ingest” (not “extract every article”), still apply the no-ads magazine pattern by default. A reliable shortcut is:
1. Copy the uploaded binary into `Inbox/` with a timestamped basename for capture/provenance.
2. Use PyMuPDF previews to identify obvious non-editorial pages (cover, blank pages, ads, classified, back-cover). Low character count alone is not enough; inspect first lines for ad/service text.
3. Write the cleaned PDF to `Attachments/` and a cleaned Markdown source with `## Pages Updated` and an attachment embed. It is acceptable to copy/archive that Markdown directly to `Sources/` and then remove the transient Inbox Markdown/PDF, as long as the source archive contains the normalized frontmatter and full retained text.
4. For dense issues, create one issue-level synthesis plus a few durable atomic notes, not one page per article unless explicitly requested.
5. Verify with exact file checks and exact searches: source archive present, cleaned PDF page count, original/uncleaned PDF absent from the vault, Inbox empty, ad/classified/back-cover strings absent from the source archive, index/log/MOC rows present.

## PyMuPDF snippets

Per-page preview:
```python
import fitz, os
p = '/path/to/upload.pdf'
doc = fitz.open(p)
print('size', os.path.getsize(p), 'pages', doc.page_count, 'metadata', doc.metadata)
for i, page in enumerate(doc, 1):
    txt = page.get_text('text')
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    print(f'{i:02d}\tchars={len(txt):5d}\t' + ' | '.join(lines[:8])[:220])
```

Build cleaned PDF:
```python
import fitz, os
src = '/path/to/upload.pdf'
out = '/vault/Attachments/Issue Cleaned No Ads.pdf'
remove = {1, 2, 3, 11}  # 1-indexed pages to drop
src_doc = fitz.open(src)
clean = fitz.open()
for i in range(src_doc.page_count):
    if (i + 1) not in remove:
        clean.insert_pdf(src_doc, from_page=i, to_page=i)
clean.save(out, garbage=4, deflate=True)
print(out, os.path.getsize(out), 'pages', clean.page_count)
```
