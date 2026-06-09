---
name: hermes-skill-installation
description: Use when installing, importing, repairing, or exposing Hermes/OpenClaw/Claude-style skills as Hermes slash commands or shell commands, especially when hub installs are blocked and a safe manual install path is needed.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, skills, slash-commands, installation, manual-import, quick-commands]
    related_skills: [hermes-agent-skill-authoring]
---

# Hermes Skill Installation and Command Exposure

## Overview

Use this skill for operational work around Hermes skills: installing third-party skills, verifying that Hermes can load them, making them available as slash commands, and optionally creating shell wrappers for scripts bundled inside a skill.

Hermes automatically turns installed skills under `~/.hermes/skills/**/SKILL.md` into slash commands named from the skill frontmatter `name`. For example, a skill with `name: last30days` becomes `/last30days` after the command map is refreshed.

## When to Use

- User asks to install a skill from GitHub or another external source.
- `hermes skills install ...` blocks a community skill after a security scan, and the user explicitly approves a manual install anyway.
- User asks to “make this skill into a command.”
- A skill has a bundled executable script and the user wants a direct shell command too.
- You need to verify whether a newly installed skill is discoverable by Hermes slash-command resolution.

Do not use this for authoring a new reusable skill from scratch; use `hermes-agent-skill-authoring` for that.

## Standard Workflow

1. Inspect the source tree before installing.
   - Look for `skills/<name>/SKILL.md`.
   - Check `HERMES_SETUP.md`, `README.md`, and the frontmatter in `SKILL.md` for expected paths, commands, bins, and optional env vars.

2. Try the supported installer first.

   ```bash
   hermes skills install owner/repo --force
   ```

3. If the hub/security scan blocks the install:
   - Report that it was blocked and why at a high level.
   - Do not bypass silently.
   - Ask for explicit user approval before manual installation.

4. If approved, install only the actual skill directory, not the entire repository.

   ```bash
   SRC=/tmp/<repo>/skills/<skill-name>
   DEST="$HOME/.hermes/skills/<category>/<skill-name>"
   rm -rf "$DEST"
   mkdir -p "$(dirname "$DEST")"
   cp -a "$SRC" "$DEST"
   git -C /tmp/<repo> rev-parse HEAD > "$DEST/.installed_from_commit" 2>/dev/null || true
   ```

   Prefer a category that matches the skill (`research`, `productivity`, etc.).

5. Verify skill load and command discovery using Hermes' own venv Python when importing Hermes internals.

   ```bash
   PYTHON="$HOME/.hermes/hermes-agent/venv/bin/python"
   PYTHONPATH="$HOME/.hermes/hermes-agent" "$PYTHON" - <<'PY'
   from agent.skill_commands import scan_skill_commands, resolve_skill_command_key
   cmds = scan_skill_commands()
   print('/skill-name in commands:', '/skill-name' in cmds)
   print('resolved:', resolve_skill_command_key('skill-name'))
   print('info:', cmds.get('/skill-name', {}))
   PY
   ```

   Important: the system `python3` may not have Hermes dependencies such as `yaml`; use the Hermes venv when importing `tools.skills_tool` or `agent.skill_commands`.

6. Tell the user how to refresh the current session.

   ```text
   /reload-skills
   ```

   Existing sessions can cache the slash-command map. New sessions generally see the installed skill automatically.

## Making a Skill Into a Hermes Slash Command

No extra command file is usually needed. Hermes scans installed `SKILL.md` files and creates slash commands automatically:

- Frontmatter `name: last30days` -> `/last30days`
- Frontmatter `name: gif-search` -> `/gif-search`

Verification:

```bash
PYTHON="$HOME/.hermes/hermes-agent/venv/bin/python"
PYTHONPATH="$HOME/.hermes/hermes-agent" "$PYTHON" - <<'PY'
from agent.skill_commands import build_skill_invocation_message
msg = build_skill_invocation_message('/last30days', 'AI news --days=7')
print('built:', bool(msg))
if msg:
    print('\n'.join(msg.splitlines()[:5]))
PY
```

If `built: True`, the slash command is wired.

## Adding a Direct Shell Command Wrapper

If the skill includes a script that can run standalone, create a wrapper under `~/.local/bin`.

Example:

```bash
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/last30days" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$HOME/.hermes/skills/research/last30days"
exec python3 "$SKILL_DIR/scripts/last30days.py" "$@"
SH
chmod +x "$HOME/.local/bin/last30days"
```

Verify:

```bash
$HOME/.local/bin/last30days --help
```

Only claim the bare command works (`last30days ...`) if `~/.local/bin` is on PATH in the user's shell. Otherwise report the absolute wrapper path.

## Common Pitfalls

1. Skipping the supported installer.
   - Always try `hermes skills install ...` first unless the user explicitly asked for a local/manual install.

2. Manually copying the whole repo.
   - Copy only `skills/<skill-name>/` into `~/.hermes/skills/<category>/<skill-name>/`. Whole repos often include tests, plans, docs, or metadata that do not belong in the runtime skill directory.

3. Treating a blocked hub scan as permission to bypass.
   - A dangerous verdict requires explicit user approval before manual install.

4. Using system Python for Hermes internals.
   - `python3` may fail with missing packages. Use `~/.hermes/hermes-agent/venv/bin/python` with `PYTHONPATH=~/.hermes/hermes-agent`.

5. Forgetting session refresh.
   - Installed skills may not appear in the current CLI/TUI command list until `/reload-skills` or a new session.

6. Confusing slash commands with shell commands.
   - `/last30days` is a Hermes skill command. `last30days` is a shell wrapper and must be created separately.

## Verification Checklist

- [ ] Source repo was inspected for `skills/<name>/SKILL.md` and setup docs.
- [ ] Supported installer was tried, or manual install was explicitly requested.
- [ ] Manual bypass happened only after explicit approval when the security scan blocked.
- [ ] Installed path contains `SKILL.md` and expected scripts/assets/references.
- [ ] `skill_view <name>` or Hermes command discovery can load the skill.
- [ ] Slash command resolves via `agent.skill_commands`.
- [ ] Any shell wrapper is executable and its `--help` or smoke test runs.
- [ ] User was told to run `/reload-skills` if the current session does not show the command.
