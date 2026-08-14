# Social Video Extraction for Wiki Ingest

Use this for Facebook/Reels/TikTok/Instagram/YouTube-style links when the user asks to ingest a video.

## Durable rule

Extract and preserve **metadata + transcript/captions only**. Do **not** download `.mp4`, `.webm`, `.m4a`, `.mov`, `.mkv`, or audio as a workaround. This keeps the vault lightweight and avoids disk/RAM pressure.

## Command pattern

```bash
mkdir -p /vault/Attachments/<collision-safe-video-folder>
yt-dlp \
  --skip-download \
  --write-info-json \
  --write-auto-subs \
  --write-subs \
  --sub-langs "en,vi,en.*" \
  --convert-subs srt \
  --write-description \
  --write-thumbnail \
  -o '/vault/Attachments/<collision-safe-video-folder>/%(title).80s' \
  '<URL>'
```

If `yt-dlp` is not installed as a command, `uvx yt-dlp ...` is a good fallback, but do not encode the absence of a binary as a durable rule.

## Summaries when captions are unavailable

When the user asks to “extract transcript and summarize” but the platform has no captions/subtitles:

1. Preserve the explicit transcript result as `No transcript available` and quote the extractor reason if available (for example, `There are no subtitles for the requested languages`).
2. Do **not** download video/audio to work around missing captions.
3. If the description/metadata contain substantive content, write a clearly caveated summary from **available metadata and description only**; do not imply it is a full spoken-video summary.
4. Mark the resulting Note as `wiki_status: draft` unless there is enough source text for semantic completeness.
5. In the chat reply, make the limitation obvious before the summary.

## Inbox source shape

After sidecars are created, write/enrich an Inbox markdown file with:

```markdown
---
tags:
  - source
  - video
  - facebook # or platform
  - transcript
type: reflection
source: "<original shared URL>"
created: YYYY-MM-DD
---
# <Video Title>

- **Title:** <title from info.json>
- **Uploader:** <uploader/channel>
- **Canonical URL:** <webpage_url from info.json>
- **ID:** <platform id>
- **Duration:** <seconds>
- **Original shared URL:** <exact user URL>
- **Description:** <description text>

## Extracted Transcript

<clean transcript, or "No transcript available.">

## Attachments

- Transcript sidecar: [[Attachments/<folder>/<file>.srt]]
- Metadata JSON: [[Attachments/<folder>/<file>.info.json]]
- Thumbnail: ![[Attachments/<folder>/<file>.jpg]]
```

## SRT cleaning pattern

Strip blank lines, numeric cue counters, timestamp lines containing `-->`, and simple HTML tags. Deduplicate consecutive repeated caption lines, but do not paraphrase the transcript in the source archive.

## Verification checklist

Before replying:

1. Source archive exists under `Sources/` (or documented fallback).
2. Inbox capture is absent or marked ingested/preserved so it will not repeat-ingest.
3. Attachment folder contains only sidecars/thumbnail, not video/audio files.
4. Created/updated Notes pages exist and link back to the source.
5. Relevant MOC, `System/wiki-index.md`, and `System/wiki-log.md` contain exact hits.
