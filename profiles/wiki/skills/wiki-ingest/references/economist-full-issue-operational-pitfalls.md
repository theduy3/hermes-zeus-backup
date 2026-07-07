# Economist full-issue operational pitfalls

Session-derived notes for full *The Economist* PDF ingests with article folders.

## Shell-script creation pitfall: ampersands in MOC names
When generating a helper script that contains strings such as `Middle East & Africa MOC` or `Finance & Economics MOC`, do **not** create the script with a shell heredoc inside `terminal()`. Hermes' foreground command guard can interpret the `&` in the command payload as shell backgrounding and reject the command before execution.

Reliable pattern:
1. Use `write_file` to write the helper script to `/tmp/...py` or another safe path.
2. Run the script with `terminal(command="python3 /tmp/script.py", timeout=600)`.
3. If the script performs partial writes before failing, inspect/patch the script and rerun idempotently; avoid rewriting infrastructure files from partial reads.

## Active Economist article folders live directly under `Sources/`
Prior issues or historical logs may mention raw article folders under `Sources/_cold/`, but current vault policy keeps active/high-value Economist issue article folders directly under:

```text
/vault/Sources/<Issue Title> Articles/
```

Do not create new active Economist folders in `_cold`; `_cold` is only for legacy bulk archive material. If you discover an active Economist issue folder still under `Sources/_cold/<Issue> Articles/`, migrate it to `/vault/Sources/<Issue Title> Articles/` and update current issue notes/MOC prose paths to the actual folder used. Historical `wiki-log.md` entries can remain historical.
Some durable notes that normally should be updated during ingest can be root-owned too, e.g. `Notes/Economic Indicators.md`. Treat them like file-level blocked infrastructure:

- Continue creating the source archive, article extracts, and new Notes pages.
- Skip only the blocked note update.
- Include the exact `sudo chown hermes:hermes ...` command in the final summary.
- Still route indicator-related article extracts to Finance & Economics MOC if that MOC is writable; if the MOC is also root-owned, report both.

## Verification pattern after partial script failure
If a helper script fails after creating some artifacts:
1. Check which files already exist (cleaned PDF, source archive, article folder, issue note).
2. Patch the script to be idempotent and avoid the failing write.
3. Rerun it to complete the workflow.
4. Verify counts and paths from actual files, not from the intended script plan.
