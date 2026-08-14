---
name: personal-list-capture
title: Personal List Capture
description: Create and maintain Duy's personal wishlist, shopping, gift, and other lightweight list notes in the Obsidian vault.
category: note-taking
---

# Personal List Capture

Use when Duy asks to create, add to, remove from, or update a personal list such as a wishlist, shopping list, gift list, wine list, restaurant list, or “save this for later.”

## Where to write

- Default for lightweight personal lists/wishlists: `/vault/Tasks/ideas/<kebab-title>.md`
- Do **not** create a dated task unless Duy gives a due date or asks for a reminder.
- Do **not** use Apple Reminders or the working directory.

## Before writing

1. Search for an existing matching note under `/vault/Tasks/ideas/` first.
2. Also search `/vault/Tasks/` by title/content to avoid duplicates.
3. If a matching list exists, update it in place instead of creating a new note.

## Note format

Use idea frontmatter:

```markdown
---
type: idea
tags: [personal, wishlist]
status: pending
---
# List Title

## Item Title

- **Field:** value
```

Add topic tags when obvious, e.g. `wine`, `travel`, `gift`, `restaurant`, `shopping`.

## Updating existing items

- If Duy says “remove that link/item, add this instead,” read the list, remove only the referenced item/link, write the replacement, then read back to verify.
- Preserve unrelated list entries.
- Convert pasted prose into concise structured bullets rather than dumping raw text.
- Keep links only if Duy asked to keep the link or the link is the item itself.

## Verification

After writing, read the note back and confirm tersely with the path and what changed.