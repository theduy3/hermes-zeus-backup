# Platform Error Message Captures

Use this when a Telegram/chat message is itself a platform/system error rather than a substantive article, repo, image, or long note.

## Pattern

1. Capture the exact error text verbatim to `Inbox/YYYY-MM-DD-HHMM-<short-slug>.md`.
2. Dedup/search for the platform, tool, or operational page that should remember the limitation.
3. Prefer updating an existing operations/setup note with a concise gotcha instead of creating a new standalone page for a one-line error.
4. Archive the Inbox capture to `Sources/` as `type: reflection`, `source: telegram` (or the relevant platform), and add `## Pages Updated`.
5. Update `wiki-index.md` for the existing page's `updated` date and append a `wiki-log.md` entry.
6. Verify: source archive exists, Inbox is empty, target note contains the exact limitation, index/log contain the updated artifact.

## Example

Telegram/Hermes message:

> The document is too large or its size could not be verified. Maximum: 20 MB.

Good ingest result:
- Update `[[Hermes Agent Setup and Operations]]` under operational gotchas.
- Record that the messaging layer has a 20 MB document-size guardrail and suggest split/compress/share-link as operational response.
- Archive the exact message in `Sources/`.

Avoid:
- Creating a new atomic wiki page just for the one-line error.
- Treating the message as a failed upload to retry blindly without preserving the operational lesson.
