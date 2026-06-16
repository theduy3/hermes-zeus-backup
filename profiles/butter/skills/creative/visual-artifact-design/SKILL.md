---
name: visual-artifact-design
description: "Umbrella for visual and browser-delivered creative artifacts: diagrams, mockups, design systems, design tokens, Excalidraw, p5.js, Pretext, and infographic formats."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, design, diagrams, html, css, mockups, p5js, excalidraw, infographic, design-systems]
---

# Visual Artifact Design

Use this umbrella when the deliverable is a visual artifact or interactive design: architecture diagrams, Excalidraw sketches, HTML mockups, visual design systems, DESIGN.md token specs, p5.js sketches, Pretext text layouts, or infographic prompts.

## Choose the right medium

- Architecture/cloud/system diagrams: dark SVG/HTML or Excalidraw depending on whether polished or hand-drawn style is requested.
- Quick UI exploration: produce 2-3 throwaway HTML variants before committing.
- Brand/style mimicry: use design-system references and HTML/CSS tokens.
- Token specs: write/validate/export DESIGN.md-style design-token documents.
- Generative/interactivity: use p5.js for canvas/WebGL sketches; use Pretext for text-as-geometry and kinetic typography.
- Infographics: pick an explicit layout and visual style, then transform dense content into a structured visual prompt.

## Shared workflow

1. Clarify audience, format, aspect ratio, theme, and required content density.
2. Pick one medium and avoid mixing incompatible conventions.
3. Create a runnable/viewable artifact, not just prose.
4. Verify by opening/rendering/exporting when tools are available.
5. Preserve source files so the user can edit them later.

## Package integrity

Many visual skills carry templates, references, or scripts. When consolidating or adapting them, keep linked assets with the skill package or re-home all referenced files and rewrite paths.