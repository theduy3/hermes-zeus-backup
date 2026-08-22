---
name: multi-profile-mcp-scoping
description: "Use when scoping MCP servers across Hermes profiles."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
metadata:
  hermes:
    tags: [MCP, profiles, gateways, graphify, telegram, tooling]
    category: mcp
    related_skills: [external-mcp-integrations, native-mcp, graphify-hermes-vault-integration]
---

# Multi-profile MCP scoping

## When to use

- Wiring or cleaning MCP servers on Hermes **default** vs named profiles (`zeus`, `thor`, `finance`, `butter`, `catthew`, `charles`, `wiki`, …)
- User reports tool-schema bloat, duplicate MCP tools, or many identical `graphify-mcp` / stdio children
- After adding a multi-server MCP pack (Graphify vault splits, etc.)

## Hard rules

1. **default ≠ every bot.** Each profile has its own `config.yaml` / `HERMES_HOME`. Enabling on default does not enable on zeus/finance/…
2. **Heavy packs stay narrow.** If a server family exposes large duplicated tool schemas (example: 4 Graphify vault graphs × ~12 tools each), only **default** may load the full set. Named profile bots keep **0–1** server from that family unless the user explicitly asks for more.
3. **Prefer one relevant slice on bots.** For theduyvault Graphify splits, profile default is `graphify-vault-core` (life/business/tasks) or none — not vault + core + sources + daily.
4. **Edit via CLI, not file tools.** `config.yaml` is often write-protected from agent patch/write. Use:
   - `hermes mcp list` / `hermes -p <profile> mcp list`
   - `hermes -p <profile> mcp remove <name>`
   - `printf 'Y\n' | hermes -p <profile> mcp add ...` when adding
5. **Restart only changed profiles.** Config change does not drop already-spawned MCP children.
   - Prefer: `hermes -p <profile> gateway run --replace` (background it — the process *is* the gateway and stays up)
   - Confirm logs: `Active profile: <name>`, `Connected to Telegram (polling mode)`, `✓ telegram connected`
6. **Verify on-disk and live.** List CLI is not enough if a stuck gateway still holds old children.

## Verified Graphify vault matrix (2026-08-21)

| Profile | Vault Graphify MCP |
|---------|--------------------|
| default | `graphify-vault`, `graphify-vault-core`, `graphify-vault-sources`, `graphify-vault-daily` (`graphify-hermes` optional/disabled) |
| zeus, finance, butter, catthew, charles | `graphify-vault-core` only |
| thor, wiki | none |

Do not re-fan all four vault graphs onto profile bots. Deeper Graphify install/refresh lives in `graphify-hermes-vault-integration` (user-owned; `hermes curator adopt graphify-hermes-vault-integration` before curator can patch it).

## Trim recipe

```bash
# Example: zeus had the full pack — keep core only
for s in graphify-hermes graphify-vault graphify-vault-sources graphify-vault-daily; do
  hermes -p zeus mcp remove "$s"
done

# finance had core+sources — keep one
hermes -p finance mcp remove graphify-vault-sources

# verify
hermes mcp list
for p in zeus finance butter catthew charles thor wiki; do
  echo "==== $p"; hermes -p "$p" mcp list
done
```

## Live footprint check

```bash
pgrep -af 'hermes.*gateway restart'   # hung default restart multiplies MCP sets
pgrep -af 'graphify-mcp' | grep -oE 'theduyvault[^ /]*' | sort | uniq -c
```

Healthy: non-core vault graphs (`theduyvault`, `theduyvault-sources`, `theduyvault-daily`) only under default. Profile bots that keep one graph show only `theduyvault-core`.

## Pitfalls

- Copying “all Graphify servers” onto zeus “for parity” recreates the 16×-style duplication.
- Foreground `gateway run --replace` never exits on success — background it; judge success from Telegram connect logs, not process exit.
- Stuck `hermes gateway restart` on default can hold a full MCP set for a long time and inflate process counts — stop that PID only (approval may be required), not the whole fleet.
- Ad-hoc `kill` of gateways may require interactive approval; prefer profile-scoped `--replace` when it works.
- Mid-session MCP add/remove does not hot-inject into the current chat; new session after gateway reload.

## Related

- `external-mcp-integrations` — class playbook for third-party MCP install
- `native-mcp` — client config reference (may be user-owned)
- `graphify-hermes-vault-integration` — Graphify build/refresh paths (user-owned unless adopted)
