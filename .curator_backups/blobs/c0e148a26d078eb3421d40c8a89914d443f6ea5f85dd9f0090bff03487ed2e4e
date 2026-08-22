# Multi-profile MCP scope

When wiring external MCP servers into multi-profile Hermes (default + Telegram bots):

## Scope rule

- Enable a server only on profiles that need it.
- Heavy multi-tool servers (multiple Graphify vault graphs, large tool schemas) → **default only**, or **0–1 per named bot**.
- Do not “enable everywhere for convenience.” That multiplies tool schemas and RAM across every gateway process.

## Graphify vault example (user policy)

- `default`: all 4 vault graphs
- `zeus` / `finance` / `butter` / `catthew` / `charles`: at most `graphify-vault-core`
- `thor` / `wiki`: none
- `graphify-hermes`: default only, usually disabled

## After config change

1. `hermes -p <p> mcp remove|add …`
2. Restart only changed profiles (one at a time on low-RAM hosts).
3. Prove **live** footprint: map gateway `HERMES_HOME` → `mcp_stdio_watchdog --ppid` children.
4. Do not trust raw `pgrep <mcp-binary>` alone (CLI sessions + watchdog pairs overcount).

Full ops probe, stuck-restart, and orphan-watchdog notes:

- `hermes-operations-troubleshooting` → `references/multi-profile-mcp-footprint.md`
