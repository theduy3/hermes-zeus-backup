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
- **Social/video URL extraction:** when a user sends a Facebook/Reels/TikTok/short-form video URL and asks to extract information, capture the URL to Inbox first, then extract **metadata + captions/transcript only** under `Attachments/`. **Never download or preserve the video/audio file** for ingest. Use `yt-dlp --skip-download --write-info-json --write-auto-subs --write-subs --sub-langs "en,vi,en.*" --convert-subs srt --write-description --write-thumbnail -o '<Attachments-path>/%(title).80s' <URL>`, clean SRT timestamps into transcript text, enrich the Inbox source with title/uploader/URL/description/transcript, and ingest normally. If there are no captions, record metadata + description and note "no transcript available" — do not download `.mp4`, `.webm`, `.m4a`, or audio as a workaround. See `references/social-video-extraction.md` for details, but this SKILL.md rule overrides any older reference text that suggests keeping video/audio.
- **When the user also asks to “search for guide video on YouTube” after ingesting a social reel:** after extracting the social transcript, derive 2–4 concrete search phrases from the transcript, run metadata-only YouTube searches with `yt-dlp --flat-playlist --print`, select credible/how-to matches, and record the best URLs inside the created wiki note. Do not use piped JSON-to-Python patterns for untrusted output; prefer `--print` fields or save output before parsing. See `references/social-video-youtube-guide-search.md`.
- **OCR Step 0 is replaced by your own vision capability.** Do NOT call
  `/root/ocr/ocr.py` (it does not exist here). Instead, for each non-markdown file in
  `/vault/Inbox/` (images of handwriting, photos, PDFs):
  1. Transcribe it with the **vision** tool (read the text faithfully; preserve
     structure/lists).
  2. Write the extracted text as a new `.md` into `/vault/Inbox/` (this becomes the
     source for the normal ingest steps below).
  3. Move the original binary into `/vault/Attachments/` using the attachment naming convention (`YYYY-MM-DD - Source Title - Attachment Descriptor.ext`, collision-safe) and add
     an Obsidian embed/link to it in the `.md` footer.
