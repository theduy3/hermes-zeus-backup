# Vault Reorganization — Consolidating Scattered Notes into Project Folders

Use this workflow when the user asks to find all notes on a topic and consolidate them into a project folder. Common triggers: "organize all X notes", "consolidate everything about Y", "clean up scattered Z files".

## When to use this vs. the CSV ingest workflow

- **CSV import ingest** (`obsidian-csv-import-ingest`): processing raw captures from `Inbox/CSV import/` — URL-backed shells that need web_extract + wiki page creation
- **Vault reorganization** (this reference): finding already-created notes scattered across the vault (Tasks/, Notes/, Sources/, Daily/, old Projects/) and consolidating them into one structured project folder

## Workflow

### Phase 1: Discovery

1. **Search the entire vault** for content matches using `search_files` with `target='content'` and `output_mode='files_only'`. Use case-insensitive patterns covering all name variants (e.g., `salon360|salonx|Salon360|SalonX`).

2. **Get the existing project directory tree** using `mcp_obsidian_fs_directory_tree` on the target project path. This shows what's already there vs. what's scattered.

3. **Read every candidate file** that isn't already in the project folder. Skip Daily/*.md files (journal entries — they reference topics in passing but aren't reference notes) unless they contain substantial unique information.

### Phase 2: Classification

Classify each file into domains based on content:
- **Business/Strategy**: plans, pricing, market analysis, Q&A documents
- **Legal**: NDAs, incorporation, IP assignment
- **Product**: feature specs, backlogs, task lists, HR/staff, operations, industry references
- **Engineering**: architecture, infrastructure, backups, dev workflows, code reviews
- **Sales**: prospects, leads, sales strategy
- **Credentials**: API keys, passwords, tokens (flag security concern)

### Phase 3: Structure Proposal

Propose a numbered domain directory structure. Present to the user as a tree with clear "KEY" markers on anchor documents. Include:
- What moves where
- Which files to merge (duplicates, fragments on same topic)
- Which files to aggregate (multiple feature notes → one Feature Backlog)
- Security flags (plaintext credentials)
- What stays (Daily journals, infrastructure files)

**Naming convention for directories**: `NN-DomainName/` — zero-padded numbers for sort order.

**Naming convention for renamed files**: Use Title Case, descriptive, keep original where possible.

### Phase 4: Execution (after user approval)

Execute in this order to minimize risk:

1. **Create all directories first** — `mcp_obsidian_fs_create_directory` for each new subdirectory (can run in parallel).

2. **Move scattered files into the project** — batch parallel `mcp_obsidian_fs_move_file` calls. Move from external locations first (Tasks/, Notes/, Sources/, old Projects/).

3. **Reorganize files already in the project** into their new subdirectories.

4. **Handle duplicates**: when two files have identical or near-identical content, move one to the target name, then move the second to the same destination (which overwrites — safe when content is identical). Prefer `mcp_obsidian_fs_move_file` — it's faster and handles overwrites cleanly.

5. **Create aggregation documents**: use `mcp_obsidian_fs_write_file` to create synthesis docs (Feature Backlog, Architecture overview, etc.) with proper wiki frontmatter (`tags`, `type: synthesis`, `created`, `updated`, `sources` with wikilinks).

6. **Rewrite CLAUDE.md**: overwrite with real project context — tech stack, architecture notes, vault organization map, key document pointers, active stores/servers. This replaces empty or stale CLAUDE.md files.

7. **Clean up empty directories**: use `rmdir` via terminal for now-empty folders.

8. **Verify**: run `mcp_obsidian_fs_directory_tree` on the project root and `search_files` to confirm no scattered files remain outside the project (excluding Daily/ and System/).

### Pitfalls

- **Daily/*.md files are noise**: 20+ Daily files may match content search but they're journal entries, not reference notes. Skip them.
- **System/ files are infrastructure**: wiki-log.md, wiki-index.md, scripts — leave these alone.
- **Duplicate detection**: Salon Expense Note and Salon Payment Note had identical content ("30%, 2 jours, Cheque..."). Always read files before moving to catch duplicates.
- **Credentials exposure**: plaintext passwords, API keys, and tokens in vault notes are a security risk. Flag them and move to a `Credentials/` or `Secrets/` subdirectory with a warning to `.gitignore` or encrypt.
- **MCP tools vs terminal**: prefer `mcp_obsidian_fs_*` tools for all vault file operations — they handle Obsidian-specific paths, avoid permission issues on macOS, and batch better than shell commands.
- **Old project directories**: check for legacy project folders (e.g., `Salon360 App/`) that should be absorbed into the new structure. Move their files then `rmdir` the empty directory.
