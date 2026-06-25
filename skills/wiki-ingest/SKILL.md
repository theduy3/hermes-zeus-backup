---
name: wiki-ingest
description: Batch-ingest theduyvault Inbox sources into the wiki; transcribe photos with vision. Scheduled headless job.
version: 1.0.0
metadata:
  hermes:
    requires_toolsets: [terminal, file, vision]
    tags: [vault, wiki, ingest, theduyvault]
---

# wiki-ingest — batch wiki ingest (headless)

You are running as a scheduled cron job. Run fully autonomously: no confirmation
prompts, no questions.

## Canonical instructions
Read and follow **`/vault/.claude/commands/wiki-ingest.md`** exactly (scan Inbox,
process each source, dedup-check, create/update wiki pages with correct frontmatter,
update MOCs, archive to Sources/, update `wiki-index.md` + `wiki-log.md`).

## Runtime adaptations (this environment) — IMPORTANT, these override the canonical file
- Vault is at **`/vault`**. All paths below are under `/vault`.
- **OCR Step 0 is replaced by your own vision capability.** Do NOT call
  `/root/ocr/ocr.py` (it does not exist here). Instead, for each non-markdown file in
  `/vault/Inbox/` (images of handwriting, photos, PDFs):
  1. Transcribe it with the **vision** tool (read the text faithfully; preserve
     structure/lists).
  2. Write the extracted text as a new `.md` into `/vault/Inbox/` (this becomes the
     source for the normal ingest steps below).
  3. Move the original binary into `/vault/Attachments/` (collision-safe name) and add
     an Obsidian embed/link to it in the `.md` footer.
- **No subagents/Task tool.** Process sources **sequentially**, one at a time.
- **Search/dedup:** there is no qmd here. Use `rg` over `/vault/Notes` and
  `/vault/System/wiki-index.md` to check whether a page already exists before creating.
- **Markdown sniffing for odd filenames:** Inbox captures may be Markdown even when the
  filename has no `.md` suffix (or has a long title fragment that `os.path.splitext`
  treats as an extension). Before treating a non-`.md` Inbox item as binary/OCR input,
  read/sniff the first bytes when possible. If it starts with YAML frontmatter (`---`) or
  otherwise contains Markdown text from a web capture, process it as a normal Markdown
  source and archive/move the original out of Inbox after creating the source archive.
- Enforce the **200-byte UTF-8 filename cap** for all basenames (5-byte reserve for
  collision suffixes), per the canonical command.
- Use the **terminal** tool (`rg`, `mv`, `ls`), the **file** tool (read/write/edit
  pages), and the **vision** tool (transcription).

## Pitfalls & environment-specific constraints

### Sources/ may be read-only — verify before choosing archive path
The `Sources/` directory and its contents are often **root-owned** or mounted
read-only, but this can vary by run. Do not assume it is blocked forever: during
pre-flight, inspect `ls -ld /vault/Sources` and use canonical `Sources/` archival if
it is writable and the source file can be moved safely. If `mv "Inbox/filename.md"
"Sources/filename.md"` fails with "Permission denied" (or the directory is clearly
not writable), archive ingested source files to `Notes/` instead (with
`type: article|reflection` and `ingested: YYYY-MM-DD` in frontmatter). Note the
`Sources/` blockage in the final summary only when the fallback was actually used.

When using this workaround, prevent repeat ingestion by either moving the Inbox source
out of `Inbox/` if allowed, or patching only its frontmatter to add `ingested: YYYY-MM-DD`.
Keep the original body unchanged. A reliable pattern is:
1. Create/update the wiki page(s) in `Notes/`.
2. Create a source archive page in `Notes/` using a collision-safe title such as
   `<Source Title> Source.md`, with `tags: [source]`, `type`, `source`, `created`, and
   `ingested` frontmatter plus a `## Pages Updated` section.
3. Patch the original Inbox file's frontmatter with the same normalized source metadata
   and `ingested: YYYY-MM-DD` so the Step 1 filter skips it next run.
4. Mention in the final summary that archival used the Notes fallback instead of Sources/.

### Infrastructure files may be root-owned
`System/wiki-index.md`, `System/wiki-log.md`, and several `MOCs/*.md` files can be
owned by `root` with restrictive permissions (`600` or `644`). When this happens:
- `read_file` returns "File not found" (empty content, 0 lines) — the file exists but
  can't be read.
- `write_file` / `patch` fail with "Permission denied."
- `terminal` commands like `head`, `wc`, `cat` also fail with "Permission denied."

