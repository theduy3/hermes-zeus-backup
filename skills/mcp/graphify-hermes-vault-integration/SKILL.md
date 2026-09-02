---
name: graphify-hermes-vault-integration
description: "Integrate Graphify with Hermes Agent and theduyvault: install graphify, build local graphs outside the vault, wire MCP servers, schedule refresh, and write an Obsidian Inbox note."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [graphify, hermes, mcp, obsidian, theduyvault, knowledge-graph]
    related_skills: [graphify, hermes-agent, obsidian, hermes-skill-management]
---

# Graphify + Hermes + theduyvault Integration

## When to use

Use this when Duy asks to integrate, repair, rebuild, or verify Graphify for:

- Hermes Agent source graphing
- theduyvault/Obsidian graphing
- Graphify MCP servers inside Hermes
- scheduled graph refresh jobs

## Principles

- Keep generated graph outputs outside `/vault` to avoid polluting Obsidian.
- Write only human-readable integration notes/summaries to `/vault/Inbox/`.
- Respect Duy's OpenAI-only preference: do not configure Gemini/Anthropic/OpenRouter for semantic extraction.
- Prefer local structural extraction first:
  - Hermes source: Graphify `--code-only` local AST.
  - theduyvault: structural Markdown extraction via Graphify's markdown extractor.
- Cron jobs from CLI sessions are local-only unless explicitly delivered to Telegram/other gateway target.

## Paths

- Hermes source: `/home/hermes/.hermes/hermes-agent`
- Hermes graph output root: `/home/hermes/.graphify/hermes/graphify-out/`
- theduyvault mount: `/vault`
- Vault graph output root: `/home/hermes/.graphify/theduyvault/graphify-out/`
- Refresh script: `/home/hermes/.hermes/scripts/graphify_refresh.py`
- Obsidian note: `/vault/Inbox/graphify-integration.md`

## Install / verify Graphify

```bash
export PATH="$HOME/.local/bin:$PATH"
uv tool install --upgrade 'graphifyy[mcp]'
graphify --version
graphify install --platform hermes
test -f ~/.hermes/skills/graphify/SKILL.md
```

If only CLI is needed and MCP is not required yet, `uv tool install --upgrade graphifyy` is enough. For MCP, install the extra: `graphifyy[mcp]`.

## Vault discovery

Check mount and approximate corpus before building:

```bash
mount | grep ' /vault ' || true
python3 - <<'PY'
from pathlib import Path
from collections import Counter
c=Counter()
for p in Path('/vault').rglob('*.md'):
    if set(p.parts) & {'.git','.obsidian','node_modules','graphify-out'}:
        continue
    rel=p.relative_to('/vault')
    c[rel.parts[0] if len(rel.parts)>1 else '(root)'] += 1
for k,n in c.most_common(40):
    print(f'{n:6} {k}')
print('TOTAL', sum(c.values()))
PY
```

Common writable vault state on VPS/container:

```text
/dev/sda4 on /vault type xfs (rw,...)
```

## Build/refresh script

Create `/home/hermes/.hermes/scripts/graphify_refresh.py` with this behavior:

1. Build Hermes graph (low-RAM host — do **not** full-tree `--force` with 4 workers):

```bash
# Script maintains ~/.hermes/hermes-agent/.graphifyignore (drops node_modules/venv/apps/…)
# then runs something equivalent to:
graphify extract /home/hermes/.hermes/hermes-agent \
  --code-only \
  --out /home/hermes/.graphify/hermes \
  --max-workers 1 \
  --no-cluster
# --force only on first scoped rebuild or GRAPHIFY_HERMES_FORCE=1
```

**OOM pitfall (recurring on ~2.5Gi cgroup):** unscoped extract sees ~7.5k code files
(node_modules/venv/apps) and dies with `SIGKILL`. Scope via `.graphifyignore`,
`GRAPHIFY_MAX_WORKERS=1` (default in script), soft-fail Hermes so vault graphs still
refresh, and never leave a 0-node `graph.json` (restore `.bak`).

2. Build theduyvault graph structurally with Python using Graphify library:

