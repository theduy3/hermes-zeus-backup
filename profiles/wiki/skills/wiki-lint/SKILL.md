---
name: wiki-lint
description: Health-check and enhance 20 theduyvault wiki pages per run. Scheduled headless job.
version: 1.0.0
metadata:
  hermes:
    requires_toolsets: [terminal, file]
    tags: [vault, wiki, lint, theduyvault]
---

# wiki-lint — wiki health check + enhancement (headless, batch 20)

You are running as a scheduled cron job. Run fully autonomously: no confirmation
prompts, no questions.

## Canonical instructions
Read and follow **`/vault/.claude/commands/wiki-lint.md`** with **batch size 20**
(scan for orphans, sparse frontmatter, MOC gaps, missing cross-references, stale
pages, contradictions; then enhance up to 20 pages, prioritizing high-issue and
high-inbound-link pages).

## Runtime adaptations (this environment)
- Vault is at **`/vault`**. Edit pages under `/vault/Notes`, MOCs under `/vault/MOCs`,
  and update `/vault/System/wiki-index.md` + append one entry to
  `/vault/System/wiki-log.md`.
- **No subagents/Task tool.** Do the scan and the enhancement **sequentially**.
- **Search:** no qmd here — use `rg` over `/vault/Notes` and `/vault/MOCs` for the
  scan (orphans, missing links, MOC membership).
- Process exactly **20** pages this run (the schedule advances the batch by `updated`
  date over successive runs). Use terminal (`rg`/`ls`) + file (read/edit) tools.
- Before counting orphan pages, filter out intentional infrastructure/date/system pages and cross-check apparent misses against `/vault/System/wiki-index.md` + MOCs.
- When the run touches root-owned infrastructure or notes, follow the exact replace
  recipe in `references/root-owned-workflow.md` instead of retrying in-place writes.
- Batch ordering and orphan filtering details live in `references/batch-and-orphan-filtering.md`.
- For an efficient sequential implementation pattern (Python scanner/editor, index regeneration, log append, and exact verification checks), see `references/automation-and-verification-pattern.md`.
- For cron-specific pitfalls around unreadable root-owned files and semantic related-link verification, see `references/cron-permission-and-semantic-verification.md`.
- For post-edit verification/log repair after semantic cross-link cleanup, see `references/post-verification-log-and-index-repair.md`.
- For sparse pages where the numeric 2-link rule would force misleading related links, see `references/semantic-low-outbound-repair.md` and prefer honest unresolved low-outbound reporting over unrelated cross-links.
- For final verification after semantic cleanup, use the list-aware frontmatter/counting cautions in `references/frontmatter-parser-and-semantic-cleanup-verification.md` so YAML list fields do not create false sparse-frontmatter counts.
- If a direct `/vault/Notes/*.md` page is unreadable during a cron scan, skip and report it unless it is explicitly selected for editing; do not let one permission error abort the batch. If sparse captures got weak forced links, remove them, rewrite the same-day log entry, and verify the honest non-zero low-outbound count. See `references/unreadable-notes-and-semantic-cleanup-2026-06-20.md`.
- After any automated related-link fill, inspect all 20 touched pages for weak `## Related` sections, remove broad/generic/MOC-substitute links, regenerate the index, rewrite the same-day log entry, and report honest low-outbound counts. See `references/semantic-cleanup-after-automated-linking.md`.
- After automated MOC fill, semantically review newly added MOC destinations and sections; broad tag overlap can place pages into misleading MOCs even when page verification passes. Move pages to the narrowest correct domain MOC/section before final verification. See `references/moc-semantic-placement-review-2026-07-03.md`.
- Treat generic overlap tags such as `ai`, `source`, `reference`, `knowledge-management`, `personal-development`, `video`, `youtube`, `github`, and `to-review` as insufficient evidence for related links. Do not let a verifier pass merely because it reports 2 outbound links; reread the actual low-content pages and remove links whose target is not a close subject neighbor.
- For source fallback pages with `## Pages Updated` sections and sparse captures where no close domain neighbor exists, count existing source-to-page links as semantic and leave unclear captures honestly low-outbound rather than forcing unrelated links. See `references/source-fallback-and-sparse-capture-semantic-cleanup-2026-07-01.md`.
- If fewer than 20 structural issue-bearing pages remain, still process exactly 20 readable pages by filling from the oldest `updated` rolling-refresh queue; keep the wiki-log consistent with post-run low-outbound counts. See `references/exactly-20-and-log-consistency.md`.
- For cron-safe fallback scripts that do not rely on optional Python packages, see `references/dependency-free-cron-scanner.md`.
- For the critical distinction between direct wiki pages and nested operational subtrees under `/vault/Notes`, plus cleanup if a recursive scan accidentally touches nested logs/ADR files, see `references/direct-notes-scope-and-semantic-link-guard.md`. This reference also records the semantic guard against adding generic high-inbound links merely because tags overlap.
- For cron index parity when direct notes are unreadable, final page_count/index-row verification, conservative fallback rows, and avoiding shell-guard false positives from ampersands inside heredoc Python, see `references/cron-index-and-shell-guard-2026-07-06.md`.
- If any referenced helper file is missing in the runtime vault, do not stop the cron job. Fall back to a self-contained `/tmp/wiki_lint_run.py` script that: scans `/vault/Notes` + `/vault/MOCs`, selects exactly 20 issue-bearing pages by oldest/missing `updated`, writes via root-owned-safe replacement, regenerates `System/wiki-index.md`, appends one `wiki-log.md` entry, and prints a JSON verification report. Prefer stdlib-only parsing/writing unless the script verifies optional dependencies first.
- If a lint script crashes after mutating pages but before final verification/logging, recover from disk rather than rerunning a fresh batch: identify the touched 20 pages, clean weak links and MOC placement, regenerate the index, append or rewrite exactly one same-day log entry, and verify the original batch. See `references/partial-run-crash-recovery-and-unreadable-mocs-2026-07-04.md`.
- When loading MOCs during cron scans or post-edit verification, wrap each MOC read in `try/except PermissionError`; unreadable root-owned MOCs should be skipped and reported with the exact `chown` command, not allowed to abort the run after page edits. See `references/partial-run-crash-recovery-and-unreadable-mocs-2026-07-04.md`.
- Some imported notes contain conflict-style frontmatter artifacts such as `>> NEW >>` / `<< OLD <<`. When linting those pages, normalize frontmatter by preserving canonical fields only (`tags`, `type`, `created`, `updated`, `sources`, `wiki_status`, plus useful metadata like `title`/`source`) and remove those artifacts from the YAML block before verification.
- After automated related-link or MOC fill, inspect every touched page's actual `## Related` entries and MOC placement, not just counts. Treat MOC links in Related sections and broad tag-overlap links (`ai`, `ai-agents`, `finance`, `tools`, `research`, `developer-tools`, `source`, `github`, `video`) as suspect unless the page title/body shows a close subject relationship. If semantic cleanup happens after the first run, regenerate the index, rewrite the same-day lint log entry, and rerun exact-20 verification. See `references/semantic-review-and-log-rewrite-2026-07-05.md`.
- When touching MOCs, ensure contiguous date-heading sections are sorted newest-first across all readable MOCs (for example `July 4th 2026`, then `June 27th 2026`, then `June 6th 2026`). Sort only date runs, preserve section bodies verbatim, skip unreadable root-owned MOCs with a `chown` fix, and verify all readable MOCs after edits. See `references/moc-date-section-ordering.md`.
- When the user says notes have excessive blank space or are hard to read, run a formatting-only whitespace cleanup. For `/vault/Notes/`, clean direct note pages. If the user asks for “all other folders as well,” also clean Markdown in writable wiki folders `MOCs/`, `Sources/`, and `System/`. Skip `Inbox/` raw captures, `Attachments/` binaries, and read-only `Daily/`/`Tasks/`. Strip trailing spaces/tabs, convert whitespace-only blank lines (including Unicode whitespace) to empty lines, collapse 3+ newlines to one visible blank line, preserve a final newline, and verify zero remaining whitespace issues. See `references/notes-whitespace-cleanup.md` and `references/vault-markdown-whitespace-cleanup.md`.

