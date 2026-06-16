---
name: obsidian
description: Read, search, and create notes in the Obsidian vault.
---

# Obsidian Vault

**Location:** Set via `OBSIDIAN_VAULT_PATH` environment variable (e.g. in `~/.hermes/.env`).

If unset, defaults to `~/Documents/Obsidian Vault`.

Note: Vault paths may contain spaces - always quote them.

## Container environment — check `/vault/` FIRST

When Hermes runs inside a Docker container (check: `test -f /.dockerenv`), the vault is often bind-mounted at `/vault/` with subdirectories like `Tasks/`, `Notes/`, `Inbox/`, `Daily/`, etc. This path is completely independent of the host path (e.g. `/root/theduyvault`).

**Before ANY vault access, probe these in order:**

```bash
# 1. Container mount (most common when in Docker)
test -d /vault/Tasks && echo "FOUND: /vault/" || echo "no /vault/"

# 2. Environment variable
test -d "$OBSIDIAN_VAULT_PATH" && echo "FOUND: $OBSIDIAN_VAULT_PATH"

# 3. Host symlink/path (rare inside container)
test -d /root/theduyvault && echo "FOUND: /root/theduyvault"
```

**Pitfall — host permission changes don't reach the container:** If `ls /root/theduyvault` fails with Permission Denied, do NOT ask the user to chmod/chown the host path. The container has its own filesystem namespace. Check `mount | grep vault` to find the actual mount point inside the container. The host path and container path are different namespaces — fixing one doesn't fix the other.

**Mount writability — ALWAYS test, don't assume:** Not all container deployments use `:ro` bind mounts. Some VPS setups mount a dedicated ext4 partition directly (e.g., `/dev/sda1[/root/theduyvault] on /vault type ext4 (rw,...)`). Before assuming read-only, test:

```bash
touch /vault/Inbox/.hermes-write-test 2>&1 && rm /vault/Inbox/.hermes-write-test && echo "WRITABLE" || echo "READ-ONLY"
```

If writable: write notes/tasks/summaries to `/vault/Inbox/` for Obsidian ingestion.
If read-only: use Hermes from the Mac host where the vault is natively writable, or ensure the bind mount is `rw`.

**Default write target — `/vault/Inbox/`, not `/home/hermes/`:** When the vault is writable from the container, all agent-generated content (notes, tasks, summaries, research) goes to `/vault/Inbox/`. The Inbox is designed as a capture zone — items are ingested/classified later by the Obsidian wiki pipeline. Never write to `/home/hermes/` when the vault Inbox is available.

**CRITICAL pitfall — cron workers are separate containers without vault mounts:** When Hermes dispatches a cron job, it often spawns a fresh container from the same Docker image. That container does NOT inherit the vault bind mounts from the gateway container. The main session container may have `/vault/` accessible while cron workers see `mount: /vault/Notes: mount point does not exist`. Fix: add the vault bind mounts to `docker-compose.yml` so every spawned container gets them. See `references/vault-docker-compose-mount.md` for the exact snippet.

**CRITICAL — cron jobs using this skill need `terminal` and `file` toolsets:** The obsidian skill relies on shell commands (`find`, `grep`, `cat`, `head`) and filesystem access. If a cron job has restricted toolsets (e.g., only `web`, `memory`, `skills`), the skill can't work. When creating or updating a cron job that uses the obsidian skill, always set `enabled_toolsets: ["web", "memory", "skills", "terminal", "file"]`.

## Cron/VPS environment checks

When an Obsidian-writing task runs from Hermes cron, first verify the runtime filesystem instead of assuming macOS paths are available. Cron jobs may run on a Linux VPS/container as the `hermes` user with `HOME=/home/hermes`, where `/Users/...` is unavailable and `/root` may be unreadable/unwritable.

Before updating or running a cron job that writes to a vault, check:

```bash
printf 'USER=%s HOME=%s PWD=%s\n' "$USER" "$HOME" "$PWD"
id
for p in "$VAULT" "$(dirname "$VAULT")"; do
  test -e "$p" && ls -ld "$p" || echo "missing $p"
  test -w "$p" && echo "writable $p" || echo "not writable $p"
done
```

For the user's VPS cron job `weekday-hermes-vault-summary`, the intended vault path is `/root/theduyvault`. Because cron runs as `hermes`, root-owned paths need permissions prepared on the VPS.

**First, check the parent directory.** `/root` is typically `0700` (drwx------) — if so, the `hermes` user cannot traverse into it at all, regardless of subdirectory permissions. Fix:

```bash
chmod o+x /root
```

**Then fix vault ownership.** The `hermes` user may not resolve by name in all root shells. Use numeric UID as a bulletproof fallback:

