---
name: paperclip-company-setup
description: Set up Paperclip companies as portable markdown packages, with Hermes agents, org charts, projects, starter tasks, routines, and import validation.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [paperclip, company, agents, orchestration, hermes, startup, import]
---

# Paperclip Company Setup

Use this when the user wants to run a business/company using Paperclip, create a Paperclip company package, configure Hermes agents for Paperclip, or turn a business idea into a Paperclip org chart with projects and tasks.

Do not confuse this with generic Hermes configuration. Paperclip company setup is primarily a markdown package authoring/import workflow.

## Core workflow

1. Gather company context
   - company name and one-sentence mission
   - product/service and target market
   - current stage
   - unfair advantage
   - 30-day objective or first milestone
   - desired agent functions: CEO, product, research, sales, engineering, content, finance, ops, etc.
   - existing repos, docs, websites, demos, or notes

2. Inspect Paperclip readiness
   - Check whether Paperclip is already running before trying to import.
   - Typical health URL: `http://127.0.0.1:3100/api/health`
   - If not running, use `npx --yes paperclipai onboard --yes --bind loopback`, then run Paperclip in background with `npx --yes paperclipai run`.

3. Verify adapter availability
   - Recent Paperclip builds include `hermes_local` as a built-in adapter.
   - Check adapters via `GET /api/adapters` or the UI before installing anything.
   - Do not assume `hermes-paperclip-adapter` must be installed as a plugin; it may already be built in.

4. Author a portable company package

   Minimal structure:

   ```text
   company-root/
   ├── COMPANY.md
   ├── .paperclip.yaml
   ├── agents/<agent-slug>/AGENTS.md
   ├── projects/<project-slug>/PROJECT.md
   ├── projects/<project-slug>/tasks/<task-slug>/TASK.md
   └── tasks/<routine-slug>/TASK.md
   ```

5. Configure `.paperclip.yaml`
   - Put Paperclip-specific runtime details here, not in base package markdown.
   - Agent adapter config belongs under `agents.<slug>.adapter`.
   - For Hermes agents, use `type: hermes_local`.
   - Keep secrets out of files; declare requirements only.

   Example:

   ```yaml
   schema: paperclip/v1
   agents:
     ceo:
       adapter:
         type: hermes_local
         config:
           provider: openai-codex
           model: gpt-5.5
           timeoutSec: 600
           maxIterations: 50
           persistSession: true
           toolsets: terminal,file,web,skills
   routines:
     weekly-review:
       triggers:
         - kind: schedule
           cronExpression: "0 9 * * 1"
           timezone: America/Vancouver
   ```

6. Validate with dry-run before import

   ```bash
   npx --yes paperclipai company import /path/to/company-package --dry-run --yes --json
   ```

   Success criteria:
   - errors: empty
   - warnings: empty or understood
   - planned agents/projects/issues match intent

7. Import only after dry-run passes

   ```bash
   npx --yes paperclipai company import /path/to/company-package --yes --json | tee /tmp/<company>-import-result.json
   ```

8. Verify the import with CLI reads, not only the import JSON
   - `company import --json` may report created company/agents/projects while omitting imported issues/routines from the final summary.
   - Verify company, agents, and issues explicitly:

   ```bash
   npx --yes paperclipai company get <company-id> --json
   npx --yes paperclipai agent list --company-id <company-id> --json
   npx --yes paperclipai issue list --company-id <company-id> --json
   ```

   Also verify each Hermes agent's persisted `adapterConfig` contains the intended `model`, `provider`, and `hermesCommand`/env if needed. If imported agents have `provider: openai-codex` but no `model`, Paperclip's Hermes adapter falls back to its built-in default `anthropic/claude-sonnet-4`, causing runs like `model=anthropic/claude-sonnet-4, provider=openai-codex` and Codex 400 errors. Patch the agents via `PATCH /api/agents/<id>` with `{adapterConfig, replaceAdapterConfig:true}` and reset status to `idle`, then run a direct adapter smoke test.

   Notes:
   - Use `--company-id`, not `--company`, for `issue list`.
   - Recurring tasks may be imported as routines and not appear in the normal issue list output.

9. If the user needs to access the local Paperclip UI/API from another machine, handle networking explicitly
   - Remember that `127.0.0.1` means the user's current machine, not the VPS. If Paperclip is bound to loopback on the server, the user's Mac will get `ERR_CONNECTION_REFUSED` at `http://127.0.0.1:3100` unless a tunnel/proxy is in place.
   - Prefer SSH local port forwarding: `ssh -L 3100:127.0.0.1:3100 <ssh-user>@<server-ip>`, then open `http://127.0.0.1:3100` locally.
   - In containerized Hermes, adding a key to `/home/hermes/.ssh/authorized_keys` may not affect the VPS host SSH daemon. If SSH still prompts/fails, switch to the actual host SSH user or a temporary trusted proxy instead of asking the user to retry the same command.
   - See `references/remote-access-and-port-forwarding.md` for the full troubleshooting pattern.

