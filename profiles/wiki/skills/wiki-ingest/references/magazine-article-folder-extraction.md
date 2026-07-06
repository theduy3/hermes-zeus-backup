# Magazine/newspaper PDF article-folder extraction

Use when the user asks to extract each article from a magazine/newspaper PDF into a folder, especially if they specify an article template.

## Required output
- Folder: `/vault/Sources/<Issue Title> Articles/`
- `00-index.md` listing every extracted article in reading order.
- One Markdown file per article, numbered in reading order: `01-<slug>.md`, `02-<slug>.md`, ...
- Cleaned no-ads PDF in `/vault/Attachments/`.

## Article file template
Every article file must include the headings from `/vault/System/Templates/Article Template.md`:

```markdown
# Type of post
# Rapid fire thoughts
# Tags
# Headlines
# Outline
# Intro
# Main points
# References/ Resources
```

Put faithful extracted article text under `# Main points`. Use frontmatter for machine-readable metadata: `tags`, `type: article`, `source`, `issue`, `section`, `title`, `headline`, `pages`, `created`, `ingested`, and `attachment`.

## Extraction workflow
1. Inspect every PDF page with PyMuPDF text previews and char counts.
2. Identify and exclude cover, blank, contents/front matter, ads, sponsored pages, course promos, and back matter.
3. Save a cleaned PDF from retained pages only; do not keep the uncleaned PDF in the vault if the user asked to delete ads/content.
4. Build an article manifest manually from TOC/page previews. Multi-page articles can share pages; this is acceptable when layout continuation makes hard segmentation unreliable.
5. Write article files and `00-index.md` using the article template headings.
6. Verify:
   - folder exists;
   - article file count excluding `00-index.md`;
   - every `.md` contains all template headings;
   - known ad/front/back-matter phrases are absent from the article folder;
   - cleaned PDF exists;
   - Inbox is empty;
   - `wiki-log.md` records output folder, count, template compliance, attachment, and removed pages.

## Pitfalls
- Page numbers in extracted files should refer to original PDF pages, not cleaned-PDF page numbers.
- Do not mistake article-folder extraction for full wiki page creation; it is a source-archive/extraction task unless the user also asks to synthesize atomic wiki notes.
- If the template is sparse, preserve it exactly and add useful content under each heading rather than inventing a different structure.