```bash
mkdir -p /root/theduyvault/Notes/Hermes\ Daily\ Summaries
# Preferred — by username:
chown -R hermes:hermes /root/theduyvault
# Fallback if 'hermes' user not found — use numeric UID (verify with: id hermes):
chown -R 1500:1500 /root/theduyvault
# Alternative: keep root ownership and grant ACLs:
setfacl -R -m u:hermes:rwx /root/theduyvault
setfacl -dR -m u:hermes:rwx /root/theduyvault
```

Verify access from the Hermes user before trusting it:

```bash
su -s /bin/bash hermes -c 'ls /root/theduyvault/'
```

If permission checks fail, update the cron prompt to report the exact write error instead of claiming success or silently falling back.

**CRITICAL — fix commands are HOST-ONLY, not container-executable:** The `chmod`, `chown`, and `setfacl` commands above MUST be run by root on the VPS host — they will always fail inside the Docker container (`Operation not permitted`, `sudo: command not found`, `setfacl: command not found`). Do NOT attempt them from the agent session. Instead, report the exact error and the required host-level fix in your response so the user can apply it. See `references/vault-write-errors.md` for canonical error patterns and recognition guide.

**Fallback when both paths fail:** If `/vault/` is read-only AND `/root/theduyvault/` is inaccessible, write the note to `/vault/Inbox/` if the Inbox is writable (test with `touch`). Only fall back to `/home/hermes/<descriptive-name>.md` as a last resort. Report the exact error and file path so the user can manually move it.

## Read a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
cat "$VAULT/Note Name.md"
```

## List notes

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# All notes
find "$VAULT" -name "*.md" -type f

# In a specific folder
ls "$VAULT/Subfolder/"
```

## Search

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# By filename
find "$VAULT" -name "*.md" -iname "*keyword*"

# By content
grep -rli "keyword" "$VAULT" --include="*.md"
```

## Create a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
cat > "$VAULT/New Note.md" << 'ENDNOTE'
# Title

Content here.
ENDNOTE
```

## Append to a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
echo "
New content here." >> "$VAULT/Existing Note.md"
```

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

## Task format and querying

Tasks live in `Tasks/tasks/` as individual `.md` files with YAML frontmatter:

```yaml
---
type: task
due_date: YYYY-MM-DD
tags: [tag1, tag2]
status: pending | in_progress | completed | blocked
---

# Task Title

Task description and notes here.
```

Related folders: `Tasks/ideas/` (no due date), `Tasks/bugs/` (issues), `Tasks/recurring-tasks.md` (periodic).

### Efficient batch query (many tasks → categorized lists)

Don't `cat` files one-by-one. Use `execute_code` to batch-parse frontmatter from all task files at once:

```bash
# In terminal, dump frontmatter from all task files:
for f in /vault/Tasks/tasks/*.md; do
  echo "===FILE:$f==="
  head -15 "$f"
  echo "===END==="
done
```

Then in `execute_code`, parse `due_date`, `status`, and title. Filter by `status != completed`, categorize by due_date vs `date.today()`.

### Tag taxonomy

- `admin` — administrative tasks
- `finance` — finance and investment
- `writing` — content creation
- `product` — product/salon360 work
- `research` — research tasks
- `personal` — personal tasks
- `urgent` — high priority

### Daily Briefing workflow

When asked to produce a "Daily Briefing" (compact market/task/weather summary), see `references/daily-briefing-format.md` for the full output template, data sources (yfinance, wttr.in, moon calc), and pitfalls.

### Hermes Daily Summary workflow

When asked to write a "Hermes operations daily summary" or when the `weekday-hermes-vault-summary` cron job fires, see `references/hermes-daily-summary-format.md` for the template, data-gathering commands (`hermes status`, `hermes doctor`, `hermes cron list`, `hermes mcp list`, `hermes gateway status` + disk/log checks), and pitfalls (vault path mismatch, stale gateway PID, UTC times).

## macOS host vault discovery

When running on macOS (not in a container), the obsidian-fs MCP server is often the preferred vault access method. Before probing filesystem paths, check the MCP server configuration:

```bash
# Discover the vault path from the MCP server (authoritative)
hermes mcp list  # verify obsidian-fs is enabled
```

Then use `mcp_obsidian_fs_list_allowed_directories` to get the exact vault path. This is more reliable than probing `/Users/theduy/theduyvault` or `/root/theduyvault` directly — the MCP server knows where the vault actually lives.

## Vault reorganization (consolidation)

When the user asks to find all notes on a topic and consolidate them into a project folder, follow the multi-phase workflow in `references/vault-reorganization.md`: search → classify → propose structure → batch-move → merge duplicates → aggregate → rewrite CLAUDE.md → clean up.

Key principle: prefer `mcp_obsidian_fs_*` MCP tools for all vault file operations — they handle Obsidian paths, avoid macOS permission issues, and support parallel batch moves. Skip Daily/*.md (journal entries) and System/ (infrastructure) files.