- **Telegram image attachments may bypass `Inbox/`.** When the conversation includes image paths such as `/home/hermes/.hermes/profiles/wiki/image_cache/...` and the user asks to ingest/save them, process those images directly even if `/vault/Inbox/` is empty: transcribe each image with vision, copy the original image into `/vault/Attachments/` using the attachment naming convention (`YYYY-MM-DD - Source Title - Attachment Descriptor.ext`, collision-safe), create normalized source archives in `/vault/Sources/` with embeds to the copied attachments, then create/update atomic pages and infrastructure as usual. Do not stop at answering “what I see” if the earlier or current user intent is ingestion into the vault.
- **No subagents/Task tool.** Process sources **sequentially**, one at a time.
- **Direct Telegram text dumps:** when the user sends a long text note and says “Ingest this,” first write the verbatim text to a timestamped `Inbox/YYYY-MM-DD-HHMM-<slug>.md` capture, then run the normal ingest steps. For dense explanatory posts, prefer creating a small cluster of atomic concept/entity pages plus updating the nearest existing related page instead of one monolithic note. Archive the normalized source in `Sources/` with `## Pages Updated`; if the raw Inbox capture is root-owned and must be preserved separately, move it to a collision-safe raw-original path under `Sources/` (for example `Sources/<stem>.inbox-original.md`), not `Notes/Archived Inbox Originals/`, to preserve current archive hygiene. Verify: created/updated note files, source archive, Inbox empty, MOC links, `wiki-index.md` rows, and `wiki-log.md` entry before replying.
- **Source archive naming convention:** whenever creating or renaming a processed source archive in `/vault/Sources/`, use `YYYY-MM-DD - Source Title.md`, where the date is the ingest date (`ingested`, then `created`, then current date) and the title is derived from source metadata/H1/content, not the user's random dump filename. Preserve random/original names in frontmatter as `original_filename: "<old name>"`. Remove unsafe filename characters, collapse spaces, enforce the 200-byte UTF-8 basename cap, and add numeric suffixes for duplicates. Do **not** rename numbered article extracts inside `Sources/<Issue> Articles/`; those preserve reading order. For existing source cleanup, use `/vault/System/scripts/normalize-source-filenames.py --dry-run` then `--apply` after review. See `/vault/System/source-naming-convention.md` and `references/source-archive-naming-convention.md`.
- **Attachment naming convention:** keep binaries/sidecars in `/vault/Attachments/` rather than moving Attachments into `Sources/`. When source relationship is clear, name standalone attachments as `YYYY-MM-DD - Source Title - Attachment Descriptor.ext`; rewrite attachment embeds/links after renames and verify old attachment names return zero matches. Do not rename legacy `Attachment-YYYY...jpg` files that are heavily referenced from read-only `Daily/` notes unless doing an explicit vault-wide migration. See `/vault/System/attachment-naming-convention.md` and `references/attachment-naming-convention.md`.
- **Bare GitHub repo shorthand captures:** when Telegram text is only an `owner/repo` string (for example `langchain-ai/deepagents`), treat it as a repository source, not a generic reflection. Capture the raw text to Inbox, normalize the source URL to `https://github.com/<owner>/<repo>`, fetch GitHub API metadata plus README, create/update a substantive repo/entity note, archive the normalized repo source in `Sources/`, preserve any separate raw Inbox original under `Sources/<stem>.inbox-original.md` only if needed, and verify Inbox emptiness plus exact index/log/MOC matches. See `references/github-repo-shorthand-capture.md`.
- **Full GitHub repo URL captures with tracking params:** when the user sends a full GitHub repo URL (including `?fbclid=...` or other tracking), capture the exact raw URL, normalize a canonical repo URL for fetching, fetch GitHub API metadata + README, dedup against existing repo/entity notes, and update the existing page when present instead of creating a duplicate. Archive the source in `Sources/` with both `source:` (raw URL) and `canonical_url:` (normalized URL), preserve any separate raw Inbox original under `Sources/<stem>.inbox-original.md` only if needed, update MOC/index/log, and verify. See `references/github-repo-url-capture-refresh.md`.
- **Platform/chat error message captures:** when the incoming Telegram text is a short platform/system error (for example `The document is too large or its size could not be verified. Maximum: 20 MB.`), still capture it verbatim to `Inbox/`, but do not create a standalone atomic page for the one-line error. Dedup/search for the relevant operations/setup note, add a concise operational gotcha there, archive the capture to `Sources/` as `type: reflection` with `source: telegram`, update index/log, and verify the Inbox is empty. See `references/platform-error-message-captures.md`.
- **Magazine/newspaper PDF ingest with ads removed:** when the user uploads a full issue PDF and asks to ingest while deleting ads, use PyMuPDF to inspect per-page text previews, identify ad/blank/front/back-matter pages, create a **cleaned no-ads PDF** in `Attachments/`, and create the Markdown source from the same retained pages. Do not keep an uncleaned PDF copy in the vault when the user explicitly asked to delete ads/content. For dense issues, create one issue-level synthesis plus 2-5 durable atomic notes rather than one note per article. Verify the cleaned PDF exists, the uncleaned copy is absent, removed-page/ad text is absent from the source archive, Inbox is empty, and index/log/MOC rows exist. See `references/magazine-pdf-no-ads-ingest.md`.
- **Magazine/newspaper PDF article-folder extraction:** for full The Economist issue PDF uploads, create `/vault/Sources/<Issue Title> Articles/` by default in addition to the issue synthesis/atomic notes; the user expects exhaustive article-level extraction for Economist issues, not only 2-5 distilled pages. Do **not** create new active Economist article folders under `Sources/_cold/`; `_cold` is only for legacy bulk archive material. If older issues or logs mention `Sources/_cold/<Issue Title> Articles/`, migrate active/high-value Economist article folders to `/vault/Sources/<Issue Title> Articles/` and make every issue note/MOC/log path match the actual folder. Also do this whenever the user says to "extract each article into a folder" or asks that each article follow the article template. Create `/vault/Sources/<Issue Title> Articles/` with `00-index.md` plus one Markdown file per article in reading order. Every article file must follow `/vault/System/Templates/Article Template.md` headings (`# Type of post`, `# Rapid fire thoughts`, `# Tags`, `# Headlines`, `# Outline`, `# Intro`, `# Main points`, `# References/ Resources`) and put the faithful extracted article text under `# Main points`. Still remove ads/front/back matter and create a cleaned no-ads PDF in `Attachments/`. **Important MOC expectation:** after article extraction, create or update ingested wiki pages under `/vault/Notes` for every article extract (reuse existing distilled pages where the article is already represented; create draft article-level notes for the rest), then route those `/vault/Notes` pages into the relevant MOC date sections. Never satisfy MOC coverage by linking raw numbered source files such as `[[01-the-world-this-week-politics]]`; raw `Sources/... Articles/NN-...` files are provenance/cold archive only. **Semantic parity expectation:** article-level Notes should match the June 6/June 27 issue style: durable topic/entity titles, source-grounded summaries, and `wiki_status: complete` when sufficiently distilled. Avoid leaving mechanical titles such as `* Economist July 2026`; rename/enhance them before final verification. Verify: every article in `00-index.md` maps to an existing Notes page, each mapped Notes page is linked from the correct MOC, no raw numbered source links remain in readable MOCs, no mechanical issue-suffix draft files remain, folder/file counts, template compliance, ad-text absence, cleaned PDF presence, Inbox emptiness, and wiki-log entry. For full issue coverage, explicitly audit the issue against the June 6th-style section structure: count source sections, confirm all semantic Notes appear in `The Economist MOC`, route every eligible article Note to a section/domain MOC, allow `Letters` to remain issue-indexed unless it has a durable domain theme, and verify newest-first date ordering. The user wants canonical Economist section numbers in the actual MOC filenames (for example `14 Business MOC.md`, not merely `# 14 Business MOC` inside `Business MOC.md`); when maintaining Economist MOCs, preserve numbered filenames and rewrite wikilinks to those targets. See `references/magazine-article-folder-extraction.md`, `references/economist-issue-semantic-note-parity.md`, `references/economist-full-issue-operational-pitfalls.md`, `references/economist-issue-moc-coverage-audit.md`, `references/economist-section-order-and-moc-titles.md`, `references/economist-moc-numbered-filenames.md`, and `references/sources-cold-storage-policy.md`.
- **Reply-to research enhancement:** when the user replies to a prior ingest result and says “add this into the research,” “do deep research,” or asks to build a protocol/routine from an attached image or extra note, treat the new material as a source for the existing target page. Transcribe/copy/archive the image or text source, update the existing note rather than creating a duplicate, add credible research grounding and safety/limitations for advice-like topics, build the requested actionable artifact (routine/checklist/protocol), then update index/log and verify. See `references/research-enhancement-from-reply.md`.
- **Reply image/document attachment to a previous saved text:** when the user says “attach this to the previous text I asked you to save/explain,” do not create an unrelated note. Copy the binary to `Attachments/`, transcribe/analyze it, patch the existing `Sources/` archive with frontmatter attachment + Obsidian embed + transcription/explanation, update any relevant atomic note, then verify attachment/source/note/index/log. See `references/reply-image-attach-to-existing-source.md`.
- **Economic indicators feed routing:** when ingesting The Economist Finance & Economics articles or daily Value Line market notes that mention jobs data, unemployment, wages, CPI/PCE/PPI, Treasury yields, oil prices, consumer sentiment, market breadth, or other macro/daily market indicators, treat them as sources for `Notes/Economic Indicators.md` and cross-link through `MOCs/15 Finance & Economics MOC.md`. Keep the latest article/issue/date entries above older ones in the relevant MOC sections. For uploaded Value Line `Selection & Opinion` PDFs, create a source-aligned PDF attachment, a normalized source archive, a `Stock Market Today <Issue Date>` note, and update `Economic Indicators` + `15 Finance & Economics MOC`; see `references/value-line-selection-opinion-pdf-ingest.md`.
- **Public-company interview/article routing:** when ingesting a public-company transcript or article (for example an After Earnings CEO interview) that discusses growth, margins, valuation, traffic, strategy, automation, or operating model, create/update a substantive company/strategy note rather than a generic transcript note. Cross-link it through `MOCs/14 Business MOC.md` and, when the source has investable public-company implications, through `MOCs/15 Finance & Economics MOC.md` (and `MOCs/Finance MOC.md` if writable). If the company ticker is not already in `System/Stock Watchlist.md` but the source presents a clear thesis, list it in the final summary under `Watchlist candidates (review — not added)`; never edit the watchlist autonomously.
- **After Earnings transcript monitoring:** when the user asks to ingest or monitor `https://www.afterearnings.com/blog/`, fetch the latest Podpage transcript, extract `.blog-post`, write a timestamped transcript source to `/vault/Inbox/`, then let this ingest skill create/update notes and MOCs. For recurring checks, use a silent `no_agent=True` cron script that tracks latest URL/fingerprint in profile state; script paths in `cronjob` must be relative to the profile scripts dir. Verify script behavior with a temporary `/tmp/hermes-verify-*` fixture-based run and report it as ad-hoc verification, not suite green. See `references/afterearnings-transcript-capture.md` and `references/afterearnings-transcript-monitoring.md`.
- **Newsletter inbox ingestion:** the user's dedicated newsletter inbox is `theduy.newsletter@gmail.com`. For newsletter subscriptions, prefer a dedicated IMAP polling capture into `/vault/Inbox/` over the Hermes Email Gateway conversation adapter: the gateway is optimized for human email threads and may ignore bulk/list mail with `List-Unsubscribe`, `Precedence: bulk`, or noreply-style headers. Configure Gmail with a 16-character app password, poll new/unseen messages, save each newsletter as a Markdown source in `Inbox/`, run this ingest, and mark messages seen only after successful capture. See `references/newsletter-imap-ingestion.md`; use `scripts/newsletter_imap_capture.py` as the reusable capture-script template.
  - **Newsletter welcome/admin email routing:** welcome, safelist, subscription-confirmation, and other low-content admin emails should still be archived and removed from `Inbox/`, but usually should not become one atomic page per email. If several admin emails establish a durable feed/network, create or update one feed/entity note (for example a newsletter-network/source-monitoring page), update the relevant source-list/routing note, add `## Pages Updated` to each archived source, and link the feed note from the appropriate Business/Finance/Technology MOCs. Future substantive issues should route to topic/company/indicator notes; short headline/admin messages can remain source-only. See `references/newsletter-welcome-admin-routing.md`.
  - **Substantive newsletter issue routing:** when a daily newsletter issue contains multiple short news items, market tables, policy blurbs, and lifestyle/business snippets, archive it as one newsletter source but triage item-by-item. Create atomic pages only for durable policy/finance/social topics, update `Economic Indicators` for market/rate/oil/jobs/inflation/sentiment signals, update the newsletter-network/source-routing page when the issue teaches future routing, and leave ads/sports/trivia/routine recs source-only unless they connect to an existing durable note. Route pages to their semantic MOC (for example US policy/household-finance items can belong in `06 US Politics & Society MOC`, not just Business/Finance). See `references/newsletter-substantive-issue-routing.md`.
  - **Scrambled-body newsletter captures with online issue links:** if the email body says the provider scrambled the email and only includes a "read it online" URL, do not treat it as low-content/admin. Preserve the original email body in the source archive, fetch/extract the online issue, then apply the substantive newsletter routing above. For Morning Brew / Tech Brew / Brew Markets pages, extracting the `<main>` HTML text after removing script/style/nav/footer boilerplate is usually enough; keep market tables and article sections, skip ads/referral boilerplate, and archive one normalized source with `online_url:` plus `## Pages Updated`. See `references/newsletter-scrambled-online-extraction.md`.
  - **Gmail app-password verification pitfall:** Gmail app passwords are often shown with spaces. If writing them into a shell-sourced `.env`, quote the value (or store the no-space form) so `set -a; . .env` does not treat chunks as commands. Verify IMAP with both exact copied form and no-space form if login fails. If Gmail returns `[AUTHENTICATIONFAILED] Invalid credentials`, remove the bad password from `.env` immediately, keep only non-secret host/email settings, and tell the user to revoke/regenerate the app password for the exact Gmail account with 2FA + IMAP enabled.
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

