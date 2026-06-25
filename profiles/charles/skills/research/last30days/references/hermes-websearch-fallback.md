# Hermes WebSearch Fallback for `/last30days`

When running `/last30days` in a Hermes runtime that does not expose a dedicated WebSearch tool, do not skip Step 2 supplements. The engine still must run first. Then use a read-only public web fallback to gather 2-3 supplemental news/blog/tutorial sources and append them to the saved raw file.

## Pattern

1. Run `scripts/last30days.py` normally with `--emit=compact` and `--save-dir`.
2. Locate the saved raw file from the engine's `[last30days] Saved output to ...` line.
3. For news/current-event topics, query Google News RSS with Python `urllib`:

```python
import urllib.request, urllib.parse, xml.etree.ElementTree as ET
url = 'https://news.google.com/rss/search?' + urllib.parse.urlencode({
    'q': '{TOPIC} when:30d',
    'hl': 'en-US',
    'gl': 'US',
    'ceid': 'US:en',
})
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
data = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'replace')
root = ET.fromstring(data)
for item in root.findall('.//item')[:5]:
    print(item.findtext('source'), item.findtext('title'), item.findtext('link'))
```

4. If a backend rate-limits or emits malformed output, retry once with a different simple public source rather than declaring supplements impossible.
5. Append a canonical `## WebSearch Supplemental Results` section to the saved raw file:

```markdown
## WebSearch Supplemental Results

- **Publisher** (domain) — One-sentence summary of what this source contributed.
- **Publisher** (domain) — One-sentence summary of what this source contributed.
- **Publisher** (domain) — One-sentence summary of what this source contributed.
```

## Output discipline

- This fallback is a supplement only, never a replacement for the Python engine.
- Do not add a visible trailing `Sources:` block in the user-facing response. LAW 1 still applies.
- Use inline Markdown links in the narrative when citing supplemental sources.
