---
name: knowledge-graph-workflows
description: Use when building, integrating, refreshing, or querying local knowledge graphs for Hermes projects, codebases, and Obsidian vaults; includes Graphify patterns, vault-safe layouts, MCP wiring, and verification.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [knowledge-graph, graphify, obsidian, mcp, codebase-analysis, vault]
---

# Knowledge Graph Workflows

Use this skill when the user asks to map a codebase, document corpus, Obsidian vault, or Hermes installation into a queryable knowledge graph, or to connect that graph back to Hermes via skills, MCP, cron, or vault notes.

## Operating principles

1. Install isolated tooling with `uv`/`uvx`; avoid system Python pollution.
2. Keep generated graph artifacts outside Obsidian vault roots unless the user explicitly asks otherwise.
3. Write only human-facing integration notes, summaries, or indexes to the vault Inbox.
4. Verify every integration with real commands before reporting success.
5. If MCP is part of the request, install optional MCP dependencies and test the server before claiming it is wired.

## Graphify quick path

Graphify's package name is `graphifyy` (double-y), while the CLI command is `graphify`.

For CLI-only use:

```bash
uv tool install --upgrade graphifyy
```

For Hermes MCP use:

```bash
uv tool install --upgrade 'graphifyy[mcp]'
```

Install the Hermes skill:

```bash
graphify install --platform hermes
test -f ~/.hermes/skills/graphify/SKILL.md
```

## Vault-safe layout

Do not place `graphify-out/` under `/vault` by default. Preferred generated-artifact locations:

```text
/home/hermes/.graphify/hermes/graphify-out/
/home/hermes/.graphify/theduyvault/graphify-out/
```

Example builds:

```bash
mkdir -p /home/hermes/.graphify/hermes /home/hermes/.graphify/theduyvault

GRAPHIFY_OUT=/home/hermes/.graphify/hermes/graphify-out \
  graphify extract /home/hermes/.hermes/hermes-agent --code-only --no-viz

GRAPHIFY_OUT=/home/hermes/.graphify/theduyvault/graphify-out \
  graphify extract /vault --no-viz
```

If a command's output option is clearer, `graphify extract --out DIR` writes to `DIR/graphify-out/`.

## Obsidian/theduyvault precautions

Before a broad vault scan, inspect top-level folder names and markdown counts, then exclude noisy or generated folders. Typical `.graphifyignore` entries:

```gitignore
.git/
.obsidian/
.trash/
node_modules/
graphify-out/
*.tmp
```

Respect the vault task convention: tasks, bugs, and ideas only go under `/vault/Tasks/{tasks,bugs,ideas}/` with the user's frontmatter. Graph generation should not create tasks as a side effect unless requested.

## MCP wiring pattern

After the graph exists and `graphifyy[mcp]` is installed:

```bash
hermes mcp add graphify-vault --command graphify-mcp --args /home/hermes/.graphify/theduyvault/graphify-out/graph.json
hermes mcp test graphify-vault
hermes mcp list
```

Optional second graph:

```bash
hermes mcp add graphify-hermes --command graphify-mcp --args /home/hermes/.graphify/hermes/graphify-out/graph.json
hermes mcp test graphify-hermes
```

## Scheduled refresh pattern

Use a script under `~/.hermes/scripts/` that:

1. Sets `PATH="$HOME/.local/bin:$PATH"`.
2. Rebuilds or updates each approved graph with explicit output paths.
3. Verifies `graph.json` exists and is non-empty.
4. Emits a concise status report.
5. Optionally writes a human-readable note to `/vault/Inbox/`, never raw generated artifacts.

Schedule with Hermes cron only after a manual build succeeds. In CLI-only sessions, remember that default cron delivery is local-only and will not message the user unless a gateway target is configured.

## Verification checklist

- `graphify --version` prints the expected version.
- `~/.hermes/skills/graphify/SKILL.md` exists after install.
- Graph JSON files exist outside `/vault` unless explicitly approved otherwise.
- A real `graphify query --graph <graph.json> "..."` or equivalent query succeeds.
- `hermes mcp test <server>` succeeds for every MCP server added.
- `/vault/Inbox/` receives only a short integration note with graph paths, commands, and query examples.

## Pitfalls

- Do not confuse package and command names: install `graphifyy`, run `graphify`.
- Do not claim MCP works after only installing the base package; Graphify's MCP server imports optional `mcp` dependencies.
- Do not dump generated `graphify-out/` trees into the Obsidian vault root by default; they can pollute search/sync.
- Do not scan a large vault blindly when a quick count/noise check would materially reduce risk and runtime.