**Adaptation:** treat infrastructure permissions file-by-file, not as an all-or-nothing
block. If `System/wiki-index.md` is root-owned/unreadable but `System/wiki-log.md` and
the relevant MOC are writable, still update the writable log and MOC, verify them with
exact searches, and report only the index rows as blocked. If a specific MOC is writable
(e.g. `Personal MOC.md`) even while other MOCs are root-owned, update that MOC normally.
Some durable content notes that are normally updated during routing can also be root-owned
(for example `Notes/Economic Indicators.md`); skip only that blocked note update, continue
creating source archives/article notes/MOCs that are writable, and include the exact
`sudo chown hermes:hermes ...` command for the blocked note in the final summary.
Skip only files that are actually unreadable/unwritable in the current run, and include
the exact `chown` command for each blocked infrastructure/content file in the summary. Still
create wiki pages in `Notes/` (usually writable).

### Terminal approval in headless cron
Terminal commands that touch files outside the working directory, delete files, or run
### Terminal approval in headless cron
Terminal commands that touch files outside the working directory, delete files, or run Python scripts may be flagged for **approval** (`pending_approval: true`). In a headless cron job there is no user to approve — these commands may silently fail,
partially execute, or have unpredictable results. **Prefer `write_file` and `patch`
tools over terminal for all file creation and editing.** Use terminal only for
read-only operations (`ls`, `stat`, `rg` searches) and narrow directory-level preservation moves for root-owned Inbox originals when the directory is writable. Avoid `rm` — if you must remove a
file, use `patch` with `replace_all` to empty it, or leave it and note it in the summary.

