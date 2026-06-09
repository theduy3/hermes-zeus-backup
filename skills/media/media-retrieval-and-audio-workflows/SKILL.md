---
name: media-retrieval-and-audio-workflows
description: "Use when retrieving GIFs or YouTube transcripts, generating AI music, or analyzing audio features/spectrograms."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [media, gif, youtube, transcript, music-generation, audio, spectrogram]
    related_skills: []
---

# Media Retrieval and Audio Workflows

## Overview

This umbrella covers lightweight media operations that are not full creative design projects: GIF search/download, YouTube transcript extraction/transformation, AI music generation with HeartMuLa-style tools, and audio visualization/feature extraction.

## When to Use

- The user asks to find or download a GIF.
- The user asks to fetch a YouTube transcript or convert it into a summary/thread/blog.
- The user asks to generate music/audio from lyrics and tags.
- The user asks to create spectrograms or extract mel/chroma/MFCC-style features.

## Modes

### GIF Search
Use Tenor/curl+jq workflows. Fetch metadata before downloading and choose the right media format for the delivery channel.

### YouTube Transcripts
Fetch transcripts with a helper script or transcript API, then transform into the requested output. Include video URL/ID and note transcript availability failures.

### AI Music Generation
Use HeartMuLa-style and AudioCraft/MusicGen workflows when local hardware and dependencies are available. Separate lyrics, tags, model choice, and output file path.

### Audio Feature Visualization
Use Songsee-style CLI workflows for spectrograms and features. Verify output image/audio paths and include parameters used.

## Archived Package References

Former narrow skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with original SKILL.md and support files intact.

## Common Pitfalls

- Assuming every YouTube video has a transcript.
- Downloading an unnecessarily large GIF format.
- Starting audio generation without checking GPU/dependency requirements.
- Reporting generated media without a local path or URL.

## Verification Checklist

- [ ] Source media or prompt inputs are explicit.
- [ ] Output path/URL is captured.
- [ ] Retrieval/generation command returned successfully or the blocker is documented.
