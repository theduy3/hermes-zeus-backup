# graphify-daily-refresh OOM / SIGKILL

Job: `graphify-daily-refresh` (`5a9aa5056402`), script `graphify_refresh.py`, `no_agent=true`.

Companion: this umbrella’s `references/no-agent-script-oom.md` (general pattern).
Integration skill (user-owned; may already note OOM briefly): `graphify-hermes-vault-integration`.
Script SoT: `/home/hermes/.hermes/scripts/graphify_refresh.py`

## Failure signature

```text
subprocess.CalledProcessError: ... 'graphify', 'extract', '.../hermes-agent',
  '--code-only', '--out', '.../.graphify/hermes', '--force', '--max-workers', '4'
  died with <Signals.SIGKILL: 9>
```

Stdout usually dies mid AST after:

```text
[graphify extract] found 7507 code, 0 docs, ...
[graphify extract] AST extraction on 7507 code files...
```

Recurring on this host for weeks. Not bad cron config — **cgroup OOM**.

## Host constraints (verified 2026-08-31)

| Limit | Value |
| --- | --- |
| cgroup `memory.max` | **2.5 GiB** |
| Host RAM | ~3.8 GiB, often tight |
| Full-tree code files | ~**7507** (`node_modules`/`venv`/`apps`) |
| Scoped code files | ~**1318** with `.graphifyignore` |

Loading the legacy ~172 MiB Hermes `graph.json` via `json.load` can itself get **Killed** under pressure.

## Fix implemented in `graphify_refresh.py`

1. Managed `~/.hermes/hermes-agent/.graphifyignore` (drop node_modules/venv/apps/docs/tests/…).
2. Default `GRAPHIFY_MAX_WORKERS=1`; Hermes extract uses `--no-cluster`.
3. `--force` only for missing/empty/legacy full-tree or `GRAPHIFY_HERMES_FORCE=1`.
4. Soft-fail per target (Hermes fail must not skip vault graphs).
5. Never leave 0-node `graph.json` — restore `graph.json.bak`.
6. Flags: `--hermes-only` / `--vault-only` / `--split-only`.

## Anti-patterns

| Approach | Result |
| --- | --- |
| Symlink-farm core dirs as extract root | `detect()` does **not** follow dir symlinks → **0 code files** |
| Full-tree `--force --max-workers 4` | Reliable SIGKILL on 2.5 Gi cgroup |
| Empty `graph.json` after failed run | Breaks `graphify-mcp` |

## Manual commands

```bash
export PATH="$HOME/.local/bin:$PATH"
uv tool run --from graphifyy python ~/.hermes/scripts/graphify_refresh.py --hermes-only
uv tool run --from graphifyy python ~/.hermes/scripts/graphify_refresh.py --vault-only
GRAPHIFY_HERMES_FORCE=1 uv tool run --from graphifyy python ~/.hermes/scripts/graphify_refresh.py --hermes-only
```

Prefer off-peak / background runs. Cron stays `no_agent=true`.

## Acceptance

- Exit 0 if any graph succeeds; soft failures recorded in `~/.graphify/last-refresh.json`.
- Hermes `graph.json` nodes > 0. Scoped size << old 137k full-tree baseline (expected).
- Vault graphs still refresh when Hermes OOMs.
- Hermes `BUILD_META.json` has `"mode": "scoped-core"` after a successful scoped rebuild.
