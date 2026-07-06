# Economist full-issue operational pitfalls

Session-derived notes for full *The Economist* PDF ingests with article folders.

## Shell-script creation pitfall: ampersands in MOC names
When generating a helper script that contains strings such as `Middle East & Africa MOC` or `Finance & Economics MOC`, do **not** create the script with a shell heredoc inside `terminal()`. Hermes' foreground command guard can interpret the `&` in the command payload as shell backgrounding and reject the command before execution.

Reliable pattern:
1. Use `write_file` to write the helper script to `/tmp/...py` or another safe path.
2. Run the script with `terminal(command="python3 /tmp/script.py", timeout=600)`.
3. If the script performs partial writes before failing, inspect/patch the script and rerun idempotently; avoid rewriting infrastructure files from partial reads.

## `_cold` archive directory may be root-owned
Prior issues may have raw article folders under `Sources/_cold/`, but `_cold` can be root-owned. If creating `Sources/_cold/<Issue> Articles/` fails with `PermissionError`, fall back to the documented article-folder location:

- `Sources/<Issue Title> Articles/`

Update all issue notes, MOC issue lines, log entries, and source paths consistently to the actual folder used. Do not claim the folder is under `_cold` unless it was actually created there.

## Root-owned content notes are not just infrastructure
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
