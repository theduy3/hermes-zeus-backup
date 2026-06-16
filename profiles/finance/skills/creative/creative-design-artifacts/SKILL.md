---
name: creative-design-artifacts
description: "Use when creating visual design artifacts: HTML mockups, design-system-inspired pages, architecture diagrams, Excalidraw diagrams, DESIGN.md token specs, or one-off design prototypes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [design, html, diagrams, excalidraw, architecture, prototypes, design-systems]
    related_skills: []
---

# Creative Design Artifacts

## Overview

This umbrella covers static visual deliverables: architecture diagrams, Excalidraw sketches, HTML mockups, design-system references, and DESIGN.md token specs. The common workflow is: choose the artifact type, gather constraints, produce a complete file, then open or validate it.

## When to Use

- The user wants a diagram, design mockup, landing page, prototype, deck-like HTML artifact, or visual spec.
- The output is primarily visual/static rather than an interactive app or generative animation.
- You need to choose between polished HTML/CSS, hand-drawn Excalidraw, SVG diagrams, or a DESIGN.md token document.

## Artifact Selection

- Architecture diagram: use dark SVG/HTML diagrams for infra, cloud, service maps, and system flows.
- Excalidraw: use for hand-drawn architecture, flows, sequence diagrams, and collaborative sketch files.
- HTML prototype/mockup: use for landing pages, dashboards, screens, decks, or multiple design variants.
- Popular web design references: use real design-system patterns as inspiration, not as copied branding.
- DESIGN.md: use when the deliverable is a portable design-token/spec document.
- Sketch variants: use when the user wants several fast alternatives before implementation.

## Workflow

1. Clarify target format only if it materially changes the artifact; otherwise choose the default suited to the ask.
2. Establish audience, dimensions, tone, palette, and content hierarchy.
3. Generate a complete artifact file, not a partial snippet.
4. Validate syntax and open/render when possible.
5. Iterate based on visible output, not just code inspection.

## Quality Bar

- Strong hierarchy and spacing.
- Legible typography and contrast.
- Specific visual metaphors tied to the user's content.
- No placeholder lorem ipsum unless explicitly requested.
- Export or delivery instructions included when the format needs them.

## Diagram Notes

- Prefer semantic grouping, labeled arrows, and concise annotations over dense walls of text.
- For Excalidraw, preserve valid JSON structure and use consistent roughness/colors.
- For architecture diagrams, include legends and trust boundaries when security or infra is involved.

## HTML/Prototype Notes

- Deliver a self-contained HTML file unless the user asks for framework code.
- Use CSS variables/design tokens for maintainability.
- Avoid external assets that may break offline unless required.

## Package Notes

The archived source packages preserve specialized templates and references for architecture diagrams, Excalidraw, design systems, DESIGN.md, Claude-style design prompts, and sketch variants. Restore them if a task needs their full template banks.

## Verification Checklist

- [ ] Output format matches the user's requested deliverable.
- [ ] File validates/parses for the chosen format.
- [ ] Visual result was inspected or a rendering path was provided.
- [ ] The artifact is complete enough to hand to the user directly.
