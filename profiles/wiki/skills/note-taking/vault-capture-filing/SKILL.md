---
name: vault-capture-filing
description: Use when filing loose vault captures into destinations.
version: 1.0.0
metadata:
  hermes:
    tags: [obsidian, vault, filing, captures]
---

# vault-capture-filing

Use this skill when turning loose/root/Inbox Obsidian captures into clean destination notes, especially in theduyvault-style vaults with `Inbox/`, `Notes/`, `Projects/`, `Tasks/`, `MOCs/`, and `System/` infrastructure.

## Core workflow

1. Resolve and read the vault conventions first (for theduyvault: `/vault/CLAUDE.md`; for scheduled filing jobs, also follow any local process skill/instructions the user invoked).
2. Discover unprocessed captures with the vault’s canonical finder when one exists; otherwise list/search the relevant root and Inbox folders.
3. Read each candidate before moving it. If it is empty or meaningless, remove it and report the cleanup.
4. Check for secrets/credentials. If a capture contains apparent secrets, leave it in place and report the blocker instead of filing it.
5. Classify by durable destination:
   - `Notes/`: durable wiki knowledge, reference material, synthesis, concepts/entities.
   - `Projects/...`: project execution material, runbooks, setup instructions, implementation notes, operational procedures tied to a named project.
   - `Tasks/tasks`, `Tasks/ideas`, `Tasks/bugs`: explicit tasks, ideas, or bug reports using the vault’s task frontmatter.
   - `Inbox/`: only if the capture truly remains unclear or needs later manual processing.
6. Before creating a new `Notes/` page, search existing notes for the topic and obvious synonyms. Fold refreshed coverage into existing pages rather than creating duplicate generic notes.
7. Use auditable file-tool edits/moves where practical; avoid hiding classification, filing, and infrastructure edits inside a large ad hoc script.
8. Verify by rerunning the canonical finder, or with a small targeted ad-hoc verifier if no suite exists.

## Project-folder filing pattern

When a loose capture is project execution material, do not force it into the wiki just because it is substantive. File it under the relevant `Projects/...` folder and clean it into a compact project reference note:

- Add frontmatter with project-specific tags plus `created`/`updated` dates.
- Preserve commands, safety warnings, handoff formats, and prerequisites.
- Remove chat transcript separators, browsing/tool narration, duplicated instructions, and conversational filler.
- Add at least one relevant project wikilink when an existing project note exists.
- Do **not** update MOCs, `System/wiki-index.md`, or `System/wiki-log.md` for a project-only note unless a `Notes/` wiki page was also created or updated.

## Wiki-note filing pattern

For `Notes/` pages, keep the page atomic and wiki-compatible:

- Use the vault’s frontmatter schema (`type`, tags, `created`, `updated`, `sources`, `wiki_status` where required).
- Add at least two related wikilinks when possible.
- Touch relevant MOCs and machine index/log files when the vault convention requires it.
- If infrastructure files are unwritable, finish the note filing and report the exact blocker.

## Verification pattern

For scheduled/headless filing runs, success means the original processable captures are either filed, removed as empty, or intentionally left in place with a reported reason. A good ad-hoc verifier checks:

- Destination file exists and has expected frontmatter/content.
- Original Inbox/root file no longer exists for processed notes.
- Expected wikilinks or project links are present.
- Wiki infrastructure was updated only when required.
- The canonical unprocessed-note finder returns zero, or only intentionally retained blockers.

If deleting a temporary verifier after moving/removing vault files, run deletion as a separate safe command rather than chaining `python verifier; rm verifier`, so headless deletion guards do not mistake it for a broad delete burst.
