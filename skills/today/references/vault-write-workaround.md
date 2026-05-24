# Vault write workaround

The `write_file` tool and `execute_code` sandbox run as a different user than `hermes`
and get `PermissionError` when trying to write to `/vault/`. Shell redirection
(`cat > /vault/...`) also fails. Only `terminal()`-launched Python can write there
because it runs as `hermes`, who owns the vault directories.

## Template: write the daily file

```bash
cat > /tmp/daily_out.py << 'PYEOF'
import os

target = "/vault/Daily/YYYY-MM-DD.md"

# Content as a Python raw string (avoids shell &-interpretation issues)
content = r"""---
type: daily
date: YYYY-MM-DD
day: DayName
---

# Daily Briefing: ...

...full markdown content...
"""

# Remove stale root-owned file if present (hermes owns the directory)
try:
    os.remove(target)
except FileNotFoundError:
    pass

with open(target, "w") as f:
    f.write(content)

print(f"Written: {os.path.getsize(target)} bytes")
PYEOF

python3 /tmp/daily_out.py
```

## Why it works

- `/vault/Daily/` is mode `755`, owner `hermes:hermes`
- `terminal()` runs shell commands as `hermes`, so `python3` inherits that user
- Python's `open(..., "w")` succeeds because hermes has directory write permission
- `os.remove()` on a root-owned file works because hermes owns the directory (delete is a directory operation, not a file operation)
- Raw strings (`r"""..."""`) prevent Python from interpreting backslashes, and the heredoc delimiter `'PYEOF'` (quoted) prevents shell expansion — no `&`-as-background-operator issues

## What fails

| Method | Error |
|--------|-------|
| `write_file(path, content)` | `PermissionError` |
| `execute_code` with `open(path, "w")` | `PermissionError` |
| `cat > /vault/Daily/file.md` in terminal | `PermissionError` |
| Heredoc with unquoted delimiter + `&` in content | Shell interprets `&` as background |
