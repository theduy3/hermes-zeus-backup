---
name: knowledge-graph-integrations
description: Use when integrating code/content knowledge graphs into Hermes, Obsidian vaults, MCP servers, or scheduled refresh workflows. Covers Graphify-style graph builds, vault-safe output placement, MCP wiring, and verification.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [knowledge-graph, graphify, hermes, obsidian, mcp, cron, code-intelligence]
---

# Knowledge Graph Integrations

Use this skill when the user asks to add a knowledge-graph system to Hermes, an Obsidian vault, a codebase, or an MCP workflow.

## Principles

- Keep generated graph artifacts outside the Obsidian vault unless the user explicitly asks for an export inside the vault.
- Write only human-readable summaries, indices, or integration notes to the vault Inbox.
- Verify with real graph stats and query output before reporting success.
- Preserve the user's provider policy. If the user is OpenAI-only, do not configure Gemini/Anthropic just because a tool suggests them.
- For Hermes CLI sessions, cron delivery set to `local` saves output but does not live-message the terminal.

## Standard Graphify + Hermes + vault workflow

1. Install Graphify in an isolated tool environment:
   ```bash
   uv tool install --upgrade 'graphifyy[mcp]'
   export PATH="$HOME/.local/bin:$PATH"
   graphify --version
   ```

2. Install the Hermes skill:
   ```bash
   graphify install --platform hermes
   ```
   Start a new Hermes session before expecting the skill to auto-load.

3. Use output roots outside the vault:
   ```text
   ~/.graphify/hermes/graphify-out/
   ~/.graphify/theduyvault/graphify-out/
   ```

4. Build a Hermes source graph locally with no LLM/API:
   ```bash
   graphify extract ~/.hermes/hermes-agent --code-only --out ~/.graphify/hermes --force --max-workers 4
   ```

5. Build a vault graph conservatively:
   - Prefer structural Markdown extraction when no approved LLM backend is available.
   - Include note/task/project/source folders.
   - Exclude noisy/private/generated folders such as `.git`, `.obsidian`, `.stversions`, `.trash`, `.smart-env`, `.stfolder`, `.superpowers`, `.claude`, `.code-review-graph`, `.zettel-notes`, `Attachments`, `graphify-out`, and `node_modules`.

6. Add MCP servers, one per graph. In non-interactive execution, pipe `Y` into the enable prompt:
   ```bash
   printf 'Y\n' | hermes mcp add graphify-hermes --command graphify-mcp --args ~/.graphify/hermes/graphify-out/graph.json
   printf 'Y\n' | hermes mcp add graphify-vault --command graphify-mcp --args ~/.graphify/theduyvault/graphify-out/graph.json
   hermes mcp list
   ```

7. Schedule refresh via a deterministic script under `~/.hermes/scripts/` and a no-agent cron job. The script should print exact graph stats.

8. Write an integration note to `/vault/Inbox/` with:
   - installed package/version
   - graph paths
   - node/edge counts
   - MCP server names
   - cron job ID/schedule
   - manual refresh/query commands

## Verification checklist

Run real checks before finalizing:

```bash
hermes mcp list
hermes cron list
cd ~/.graphify/hermes && graphify query "tool registry" --graph graphify-out/graph.json --budget 600
cd ~/.graphify/theduyvault && graphify query "tasks finance" --graph graphify-out/graph.json --budget 600
```

Also read `graph.json` and report actual node/edge counts.

## Pitfalls

- `hermes mcp add` can connect, list tools, then cancel if the enable prompt is unanswered. A cancelled add saves nothing.
- `graphify extract` requires a backend for docs/papers/images unless using `--code-only` or a custom structural extraction path.
- Do not put large `graphify-out/` directories into an Obsidian vault by default.
- Do not report MCP tools as available in the current Hermes session after adding them; the user needs a new session for tool discovery.
