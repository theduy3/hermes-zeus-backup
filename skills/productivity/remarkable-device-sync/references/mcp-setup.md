# reMarkable MCP setup (Hermes host)

## Default choice
**SamMorrowDrums/remarkable-mcp**, cloud mode, on the profile that serves Telegram (usually default).

## Auth
1. https://my.remarkable.com/device/desktop/connect → one-time code
2. As gateway OS user:
   ```bash
   uvx --from git+https://github.com/SamMorrowDrums/remarkable-mcp \
     remarkable-mcp --register CODE
   ```
3. Prefer `~/.rmapi` readable by gateway; else `REMARKABLE_TOKEN` in MCP env

## Add to Hermes
```bash
hermes mcp add remarkable \
  --command uvx \
  --args --from git+https://github.com/SamMorrowDrums/remarkable-mcp remarkable-mcp \
  --connect-timeout 120
```
Restart gateway. Tools: `mcp_remarkable_*`.

## Topology
| Mode | Remote VPS |
|---|---|
| Cloud + Connect | Yes (default) |
| USB / local-dir / SSH | Only if host reaches tablet or desktop cache |

## Alternatives (when not default)
- praveensehgal/remarkable-mcp — similar, smaller
- wavyrai/rm-mcp — cloud read-focused
- remarkable-mcp.rs — page images, no OCR
- remarkable-brain — local FTS; often Anthropic on sync → skip if OpenAI-only

## Hardening
Read-only / `REMARKABLE_ROOT_PATH` until trusted. Token = full library. No public unauthenticated HTTP MCP. Per-profile enable. Undocumented cloud API may break.
