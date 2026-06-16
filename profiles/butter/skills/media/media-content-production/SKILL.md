---
name: media-content-production
description: "Umbrella for media workflows: YouTube transcripts, GIF search, ASCII/video production, Manim animation, audio analysis, songwriting, and AI music generation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [media, video, audio, youtube, gif, music, songwriting, manim, ascii-video]
---

# Media Content Production

Use this umbrella for workflows that ingest, transform, create, or analyze media: YouTube summaries, GIF retrieval, ASCII video, explanatory animation, song lyrics/prompts, AI music generation, and audio spectrogram/features.

## YouTube and web video content

Fetch transcripts when possible, then produce the requested output form: summary, blog post, thread, notes, outline, or repurposed content. If transcript fetch fails, say so and use alternative extraction only when available.

## GIF search

Use Tenor/GIF search workflows when the user wants reaction GIFs or downloadable GIF assets. Prefer explicit query terms, content rating constraints, and verify returned URLs.

## ASCII and animation video

- ASCII video: convert image/video/audio inputs into terminal-style colored ASCII MP4/GIF outputs; preserve composition and performance constraints.
- Manim: use for mathematical, algorithmic, or paper-explainer animations; plan scenes before rendering.

## Audio and music

- Songwriting: develop premise, structure, lyrics, rhyme/meter, genre tags, and Suno-style prompts.
- AI music generation: use HeartMuLa-style workflows when generating from lyrics and tags.
- Audio analysis: use spectrograms and features such as mel, chroma, and MFCC when analyzing songs or sounds.

## Verification

For generated media, report exact output paths/URLs and run or inspect the renderer/CLI output. For analyses, include the input file/source and extraction method.