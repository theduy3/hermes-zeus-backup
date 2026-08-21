# reMarkable MCP ↔ Hermes

Session-backed class notes (research 2026-08-20).
Session: @session:default/20260820_183206_0f8a25
Handoff: ~/.hermes/projects/remarkable-mcp/RESUME.md

## Product split

| Piece | Role |
|---|---|
| reMarkable **Connect** | Required for **cloud** library access |
| Claude / Hermes / other MCP client | Client only — does not unlock the tablet API |
| MCP server process | USB web, local desktop cache, cloud, or SSH |

No special "Remarkable Claude subscription." Cloud needs Connect; the AI is the client.

## Server choice

1. **SamMorrowDrums/remarkable-mcp** — default. USB / local-dir / cloud / SSH; caching; stdio + HTTP; root-path filter; read-only
2. praveensehgal/remarkable-mcp — similar tools (`remarkable-mcp` / `remarkable-mcp-rw`); smaller
3. wavyrai/rm-mcp — cloud-first, mostly read
4. Bradley-Butcher/remarkable-mcp.rs — cloud, page images, no OCR
5. gabrielanhaia/remarkable-brain — local SQLite/FTS; heavier; often Anthropic vision on sync (skip if OpenAI-only)

Common CLI:

```bash
uvx remarkable-mcp --register <ONE_TIME_CODE>
uvx remarkable-mcp              # cloud default
uvx remarkable-mcp --usb
uvx remarkable-mcp --ssh
uvx remarkable-mcp --local-dir
```

Confirm flags on the chosen README before apply.

## Transport for remote Hermes

| Mode | Use on remote VPS/Docker |
|---|---|
| **Cloud** | **Yes — default** (Connect + token) |
| USB web | Only if host reaches tablet (`10.11.99.1` or LAN IP with USB web enabled) |
| Local directory | Only if desktop app cache is on the Hermes host |
| SSH | Developer mode; power users only |

## Cloud auth

1. One-time code: https://my.remarkable.com/device/desktop/connect
2. `uvx remarkable-mcp --register CODE` → `~/.rmapi` and/or token print
3. Hermes subprocess: pass `REMARKABLE_TOKEN` in `mcp_servers.*.env` when `~/.rmapi` is not readable by the gateway user
4. Token = full library access — secret store only

## Hermes config (conceptual)

```yaml
mcp_servers:
  remarkable:
    command: uvx
    args: ["remarkable-mcp"]
    env:
      REMARKABLE_TOKEN: "..."
      # REMARKABLE_ROOT_PATH: "/Planner"
      # REMARKABLE_OCR_BACKEND: "sampling"  # google | tesseract | auto
      # GOOGLE_VISION_API_KEY: "..."
    timeout: 180
    connect_timeout: 60
```

Restart gateway after change. Tools appear as `mcp_remarkable_*`.

Typical upstream tools: `remarkable_status`, `browse`, `recent`, `read`, `search`, `image`; write modes may add upload/mkdir/move/delete.

## OCR

- Typed / Type Folio / PDF text: usually fine without OCR
- Sampling: client LLM via MCP sampling (Hermes supports sampling)
- Google Vision: best handwriting consistency; paid after free tier
- Tesseract: offline, weak on handwriting
- Page image + Hermes vision: alternative without separate OCR service

Cron: scope planner path + few pages or `recent` + change detection. Never full-library OCR every tick.

## Workflows

**On-demand gateway:** browse/search/read from Telegram/Discord/CLI once that profile's gateway has the server.

**Cron planner digest:** status/recent or fixed path → read N pages → short summary → deliver. Optional silent tick when content hash unchanged.

## Hardening

- Read-only / root-path scope until trusted
- No unauthenticated Streamable HTTP beyond loopback
- Enable on each profile that should answer
- Undocumented cloud sync protocol — can break; not endorsed by reMarkable AS

## Implement checklist

1. Confirm Connect active
2. Pick server (default SamMorrowDrums)
3. Register token as gateway OS user
4. Add `mcp_servers.remarkable`
5. Restart profile gateway(s)
6. Smoke: status → recent → browse → read 1–3 pages → search
7. Add scoped cron only after smoke passes

## Pitfalls

- Claude sub alone ≠ tablet API
- USB mode on host with no device path
- Expecting tools without restart
- Wrong profile enabled
- Tokens in chat/git
- remarkable-brain when Anthropic is disallowed