- Include top-level folders:
  - `AgentMemory`, `Clippings`, `Daily`, `Inbox`, `MOCs`, `Notes`, `Projects`, `Sources`, `Stock Watchlist`, `System`, `Tasks`
- Exclude:
  - `.git`, `.obsidian`, `.stversions`, `.trash`, `.smart-env`, `.stfolder`, `.superpowers`, `.claude`, `.code-review-graph`, `.zettel-notes`, `Attachments`, `graphify-out`, `node_modules`
- Use `graphify.extract.extract()` over markdown files with `root=/vault` and `cache_root=/home/hermes/.graphify/theduyvault`.
- Build with `graphify.build.build_from_json()`.
- Cluster/report/export to `/home/hermes/.graphify/theduyvault/graphify-out/`.

Known-good script exists at:

```bash
/home/hermes/.hermes/scripts/graphify_refresh.py
```

Run manually:

```bash
export PATH="$HOME/.local/bin:$PATH"
# full: hermes + 4 vault graphs
uv tool run --from graphifyy python /home/hermes/.hermes/scripts/graphify_refresh.py
# flags: --hermes-only | --vault-only | --split-only
# env: GRAPHIFY_MAX_WORKERS=1  GRAPHIFY_HERMES_FORCE=1
```

Expected outputs from initial integration:

```text
/home/hermes/.graphify/hermes/graphify-out/graph.json
/home/hermes/.graphify/theduyvault/graphify-out/graph.json
/home/hermes/.graphify/last-refresh.json
```

## Query smoke tests

```bash
export PATH="$HOME/.local/bin:$PATH"
cd /home/hermes/.graphify/hermes
graphify query 'tool registry' --graph graphify-out/graph.json --budget 600

cd /home/hermes/.graphify/theduyvault
graphify query 'tasks finance' --graph graphify-out/graph.json --budget 600
```

Initial verified graph sizes:

```text
Hermes:       137,980 nodes / 309,524 edges
Theduyvault:   22,237 nodes /  21,658 edges / 4,577 markdown files
```

Treat these as rough regression baselines, not fixed requirements.

## MCP setup

Install MCP extra first:

```bash
export PATH="$HOME/.local/bin:$PATH"
uv tool install --upgrade 'graphifyy[mcp]'
graphify-mcp --help
```

Add Hermes MCP servers non-interactively by piping `Y`:

```bash
printf 'Y\n' | hermes mcp add graphify-hermes \
  --command graphify-mcp \
  --args /home/hermes/.graphify/hermes/graphify-out/graph.json

printf 'Y\n' | hermes mcp add graphify-vault \
  --command graphify-mcp \
  --args /home/hermes/.graphify/theduyvault/graphify-out/graph.json

hermes mcp list
```

Expected servers:

```text
graphify-hermes  graphify-mcp /home/hermes...   all  enabled
graphify-vault   graphify-mcp /home/hermes...   all  enabled
```

A new Hermes session is required for newly added MCP tools to appear.

After reload, expected tool namespaces may include:

- `mcp__graphify_hermes__query_graph`
- `mcp__graphify_hermes__graph_stats`
- `mcp__graphify_vault__query_graph`
- `mcp__graphify_vault__graph_stats`

## Cron refresh

Use the `cronjob` tool from an interactive Hermes session, not raw file editing:

```text
action=create
name=graphify-daily-refresh
schedule=30 3 * * *
script=graphify_refresh.py
no_agent=true
deliver=local
```

Current known job:

```text
Job: graphify-daily-refresh
ID: 5a9aa5056402
Schedule: daily 03:30 America/Vancouver
Delivery: local-only
```

CLI session caveat: local-only cron output is saved and visible in cron job state/listing; it is not delivered back into the terminal as a live message.

## Obsidian note

Write a concise integration note to:

```text
/vault/Inbox/graphify-integration.md
```

Include:

- installed package/version
- graph paths and sizes
- MCP server names
- cron job ID/schedule
- manual refresh/query commands
- note that Graphify outputs are outside `/vault`
- note that vault graph is structural Markdown-only unless OpenAI semantic extraction is configured

## Telegram/profile distribution

