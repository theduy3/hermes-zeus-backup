# Multi-profile MCP footprint and stuck gateway restart

Use when trimming or auditing heavy MCP servers across default + Telegram profile bots (Graphify vault graphs are the canonical case).

## Policy example (Graphify vault)

- `default`: all 4 vault graphs (`graphify-vault`, `graphify-vault-core`, `graphify-vault-sources`, `graphify-vault-daily`)
- named bots: **0–1** vault graph (prefer core for zeus/finance/butter/catthew/charles; thor/wiki = 0)
- `graphify-hermes`: default only, usually disabled

Do not enable the full multi-graph set on every profile. That multiplies tool schemas and RAM.

## Config vs live

`hermes mcp list` / `hermes -p <p> mcp list` prove config only.

Live proof: map each gateway PID’s `HERMES_HOME` to its `mcp_stdio_watchdog --ppid <pid>` children.

```bash
for pid in $(pgrep -f 'python3 .*hermes.*gateway run' || true); do
  hh=$(tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | awk -F= '/^HERMES_HOME=/{print $2}')
  name=$(basename "$hh")
  [ "$name" = ".hermes" ] && name=default
  graphs=$(ps -eo cmd | grep "mcp_stdio_watchdog.py --ppid $pid" | grep -v grep \
    | sed -n 's|.*\.graphify/\([^/]*\)/graphify-out/graph.json.*|\1|p' | sort | tr '\n' ',')
  echo "$name pid=$pid graphs=${graphs:-none}"
done
```

Identify profile gateways by `HERMES_HOME=.../profiles/<name>`, not only argv `-p` (some launches show bare `hermes gateway run`).

## Overcount trap

Raw `pgrep graphify-mcp | uniq -c` overcounts because:

1. each server has watchdog + process
2. interactive CLI Hermes sessions also load default MCP
3. stuck `gateway restart` PIDs can hold a second full set

Always attribute by parent gateway before “fixing” duplication.

## Restart discipline

1. Change config first: `hermes -p <p> mcp remove <name>` (or add).
2. Restart **only changed profiles**, one at a time on low-RAM hosts (~4G).
3. Wait for `✓ telegram connected` before the next profile.
4. Keep `~/.hermes/scripts/profile_gateway_supervisor.sh` running for butter/catthew/charles/finance/thor/zeus.
5. Avoid stacking host/root `hermes gateway restart` while MCP children are still spawning — unclean exits and mass profile drops are common.

## Stuck restart PID

A long-lived `hermes gateway restart` process can hold a full MCP set beside a real `gateway run`.

- Kill the stuck **restart** PID only.
- Confirm exactly one healthy `gateway run` remains for default.
- Re-check telegram connected + MCP children.

## Orphan watchdogs

After unclean gateway death, `mcp_stdio_watchdog --ppid <dead>` can keep MCP servers alive.

1. List watchdogs whose `--ppid` process is gone.
2. TERM/KILL those watchdog PIDs (children usually die with them).
3. Re-verify each live profile still has the intended 0–1 MCP set and telegram connected.

## Duplicate profile PIDs

Supervisor auto-start + manual `gateway run --replace` can leave two PIDs for one profile. Keep one; confirm a single telegram connection path.

## Related

- Graphify install/split paths: skill `graphify-hermes-vault-integration` (may be user-owned; adopt before curator patches).
- Docker HERMES_HOME isolation: `references/docker-profile-gateway-hardening.md`.
