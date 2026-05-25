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
Python scripts may be flagged for **approval** (`pending_approval: true`). In a
headless cron job there is no user to approve — these commands may silently fail,
partially execute, or have unpredictable results. **Prefer `write_file` and `patch`
tools over terminal for all file creation and editing.** Use terminal only for
read-only operations (`ls`, `stat`, `rg` searches). Avoid `rm` — if you must remove a
file, use `patch` with `replace_all` to empty it, or leave it and note it in the
summary.

### read_file tool degrades on permission-denied files
The `read_file` tool may succeed on the first call to a root-owned file (cached read)
but fail on subsequent calls, returning 0 lines with error "File not found." The file
still exists on disk (`os.path.exists` returns True). **Fallback:** use
`search_files(target='content')` to grep the file, or `execute_code` with
`os.path.exists` + `os.path.getsize` to confirm presence. Do not retry `read_file`
more than twice on the same path — switch to the fallback.