Hard rule: **only `default` loads all 4 vault Graphify MCP servers.** Named profile bots keep **0–1** vault Graphify server. That avoids multi-profile × multi-graph tool-schema duplication (the old “every bot loads every vault graph” blowup).

Recommended MCP profile split for Telegram gateways:

- `default`: all 4 vault Graphify servers (`graphify-vault`, `graphify-vault-core`, `graphify-vault-sources`, `graphify-vault-daily`). `graphify-hermes` optional/disabled unless actively debugging Hermes source.
- Named profile bots (`zeus`, `finance`, `butter`, `catthew`, `charles`): at most **one** vault graph — prefer `graphify-vault-core` when they need life/business/tasks lookup.
- `thor`, `wiki`: **0** Graphify by default (no vault graph MCP).
- Never enable the full 4-vault set on a non-default profile.
- Do not put `graphify-hermes` on profile bots unless explicitly requested for code work.

Trim with `hermes -p <profile> mcp remove <name>`, then restart that profile gateway. Verify with `hermes -p <profile> mcp list`.

After patching profile `config.yaml`, restart affected gateways with `hermes -p <profile> gateway run --replace` or profile-specific restart. Verify newest logs show `Connected to Telegram (polling mode)` and `✓ telegram connected`.

## Verification checklist

- `graphify --version` works.
- `~/.hermes/skills/graphify/SKILL.md` exists.
- `/home/hermes/.graphify/hermes/graphify-out/graph.json` exists and has nonzero nodes/edges.
- `/home/hermes/.graphify/theduyvault/graphify-out/graph.json` exists and has nonzero nodes/edges.
- Query smoke tests return Graphify traversal output.
- `hermes mcp list` shows `graphify-hermes` and `graphify-vault` enabled.
- Cron job `graphify-daily-refresh` exists.
- `/vault/Inbox/graphify-integration.md` exists.

## Split vault graphs

For cleaner retrieval, build these in addition to the legacy all-vault graph:

- `theduyvault-core`: MOCs, Notes, Projects, Tasks; excludes `Notes/Claude-Context/` session logs.
- `theduyvault-sources`: Sources, Clippings, Stock Watchlist.
- `theduyvault-daily`: Daily, AgentMemory, Inbox, System, plus `Notes/Claude-Context/` session logs.

Output paths:

```text
/home/hermes/.graphify/theduyvault-core/graphify-out/graph.json
/home/hermes/.graphify/theduyvault-sources/graphify-out/graph.json
/home/hermes/.graphify/theduyvault-daily/graphify-out/graph.json
```

Add MCP servers:

```bash
printf 'Y\n' | hermes mcp add graphify-vault-core \
  --command graphify-mcp \
  --args /home/hermes/.graphify/theduyvault-core/graphify-out/graph.json
printf 'Y\n' | hermes mcp add graphify-vault-sources \
  --command graphify-mcp \
  --args /home/hermes/.graphify/theduyvault-sources/graphify-out/graph.json
printf 'Y\n' | hermes mcp add graphify-vault-daily \
  --command graphify-mcp \
  --args /home/hermes/.graphify/theduyvault-daily/graphify-out/graph.json
```

Use graph choice by intent:

- core: life/business/projects/tasks questions.
- sources: article/research/market-source questions.
- daily: daily notes, session logs, Inbox/System operational questions.
- legacy all-vault: broad recall when unsure.

Current split baseline:

```text
theduyvault-core:     9,451 nodes / 11,300 edges / 1,673 files
theduyvault-sources:  8,053 nodes /  6,304 edges / 2,223 files
theduyvault-daily:   12,751 nodes / 14,348 edges / 1,860 files
```

## Pitfalls

- `hermes mcp add` prompts to enable tools. Pipe `Y` for non-interactive automation.
- `graphify extract` on mixed docs needs an LLM backend unless `--code-only` is used. Do not configure Gemini/Anthropic for Duy unless he explicitly changes provider preference.
- The full Hermes graph may be very large; avoid HTML visualization unless needed.
- Do not place `graphify-out/` under `/vault`.
- MCP tools added mid-session require MCP reload or a new Hermes session before they appear.
- The all-vault graph can be noisy; prefer split graphs for normal queries.
