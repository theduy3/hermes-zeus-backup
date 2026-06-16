---
name: creative-html-artifacts
description: "Use when designing one-off browser-rendered artifacts: landing pages, prototypes, HTML mockups, and style explorations. Consolidates design generation, variant comparison, and web visual polish workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, html, css, design, prototypes, mockups]
    related_skills: [popular-web-designs, architecture-diagram, p5js]
---

# Creative HTML Artifacts

## Overview

Use this umbrella for browser-rendered visual deliverables: landing pages, throwaway prototypes, mockups, decks, and design variants. Narrow historical procedures are preserved in:

- `references/claude-design.md`
- `references/sketch.md`

Keep heavyweight specialist packages such as architecture diagrams, p5.js, Pretext, and popular-web-design templates as references or related skills when their support files are needed.

## When to Use

- The user asks for an HTML/CSS visual artifact.
- The task benefits from 2-3 quick variants before choosing a direction.
- The goal is visual communication rather than production app code.
- You need to imitate or synthesize modern web design systems.

## Workflow

1. Identify the artifact type: landing page, explainer, deck, dashboard, mockup, or prototype.
2. Establish visual constraints: audience, tone, aspect ratio, brand/style references, required content.
3. Produce a self-contained HTML artifact with inline CSS/JS unless the user requests a framework.
4. For subjective design tasks, create multiple variants and label trade-offs.
5. Verify by opening/rendering the artifact or checking generated markup for obvious breakage.

## Design Heuristics

- Use real hierarchy: headline, subhead, primary action, supporting details.
- Prefer fewer, stronger visual motifs over scattered decoration.
- Include responsive behavior if the artifact may be viewed in a browser.
- Treat screenshots and existing design systems as constraints, not optional inspiration.

## Verification Checklist

- [ ] Artifact is self-contained or dependencies are clearly listed.
- [ ] Visual hierarchy and spacing are deliberate.
- [ ] The deliverable was rendered or syntax-checked when tooling was available.
- [ ] User can open/copy the output without hidden session state.
