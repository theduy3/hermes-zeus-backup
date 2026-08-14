# 2026-07-20 multi-profile recap: truncated discovery and late files

Context: weekday recap ran at 18:00 America/Vancouver while the host date was already 2026-07-21 UTC. The day’s relevant outputs lived across default plus named profiles (`zeus`, `wiki`, `thor`, `catthew`, `charles`).

Reusable lessons:

- Always resolve the reporting day in the user/job timezone. In this run, `date` returned `2026-07-21 UTC`, but `TZ=America/Vancouver date` returned `2026-07-20 PDT`; the recap correctly covered July 20.
- `search_files` over `~/.hermes/profiles` truncated at 200 results even though the full day had 333 output files. Do not treat a truncated `search_files` listing as complete on cron-heavy days.
- Use terminal/Python glob aggregation for full coverage:
  ```python
  import glob, os
  paths = glob.glob('/home/hermes/.hermes/cron/output/*/2026-07-20_*.md') \
        + glob.glob('/home/hermes/.hermes/profiles/*/cron/output/*/2026-07-20_*.md')
  print(len(paths))
  for p in sorted(paths, key=os.path.getmtime)[-15:]:
      print(p)
  ```
- Sorting by mtime exposed just-finished co-scheduled files that the first pass missed: `wiki/vault-tonight` at `18-01-05` and default profile gateway watchdog at `18-01-17`. The count changed from 331 to 333 and the evening digest should be included.
- For large no-agent job groups, aggregate by profile/job and then sample only non-silent/nonempty bodies. In this run, many `zeus` task/calendar sync outputs were repetitive and should be summarized as counts plus notable nonzero updates, not listed individually.
- A blocker scan should parse the final response section only. This avoided treating prompt boilerplate or benign phrases such as “no helper error text leaked” as failures.
