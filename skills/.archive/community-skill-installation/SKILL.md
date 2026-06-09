---
name: community-skill-installation
description: Install and verify third-party/community Hermes skills, including safe handling when the hub security scan blocks installation and the user explicitly authorizes a manual install.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, skills, community-skills, installation, security-scan, verification]
    related_skills: [hermes-agent, hermes-agent-skill-authoring]
---

# Community Skill Installation

Use this when the user asks to install a third-party/community Hermes skill from GitHub or a non-bundled source.

## Workflow

1. Load `hermes-agent` first for current Hermes CLI commands and skill paths.
2. Check whether the skill already exists:
   - `hermes skills list`
   - search `~/.hermes/skills/` for the skill name if needed.
3. Try the official install path first:
   - `hermes skills install owner/repo --force`
4. Read the install output carefully.
   - If the hub security scan allows it, continue to verification.
   - If the scan blocks it as `DANGEROUS`, do not bypass silently.
5. If blocked, summarize the verdict and ask the user whether to proceed manually.
   - Offer choices such as: leave blocked, manually install anyway, install only the skill subdirectory, or show scan findings.
6. Only after explicit user approval, manually install.

## Manual install pattern after explicit approval

For repos with a `skills/<skill-name>/SKILL.md` layout:

```bash
rm -rf /tmp/<repo>
git clone --depth 1 https://github.com/<owner>/<repo> /tmp/<repo>
DEST="$HOME/.hermes/skills/<category>/<skill-name>"
rm -rf "$DEST"
mkdir -p "$(dirname "$DEST")"
cp -a /tmp/<repo>/skills/<skill-name> "$DEST"
(cd /tmp/<repo> && git rev-parse HEAD) > "$DEST/.installed_from_commit"
```

Prefer installing only the `skills/<skill-name>` subtree rather than the entire repository when manually bypassing a hub block. This reduces copied surface area while preserving the actual skill files.

## Verification

After install, verify all of the following:

```bash
hermes skills list | grep -i '<skill-name>' || true
python3 --version
node --version || true
```

Then load the skill:

```text
skill_view(name='<skill-name>')
```

If the skill includes runnable scripts, run the safest no-side-effect checks available, for example:

```bash
python3 ~/.hermes/skills/<category>/<skill-name>/scripts/<entrypoint>.py --help
python3 ~/.hermes/skills/<category>/<skill-name>/scripts/<entrypoint>.py --diagnose
```

Report:
- installed path
- version from `SKILL.md`
- source commit if recorded
- verification commands that succeeded
- available vs missing optional sources/providers, if the skill has diagnostics

## Pitfalls

- `--force` does not override a `DANGEROUS` hub security verdict. Manual copy is a bypass and needs explicit user approval.
- Do not edit protected bundled skills when recording this workflow; create or update a non-protected umbrella skill instead.
- Do not turn transient missing optional credentials into durable negative memories. Report them as current diagnostic state only.
- If the user prefers terse output, keep the final report short: path, version, commit, verification status, and usage command.
