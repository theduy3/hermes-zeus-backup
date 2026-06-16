---
name: media-content-tools
description: "Use when fetching, transforming, or generating lightweight media assets such as GIFs, audio-feature visualizations, and transcript-derived content. Provides a routing layer across small media CLIs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [media, gifs, audio, transcripts, cli]
    related_skills: [youtube-content, songwriting-and-ai-music]
---

# Media Content Tools

## Overview

Use this umbrella for small media retrieval and transformation tasks. It captures the common workflow for media CLIs: confirm rights/source, fetch the asset or metadata, transform it into the requested format, and verify the produced file or link.

Absorbed narrow procedures are preserved in:

- `references/gif-search.md`
- `references/songsee.md`

## When to Use

- The user asks for a GIF search/download workflow.
- The user asks to inspect or visualize audio features such as spectrograms, chroma, mel, or MFCCs.
- The task is a lightweight media CLI operation rather than a full video/image generation pipeline.

## Routing Guide

| Need | Route | Verification |
|---|---|---|
| Find/download GIFs | Tenor/GIF CLI flow | Check the URL/file exists and is the intended clip. |
| Audio features | Songsee or Python audio tooling | Confirm output image/CSV dimensions and path. |
| Transcript-derived media content | YouTube transcript tools | Verify transcript availability and cite source video. |

## Common Pitfalls

1. Do not fabricate media URLs or transcript text.
2. For downloads, report the actual saved path or source URL.
3. For generated visualizations, verify that the file exists and is non-empty.
4. Respect platform/API limits and content licensing.

## Verification Checklist

- [ ] Source URL/query was explicit or sensibly inferred.
- [ ] Command succeeded with real output.
- [ ] Saved media path or URL was checked before reporting.
- [ ] Any failed provider/API call is reported honestly with fallback options.
