# Dotted wikilink target normalization (2026-07-19)

During a cron wiki-lint broken-link repair, verification initially reported false broken links for pages like `[[Claude Opus 4.6 Operator Guide]]` and `[[Operators Guide to Opus 4.6]]`. The cause was using `Path(target).stem` on wikilink targets. For note titles containing dots/version numbers, `Path('Claude Opus 4.6 Operator Guide').stem` incorrectly truncates to `Claude Opus 4` because `.6 Operator Guide` is treated as a suffix.

## Durable rule

When normalizing Obsidian wikilink targets, do **not** use `Path(...).stem` on the full target string. Normalize manually:

1. Remove alias and heading suffixes: split on `|`, then `#`.
2. Strip a literal trailing `.md` only if present.
3. Strip folder prefixes by splitting on `/` and taking the last segment.
4. Preserve all other dots in the title.

```python
def wikilink_target_base(raw: str) -> str:
    target = raw.split('|', 1)[0].split('#', 1)[0]
    if target.endswith('.md'):
        target = target[:-3]
    if '/' in target:
        target = target.rsplit('/', 1)[-1]
    return target
```

## Verification implication

If a verifier still reports broken links after an automated repair, inspect whether the broken target is a versioned/dotted page title before editing the note again. The note may already be correct and only the verifier's target normalization is wrong.