**Detection:** run `ls -la /vault/System/` and `ls -la /vault/MOCs/` early in the run.
If any infrastructure files are `root root`, note which ones. `search_files` and
`search_files(target='files')` still work for discovery. See
`references/root-owned-infrastructure.md` for exact error signatures, detection steps,
and the required `chown` fix command.

**Adaptation:** when infrastructure files are root-owned, skip Steps 3 (wiki-index,
wiki-log) and Step 2d (MOC updates). Report all blocked files in the summary with the
exact `chown` command needed. Still create wiki pages in `Notes/` (usually writable).

### Terminal approval in headless cron
Terminal commands that touch files outside the working directory, delete files, or run
### Terminal approval in headless cron
Terminal commands that touch files outside the working directory, delete files, or run Python scripts may be flagged for **approval** (`pending_approval: true`). In a headless cron job there is no user to approve — these commands may silently fail,
partially execute, or have unpredictable results. **Prefer `write_file` and `patch`
tools over terminal for all file creation and editing.** Use terminal only for
read-only operations (`ls`, `stat`, `rg` searches) and narrow directory-level preservation moves for root-owned Inbox originals when the directory is writable. Avoid `rm` — if you must remove a
file, use `patch` with `replace_all` to empty it, or leave it and note it in the summary.

Do not use `execute_code` for cron wiki ingest batching. In this runtime, arbitrary local Python execution may be approval-blocked in cron; the reliable pattern is explicit `write_file`/`patch` calls for Notes/System/MOC edits, followed by small terminal read-only checks and a single targeted `mkdir -p && mv && test` only when preserving a root-owned Inbox original out of Inbox.

### Root-owned Inbox markdown sources
Markdown captures in `Inbox/` can be owned by `root:root` while the `Inbox/` directory itself is writable by `hermes`. In that case, patching frontmatter may fail or be undesirable, but a directory-level `rename`/move can still work because moving depends on directory permissions, not file ownership.

Safe pattern when `Sources/` is writable:
1. Create a normalized source archive directly in `Sources/<original basename>.md` with `tags: [source]`, source `type`, `source`, `created`, `ingested`, and `## Pages Updated`.
   - For short sources, `write_file` the archive with normalized frontmatter plus the original body.
   - For large root-owned Markdown captures where reconstructing the full body would be error-prone, use a targeted `cp` from `Inbox/` to `Sources/`, then patch only the archive copy's frontmatter / `## Pages Updated`. Do **not** patch the root-owned Inbox original. Verify the archive copy exists and has the expected size/content before moving the original out of Inbox.
2. Move the root-owned Inbox original to `Notes/Archived Inbox Originals/` (collision-safe basename) to prevent repeat ingestion while preserving the raw capture.
3. Verify three facts explicitly: the Inbox original is absent, the `Sources/` archive exists, and the preserved original exists under `Notes/Archived Inbox Originals/`.
4. Mention the preservation path in the final summary, but do **not** call this a Notes fallback if the canonical source archive was successfully written to `Sources/`.

Safe pattern when `Sources/` is blocked or a move/write to `Sources/` fails:
1. Create `Notes/<Source Title> Source.md` with `ingested: YYYY-MM-DD` and `## Pages Updated`.
2. Move the root-owned Inbox original to `Notes/Archived Inbox Originals/` (collision-safe basename) to prevent repeat ingestion while preserving raw content.
3. Verify `Inbox/` is empty or contains only unprocessed files that intentionally remain.
4. Mention the Notes fallback and original-preservation location in the final summary.

### Metadata-only URL captures
If an Inbox source contains only a URL and remote fetch/extraction is unavailable or times out in headless cron, do not fabricate a wiki page from the title alone. Create a metadata-only source archive in `Notes/` with `Pages Updated: None`, move/archive the original out of `Inbox/`, and report that no wiki page was created because the source body was unavailable.
summary.

### read_file/search can degrade on permission-denied files
The `read_file` tool may succeed on the first call to a root-owned file (cached read)
but fail on subsequent calls, returning 0 lines with error "File not found." The file
still exists on disk (`os.path.exists` returns True). **Fallback:** use
`search_files(target='content')` to grep the file, or `execute_code` with
`os.path.exists` + `os.path.getsize` to confirm presence. Do not retry `read_file`
more than twice on the same path — switch to the fallback.

