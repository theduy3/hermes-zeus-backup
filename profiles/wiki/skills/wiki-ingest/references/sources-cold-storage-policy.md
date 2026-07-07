# Sources cold-storage policy

Use when deciding whether source material belongs directly under `/vault/Sources/` or in `/vault/Sources/_cold/`.

## Current policy

Use a hybrid policy:

- Future processed source archives go directly under `/vault/Sources/` using `YYYY-MM-DD - Source Title.md`.
- Active/high-value source folders go directly under `/vault/Sources/`, especially full Economist issue article folders.
- `_cold` remains only for legacy/bulk archive material such as old CSV imports and low-browse historical captures.

Do not create new active Economist article folders under `_cold`.

## Economist issue folders

Full Economist issue article folders should live at:

```text
/vault/Sources/<Issue Title> Articles/
```

not:

```text
/vault/Sources/_cold/<Issue Title> Articles/
```

If an active Economist issue folder is discovered under `_cold`, migrate it to top-level `Sources/` and update current issue notes/MOC prose references to match the actual folder. Historical `wiki-log.md` entries can remain historical.

## Why not delete `_cold` entirely?

`_cold` can still be useful for legacy/bulk imports and keeps the active source surface browsable. The user chose the recommendation/hybrid approach: stop future active use, move active/high-value folders out, leave legacy bulk cold.

## Migration checklist

1. Inventory candidate active folders under `Sources/_cold/`.
2. Ensure the target under `Sources/` does not already exist.
3. Move the active folder to top-level `Sources/`.
4. Update current `Notes/`, `MOCs/`, and `System/` prose references that point to `Sources/_cold/<Issue> Articles/`.
5. Do not rewrite old historical `wiki-log.md` entries except by appending a new migration log entry.
6. Verify the hot folder exists, the cold copy is gone, file counts match, and no active note/MOC/System references still point to the old cold path.

## Known verification pattern

For active Economist folders, verify file counts after move and absence of current references to `Sources/_cold/The Economist...` in Notes/MOCs/System (excluding historical log text).