Do not use `execute_code` for cron wiki ingest batching. In this runtime, arbitrary local Python execution may be approval-blocked in cron; the reliable pattern is explicit `write_file`/`patch` calls for Notes/System/MOC edits, followed by small terminal read-only checks and a single targeted `mkdir -p && mv && test` only when preserving a root-owned Inbox original out of Inbox. When a helper script is still the safest way to generate many files (for example a full issue PDF article extraction), write the script with `write_file` first and then run `python3 /tmp/script.py` via `terminal`; do not embed long shell heredocs in `terminal()`, especially when the script text contains MOC names with `&`, because the foreground command guard can reject the payload as shell backgrounding. See `references/economist-full-issue-operational-pitfalls.md`.

### Root-owned Inbox markdown sources
Markdown captures in `Inbox/` can be owned by `root:root` while the `Inbox/` directory itself is writable by `hermes`. In that case, patching frontmatter may fail or be undesirable, but a directory-level `rename`/move can still work because moving depends on directory permissions, not file ownership.

Safe pattern when `Sources/` is writable:
1. Create a normalized source archive directly in `Sources/<original basename>.md` with `tags: [source]`, source `type`, `source`, `created`, `ingested`, and `## Pages Updated`.
   - For short sources, `write_file` the archive with normalized frontmatter plus the original body.
   - For large root-owned Markdown captures where reconstructing the full body would be error-prone, use a targeted `cp` from `Inbox/` to `Sources/`, then patch only the archive copy's frontmatter / `## Pages Updated`. Do **not** patch the root-owned Inbox original. Verify the archive copy exists and has the expected size/content before moving the original out of Inbox.
