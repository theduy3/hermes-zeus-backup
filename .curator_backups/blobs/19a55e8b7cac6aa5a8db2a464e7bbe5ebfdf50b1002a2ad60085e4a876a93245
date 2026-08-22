---
name: multi-profile-mcp-footprint
description: "Use when scoping heavy MCP across Hermes profiles."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
metadata:
  hermes:
    tags: [MCP, Graphify, profiles, gateway, Telegram, RAM]
    category: mcp
    related_skills: [external-mcp-integrations, hermes-operations-troubleshooting, graphify-hermes-vault-integration]
---

# Multi-profile MCP footprint

Class-level playbook for **where** heavy MCP servers should run on a multi-profile Hermes host, and how to prove the live process tree matches config.

## When to use

- User wants Graphify (or other heavy MCP) on some bots but not all
- Process counts for `graphify-mcp` / MCP watchdogs look “duplicated”
- After `hermes mcp remove` / profile restarts, need to verify 0–1 vs full set
- Stuck `gateway restart` or orphan MCP children after unclean exits

## Hard scope rule

- **default**: may load the full intentional set (e.g. all 4 vault Graphify graphs)
- **named Telegram bots**: **0–1** heavy multi-tool MCP server each
- Never enable “every graph on every bot” for convenience — that multiplies tool schemas and RAM

### Graphify vault policy (user)

| Profile | Vault Graphify |
|---------|----------------|
| default | `graphify-vault` + `core` + `sources` + `daily` |
| zeus, finance, butter, catthew, charles | `graphify-vault-core` only |
| thor, wiki | none |
| `graphify-hermes` | default only, usually **disabled** |

## Trim + verify sequence

1. Config:
   ```bash
   hermes -p <profile> mcp remove <server>
   hermes mcp list
   hermes -p <profile> mcp list
   ```
2. Restart **only changed profiles**, one at a time on low-RAM (~4G) hosts:
   ```bash
   hermes -p <profile> gateway run --replace
   # wait for: ✓ telegram connected
   ```
3. Keep supervisor up for butter/catthew/charles/finance/thor/zeus:
   `~/.hermes/scripts/profile_gateway_supervisor.sh`
4. Live proof (config list is not enough) — map `HERMES_HOME` → watchdog children:
   ```bash
   for pid in $(pgrep -f 'python3 .*hermes.*gateway run' || true); do
     hh=$(tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | awk -F= '/^HERMES_HOME=/{print $2}')
     name=$(basename "$hh"); [ "$name" = ".hermes" ] && name=default
     graphs=$(ps -eo cmd | grep "mcp_stdio_watchdog.py --ppid $pid" | grep -v grep \
       | sed -n 's|.*\.graphify/\([^/]*\)/graphify-out/graph.json.*|\1|p' | sort | tr '\n' ',')
     echo "$name pid=$pid graphs=${graphs:-none}"
   done
   ```
5. Identify profile gateways by `HERMES_HOME=.../profiles/<name>`, not only argv `-p`.

## Overcount trap

Raw `pgrep graphify-mcp | uniq -c` overcounts because:

1. watchdog + server pair per graph
2. interactive **CLI Hermes sessions** also load default MCP
3. stuck `hermes gateway restart` PIDs can hold a second full set

Always attribute by parent gateway before “fixing” duplication.

## Stuck restart / orphans / duplicates

- **Stuck restart PID:** kill only the long-lived `gateway restart` process; keep one healthy `gateway run` per profile; re-check telegram + MCP children.
- **Orphan watchdogs:** `mcp_stdio_watchdog --ppid <dead>` keeps MCP alive after gateway death — TERM/KILL those watchdogs, then confirm bots still have the intended 0–1 set.
- **Duplicate profile PIDs:** supervisor + manual `--replace` can leave two gateways; keep one.
- **Do not stack host/root restarts** while MCP is still spawning — unclean exits and mass profile drops are common.

## Related

- Install/build paths may live in `graphify-hermes-vault-integration` (user-owned unless `hermes curator adopt graphify-hermes-vault-integration`)
- Gateway HERMES_HOME isolation: `hermes-operations-troubleshooting` → `references/docker-profile-gateway-hardening.md`
- Duplicate notes also under:
  - `hermes-operations-troubleshooting/references/multi-profile-mcp-footprint.md`
  - `external-mcp-integrations/references/multi-profile-mcp-scope.md`
