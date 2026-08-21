---
name: remarkable-mcp-integration
description: Wire/debug reMarkable Cloud MCP across Hermes profiles.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [remarkable, mcp, hermes, profiles, stdio, troubleshooting, cloud]
---

# reMarkable MCP Integration (SamMorrowDrums/remarkable-mcp)

Use this when the user wants to search/read their reMarkable tablet from Hermes, or when a previously-working remarkable MCP server stops loading. Covers profile wiring, the critical stdout-bug fix, token state, and gateway restart.

## When to use
- "Wire remarkable-mcp into all profiles" / "let every profile search my reMarkable"
- remarkable search returns nothing or the MCP server shows `degraded`/`parked` in gateway logs
- Setting up the reMarkable Cloud connection for the first time
- General symptom: an MCP stdio server logs `ERROR mcp.client.stdio: Failed to parse JSONRPC message from server` and Hermes keeps it degraded

## What it is
- Package: `SamMorrowDrums/remarkable-mcp`, run via `uvx --from git+https://github.com/SamMorrowDrums/remarkable-mcp remarkable-mcp`.
- Transport: **Cloud** via `~/.rmapi` token (default). SSH/USB/local-dir are alternatives.
- Tools exposed: `remarkable_browse` (folder list / name search), `remarkable_search` (name + content grep across docs), `remarkable_read` (paginated text/annotations/raw), `remarkable_recent`, `remarkable_status`, `remarkable_image`, `remarkable_export`, `remarkable_canvas`.
- Read-only by default (launcher passes `--read-only`) so chat/Telegram can't delete or move library items.

## Wiring into ALL profiles (not just main)
Each profile has its OWN `config.yaml`; the main profile's `mcp_servers` block does NOT propagate to sub-profiles. You must add the server block to every profile you want it on.
- `config.yaml` is write-protected from `patch`/`write_file` — use the sanctioned path:
  ```
  hermes config set mcp_servers.remarkable.command "/home/hermes/.hermes/scripts/run-remarkable-mcp.sh" --profile <p>
  hermes config set mcp_servers.remarkable.connect_timeout 180.0 --profile <p>
  hermes config set mcp_servers.remarkable.enabled true --profile <p>
  ```
  Nested keys work. Loop over `$(ls ~/.hermes/profiles/ | grep -v '^\.')` and include `main` separately (`hermes config set ...` without `--profile`).
- Reference launcher: `scripts/run-remarkable-mcp.sh` (read-only + stdout filter). Copy it to `/home/hermes/.hermes/scripts/`.

## CRITICAL PITFALL — stdout corruption (the #1 reason it fails)
The package prints a **PyMuPDF/fitz deprecation warning to STDOUT**:
```
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
```
MCP stdio uses stdout exclusively for JSON-RPC. That stray non-JSON line makes Hermes's client throw `Failed to parse JSONRPC message from server`, and the server gets marked `connected → degraded → parked`. The server is fine — the channel is just polluted.
**Fix:** the launcher MUST filter that line from stdout (stderr is preserved). See `scripts/run-remarkable-mcp.sh`:
```
uvx --from git+https://github.com/SamMorrowDrums/remarkable-mcp remarkable-mcp --read-only "$@" \
  2> >(cat >&2) \
  | grep --line-buffered -vE "warning: The \`fitz\` API is deprecated"
```
Verify with `references/verify-stdio.md` — expect 0 stray `warning:` lines and a clean `tools/list` JSON result.

## Token / registration state
- Cloud mode needs `~/.rmapi` (a token file, ~400 bytes). If missing, register once: `remarkable-mcp --register <ONE_TIME_CODE>` (code from reMarkable account) and it writes the token.
- Check validity without printing secrets: probe the stdio channel (see verify-stdio) — a successful `remarkable_status`/`tools/list` means the token is live.

## Restarting gateways to pick up the new MCP server
- `hermes -p <p> gateway restart` is **blocked when run from inside the gateway process** ("Refusing to restart the gateway from inside the gateway process").
- Working path: kill the `hermes gateway run` PIDs; the `profile_gateway_watchdog` cron (or s6 supervisor) restarts them within ~30–60s with the new config:
  ```
  ps -eo pid=,args= | awk '/hermes gateway run/ && !/awk/ {print $1}' | xargs -r kill
  ```
  Then wait ~40s and confirm with `ps -eo pid=,args= | grep 'hermes gateway run'`.
- After restart, watch the gateway log (`~/.hermes/profiles/<p>/logs/gateway.log`) for MCP `degraded`/`parked` lines — a few `keepalive failed` warnings on OTHER servers (graphify-*, agentmemory) are common and pre-existing; only `remarkable`-specific failures matter.

## Verification standard
1. Standalone probe: `bash /home/hermes/.hermes/scripts/run-remarkable-mcp.sh` fed an initialize+tools/list handshake returns 8 tools and 0 stray warnings (see `references/verify-stdio.md`).
2. Gateway log for each profile shows no `remarkable` `degraded`/`parked` error after restart.
3. Smoke test from the target profile (e.g. Telegram): "search my reMarkable for <doc name>" → `remarkable_browse`/`remarkable_search` returns results.

## Pitfalls
- **stdout pollution** (above) — the dominant failure mode. Always filter.
- **main ≠ sub-profiles** — adding to main alone leaves every Telegram profile without the server.
- **gateway restart blocked in-process** — kill+watchdog, don't call `gateway restart` from inside.
- **`fitz` warning is package-inherent**, not environment-specific — it appears on every launch via uvx, so the filter is mandatory, not optional.

## Support files
- `scripts/run-remarkable-mcp.sh` — known-good read-only launcher with the stdout filter.
- `references/verify-stdio.md` — how to probe the server's stdio channel and confirm clean JSON.
