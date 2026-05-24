# Obsidian task folder audit and migration

Use this when the user asks to move, audit, or normalize task/idea notes in the vault.

## Correct locations

- Due-date tasks and `type: task` notes: `/vault/Tasks/tasks/`
- No-date ideas and `type: idea` notes: `/vault/Tasks/ideas/`
- Templates under `/vault/System/Templates/` are not active tasks and should be excluded from migration.

## Required body format

Task bodies should use checkbox items, not plain paragraphs:

```md
- [ ] Task item
```

For a migrated task whose source has a plain body paragraph, preserve the title/frontmatter and convert the actionable paragraph into one or more checkbox lines.

## Audit script

Run this to find task/idea notes outside the correct folders. It excludes templates.

```bash
python3 - <<'PY'
from pathlib import Path
import re
rows=[]
for p in Path('/vault').rglob('*.md'):
    s=str(p)
    if '/System/Templates/' in s:
        continue
    try:
        txt=p.read_text(errors='ignore')[:2000]
    except Exception:
        continue
    m=re.match(r'^---\n(.*?)\n---', txt, re.S)
    if not m:
        continue
    fm=m.group(1)
    typ=re.search(r'^type:\s*(\w+)', fm, re.M)
    due=re.search(r'^due_date:\s*([0-9-]+)', fm, re.M)
    if typ and typ.group(1) in ('task','idea'):
        correct = Path('/vault/Tasks/tasks') if (typ.group(1)=='task' or due) else Path('/vault/Tasks/ideas')
        if p.parent != correct:
            rows.append(str(p))
print('\n'.join(rows) if rows else 'OK')
PY
```

## Migration pattern

1. Read the source note.
2. Search the destination folder for duplicates by distinctive title/body terms before creating a migrated copy.
3. Write the corrected note into the destination folder with normalized checkbox body.
4. Attempt to remove the old source only if it is safe and permissions allow.
5. Re-run the audit script to verify.

## Permission pitfall

If deleting the old source fails with `Permission denied`, do not claim the migration is fully clean. Report that the corrected copy exists in the proper folder and name the old duplicate that remains. Do not try host-level permission fixes from inside the container.