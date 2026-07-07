# Economist section order and numbered MOC titles

Use when ingesting, repairing, or reorganising full *The Economist* issues so issue pages and MOCs preserve the magazine's table-of-contents order.

## Canonical section order
For full issues, derive the section order from the issue `00-index.md` / table of contents and keep it explicit in `MOCs/The Economist MOC.md`:

1. The world this week
2. Leaders
3. Letters
4. By Invitation
5. Essay
6. United States → `US Politics & Society MOC`
7. The Americas → `The Americas MOC`
8. International → `International MOC`
9. Asia → `Asia MOC`
10. China → `China MOC`
11. Middle East & Africa → `Middle East & Africa MOC`
12. Europe → `Europe MOC`
13. Britain → `Britain MOC`
14. Business → `Business MOC`
15. Finance & economics → `Finance & Economics MOC`
16. Science & technology → `Science & Technology MOC`
17. Culture → `Culture MOC`
18. Obituary → usually `Culture MOC` unless a subject-domain MOC is stronger

## MOC title convention
The user wants the order visible in the MOC titles themselves. Do **not** rename files unless explicitly asked; instead update each MOC's H1 and preserve wikilink targets:

- `# 06 US Politics & Society MOC`
- `# 07 The Americas MOC`
- `# 08 International MOC`
- `# 09 Asia MOC`
- `# 10 China MOC`
- `# 11 Middle East & Africa MOC`
- `# 12 Europe MOC`
- `# 13 Britain MOC`
- `# 14 Business MOC`
- `# 15 Finance & Economics MOC`
- `# 16 Science & Technology MOC`
- `# 17 Culture MOC`

Keep `Culture` as `17`; note that Obituary is section 18 and normally routes through Culture.

## The Economist MOC link aliases
In `The Economist MOC`, display numbered aliases while preserving existing filenames:

```md
06. [[US Politics & Society MOC|06 US Politics & Society MOC]] — **United States**
14. [[Business MOC|14 Business MOC]] — **Business**
17. [[Culture MOC|17 Culture MOC]] — **Culture**
18. [[Culture MOC|17 Culture MOC]] — **Obituary**
```

Also add a convention note under `## Articles by Issue`:

```md
Within each issue, article links are ordered by the magazine table of contents. Section numbers follow the canonical *Economist* order above.
```

## Planning preference
For structural MOC reorganisation (renaming headings, changing link display, changing ordering conventions), show a concise plan before executing. The user specifically asked for plan-first before adding section numbers to MOC titles.

## Verification
After edits, verify:
- `The Economist MOC` lists all 18 canonical sections in order.
- All 12 domain MOCs have numbered H1 titles and `Economist section order` markers.
- File names and wikilink targets are unchanged unless explicitly requested.
- Per-issue article links remain in original TOC order.
- No raw numbered source links such as `[[01-...]]` appear in MOCs.
- `wiki-log.md` records the structural update.
