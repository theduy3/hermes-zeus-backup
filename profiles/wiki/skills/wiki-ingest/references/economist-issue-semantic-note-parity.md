# The Economist issue semantic note parity

Use this reference when ingesting or repairing full *The Economist* issue PDFs with article folders.

## Lesson
For this user, article-folder extraction is not enough. Each numbered source extract (`Sources/<Issue> Articles/NN-slug.md`) must map to an ingested `/vault/Notes` page, and MOCs must link those Notes pages — never the raw numbered source files.

## Quality bar from prior issues
June 6 and June 27 issues established the expected shape:
- source folder contains exhaustive numbered article extracts;
- MOCs link polished semantic Notes such as `[[Rural India Smartphone Revolution]]`, `[[AI Compute Futures Markets]]`, `[[US Treasury Market Fragility]]`;
- Notes are topic/entity named, not mechanical issue-title wrappers;
- article Notes should generally be `wiki_status: complete` once they have source-grounded summaries and MOC routing.

## Anti-pattern found in July 4 repair
Do not create or leave mechanical titles like:
- `[[Imran Khan v Asim Munir Economist July 2026]]`
- `[[Buttonwood A new Plaza Accord Economist July 2026]]`
- `[[A23a Economist July 2026]]`

Rename/enhance them into semantic wiki pages such as:
- `[[Pakistan Khan Munir Power Struggle]]`
- `[[New Plaza Accord Exchange Rate Limits]]`
- `[[A23a Iceberg Obituary]]`

## Repair/verification checklist
1. Build a mapping from every numbered article extract in `00-index.md` to an existing or new `/vault/Notes` page.
2. Reuse existing durable pages when the article is already represented; otherwise create a semantic article-level Note.
3. Rename mechanical `... Economist <Month> <Year>` draft pages into durable topic/entity titles.
4. Update every readable MOC date section to link the ingested Notes pages.
5. Verify:
   - every source extract maps to at least one existing Note;
   - every mapped Note is linked from the correct readable MOC;
   - raw numbered source links like `[[01-...]]` do not appear in readable MOCs;
   - no mechanical `*Economist <Month> <Year>.md` article files remain;
   - July issue Notes are marked complete when summaries are source-grounded;
   - root-owned/unreadable MOCs are reported with exact `chown` commands.

## Permission caveat
If a MOC is root-owned/unreadable, skip only that MOC, update all writable MOCs, and report the exact command, e.g.:

```bash
sudo chown hermes:hermes /vault/MOCs/Europe\ MOC.md /vault/MOCs/Finance\ MOC.md
```
