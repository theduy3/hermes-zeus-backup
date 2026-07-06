# Reply image attachment to an existing saved source

Use this when the user replies after a previous “save this text / explain this” capture and says to attach a new image or document to that previous text.

## Pattern
1. Treat the new attachment as an addendum to the existing source archive, not as an unrelated new source, unless the user explicitly asks for a new note.
2. Locate the prior source archive by the user’s wording and current conversation context (for example `Sources/YYYY-MM-DD-HHMM-<slug>.md`).
3. Copy the binary into `/vault/Attachments/` with a descriptive collision-safe filename.
4. Transcribe/analyze the image with vision.
5. Patch the existing source archive:
   - add `attachment: "Attachments/<filename>"` to source frontmatter when there is one primary attachment;
   - add an Obsidian embed `![[<filename>]]` under an “Attached Image”/“Addendum” section;
   - include faithful transcription and a concise explanation.
6. If the content belongs in an existing atomic note, update that note instead of creating a duplicate. Add the source archive to `sources:` and link back from a relevant section.
7. Update `wiki-index.md` for any changed `Notes/*.md` updated date and append `wiki-log.md` with the attachment path, affected note(s), and archive/source.
8. Verify: attachment exists, source archive contains the embed/transcription, target note contains the distilled update, index/log entries are searchable, and Inbox is empty.

## Pitfall
Do not answer only in chat when the user says “attach this to the previous text”. The work product is the existing source archive plus any relevant note update in the vault.