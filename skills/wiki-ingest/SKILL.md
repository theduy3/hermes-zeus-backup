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

### Sources/ is read-only
The `Sources/` directory and its contents are often **root-owned** or mounted
read-only. The canonical instruction to `mv "Inbox/filename.md" "Sources/filename.md"`
will fail with "Permission denied." **Workaround:** archive ingested source files to
`Notes/` instead (with `type: article|reflection` and `ingested: YYYY-MM-DD` in
frontmatter). Note the `Sources/` blockage in the final summary.

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
Markdown captures in `Inbox/` can be owned by `root:root` while the `Inbox/` directory itself is writable by `hermes`. In that case, patching frontmatter may fail or be undesirable, but a directory-level `rename`/move can still work because moving depends on directory permissions, not file ownership. Safe pattern after creating the source archive page in `Notes/`:
1. Create `Notes/<Source Title> Source.md` with `ingested: YYYY-MM-DD` and `## Pages Updated`.
2. Move the root-owned Inbox original to `Notes/Archived Inbox Originals/` (collision-safe basename) to prevent repeat ingestion while preserving raw content.
3. Verify `Inbox/` is empty or contains only unprocessed files that intentionally remain.
4. Mention the Notes fallback and original-preservation location in the final summary.

### Metadata-only URL captures
If an Inbox source contains only a URL and remote fetch/extraction is unavailable or times out in headless cron, do not fabricate a wiki page from the title alone. Create a metadata-only source archive in `Notes/` with `Pages Updated: None`, move/archive the original out of `Inbox/`, and report that no wiki page was created because the source body was unavailable.
summary.

### read_file tool degrades on permission-denied files
The `read_file` tool may succeed on the first call to a root-owned file (cached read)
but fail on subsequent calls, returning 0 lines with error "File not found." The file
still exists on disk (`os.path.exists` returns True). **Fallback:** use
`search_files(target='content')` to grep the file, or `execute_code` with
`os.path.exists` + `os.path.getsize` to confirm presence. Do not retry `read_file`
more than twice on the same path — switch to the fallback.

### Verify infrastructure edits by searching exact new artifacts
After updating `System/wiki-index.md`, `System/wiki-log.md`, or MOCs, verify with an exact search for the new page/source title, not just by trusting a write succeeded. When patching index rows, do not assume the row's tag/type text from memory; first inspect the actual neighboring row or use an exact old_string from the current file. If the exact artifact is missing after a broad rewrite, patch it in with a small targeted replacement and verify again.

### Notes fallback source archives still count as indexed pages
When `Sources/` is blocked and the source archive is created under `Notes/` (for example `Notes/<Source Title> Source.md`), treat that archive as a page for infrastructure bookkeeping:
- Add an index row for both the substantive wiki page(s) and the source archive page.
- Increment `page_count` for every new `Notes/*.md` created, including `type: repo|article|reflection` source archives.
- If existing pages are updated from the source, update their `updated` date rows in `wiki-index.md` too.
- Verify exact searches for the content page title, source archive title, touched MOC link, and `wiki-log.md` entry before finalizing.

### Root-owned Inbox original preservation verification
When using the root-owned Inbox markdown safe pattern, a directory-level `mv` to `Notes/Archived Inbox Originals/` can succeed even though file patching would be undesirable. After the move, verify both sides explicitly: the original basename is absent from `Inbox/` and present under `Notes/Archived Inbox Originals/`. Report this preservation path in the final summary.
