# Root-owned infrastructure during wiki ingest

Observed failure mode:
- `read_file` on `/vault/System/wiki-index.md` or `/vault/System/wiki-log.md` may return empty/0 lines with `File not found` even though the file exists.
- `patch`/`write_file` on root-owned infrastructure files can fail with `Permission denied`.
- `terminal` reads like `ls -l` still reveal ownership and confirm the file is present.

Detection:
- Run `ls -la /vault/System/` and `ls -la /vault/MOCs/` early.
- Treat `root root` ownership on `wiki-index.md`, `wiki-log.md`, or MOC files as a hard blocker for Step 3 and Step 2d.

Response:
- Continue ingesting and writing wiki pages in `Notes/` if those files are writable.
- Skip `wiki-index.md`, `wiki-log.md`, and MOC updates for the run.
- Report the blocked files and the fix in the final summary.

Fix command:
```bash
sudo chown hermes:hermes \
  '/vault/Notes/Hermes Agent Setup and Operations.md' \
  '/vault/System/wiki-index.md' \
  '/vault/System/wiki-log.md' \
  '/vault/MOCs/AI Agent Tooling MOC.md' \
  '/vault/MOCs/Personal MOC.md'
```
