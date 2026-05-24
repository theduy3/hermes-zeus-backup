---
name: obsidian-csv-import-ingest
description: Process Obsidian Inbox/CSV import captures into the wiki by identifying URL-backed shells, archiving source files, creating Notes pages, and updating MOCs/index/log.
---

# Obsidian CSV Import Ingest

Use this when the vault has many files in `Inbox/CSV import/` that came from a CSV import and need to be turned into proper wiki entries.

This workflow is specific to the user's LLM-wiki-style Obsidian vault at `/Users/theduy/theduyvault`.

## What makes these files special

CSV-imported files are often thin shells with frontmatter-like fields such as:
- `Name:`
- `Created time:`
- `Highlights:`
- `URL:`
- `Archived:`

Important finding: many recent files have little or no body content, so the real signal is usually the `URL:` field, not the body text.

## Orientation first

Before ingesting, read:
1. `theduyvault/CLAUDE.md`
2. `System/wiki-index.md`
3. `System/wiki-log.md`
4. relevant MOCs you expect to touch

Follow the vault rule that `Inbox/` is immutable in principle, but in practice processed raw captures from `Inbox/CSV import/` have been archived by moving them into `Sources/` during ingest. Preserve original filenames when archiving.

## Discovery workflow

1. Inspect `Inbox/CSV import/`.
2. Expect a very large backlog; process in batches, not all at once.
3. Use a script/terminal pass to identify candidates with non-empty `URL:` values.
4. Prefer the most recent URL-backed captures first.
5. Skip empty shells unless the title clearly matches an already-known source worth promoting.

Example terminal pattern:
- scan files in `/Users/theduy/theduyvault/Inbox/CSV import`
- parse `URL:` line
- sort by modification time descending
- review the latest candidates

## Selection heuristics

Good candidates:
- non-empty `URL:`
- recent mtime
- specific title
- likely fit with existing domains (AI tools, Claude Code, finance, automation, Obsidian workflows, knowledge management, etc.)
- non-social sources with enough substance to produce a durable note

Low-value candidates:
- generic Facebook links with no usable context
- Reddit links when `web_extract` cannot scrape them reliably
- empty shells with blank URL
- image-only placeholders
- one-off commerce/listing pages unless they support an existing research thread
- duplicate topics already processed unless the new source materially adds information

Important extractor finding:
- `web_extract` works well for GitHub repos and many normal sites
- Reddit often fails with "Website Not Supported", so skip or defer Reddit-backed CSV imports unless you want to handle them another way
- webinar landing pages and marketing pages are usually still usable, but should be summarized as claims/framing rather than treated like high-confidence research

Practical prioritization rule discovered in later batches:
- when the backlog is large, prefer non-social, reusable sources first
- favor sources that can become enduring concept/entity notes over ephemeral news or product listings
## Ingest steps

For each selected item:

1. Read the source shell from `Inbox/CSV import/`.
2. Search `Notes/`, `Sources/`, and `System/wiki-index.md` for possible existing coverage before creating anything new.
   - Important: sometimes there is already a rough or legacy note (for example, a note with title/source but weak frontmatter). In that case, upgrade the existing note instead of creating a duplicate.
3. Fetch the URL with `web_extract` to get actual content.
4. Synthesize a proper source note in `Sources/` using the original filename.
   - add source frontmatter
   - set `created` and `ingested`
   - keep the original filename
5. Move the raw capture from `Inbox/CSV import/` to `Sources/` using `mcp_obsidian_fs_move_file`.
6. Overwrite the moved file in `Sources/` with the cleaned-up archived source content if needed.
7. Create a corresponding wiki page in `Notes/`, or upgrade an existing rough note instead of creating a duplicate.
   - include full frontmatter: `tags`, `type`, `created`, `updated`, `sources`, `wiki_status`
   - use only valid wiki `type` values for `Notes/`: `entity`, `concept`, `comparison`, or `synthesis`
   - do not use `type: source` in `Notes/`; source pages belong in `Sources/`
   - add at least 2 internal links
   - connect it to relevant existing pages/MOCs