9. If the user needs to access Paperclip from a local machine while it runs on a VPS/container, use the remote-access pattern before exposing public ports
   - `127.0.0.1` in the user's browser means the user's machine, not the VPS/container.
   - Prefer SSH local port forwarding from the user's machine to the VPS host: `ssh -L 3100:127.0.0.1:3100 <host-user>@<vps-ip>`, then open `http://127.0.0.1:3100` locally.
   - Be explicit about where each command runs: user's Mac, VPS host/provider console, or Hermes container.
   - Do not assume the container user exists as a host SSH user. If `chown hermes:hermes` fails with `invalid user`, create the host user first or use the existing host account such as `root`/`ubuntu`.
   - Avoid treating a container-side key update as sufficient for host SSH. See `references/remote-access-vps-container.md`.

9. If the user wants Discord to operate the company, implement the smallest tested bridge first
   - First clarify whether Discord is actually required now. Local Paperclip/Hermes automation does not require Discord; Discord is only an input/output layer.
   - Finish and verify the local path first: Paperclip server → company/agents → helper script → issue create/list/get/comment/checkout/release/done → smoke test.
   - Prefer the minimal path before building a native bot: Discord user → Hermes Discord gateway profile → terminal helper script → Paperclip CLI/API → Paperclip issue/comment/checkout → Hermes local agent.
   - Create a company-local helper script that pins company/project/agent IDs and wraps `paperclipai issue list/create/comment/checkout/get/release/update-done` so Hermes agents can invoke it safely.
   - Include local-ops verbs in the helper (`health`, `smoke`, `open`, `dashboard`, `activity`, `get`, `release`, `done`) because Paperclip issues can auto-start, lock, or enter recovery states; operators need safe commands to inspect and resolve them without remembering raw CLI flags.
   - Smoke-test at least `health`/`smoke`, `company`, `agents`, `open`, and one issue-level read such as `get <issue-id>`; also dry-run import the company package.
   - Write a local automation doc before Discord docs. Keep Discord docs framed as optional unless the user explicitly asks to operate from Discord now.
   - If the user asks to chat with agents like employees in Discord, start with one CEO/dispatcher Discord bot/profile, then add per-employee bots later only if requested. Use `DISCORD_ALLOW_BOTS=mentions` for bot-to-bot handoffs and avoid `DISCORD_ALLOW_BOTS=all` to prevent loops. See `references/discord-employee-agent-setup.md`.
   - A Discord bot token can validate and the Hermes gateway can connect even when the bot is not in the target server. Verify guild/channel discovery separately; if guilds are empty, provide OAuth invite links and report the state as "connected but not invited" rather than continuing Discord tests.
   - When changing a Discord employee profile's model/provider, use `hermes -p <profile> config set model.default <model>` and `hermes -p <profile> config set model.provider <provider>`, then restart or relaunch the profile gateway with `HERMES_HOME=~/.hermes/profiles/<profile> hermes -p <profile> gateway run`. Verify with `hermes -p <profile> gateway status`, `hermes profile list`, `ps`, the first lines of `config.yaml`, and recent `logs/gateway.log` before reporting success.
   - A Discord bot token can validate and the Hermes gateway can connect even when the bot is not in the target server. Verify guild/channel discovery separately; if guilds are empty, provide OAuth invite links and report the state as "connected but not invited" rather than continuing Discord tests.
   - When changing per-employee Hermes profile model/provider settings, remember config changes do not affect already-running gateways. Update the profile config, restart the matching gateway, then verify both the config and the live process. A practical verification is: process start time must be after the profile `config.yaml` mtime, `hermes profile list` shows the new model, and the gateway log shows the bot reconnected.
   - In Docker/manual multi-profile gateways, `hermes -p <profile> gateway restart` may run the gateway in the foreground and appear to hang. Prefer a controlled stop/start: stop the old `hermes -p <profile> gateway run` process, then launch the gateway with explicit `HERMES_HOME=/home/hermes/.hermes/profiles/<profile>` in a tracked background process; do not use shell-level `&` inside a foreground terminal tool call.
   - When testing Discord mentions, verify the user mentioned the actual bot user, not a Discord role (`<@&...>`). If they want plain messages in a trusted channel, put that channel in `DISCORD_FREE_RESPONSE_CHANNELS` and restart the profile gateway.
   - Comment on the controlling Paperclip issue with script path, docs path, test results, and the known limitation that this is not yet a native Discord slash-command bot.
   - Mark the Paperclip issue done only after the helper script and docs are both written and smoke-tested.