Broad `search_files`/`rg` over all of `Notes/` can also abort when it hits an unreadable
root-owned note. For dedup checks, avoid one huge content search when permission hazards
are visible: first check `System/wiki-index.md` and likely exact filenames/titles, then
run targeted content searches with narrow terms and paths. If a broad search fails on a
permission-denied file, do not treat that as "no duplicate"; retry with a narrower query
or rely on the readable index plus exact filename/title probes.

### Opaque or overlong Inbox filenames from web clips
Inbox files such as `de.md` or `dg.md` may contain fully titled article captures even
though the filename is opaque. In that case, name the substantive wiki page from the
source title/date (for example `Stock Market Today May 26 2026.md`) while preserving the
canonical archive basename in `Sources/<original>.md`. Use the original basename in the
page `sources:` wikilink (e.g. `[[dg]]`) and in `wiki-log.md`; do not force a rename of
the source archive just to make it human-readable.

If the Inbox basename is itself over the 200-byte cap or has no `.md` suffix because a
long title fragment was parsed as an "extension", first sniff/read it as Markdown. If it
is a web-clip Markdown source, create a shortened collision-safe archive basename in
`Sources/` (for example `<owner>_<repo> concise title GitHub.md`) and use that shortened
archive basename consistently in new page `sources:` wikilinks, `## Pages Updated`,
`wiki-index.md`, and `wiki-log.md`. For root-owned overlong Markdown, use the root-owned
Inbox pattern: `cp` the raw file to the shortened `Sources/` path, patch only the archive
copy's normalized frontmatter and `## Pages Updated`, then move the raw Inbox original to
`Notes/Archived Inbox Originals/` with a shortened preservation name. Verify: Inbox
absence, `Sources/` archive presence, preserved-original presence, and exact index/log/MOC
matches before summarizing.

### Verify infrastructure edits by searching exact new artifacts
After updating `System/wiki-index.md`, `System/wiki-log.md`, or MOCs, verify with an exact search for the new page/source title, not just by trusting a write succeeded. When patching index rows, do not assume the row's tag/type text from memory; first inspect the actual neighboring row or use an exact old_string from the current file. If the exact artifact is missing after a broad rewrite, patch it in with a small targeted replacement and verify again.

When inserting a new index row by replacing a neighboring row, preserve the neighboring row verbatim in `new_string`; otherwise the patch can silently delete or mutate an unrelated page row while adding the new one. Immediately re-read a small window around the insertion and search for both the newly inserted row and the preserved neighbor. If the neighbor disappeared or changed, repair it before finalizing.

For file-presence checks, remember that `search_files(target="files")` uses glob-style filename matching, not regex alternation. A pattern like `a.md|b.md` will not verify multiple files. Use separate exact file probes, a simple wildcard that actually matches, or a narrow read-only `ls -la <file1> <file2> ...` verification when confirming source archives and preserved Inbox originals.

Before adding a wikilink to a related page that was inferred from source content, exact-search `Notes/` for that page title. If no page exists and the source does not warrant creating one now, mention the entity in plain text instead of creating a dangling wikilink just to satisfy outbound-link count.

### Preserve exact captured URLs when normalizing source frontmatter
When converting clipped source frontmatter to normalized `Sources/` frontmatter, copy the `source:` URL exactly from the Inbox read, especially long `fbclid`/tracking URLs. Do not retype or abbreviate from memory: one-character drift silently changes provenance. After patching the source archive frontmatter, re-read the first 10–20 lines of the archive and compare the URL/title against the original source metadata before moving the Inbox original out of `Inbox/`.

### Notes fallback source archives still count as indexed pages
When `Sources/` is blocked and the source archive is created under `Notes/` (for example `Notes/<Source Title> Source.md`), treat that archive as a page for infrastructure bookkeeping:
- Add an index row for both the substantive wiki page(s) and the source archive page.
- Increment `page_count` for every new `Notes/*.md` created, including `type: repo|article|reflection` source archives.
- If existing pages are updated from the source, update their `updated` date rows in `wiki-index.md` too.
- Verify exact searches for the content page title, source archive title, touched MOC link, and `wiki-log.md` entry before finalizing.

### Root-owned Inbox original preservation verification
When using the root-owned Inbox markdown safe pattern, a directory-level `mv` to `Notes/Archived Inbox Originals/` can succeed even though file patching would be undesirable. After the move, verify both sides explicitly: the original basename is absent from `Inbox/` and present under `Notes/Archived Inbox Originals/`. Report this preservation path in the final summary.
