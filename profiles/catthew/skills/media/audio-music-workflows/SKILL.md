---
name: audio-music-workflows
description: "Use when creating, prompting, generating, or analyzing music/audio: songwriting, Suno-style prompts, HeartMuLa/AudioCraft generation, and spectrogram or feature analysis."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [audio, music, songwriting, suno, audiocraft, heartmula, spectrograms]
    related_skills: []
---

# Audio and Music Workflows

## Overview

This umbrella covers music and audio work across the pipeline: writing lyrics, creating AI music prompts, generating audio with local/model tools, and analyzing audio with spectrogram/features. The common goal is an actual musical or analytical artifact backed by tool output when generation/analysis is requested.

## When to Use

- The user asks for lyrics, song structure, parody/adaptation, or Suno-style prompts.
- The user asks to generate music or sound effects with AudioCraft/MusicGen/AudioGen or HeartMuLa-like tools.
- The user asks for spectrograms, mel/chroma/MFCC features, or audio visualization.
- The user wants both creative direction and technical generation settings.

## Songwriting and Prompting

Establish genre, mood, perspective, tempo/energy, structure, and lyrical constraints. Use tags and section markers appropriate to the target generator. Write lyrics that scan: meter, rhyme, singability, emotional arc, and contrast matter.

## Generation Tools

Check hardware and Python/version requirements before installing or running heavy audio models. AudioCraft/MusicGen fits text-to-music and AudioGen fits text-to-sound effects. HeartMuLa-style workflows require model setup and enough VRAM/CPU budget. Save generated audio to a named file and return the path/media handle.

## Audio Analysis

Use spectrogram and feature extraction when the user asks what is in an audio file or wants visuals. Choose visualization type deliberately: waveform, spectrogram, mel, chroma, MFCC, or onset/tempo features. Report parameters when they matter.

## Common Pitfalls

1. Prompt-only when generation was requested.
2. Ignoring hardware constraints.
3. Overstuffed tags.
4. Unverified outputs.

## Verification Checklist

- [ ] Creative brief or analysis question is clear.
- [ ] Required model/CLI dependencies were checked before use.
- [ ] Generated/analysis artifact path exists.
- [ ] Final answer includes prompts/settings and output files or blockers.