8. If the CSV title is generic (for example `GitHub Link`) or awkward, keep the original filename only for the archived file in `Sources/`, but give the `Notes/` page a clear semantic title.
9. Update the relevant MOCs.
10. Update `System/wiki-index.md` page count and add rows for new or upgraded notes.
11. Append an ingest entry to `System/wiki-log.md`.

## Additional findings from later batches

- Generic CSV-import filenames are common. A reusable pattern is:
  - archive the raw source under its original filename in `Sources/`
  - create a clearer `Notes/` title such as `Obsidian Homepage Dashboard` or `WassupJay N8N Free Templates Repository`
- Existing notes can be improved in place. Example: `Anthropic Prompt Engineering Tutorial` already existed and was promoted to a full wiki note rather than duplicated.
- Webinar and landing-page sources are often better represented as concept/entity notes that summarize the framing or claims, not as literal source-typed notes inside `Notes/`.
- When a source is mostly marketing framing, say so explicitly in the note so the wiki preserves the right confidence level.
- Generic source captures can still produce durable wiki notes if the underlying URL is substantive. Examples from later batches included:
  - beginner Obsidian onboarding guides
  - Zettelkasten workflow explainers
  - Notion-to-Obsidian migration instructions
  - investment/webinar pages recast as finance concepts or claim summaries
- A useful pattern for finance or market pages is to create:
  - one durable synthesis note for the core idea or framing
  - optionally one lighter note that preserves the source title when the title itself may be useful for later recall
- Another strong pattern discovered in later finance batches: if several adjacent CSV-import items are really multiple explainers on the same concept, combine them into one higher-quality synthesis note instead of creating one wiki page per source. Example: multiple dark-pool articles were combined into `Dark Pool Trading Market Structure` with several entries in the `sources:` list.
- When one URL resolves badly or redirects to generic hub content, still archive it to `Sources/`, but mark it clearly as a partial/failed capture and rely more heavily on the better extracted companion sources for the synthesis note.
- For finance concepts, useful clustering heuristics include:
  - market structure topics (for example dark pools, payment for order flow, execution quality)
  - cross-asset macro topics (for example intermarket relationships)
  - investor decision frameworks (for example lump sum vs DCA)
  These clusters often make better permanent notes than preserving each article as a separate wiki page.

## MOC routing patterns discovered

Use these common placements when the topic fits:

- `MOCs/AI Development MOC.md`
  - Claude Code & Tooling
  - AI Coding & Workflows
  - AI Products & Applications
- `MOCs/AI Agent Tooling MOC.md`
  - Core Agent Frameworks
  - AI Trading Agents
- `MOCs/Finance MOC.md`
  - AI Trading Tools
  - Market Research & Strategy

## Batch size guidance

Do not try to process the whole folder in one pass when there are hundreds of files.
A good batch is around 5 recent URL-backed captures.
This keeps MOC/index/log updates manageable and avoids mass-changing the vault without explicit user direction.

## Verification checklist

Before finishing:
- confirm Inbox copy no longer exists for processed items
- confirm archived copy exists in `Sources/`
- confirm wiki pages exist in `Notes/`
- confirm MOCs contain the new wikilinks
- confirm `System/wiki-index.md` page count increased correctly
- confirm `System/wiki-log.md` has a batch ingest entry

## Pitfalls

- Many CSV import files look non-empty because they contain metadata fields, but still have no useful body content.
- The `URL:` field is the main discriminator; blank-body files can still be valid ingest candidates if URL is present.
- Do not rely on full-folder MCP listings for this directory when the response is huge; use targeted scans/scripts instead.
- Prefer batches over mass ingest because this vault has established wiki curation conventions.
- Preserve original filenames when archiving to `Sources/`.

## Example outcome from a successful batch

A reusable batch processed these 5 URL-backed captures:
- Kilo Code
- VibeBible
- RealtyLens AI
- NSE Stock Research Analysis System
- n8n Workflow Automation Templates

Actions taken:
- moved raw captures to `Sources/`
- created 5 `Notes/` pages
- updated AI Development, AI Agent Tooling, and Finance MOCs
- updated `System/wiki-index.md`
- appended batch entry to `System/wiki-log.md`
