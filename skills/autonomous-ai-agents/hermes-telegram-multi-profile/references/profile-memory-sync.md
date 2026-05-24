# Profile Memory Sync

When profiles are cloned or created in bulk, the durable memory files
(MEMORY.md and USER.md) can drift apart. This is a maintenance step to
bring them back in sync from the source-of-truth profile.

## Where memory lives

Each profile has its own memory files:

```
~/.hermes/memories/MEMORY.md        # Agent's personal notes
~/.hermes/memories/USER.md          # User profile / preferences

~/.hermes/profiles/<name>/memories/MEMORY.md
~/.hermes/profiles/<name>/memories/USER.md
```

These are injected into every session's system prompt (at the top, before
skills). The `memory` tool writes to these files, NOT to the SQLite state.db.

## How to check for drift

```bash
for p in . profiles/*/; do
  mp="${p}memories"
  [ -d "$mp" ] && echo "${p#profiles/} $(wc -c < "$mp/MEMORY.md" 2>/dev/null || echo 0)B $(wc -c < "$mp/USER.md" 2>/dev/null || echo 0)B"
done
```

Different sizes mean different content — profiles are out of sync.

## How to sync

Copy from the source-of-truth profile (usually the main orchestrator) to
all others:

```bash
for p in thor zeus alan mira turing finance charles maily 3r charlesbourg ss catthew; do
  mp="$HOME/.hermes/profiles/$p/memories"
  [ -d "$mp" ] && cp ~/.hermes/memories/MEMORY.md "$mp/" && cp ~/.hermes/memories/USER.md "$mp/" && echo "$p: synced"
done
```

Or use python for a one-liner:

```python
import shutil, os
src = os.path.expanduser("~/.hermes/memories")
profiles_dir = os.path.expanduser("~/.hermes/profiles")
for name in os.listdir(profiles_dir):
    dst = os.path.join(profiles_dir, name, "memories")
    if os.path.isdir(dst):
        shutil.copy2(os.path.join(src, "MEMORY.md"), dst)
        shutil.copy2(os.path.join(src, "USER.md"), dst)
```

## When to sync

- After cloning profiles with `hermes profile create --clone`
- After restoring from GitHub backup
- When profiles start giving stale or wrong memory responses
- As part of regular profile maintenance
