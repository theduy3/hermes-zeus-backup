---
name: creative-artifact-generation
description: "Use when producing visual, textual, interactive, diagrammatic, animation, web-design, infographic, ASCII, or music-prompt creative artifacts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, design, diagrams, html, ascii, p5js, manim, infographics, songwriting]
    related_skills: []
---

# Creative Artifact Generation

## Overview

This umbrella covers creative production workflows: diagrams, one-off HTML designs, mockups, design systems, p5.js/pretext sketches, Manim animations, ASCII art/video, infographics, humanized prose, and songwriting/music prompts. Treat these as modes of one artifact-generation class with shared standards: understand the audience, choose a medium, generate a concrete artifact, and verify/render it.

## When to Use

- The user asks for a visual/design artifact, diagram, infographic, mockup, landing page, or prototype.
- The user asks for generative art, p5.js, pretext, Manim, ASCII art, or ASCII video.
- The user asks to humanize prose or produce lyrics/music prompts.
- The user asks for style-system-driven output such as DESIGN.md or popular web-design references.

## Universal Creative Workflow

1. Identify the deliverable medium and constraints: static image/SVG/HTML, interactive HTML, video, text, or prompt.
2. Choose the mode below and use its archived package reference for detailed recipes when needed.
3. Produce an actual artifact file or final text, not just a concept.
4. Verify by rendering, opening, linting, or otherwise checking the output when tools allow.
5. Report the artifact path/URL and what verification returned.

## Modes

### Diagrams and Infographics
Use architecture-diagram, Excalidraw, or Baoyu infographic patterns depending on whether the desired style is polished SVG/HTML, hand-drawn, or visual-explanatory.

### HTML Design and Mockups
Use Claude Design, Sketch, Popular Web Designs, or DESIGN.md patterns for polished one-off artifacts, variant exploration, real-design-system imitation, or token-spec authoring.

### Generative and Interactive Art
Use p5.js and pretext patterns for browser sketches, shaders, typography-as-geometry, interaction, and export pipelines.

### Animation and Video
Use Manim for math/algorithm/3Blue1Brown-style explanatory animation. Use ASCII-video for stylized terminal/video transformations.

### Text and Voice
Use Humanizer for removing AI-isms and adding calibrated voice. Use Songwriting/AI Music patterns for lyrics, structure, meter, Suno-style prompts, and phonetic tricks.

### ASCII Utility Art
Use ASCII-art patterns for pyfiglet, cowsay, boxes, TOIlet, and image-to-ASCII conversions.

## Archived Package References

Former narrow skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with original SKILL.md and support files intact.

## Common Pitfalls

- Picking a medium before understanding the user’s use case.
- Delivering a design description instead of a real artifact.
- Forgetting to render or inspect generated HTML/video/image outputs.
- Flattening style guides into generic “modern” visuals rather than applying concrete tokens/examples.

## Verification Checklist

- [ ] Medium, style, and audience are explicit.
- [ ] Artifact was generated or final creative text was delivered.
- [ ] Render/lint/export verification was run where applicable.
