---
name: obsidian
description: Read, search, and create notes in the Obsidian vault.
---

# Obsidian Vault

**Location:** Set via `OBSIDIAN_VAULT_PATH` environment variable (e.g. in `~/.hermes/.env`).

If unset, defaults to `~/Documents/Obsidian Vault`.

Note: Vault paths may contain spaces - always quote them.

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

For the user's VPS cron job `weekday-hermes-vault-summary`, the intended vault path is `/root/theduyvault`. Because cron runs as `hermes`, root-owned paths need permissions prepared on the VPS, for example:

```bash
mkdir -p /root/theduyvault/Notes/Hermes\ Daily\ Summaries
chown -R hermes:hermes /root/theduyvault
# or keep root ownership and grant ACLs:
setfacl -R -m u:hermes:rwx /root/theduyvault
setfacl -dR -m u:hermes:rwx /root/theduyvault
```

If permission checks fail, update the cron prompt to report the exact write error instead of claiming success or silently falling back.

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
