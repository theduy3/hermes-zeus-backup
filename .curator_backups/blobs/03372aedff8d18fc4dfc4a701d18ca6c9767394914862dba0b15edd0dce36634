---
name: external-mcp-integrations
description: "Use when wiring external MCP servers into Hermes."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
metadata:
  hermes:
    tags: [MCP, Integrations, Devices, Notes, Cron, Gateways]
    category: mcp
    related_skills: [native-mcp, mcporter]
---

# External MCP Integrations

Class-level playbook for connecting **third-party MCP servers** to Hermes so tools work from CLI, messaging gateways, and cron. Complements (does not replace) the `native-mcp` skill for client mechanics.

## When to Use

- User wants Hermes to talk to an external system via MCP (tablet, notes app, SaaS, local daemon)
- Planning research-only first, then later install
- Choosing transport (stdio vs HTTP), auth, profile scope, OCR/vision, or cron digests on top of MCP tools

## Core Rules

1. **Research before install** when the user says so — capture options, constraints, and a recommended path; do not mutate config.
2. **Hermes is the MCP client.** A vendor AI subscription (e.g. Claude) does not by itself unlock device APIs; the device/cloud account + MCP server do.
3. **Match transport to host topology.** Remote VPS/Docker Hermes cannot use USB-only device modes unless the device is reachable from that host. Prefer cloud/API tokens for always-on remote access.
4. **Config lives under `mcp_servers`** (see `native-mcp`). Stdio: `command` + `args` + `env`. Secrets only via `env` (filtered subprocess environment).
5. **Restart required.** Successful `hermes mcp add` / config edit does **not** hot-inject tools into the current conversation. Restart the target profile's agent/gateway, then smoke-test in a new session.
6. **Per-profile.** Each Hermes profile/gateway has its own process and config. Enable the server on every profile that should answer those questions (default ≠ named profiles).
7. **Cron inherits tools from the profile that runs the job.** Fresh session, self-contained prompt; scope reads (path, page count) and prefer change-detection for digests.
8. **Harden first.** Prefer read-only flags / narrow root paths; treat device tokens as full-access secrets; do not expose unauthenticated Streamable HTTP beyond loopback.

## Standard Implementation Sequence

1. Confirm account prerequisites (subscription, API, device pairing page).
2. Pick server implementation (stars, maintenance, transport modes, write surface).
3. Register/auth on the **same OS user** that runs the gateway when possible.
4. Add `mcp_servers.<name>` with minimal env secrets.
5. Restart gateway(s) for the chosen profile(s).
6. Smoke: status/list → targeted read → search → (optional) write in a sandbox folder.
7. Only then: cron digests or multi-gateway rollout.

## Device / notes: reMarkable

Full notes: `references/remarkable-mcp.md`.

Summary defaults:

- Prefer **SamMorrowDrums/remarkable-mcp** (cloud) on remote Hermes
- Requires **reMarkable Connect** for cloud; one-time code → `REMARKABLE_TOKEN` / `~/.rmapi`
- Tools: browse / recent / read / search / image (+ manage in write modes)
- Handwriting: sampling OCR, Google Vision, Tesseract, or page-image + vision
- Cron: few planner pages or recent-only — never full-library OCR every tick
- Avoid Anthropic-hardwired extractors when the user is OpenAI-only (e.g. some "brain" pipelines)

## Research Fallback When Managed Web Extract Is Unavailable

Still research with primary sources:

- GitHub API: `https://api.github.com/repos/<owner>/<repo>`
- Raw README: `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/README.md`
- Repo search API for alternate implementations

Do not invent tool lists from memory when the README is fetchable this way.

## Session Handoff (research-done, implement later)

When the user parks the work:

1. `hermes sessions rename <id> "<clear title>"`
2. `hermes sessions pin <id>`
3. `hermes sessions export --session-id <id> --format md <dir>`
4. Write a short `RESUME.md` in a project dir under `~/.hermes/projects/`
5. Optional vault idea: `/vault/Tasks/ideas/<kebab>.md` with session link + next actions

## Pitfalls

- Configuring USB/local-desktop modes on a host that never sees the device
- Expecting MCP tools mid-session without restart
- Enabling MCP on one profile while the user messages another
- Dumping long install steps during an explicit research-only turn
- Full-corpus OCR or unbounded search in cron
- Committing tokens or putting them in chat

## Related

- `native-mcp` — Hermes client config reference (user-owned here; run `hermes curator adopt native-mcp` before curator patches)
- `mcporter` — ad-hoc CLI calls without permanent config
- `references/remarkable-mcp.md` — reMarkable deep dive
