# Social video recipe extraction

Use when a Facebook/Reels/TikTok/Instagram/YouTube short contains a recipe in its description/captions and the user asks to extract the recipe.

## Pattern from July 2026 session

1. Capture the URL to `Inbox/` first, even if the user only asks to "extract" rather than explicitly "ingest".
2. Use the normal social-video sidecar workflow: `yt-dlp --skip-download --write-info-json --write-auto-subs --write-subs --sub-langs "en,vi,en.*" --convert-subs srt --write-description --write-thumbnail ...`.
3. Never download or retain video/audio (`.mp4`, `.webm`, `.m4a`) for recipe extraction.
4. Read both:
   - `.description` / metadata description, which often contains the complete ingredient list and steps; and
   - `.srt` transcript, which often clarifies technique/timing but may omit exact quantities.
5. Create a normalized source archive in `Sources/YYYY-MM-DD - <Recipe Title> Facebook Recipe Video.md` containing:
   - original shared URL and canonical URL;
   - uploader/title;
   - exact extracted recipe from description;
   - cleaned transcript;
   - sidecar links and thumbnail embed;
   - `## Pages Updated` linking the recipe note.
6. Create/update a practical recipe note under `Notes/` with:
   - compact summary;
   - ingredients grouped by component;
   - method as numbered steps;
   - practical notes for imprecise quantities or doneness/timing caveats;
   - source link and original URL.
7. Route the recipe through `Personal MOC` → `Lifestyle` unless a more specific food/health MOC exists.
8. Update `wiki-index.md` and `wiki-log.md` and verify:
   - note exists;
   - source archive exists;
   - Inbox capture is gone/preserved outside Inbox;
   - MOC/index/log exact hits exist;
   - attachment folder contains no video/audio files.

## Pitfalls

- The transcript may say "ingredients below" while the actual quantities are only in the video description. Do not summarize from captions alone when a description is available.
- Social descriptions may use imprecise quantities such as `0.3 cup`; preserve the original in the source archive, but convert gently in the recipe note (e.g. "roughly 1/3 cup") with a practical note.
- Keep the source archive faithful; put cooking interpretation/caveats in the recipe note.