2. Preserve the root-owned Inbox original **outside `Notes/`** to avoid polluting the wiki graph. Prefer a collision-safe filename in `Sources/`, e.g. `Sources/<original stem>.inbox-original.md`, after the normalized archive exists. Do not recreate `Notes/Archived Inbox Originals/`; current archive hygiene treats raw originals under `Notes/` as a lint issue.
3. Verify three facts explicitly: the Inbox original is absent, the normalized `Sources/<original basename>.md` archive exists, and the preserved raw original exists at its `Sources/*.inbox-original.md` path.
4. Mention the preservation path in the final summary, but do **not** call this a Notes fallback if the canonical source archive was successfully written to `Sources/`.

Safe pattern when `Sources/` is blocked or a move/write to `Sources/` fails:
1. Create `Notes/<Source Title> Source.md` with `ingested: YYYY-MM-DD` and `## Pages Updated` only as the documented fallback.
2. Move the root-owned Inbox original out of `Inbox/` if directory permissions allow. If `Sources/` is blocked, use the least-bad collision-safe preservation location available and report it explicitly; avoid `Notes/Archived Inbox Originals/` unless there is no writable non-Notes option.
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
copy's normalized frontmatter and `## Pages Updated`, then move/preserve the raw Inbox
original outside `Notes/`, preferably as a shortened `Sources/*.inbox-original.md` file.
Verify: Inbox absence, `Sources/` archive presence, preserved-original presence, and exact
index/log/MOC matches before summarizing.

