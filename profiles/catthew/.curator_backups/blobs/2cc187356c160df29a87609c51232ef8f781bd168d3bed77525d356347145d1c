---
name: video-product-extraction
description: Extract visible products, brands, labels, ingredients, or shopping-list items from short videos/reels/TikToks/Facebook/Instagram posts. Use when the user asks to identify products from a video URL or wants a list of items shown in a clip.
---

# Video Product Extraction

Use this skill when the user asks to extract products/items from a video, reel, short, TikTok, Facebook, Instagram, or other social video.

## Output style for this user

- Be terse: product list first, no process explanation unless asked.
- Include timestamps when available.
- Mark uncertainty plainly: `brand partly obscured`, `label not visible`, `likely ...`.
- Do not invent product names from blurry frames; report only what can be read or strongly verified.
- If asked for products, include both deliberate showcased products and clearly readable incidental/background products separately.

## Workflow

1. **Extract page metadata first**
   - Use `web_extract` on the URL for title/description/canonical URL.
   - If it is a Facebook share link, resolve it to the reel/watch URL where possible.
   - Search the exact title/caption if metadata hints at brand names or creator comments.

2. **Download or access the actual video**
   - Prefer `yt-dlp` for public social videos:
     ```bash
     yt-dlp --no-playlist --skip-download --print '%(title)s\n%(description)s\n%(webpage_url)s\n%(duration)s\n%(thumbnail)s' '<url>'
     yt-dlp -f 'bv*+ba/b' --merge-output-format mp4 -o '/tmp/video_products/video.%(ext)s' '<url>'
     ```
   - If `yt-dlp` is unavailable, use a temporary venv rather than altering system Python:
     ```bash
     python3 -m venv /tmp/video-product-venv
     /tmp/video-product-venv/bin/pip install -q yt-dlp
     /tmp/video-product-venv/bin/yt-dlp ...
     ```

3. **Sample frames**
   - Extract contact-sheet frames at 1 fps for shorts/reels:
     ```bash
     mkdir -p /tmp/video_products/frames
     ffmpeg -hide_banner -loglevel error -i /tmp/video_products/video.mp4 -vf 'fps=1,scale=540:-1' /tmp/video_products/frames/frame_%03d.jpg
     ```
   - Build contact sheets in chunks (about 20 frames per image) to inspect efficiently. If Pillow is not available, install it in the same temporary venv.

4. **Use vision on contact sheets**
   - Ask vision to identify every product shown, read labels carefully, and return timestamps/frame numbers.
   - For blurry or key labels, extract individual high-resolution frames around that timestamp and re-run vision:
     ```bash
     ffmpeg -hide_banner -loglevel error -ss 45 -i /tmp/video_products/video.mp4 -frames:v 1 /tmp/video_products/key_45.jpg
     ```

5. **Cross-check product names**
   - Use web search only to confirm ambiguous labels or exact product names; do not substitute search guesses for unreadable video evidence.
   - Useful query pattern: exact caption/title plus clearly visible brands.

## Final answer pattern

```text
Extracted products/items shown:

- Brand Product Name — flavor/size/details — ~12–20s
- ...

Incidental/background product visible:
- ...
```

## Pitfalls

- Social pages often expose only caption/thumbnail metadata; do not stop there if the task requires all products in the video.
- A frame sequence can show the same product repeatedly; dedupe repeated frames into one product entry with a timestamp range.
- Some products are generic foods (avocado, eggs, butter stick). Include them if the user asked for “all the product/items,” but distinguish generic items from branded products.
- Background fridge/pantry items may be readable but not intentionally featured; list separately to avoid clutter.
