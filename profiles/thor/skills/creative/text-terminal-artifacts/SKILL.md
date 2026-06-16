---
name: text-terminal-artifacts
description: "Use when creating text-mode visual artifacts: ASCII art, terminal-styled banners, boxes, or conversions of images/video into character-based media. Consolidates static and animated ASCII workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ascii, terminal-art, text-art, media]
    related_skills: [ascii-video]
---

# Text and Terminal Artifacts

## Overview

Use this umbrella for character-based visual deliverables. Static ASCII banners and boxes share planning concerns with animated ASCII video: choose a rendering style, preserve legibility at the target size, and verify the output in the medium where the user will consume it.

Absorbed narrow procedures are preserved in:

- `references/ascii-art.md`

The larger ASCII video package remains a related specialist skill when its multi-file rendering pipeline is needed.

## When to Use

- The user asks for ASCII art, terminal banners, boxes, or text illustrations.
- The user asks to convert images/video into character-based output.
- The artifact must render acceptably in monospaced text.

## Workflow

1. Identify the output medium: chat, terminal, Markdown, image, GIF, or MP4.
2. Choose static tools for banners/boxes and video tools for frame-based media.
3. Check width constraints; most chat clients wrap long lines.
4. Preview the exact text or generated file before final delivery.

## Verification Checklist

- [ ] Output fits the target width.
- [ ] Monospace formatting is preserved.
- [ ] Generated files exist and are non-empty when media conversion is used.
- [ ] Final answer includes the artifact or a valid path/attachment.
