---
name: creative-browser-artifacts
description: "Use when creating visual browser-based artifacts: HTML/CSS mockups, landing pages, architecture diagrams, Excalidraw-style diagrams, p5.js sketches, design tokens, or design-system-inspired pages."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, html, css, diagrams, p5js, design, mockups, excalidraw]
    related_skills: []
---

# Creative Browser Artifacts

## Overview

This umbrella covers visual artifacts delivered as browser-viewable files or design specs: HTML pages, mockup variants, landing/deck/prototype pages, architecture diagrams, Excalidraw JSON, p5.js generative sketches, typographic demos, and DESIGN.md token specs. The shared workflow is to make the artifact real, viewable, and iterated.

## When to Use

- The user asks for a mockup, prototype, landing page, visual concept, or design variants.
- The output should be HTML/CSS/JS, p5.js, SVG/diagram, or Excalidraw.
- The user wants design-system inspiration or tokenized design guidance.
- The user wants architecture/cloud/infra diagrams with polished visual language.

## Core Workflow

1. Determine artifact type: mockup, page, diagram, sketch, token spec, or typographic demo.
2. Pick a visual direction from user context, not generic vibes.
3. Create a real file with complete HTML/CSS/JS or the target diagram/spec format.
4. Include enough sample content/data to judge layout.
5. Verify by opening/rendering/exporting when possible.
6. Return the path/link and concise design choices.

## Labeled Subsections

### HTML Mockups and Prototypes
Build 2–3 variants when comparing directions. Use polished spacing, typography, color systems, and responsive behavior.

### Architecture and Excalidraw Diagrams
Choose diagram grammar first: cloud architecture, flow, sequence, system map, or hand-drawn sketch. Use semantic color and grouping. For Excalidraw, produce valid JSON and verify required fields.

### p5.js and Creative Demos
Use p5.js for generative art, shader-like effects, interactive sketches, 2D/3D motion, and frame export. Keep sketches self-contained with controls or deterministic seeds when useful.

### DESIGN.md and Tokens
Use DESIGN.md for reusable design-token specs. Separate colors, typography, spacing, components, and usage rules.

## Common Pitfalls

1. Describing instead of building a file/renderable artifact.
2. One-size-fits-all aesthetics.
3. Invalid diagram/spec formats.
4. No preview evidence.

## Verification Checklist

- [ ] Artifact file exists and is complete.
- [ ] Syntax/format is valid for the chosen medium.
- [ ] Visual choices match the requested style and use case.
- [ ] Final response includes file path/link and preview/export notes.
