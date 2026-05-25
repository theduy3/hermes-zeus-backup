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

## Verification checklist
- Re-read all 20 enhanced pages, not just a sample, and confirm frontmatter still parses, `updated` is the run date, `wiki_status` is appropriate, and new links are present.
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