## Verification checklist
- Re-read all 20 enhanced pages, not just a sample, and confirm frontmatter still parses, `updated` is the run date, `wiki_status` is appropriate, and new links are present.
- Confirm enhanced pages' frontmatter contains no merge/conflict artifacts such as `>> NEW >>` or `<< OLD <<`.
- Spot-check auto-added cross-reference sentences for semantic relevance; if a heuristic picks unrelated pages, replace them with closer domain neighbors before final verification.
- After regenerating the index, verify `updated` and `page_count` in the header and confirm all 20 batch titles have index rows.
- Verify exactly one wiki-log entry was appended for the run.
- Keep the run bounded to 20 pages; log the remainder as pending work rather than silently expanding scope.

## Pitfall: Root-owned files block writes

Some vault files may be owned by `root` (from prior Docker/migration runs). All write
tools (`write_file`, `patch`, Python `open()`, `sed -i`) fail with `Permission denied`
on these files even though the `hermes` user owns the parent directory.

**Detection**: `stat -c '%U' /vault/Notes/<file>.md` returns `root`.

**Workaround for Notes/ files**: Delete the root-owned file (allowed because the
directory is hermes-owned), then write new content (the new file will be hermes-owned):
```bash
rm "/vault/Notes/Page Name.md"
# Then write new content via terminal Python script
```

**Workaround for System/ files** (wiki-index.md, wiki-log.md): Use cp to replace:
```bash
# Copy updated version over root-owned original
cp --remove-destination /tmp/wiki-index-updated.md /vault/System/wiki-index.md
```

**Bulk fix** (optional — not required per run): `cp --remove-destination` on each
root-owned file will re-create it as hermes-owned. Note: `cp file file` (same path)
is detected as no-op by GNU cp; instead use a two-step move via /tmp or a different
approach.

**Write strategy**: Write enhanced pages using a Python script saved to `/tmp/`,
executed via `terminal`. The script uses `open(path, 'w')` — works on hermes-owned
files and newly created files. For root-owned files, delete first then write.
