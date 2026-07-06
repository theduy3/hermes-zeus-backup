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
- After automated related-link insertion, print and inspect the batch `## Related` / `Related:` lines before final reporting; remove weak forced links and rewrite the same-day log/index if needed. See `references/semantic-repair-after-auto-linking-2026-06-21.md`, `references/semantic-cleanup-and-log-repair-2026-06-22.md`, and `references/semantic-cleanup-low-context-captures-2026-06-23.md`.
- When regenerating `System/wiki-index.md`, normalize empty list headers so `None` never appears as a rendered tag, and bound `## Related` inspection at the next heading or horizontal rule so source-body text is not mistaken for related links. See `references/index-tag-normalization-and-related-section-bounds-2026-06-24.md`.
- If semantic cleanup removes auto-added links from sparse captures, rerun verification from the edited files and report the honest non-zero low-outbound count instead of preserving the pre-cleanup success count. For empty or minimal captures, add only honest stub context/title if needed; do not invent source content or force broad-tag links. If cleanup increases the post-run low-outbound count, treat that as correct quality control, regenerate the index, and rewrite the same-day log entry to match the verified state. See `references/semantic-cleanup-honest-low-outbound-2026-06-25.md`.
- If a direct `/vault/Notes/*.md` page is unreadable during a cron scan, skip and report it unless it is explicitly selected for editing; do not let one permission error abort the batch. If sparse captures got weak forced links, remove them, rewrite the same-day log entry, and verify the honest non-zero low-outbound count. See `references/unreadable-notes-and-semantic-cleanup-2026-06-20.md`.
- If fewer than 20 structural issue-bearing pages remain, still process exactly 20 readable pages by filling from the oldest `updated` rolling-refresh queue; keep the wiki-log consistent with post-run low-outbound counts. See `references/exactly-20-and-log-consistency.md`.
- For cron-safe fallback scripts that do not rely on optional Python packages, see `references/dependency-free-cron-scanner.md`.
- For the critical distinction between direct wiki pages and nested operational subtrees under `/vault/Notes`, plus cleanup if a recursive scan accidentally touches nested logs/ADR files, see `references/direct-notes-scope-and-semantic-link-guard.md`. This reference also records the semantic guard against adding generic high-inbound links merely because tags overlap.
- If any referenced helper file is missing in the runtime vault, do not stop the cron job. Fall back to a self-contained `/tmp/wiki_lint_run.py` script that: scans `/vault/Notes` + `/vault/MOCs`, selects exactly 20 issue-bearing pages by oldest/missing `updated`, writes via root-owned-safe replacement, regenerates `System/wiki-index.md`, appends one `wiki-log.md` entry, and prints a JSON verification report. Prefer stdlib-only parsing/writing unless the script verifies optional dependencies first.
- Some imported notes contain conflict-style frontmatter artifacts such as `>> NEW >>` / `<< OLD <<`. When linting those pages, normalize frontmatter by preserving canonical fields only (`tags`, `type`, `created`, `updated`, `sources`, `wiki_status`, plus useful metadata like `title`/`source`) and remove those artifacts from the YAML block before verification.
- If semantic inspection removes weak heuristic links and raises the verified low-outbound count, preserve that honest count, regenerate the index, and rewrite the same-day log from final edited files. See `references/semantic-cleanup-honest-low-outbound-2026-06-26.md`.
- When verifying low-outbound counts after cleanup, count only outbound links to direct `/vault/Notes/*.md` pages. MOC links such as `[[Personal MOC]]` are useful navigation but do not satisfy the 2-note cross-reference rule. See `references/semantic-cleanup-and-moc-link-counting-2026-06-27.md`.
- If the run creates or edits helper code/scripts (for example `/tmp/wiki_lint_run.py`, `/tmp/wiki_lint_cleanup.py`, or targeted patch scripts), finish with a disposable `/tmp/hermes-verify-*.py` ad-hoc verifier that compiles changed scripts and checks final note/index/log behavior. Remove the verifier after running and report it as targeted ad-hoc verification, not a canonical suite pass. See `references/ad-hoc-verification-after-helper-script-edits-2026-06-28.md`.
- When semantic cleanup removes weak related links, scope verifier assertions to the exact pages/line occurrences cleaned up; do not globally ban a linked title that may be legitimate elsewhere. Preserve honest low-outbound counts when pages have only MOC links or no direct note links. See `references/semantic-cleanup-verifier-scoping-2026-06-29.md`. 

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
