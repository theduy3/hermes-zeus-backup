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
- For exact-20 cron runs that include low-context captures or source fallback pages, leave pages honestly low-outbound rather than forcing generic links, count source-to-page provenance links as meaningful for fallback sources, semantically review MOC placement after tag-based fills, and avoid `execute_code` in cron verification helpers. See `references/semantic-cleanup-low-context-and-cron-2026-07-07.md`.
- When touching MOCs, ensure contiguous date-heading sections are sorted newest-first across all readable MOCs (for example `July 4th 2026`, then `June 27th 2026`, then `June 6th 2026`). Sort only date runs, preserve section bodies verbatim, skip unreadable root-owned MOCs with a `chown` fix, and verify all readable MOCs after edits. See `references/moc-date-section-ordering.md`.
- When the user says notes have excessive blank space or are hard to read, run a formatting-only whitespace cleanup. For `/vault/Notes/`, clean direct note pages. If the user asks for “all other folders as well,” also clean Markdown in writable wiki folders `MOCs/`, `Sources/`, and `System/`. Skip `Inbox/` raw captures, `Attachments/` binaries, and read-only `Daily/`/`Tasks/`. Strip trailing spaces/tabs, convert whitespace-only blank lines (including Unicode whitespace) to empty lines, collapse 3+ newlines to one visible blank line, preserve a final newline, and verify zero remaining whitespace issues. See `references/notes-whitespace-cleanup.md` and `references/vault-markdown-whitespace-cleanup.md`.
- After any exact-20 cron autolink run, perform a semantic repair pass before final reporting: remove MOC links from `## Related`, remove broad-tag-only links, keep honest low-outbound counts instead of forcing replacements, review MOC placement for stale/wrong tags, regenerate the index, and rewrite the same-day log entry. See `references/semantic-repair-after-cron-autolink-2026-07-08.md`.
- For Economist-heavy lint batches, preserve numbered Economist MOC filenames, keep active/high-value sources directly under `/vault/Sources/` (not `_cold`), keep binaries in `/vault/Attachments/`, and treat source issue links as valid provenance while still removing MOC links and token-collision links from `## Related`. See `references/semantic-review-economist-related-links-2026-07-09.md`.
- After semantic cleanup, do not make verification fail solely because sparse/low-context pages remain honestly low-outbound; remove weak forced links, regenerate the index, rewrite the same-day log entry, and ensure post-repair issue counts use the canonical scanner semantics rather than a naive corpus count. See `references/semantic-repair-and-log-count-consistency-2026-07-10.md`.
- For exact-20 batches where the first automated pass numerically satisfies outbound counts by adding MOC links or broad/token-collision links, run a separate semantic repair pass: print every touched page's `## Related`, remove all `[[... MOC]]` entries and unrelated generic links, add only close same-domain siblings when available, then regenerate the index, rewrite the same-day lint log, and reverify exact-20. Low-context clippings may remain honestly low-outbound. See `references/semantic-repair-low-context-and-moc-related-2026-07-11.md`.
- After exact-20 cron runs, also inspect newly added MOC destinations, not just page `## Related` sections: remove broad tag-driven placements, move personal/contact/language stubs to `Personal MOC`, place politics clippings in a narrow politics/international section with explanatory text, remove MOC-substitute links/prose from note bodies, then regenerate the index, rewrite exactly one same-day log entry, and rerun final verification. See `references/semantic-moc-repair-and-finalize-2026-07-12.md`.
- When semantic cleanup raises the low-outbound count, that is acceptable if the removed links were weak. Country-only, section-only, publication-only, or broad-tag-only links (`ai`, `research`, `marketing`, `management`, `business`, `finance`, `economist`, region tags, etc.) are not valid `## Related` evidence. Re-read all 20 touched pages, remove weak links, add replacements only for close subject neighbors, then regenerate the index, rewrite exactly one same-day log entry, and verify exact-20. See `references/semantic-repair-2026-07-13.md`.
- After a cron lint run, if the first automated pass numerically succeeds but produces weak `## Related` links, run a separate semantic repair pass before final reporting: print/re-read every touched page's actual Related section, search by distinctive subject terms rather than broad tags, leave sparse captures honestly low-outbound when no close neighbor exists, regenerate the index, rewrite the same-day lint log, and prefer canonical `wiki-health.py` counts in the report when available. Use terminal-run Python helpers in cron if arbitrary code helpers are blocked by approval policy. See `references/semantic-repair-and-cron-tooling-2026-07-14.md`.
- For final cron verification consistency, be careful with wikilink regex capture groups when optional embed markers are present (`(!?)\[\[([^\]]+)\]\]` means the target is group 2, not group 1); a capture-group mismatch can falsely mark all pages as MOC gaps. After semantic repair, rerun canonical `System/scripts/wiki-health.py`, rewrite the same-day log with canonical counts, and re-read selected pages for broken links. See `references/cron-final-verification-consistency-2026-07-15.md`.
- After broken-link or semantic Related cleanup, inspect frontmatter source links as well as body links: canonical `wiki-health.py` counts `[[...]]` inside YAML `sources:` fields. If a source wikilink has no real page and no correct target, preserve the provenance as plain text/URL rather than creating dummy pages; also remove empty `## Related` headings left by cleanup. Regenerate the index, rewrite exactly one same-day log entry, and verify all 20 pages. See `references/frontmatter-source-link-and-empty-related-cleanup-2026-07-16.md`.
- For newly indexed business/operational pages selected by exact-20 lint, search by distinctive title/body terms before adding Related links; broad tags like `ai`, `business`, `marketing`, or `startup` can otherwise create weak links. Remove source/provenance-only Related entries after broken-link cleanup, move SalonX/nail-salon notes to `Personal MOC` → `Business & Salon` rather than generic date buckets, then regenerate index/log and verify all 20 again. See `references/semantic-repair-salonx-and-source-related-2026-07-17.md`.
- When fixing broken outbound links in exact-20 batches, distinguish close note aliases from source/provenance-only targets: repoint aliases to real note basenames, but convert source-only dangling wikilinks to plain provenance text instead of creating dummy pages. After semantic cleanup, regenerate the index with list-aware tag parsing so YAML `tags:` list items do not leak literal dashes into index rows, then verify all 20 touched pages and exactly one same-day lint log entry. See `references/source-only-broken-link-repair-and-index-tags-2026-07-18.md`.
- When normalizing wikilink targets in scanners/verifiers, do not use `Path(target).stem` on titles because dotted/versioned page names like `Claude Opus 4.6 Operator Guide` get truncated to `Claude Opus 4`. Strip aliases/headings, remove only a literal `.md` suffix, then remove folder prefixes. See `references/dotted-wikilink-target-normalization-2026-07-19.md`.
- After the first exact-20 lint mutation, freeze the selected titles and use that same list for every repair, verification, index regeneration, and log rewrite. Do not rerun a selector/mutator helper after repairs, because lowered issue counts can cause a second rolling batch to be touched in the same cron run. When touched pages have polluted `tags:` values such as URLs, `[[wikilinks]]`, or `none`, move useful provenance into quoted `sources:` entries, keep only semantic tags, regenerate the index, and verify the frozen batch. See `references/exact-20-batch-freeze-and-tag-pollution-repair-2026-07-20.md`.
- When a custom lint selector reports counts that conflict with `System/scripts/wiki-health.py`, treat `wiki-health.py` as canonical for vault-wide health and label custom counts as selected-batch candidates only. Custom scanners commonly over-count orphans if they ignore MOC/index semantics. After semantic cleanup, rewrite the same-day log with canonical health plus frozen-batch verification. See `references/canonical-health-vs-custom-selector-2026-07-21.md`.
- When only a few structural issue-bearing direct Notes pages remain, freeze those plus the oldest rolling-refresh fill to exactly 20, then use that same frozen list for semantic cleanup, index regeneration, log rewrite, and final verification. Removing weak Related links can leave sparse/source pages honestly low-outbound; report that instead of forcing unrelated links. See `references/rolling-refresh-semantic-cleanup-2026-07-22.md`.

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
