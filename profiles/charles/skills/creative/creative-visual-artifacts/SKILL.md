---
name: creative-visual-artifacts
description: "Use when creating visual artifacts: HTML mockups, design systems, diagrams, infographics, generative sketches, ASCII/video art, Manim animations, Excalidraw, TouchDesigner, or ComfyUI workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, visual-design, diagrams, html, generative-art, animation, video]
    related_skills: []
---

# Creative Visual Artifacts

## Overview

This is the discoverable umbrella for visual creation workflows. It keeps the mode-selection guidance in one place while preserving each renderer/tool package under `references/source-packages/`.

## When to Use

- Produce a visual artifact, mockup, diagram, animation, infographic, or generative art piece.
- Choose among HTML/CSS, p5.js, Manim, Excalidraw, ASCII, TouchDesigner, ComfyUI, or design-system templates.
- Need a quick creative prototype and then verification/export.

## Mode Selection

- **HTML one-offs and landing/deck/prototype artifacts:** `claude-design`, `popular-web-designs`, `sketch`, `design-md`.
- **Architecture/flow diagrams:** `architecture-diagram` or `excalidraw`.
- **Infographics/knowledge visuals:** `baoyu-infographic`.
- **Generative browser art:** `p5js` and `pretext`.
- **Math/algorithm animation:** `manim-video`.
- **ASCII art/video:** `ascii-art`, `ascii-video`.
- **Node-based realtime/generative media:** `touchdesigner-mcp` or `comfyui`.

## Standard Workflow

1. Clarify output medium, aspect ratio, audience, and delivery format only when not obvious.
2. Pick the narrow renderer reference package.
3. Create a real artifact file, not just prose.
4. Run the renderer/export/validation path for that medium.
5. Return the artifact or a screenshot/link with notes on limitations.

## Package References

Full source packages are copied under `references/source-packages/<old-skill>/`.

## Common Pitfalls

1. Do not use generic AI-image prompting when the user asked for editable HTML/SVG/JSON/code artifacts.
2. Preserve templates/scripts when demoting tool-heavy skills; many renderers depend on support files.
3. Verify outputs by opening, rendering, linting, or exporting where feasible.

## Verification Checklist

- [ ] Medium/tool selected deliberately.
- [ ] Source package consulted for exact commands/templates.
- [ ] Artifact generated and verified with a concrete tool output.