## Important package rules and pitfalls

- For completed work that Paperclip automation keeps re-locking or recovering as `stranded_assigned_issue` / `adapter_failed`, use the manual-resolution pattern in `references/manual-resolution-and-access-verification.md`: `issue release <id>` first, then `issue update --status done ... --comment ...`.
- For follow-up issues and live execution handoffs, use `references/execution-monitoring-and-followups.md`: create/assign, fetch with `issue get <id> --json`, report `status` and `executionRunId`, then poll instead of claiming completion before `completedAt` or `status: done` verifies it.
- If creating a follow-up issue with an assignee, Paperclip may auto-start execution immediately. A 409 on a later manual checkout can mean the issue is already running, not that creation failed; verify with `issue get <id> --json`.
- When a follow-up creates a user-visible task, write the Obsidian task into `/vault/Tasks/tasks/<kebab-title>.md` using the Tasks frontmatter convention, not the working directory.
- For project deliverables, prefer writing both a local repo doc and a Paperclip managed `_default` work product, then cite both paths in the issue comment.
- `COMPANY.md`, `AGENTS.md`, `PROJECT.md`, and `TASK.md` use YAML frontmatter plus markdown body.
- Agent instructions belong in the body of `AGENTS.md`.
- Runtime-specific adapter config belongs in `.paperclip.yaml`, not in `AGENTS.md`.
- Recurring tasks must have `recurring: true` and must declare `project: <project-slug>` if importing as Paperclip routines.
- If `AGENTS.md` references a skill by name, Paperclip may warn if that skill is not present inside the package. Either vendor the skill under `skills/<name>/SKILL.md` or omit skill references and rely on the Hermes runtime's own skill system.
- A private/inaccessible GitHub repo should be represented as a task for the engineering agent to request access; do not invent repo facts.
- Avoid machine-local absolute paths in package content except when giving the user the local package location after creation.
- Keep package names and slugs stable, lowercase, and URL-safe.

## Recommended first company artifacts

For a new startup/company, create:

- `COMPANY.md`: mission, market, product, unfair advantage, 30-day goal
- CEO agent: prioritization and delegation
- Product lead: roadmap, specs, demo-readiness
- GTM lead: ICP, positioning, offer, launch plan
- Sales rep: prospecting, outreach, follow-up, demos
- Market researcher: competitors, directories, lead sources, buyer pain
- Engineer: repo inspection, MVP fixes, demo blockers
- One 30-day launch project
- 3-7 seed tasks directly tied to the milestone
- 1-2 recurring routines, such as daily outreach and weekly pipeline review

## References

- `references/wylios-salonx.md` — concrete Wylios/SalonX setup example, including org shape, Discord operations expansion, recurring-task import pitfalls, validation/import results, and post-import verification commands.
- `references/remote-access-vps-container.md` — troubleshooting remote browser access when Paperclip is healthy on VPS/container loopback but unavailable from the user's local machine; covers SSH tunneling, host-vs-container SSH users, and public port pitfalls.
- `references/manual-resolution-and-access-verification.md` — workflow for inaccessible/private repo verification, dual report locations, and manually resolving Paperclip issues stuck in `stranded_assigned_issue` / `adapter_failed` recovery.
- `references/local-automation-before-discord.md` — local Paperclip/Hermes automation pattern to finish before Discord: helper verbs, smoke tests, and terse reporting format.
- `references/discord-employee-agent-setup.md` — Discord employee-agent setup: CEO dispatcher bot first, per-employee bots later, allowlists/free-response channels, and bot-to-bot loop prevention.
- `references/execution-monitoring-and-followups.md` — pattern for creating/assigning follow-up issues, recognizing auto-started execution runs, polling stable status fields, and writing related Obsidian tasks.
- `references/execution-monitoring-and-followups.md` — pattern for creating/assigning follow-up issues, recognizing auto-started execution runs, polling stable status fields, and writing related Obsidian tasks.
- `references/execution-monitoring-and-followups.md` — pattern for creating/assigning follow-up issues, recognizing auto-started execution runs, polling stable status fields, and writing related Obsidian tasks.
- `references/discord-employee-agent-gateway.md` — setup pattern for Discord-facing company/employee bots, owner allowlists, safe bot-to-bot mentions, gateway verification, and VPS SSH tunneling for local Paperclip UI access.

## User-facing output style

For this user, keep the final report terse:

- path created
- Paperclip server/API status
- dry-run result: errors/warnings/agent/project/issue counts
- exact import command
- any blockers, such as private repo access

Avoid long explanations unless asked.