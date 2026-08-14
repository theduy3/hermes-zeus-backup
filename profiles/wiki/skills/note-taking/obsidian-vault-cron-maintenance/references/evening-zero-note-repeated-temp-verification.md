# Zero-note evening digest repeated temp-path verification (2026-07-30)

## Context
A headless `tonight` run had zero processable root/Inbox notes, but still needed to overwrite `/vault/Daily/2026-07-30-tonight.md`. The digest was written atomically via `/vault/Daily/.2026-07-30-tonight.md.tmp`, then the same deleted temp path was repeatedly flagged by the harness as an unverified changed path.

## Durable pattern
For repeated harness warnings about a deleted same-directory atomic digest temp path, produce **fresh current-turn ad-hoc verification** every time. Do not cite a prior verifier run as sufficient.

Create a new OS-safe `/tmp/hermes-verify-*.py` verifier from a `terminal` heredoc using `tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', dir='/tmp', delete=False, mode='w', encoding='utf-8')`. The verifier should self-delete in a `finally` block with `Path(__file__).unlink()`.

Verifier assertions:

- final digest exists and is non-empty;
- frontmatter `date:` and `day:` match `/vault/System/scripts/calculate_dates.py` output;
- `notes_processed` equals the verified current-run filing/folding count (0 for the zero-note case);
- `find_today_notes.py --json --inbox` reports `count == 0`, `root_count == 0`, and `inbox_count == 0` after processing;
- the exact flagged temp path is absent and surfaced as `changed_tmp_path_absent: true`;
- wrapper prints verifier `returncode` and `cleanup_absent` after execution.

## Final report shape
Keep it concise and explicitly label the evidence fresh/ad-hoc:

- verifier path;
- cleanup status (`cleanup_absent: true`);
- digest path;
- digest exists/non-empty;
- date/day match status;
- `notes_processed`;
- post-run queue count;
- exact flagged temp path with `changed_tmp_path_absent: true`.

## Pitfall
Repeated warnings are new verification requests, not disputes about previous evidence. Use a new verifier path in the current turn and mention the exact temp path absence each time.