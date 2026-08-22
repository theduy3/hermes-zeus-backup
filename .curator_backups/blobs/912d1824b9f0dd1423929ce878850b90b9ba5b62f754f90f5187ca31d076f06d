# Graphify vault MCP matrix (session 2026-08-21)

User directive: only default loads all 4 vault graphifies; profile bots keep 0–1. Kills multi-profile × multi-graph duplication.

## On-disk target

- default: graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily (graphify-hermes disabled OK)
- zeus / finance / butter / catthew / charles: graphify-vault-core only
- thor / wiki: none

## Commands that worked

```bash
hermes -p zeus mcp remove graphify-hermes
hermes -p zeus mcp remove graphify-vault
hermes -p zeus mcp remove graphify-vault-sources
hermes -p zeus mcp remove graphify-vault-daily
hermes -p finance mcp remove graphify-vault-sources
hermes -p zeus gateway run --replace   # background; stays up
hermes -p finance gateway run --replace
```

## Ops notes

- Profile supervisor: `~/.hermes/scripts/profile_gateway_supervisor.sh` (butter catthew charles finance thor zeus).
- Logs: `~/.hermes/profiles/<p>/logs/gateway.log`
- Hung `hermes gateway restart` on default multiplies live graphify-mcp children until stopped.
- Foreground skill patch of `graphify-hermes-vault-integration` already has the hard rule; background curator cannot patch that skill until `hermes curator adopt graphify-hermes-vault-integration`.
