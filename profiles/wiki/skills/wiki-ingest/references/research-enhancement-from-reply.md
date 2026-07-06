# Research enhancement from a reply-to prior ingest

Use when the user replies to an earlier ingest summary and says things like “add this into the research,” “do deep research,” or asks to build a protocol/routine from an attached image or extra note.

## Pattern

1. **Treat the new material as a source, not a chat aside.**
   - For images: use vision to transcribe faithfully, copy the image into `Attachments/` with a descriptive collision-safe name, and create a `Sources/YYYY-MM-DD-HHMM-<topic>.md` source archive with transcription, context, attachment embed, and `## Pages Updated`.
   - For text: capture verbatim into a source archive or Inbox first if it is long enough to need provenance.
2. **Patch the existing note named in the reply context** when it is clearly the target, instead of creating a second competing note. Add the new source to frontmatter `sources:` and update `updated:`.
3. **Research grounding:** for health/wellness or other advice-like topics, add a safety/limitations section and cite credible sources actually checked (clinical/org docs, manuals, official docs). Distinguish social-media claims from vetted guidance.
4. **Turn research into an actionable artifact** when the user asks for one: e.g. a timed daily routine, checklist, 7-day trial protocol, stop criteria, or verification checklist.
5. **Update infrastructure**: `wiki-index.md`, relevant MOC only if the note is newly created or moved categories, and `wiki-log.md` with the source + updated page.
6. **Verify exact artifacts**: updated note has the new section, source archive exists, attachment exists, index/log rows reflect the update.

## Example output shape for a health routine enhancement

- `## Captured Order From Screenshot`
- `## Research Grounding`
- `## Safety / When Not To Do It`
- `## Daily 10-Minute Routine`
- `## 7-Day Trial Protocol`
- `## Research Sources`
