# no_agent script jobs: SIGKILL / OOM

## When this applies

Cron row has `no_agent: true` + `script: …`, `last_status: error`, and `last_error` contains:

- `died with <Signals.SIGKILL: 9>`
- or exit after heavy subprocess with no Python traceback from the child

Provider/model fields are **null and irrelevant** — the LLM never runs.

## First checks

1. Read full `last_error` from default `~/.hermes/cron/jobs.json` (or profile jobs.json).
2. Tail newest file under `~/.hermes/cron/output/<job_id>/`.
3. Host pressure: `cat /sys/fs/cgroup/memory.max memory.current`; `free -h`.
4. Confirm the script path resolves under `~/.hermes/scripts/`.

## Known offender

**graphify-daily-refresh** (`5a9aa5056402`) — full Hermes `graphify extract --force --max-workers 4` on ~7.5k code files inside a **~2.5 Gi** cgroup.

Canonical fix and scoped rebuild rules live in:

`graphify-hermes-vault-integration` → `references/oom-sigkill-daily-refresh.md`

Script SoT: `/home/hermes/.hermes/scripts/graphify_refresh.py`

## Fix pattern (general)

1. Reduce peak RAM (fewer workers, smaller corpus, no forced full rescan every night).
2. Soft-fail independent targets so one OOM does not skip the rest.
3. Never overwrite a good artifact with an empty/failed output.
4. Prefer off-peak schedules for heavy extract jobs; keep `no_agent=true`.

## Do not

- Convert the job to an agent/LLM prompt “to be safer.”
- Pin `provider`/`model` on pure script jobs as an OOM fix.
- Re-run full-tree forced extracts in a live chat session without checking free memory first.