### Verify infrastructure edits by searching exact new artifacts
After updating `System/wiki-index.md`, `System/wiki-log.md`, or MOCs, verify with an exact search for the new page/source title, not just by trusting a write succeeded. When patching index rows, do not assume the row's tag/type text from memory; first inspect the actual neighboring row or use an exact old_string from the current file. If the exact artifact is missing after a broad rewrite, patch it in with a small targeted replacement and verify again.

**Append-only infrastructure preservation:** never use `write_file` to rewrite `System/wiki-log.md`, `System/wiki-index.md`, or MOCs from a partial/paginated read. For log appends, read the tail and use a targeted `patch` that replaces the final known line/block with itself plus the new entry. If a partial rewrite accidentally truncates an infrastructure file and `/vault` is a git repo, recover from `git -c safe.directory=/vault -C /vault show HEAD:<path>` before re-applying the new entry. See `references/infrastructure-log-recovery.md`.

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
When using the root-owned Inbox markdown safe pattern, a directory-level `mv` out of `Inbox/` can succeed even though file patching would be undesirable. After the move, verify both sides explicitly: the original basename is absent from `Inbox/` and the preserved raw original is present at the chosen non-Inbox path. If `Sources/` is writable, prefer `Sources/<stem>.inbox-original.md` instead of any `Notes/Archived Inbox Originals/` path, because raw archives under `Notes/` violate current archive hygiene. Report this preservation path in the final summary.

### Legacy `Notes/Archived Inbox Originals/` cleanup requests
When the user asks whether `Notes/Archived Inbox Originals/` can be removed or asks to clean it up, treat it as archive hygiene rather than normal ingest:
1. First verify whether `/vault/Notes/Archived Inbox Originals/` exists and inventory it if present.
2. If absent, do not attempt a destructive delete; report that it is already gone.
3. If present, only delete after every contained file is verified as duplicated in `Sources/` or `Attachments/`; move any unique raw original to `Sources/<stem>.inbox-original.md` first.
4. Clean living-note references that describe the folder as an active/current preservation path, replacing them with current `Sources/*.inbox-original.md` policy language.
5. Leave historical `System/wiki-log.md` mentions alone unless the user explicitly asks to normalize logs; they are audit history, not active guidance.
6. Verify with exact file/content searches under `Notes/`: no folder remains, and any remaining mentions are clearly marked as legacy/historical.

### Duplicate source captures already represented in the wiki
When an Inbox markdown source is a duplicate of an already-ingested source/page, do not update the substantive wiki note or create a second atomic page just to clear Inbox. Instead:
1. Confirm the duplicate by checking the existing note and/or source archive (for example, same title/body in `Notes/<page>.md` and `Sources/<source>.md`).
2. Create a normalized duplicate archive in `Sources/<current Inbox basename>.md` with source frontmatter, `ingested: YYYY-MM-DD`, a `duplicate_of: "[[Existing Source]]"` field when an existing source archive is known, and `## Pages Updated` saying no page changed because the content was already represented.
3. If the Inbox file is root-owned, preserve the raw original as `Sources/<current stem>.inbox-original.md` via directory-level move after the normalized duplicate archive exists. Do not patch the root-owned Inbox original.
4. Append a `wiki-log.md` entry with `Created: None`, `Updated: None — duplicate of ...`, `MOCs touched: None`, and the archive/preservation path.
5. Verify the Inbox file is absent, both archive files are present when applicable, the existing note still exists, and the exact wiki-log entry is searchable.

### Direct Telegram image ingest pattern
When processing image attachments that are not present as files under `/vault/Inbox/`:
1. Treat the image-cache paths from the conversation as the raw sources.
2. Use `vision_analyze` on each image with a faithful-transcription prompt; preserve tables, highlighted text, dates, and headings.
3. Copy each original image to `/vault/Attachments/` with descriptive, collision-safe basenames. Avoid generic `img_*.jpg` names in the vault.
4. Group related pages into source archives under `/vault/Sources/` when they are parts of the same handout/document (for example page 1/page 2 of a checklist), and include Obsidian embeds for every copied attachment.
5. Create/update typed atomic notes in `/vault/Notes/`, link them to related existing pages/MOCs, then update `wiki-index.md` and `wiki-log.md`.
6. Verify exact note files, source archives, attachment copies, MOC links, and index/log rows before finalizing.
