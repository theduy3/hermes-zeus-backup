---
name: life-knowledge-base
description: "Use when capturing or retrieving private life context."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [private, markdown, provenance, context]
    related_skills: [life-tracker]
---
# Life Knowledge Base

## When to Use
Use for durable private personal context and evidence-only exports.

## Steps
1. Read `/home/hermes/.hermes/projects/life-os/life-knowledge-base/agent_rules.md`.
2. Lexically search the KB, then read the canonical summary and newer records.
3. Capture only durable context; label epistemic state and provenance.
4. Preserve corrections with supersession; do not invent facts.
5. Validate with `python3 /home/hermes/.hermes/projects/life-os/tracker/tools.py`.

## Pitfalls
Never use `/vault/AgentMemory`; it is quarantined generated output. Reject secrets and never transmit KB contents without approval.

## Verification
- [ ] Rules and authority searched
- [ ] Status/provenance explicit
- [ ] Validator passes
