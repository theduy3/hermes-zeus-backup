# Social video extraction pattern

Use this when the user sends a Facebook/Reels/TikTok/short-form video URL and asks to extract information into the vault.

## Pattern

1. Capture the URL immediately into `Inbox/YYYY-MM-DD-HHMM-<slug>.md` with source frontmatter and the raw URL.
2. Try to resolve/download the video into `Attachments/<slug-date>/` with metadata, thumbnail, and media preserved. A reliable command shape is:
   ```bash
   mkdir -p /vault/Attachments/<slug-date>
   uvx --from yt-dlp yt-dlp --no-playlist --write-info-json --write-description --write-thumbnail --restrict-filenames \
     -o '/vault/Attachments/<slug-date>/%(title).80s-%(id)s.%(ext)s' '<url>'
   ```
3. Extract audio with ffmpeg and transcribe with the available speech model/tool. For local Faster Whisper, a working pattern is:
   ```bash
   ffmpeg -y -i <downloaded-video>.mp4 -vn -ac 1 -ar 16000 /tmp/<slug>.wav
   python3 - <<'PY'
   from faster_whisper import WhisperModel
   model = WhisperModel('small', device='cpu', compute_type='int8')
   segments, info = model.transcribe('/tmp/<slug>.wav', beam_size=5, vad_filter=True)
   print('language', info.language, info.language_probability)
   for s in segments:
       print(f'[{s.start:.2f}-{s.end:.2f}] {s.text}')
   PY
   ```
4. Build the Inbox markdown into a real source: include original URL, resolved URL, creator/uploader, video ID, upload date, duration, view count, original description, extracted bullets, rough transcript, and Obsidian links to media/thumbnail/metadata attachments.
5. Ingest normally: create/update a substantive `Notes/` page, write the normalized archive in `Sources/`, add `## Pages Updated`, move/preserve the Inbox capture outside Inbox, and update MOC/index/log.

## Quality notes

- Do not fabricate content from the title if download/transcription fails. Archive a metadata-only source and report that the body was unavailable.
- Whisper transcripts of Vietnamese social videos may contain homophone errors. Use the transcript plus title/description/context to write a cleaned **rough transcript**, not a verbatim legal transcript.
- Preserve downloaded video, thumbnail, and `.info.json` under `Attachments/` and link them from the source archive.
- Verify: source archive exists, Inbox capture is no longer in Inbox, attachment files exist, new/updated Note is indexed, MOC/log entries contain exact title.