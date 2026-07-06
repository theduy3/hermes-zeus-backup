# Ad-hoc verification after wiki-lint helper script edits (2026-06-28)

## Trigger
Use this when a wiki-lint run creates or edits temporary/helper code such as `/tmp/wiki_lint_run.py`, `/tmp/wiki_lint_cleanup.py`, or targeted note/index/log patch scripts, especially when no canonical test/lint/build command exists.

## Pattern
1. After the run and any semantic cleanup, create a focused temporary verifier under `/tmp` with a `hermes-verify-` filename prefix.
2. Keep the verifier narrow and behavior-oriented:
   - `py_compile.compile(..., doraise=True)` for any changed Python helper scripts.
   - Assert edited note content has the expected `updated` date, no diff-marker artifacts, expected semantic links, and removed weak links are absent.
   - Assert `System/wiki-index.md` header date/page_count and rows for touched pages.
   - Assert `System/wiki-log.md` has exactly one same-day lint entry and its counts match the final post-cleanup state.
3. Run the verifier with `python3 /tmp/hermes-verify-*.py`.
4. Remove the temporary verifier after it runs when possible.
5. Report it explicitly as **targeted ad-hoc verification**, not as a canonical suite pass.

## Pitfalls
- Do not claim a wiki-lint run is fully verified just because the scanner printed a JSON report if later manual patches changed files.
- If a cleanup script is rerun after a manual patch, rerun the ad-hoc verifier afterward; cleanup scripts may rewrite the log/index and can accidentally reintroduce stale counts.
- Keep this separate from the main wiki-lint run script. The verifier should be disposable and named with `hermes-verify-` so it is obvious that it is not vault content.
