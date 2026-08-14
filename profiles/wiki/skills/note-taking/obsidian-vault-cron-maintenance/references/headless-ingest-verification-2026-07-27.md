# Headless newsletter ingest verification notes — 2026-07-27

This run processed two scrambled newsletter captures (Tech Brew `Open weight gets heavy`, Brew Markets `Back to the futures`) and exposed two reusable verification lessons for cron vault jobs.

## Patch contamination recovery
- A malformed `patch` replacement inserted JSON/tool-call residue (`}},{`) into YAML frontmatter.
- Correct response: stop normal edits, repair the exact polluted scalar with a narrow patch, then exact-search the touched vault for the distinctive residue and validate frontmatter delimiters on every touched source/note before finalizing.
- Do not assume a successful patch means the replacement text was semantically clean; inspect the diff returned by every patch that touches YAML or infrastructure tables.

## Infrastructure verification without misleading git diff
- `git diff --stat` against `/vault` may show huge unrelated infrastructure churn when the repository baseline is stale or older than recent cron jobs.
- Treat broad git diff as a sanity check only. For final verification, prefer exact searches for:
  - new note filenames under `Notes/`
  - normalized source archives and `.inbox-original.md` files under `Sources/Newsletter/`
  - exact `wiki-index.md` rows and page_count
  - exact `wiki-log.md` headings
  - exact MOC links for each created page
  - Inbox emptiness
- If a broad diff looks huge, do not rewrite infrastructure from HEAD or from a partial read unless there is proven truncation. Verify current artifacts directly.

## Newsletter routing pattern from this run
- Scrambled online issue URLs can work directly; inspect extracted text before deriving fallback slugs.
- Create atomic pages only for durable mechanisms: open-model cyberdefense governance, AI chat/artifact share-link leakage, Chinese DRAM IPO shock, IPO issuance as bubble signal, retail single-stock futures leverage.
- Update existing notes for extension-only items: event-cinema scarcity, smart-glasses privacy delay, AI infrastructure circular financing, economic indicator tables.
