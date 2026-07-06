# Newsletter welcome/admin email routing

Use this when newsletter IMAP capture drops welcome, safelist, confirmation, onboarding, or other low-content admin emails into `/vault/Inbox/`.

## Pattern

1. Treat the emails as real sources: normalize frontmatter with `tags: [source, newsletter, ...]`, `type: article` or `reflection`, `source: email`, `created`, and `ingested`.
2. Do not create one wiki note per welcome/admin email. These are usually source-only unless they establish a durable feed, publisher, or routing rule.
3. If multiple welcome/admin emails establish a durable feed family/network, create or update one entity/source-monitoring page for the feed network.
4. Update the nearest existing routing/source-list page with how future issues should be handled.
5. Add `## Pages Updated` to each archived source, even if the email itself was mostly administrative.
6. Archive every processed email to `Sources/` and clear `Inbox/`.
7. Update MOCs that reflect future routing (e.g. Business, Finance & Economics, Finance, AI/Technology) and update `wiki-index.md` + `wiki-log.md`.
8. Verify exact artifacts: empty Inbox, source archive files, `## Pages Updated`, created/updated note, MOC links, index row(s), and log entry.

## Example: Morning Brew family

Three welcome emails from Morning Brew, Tech Brew, and Brew Markets should produce one durable note such as `Morning Brew Newsletter Network.md`, not three separate welcome-email notes.

Useful routing:
- Morning Brew: daily business/news brief; route substantive issues to business, macro, media, or company notes.
- Tech Brew: AI, tech policy/culture, emerging tech, and tech-business trends; route substantive issues to AI/technology/regulation notes.
- Brew Markets: investing and market movement; route substantive issues to finance/markets, `Economic Indicators`, and company/sector notes.

Keep short headline/admin messages source-only when they do not add durable wiki knowledge.
