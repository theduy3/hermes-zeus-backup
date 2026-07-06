# Social Video Ingest + YouTube Guide Search

Use when the user asks to ingest a Facebook/Reels/TikTok/short-form video and also asks for guide/how-to videos on YouTube.

## Pattern that worked

1. Capture the shared social URL verbatim in `Inbox/YYYY-MM-DD-HHMM-<slug>.md`.
2. Extract sidecars only:
   ```bash
   yt-dlp --skip-download \
     --write-info-json --write-auto-subs --write-subs \
     --sub-langs "en,vi,en.*" --convert-subs srt \
     --write-description --write-thumbnail \
     -o '/vault/Attachments/<safe-folder>/%(title).80s' '<URL>'
   ```
   Keep `.info.json`, `.description`, `.srt`, thumbnail. Do **not** keep `.mp4`, `.webm`, `.m4a`, or audio.
3. Clean the SRT by dropping sequence numbers, timestamp lines, blank lines, and HTML tags; dedupe only consecutive repeated captions.
4. Enrich the Inbox source with title, uploader, canonical URL, original URL, duration, description, transcript, and attachment wikilinks.
5. Create/update atomic wiki note(s). For health/wellness reels, include a caution that social-media claims are not medical advice when appropriate.
6. For the YouTube guide request, derive precise search phrases from the transcript. Use `yt-dlp --flat-playlist --print '%(title)s ||| %(id)s ||| %(uploader)s ||| %(duration_string)s' 'ytsearch8:<query>'`.
   - Avoid piping untrusted search JSON directly into Python; use `--print` or save output first.
   - If the first query is sparse, retry with alternate terms from the transcript and domain synonyms.
   - Prefer guide/how-to matches from channels whose title/channel/length suggest instructional content; record 3–6 best URLs in the note.
7. Archive the enriched source to `Sources/`, preserve/move Inbox original if needed, update MOC/index/log, and verify: note file, source archive, Inbox empty, no video/audio files in the attachment folder, MOC/index/log hits.

## Example query adaptation

A Facebook reel about “detox drainage” mentioned collarbone, neck, underarms, abdomen, groin, back of knees, rebounder, and shaking. Good YouTube searches were:

- `BIG 6 lymphatic drainage reset collarbone neck armpit abdomen groin knees`
- `3 minute lymphatic drainage massage water retention face collarbone neck underarms abdomen groin back of knees`
- `lymphatic drainage massage routine collarbone neck underarms abdomen groin back of knees rebounder`

This found guide candidates such as GuerrillaZen Fitness “5-Minute Lymph Reset”, RE•KŌD “Big 6 Lymphatic Reset”, Oak City Chiropractic “Big Six Lymphatic Drainage”, Doc Talks Detox “Specific 7”, and Cancer Rehab PT dry brushing.
