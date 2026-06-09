---
name: research-intelligence-workflows
description: "Use when discovering, monitoring, synthesizing, or writing from research sources: arXiv, blogs/RSS, LLM wikis, prediction markets, YouTube transcripts, and academic paper workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, arxiv, rss, blogs, youtube, polymarket, literature-review, papers]
    related_skills: []
---

# Research Intelligence Workflows

## Overview

This umbrella covers research discovery and synthesis across academic papers, RSS/blog monitoring, prediction markets, domain wikis, YouTube transcripts, and ML paper writing. Use it when the task is to find sources, monitor changes, summarize evidence, or turn research into a written artifact.

## When to Use

- Search or retrieve arXiv papers, metadata, PDFs, or BibTeX.
- Monitor blogs/RSS feeds or summarize new posts.
- Build/query an interlinked LLM/domain wiki.
- Query Polymarket markets, prices, orderbooks, or history.
- Extract and transform YouTube transcripts into summaries, threads, or blogs.
- Plan, write, or revise ML research papers.

## Research Workflow

1. Clarify the question and output format.
2. Choose source mode: papers, feeds, markets, transcripts, wiki, or writing pipeline.
3. Retrieve primary data with tools; do not invent current facts.
4. Normalize citations/URLs/market IDs/video IDs early.
5. Synthesize with provenance: separate claims, evidence, and uncertainty.
6. For writing, maintain contribution, experiment, evaluation, and reviewer-checklist sections.

## Source Modes

### arXiv / Papers
Use arXiv search by keyword, author, category, or ID. Fetch specific papers and produce BibTeX/citations when requested.

### Blog/RSS Monitoring
Use blogwatcher-style tools for feed registration, update checks, and concise change summaries.

### LLM Wiki / Knowledge Base
Resume existing wiki state before adding pages. Preserve frontmatter and links; keep domain conventions consistent.

### Prediction Markets
Use public Polymarket APIs for market discovery, prices, orderbooks, and history. Parse double-encoded fields and report limitations.

### YouTube Transcripts
Fetch transcripts, then produce the requested format: summary, thread, blog post, outline, or extracted claims.

### Paper Writing
Treat paper writing as a full pipeline: setup, related work, experiments, result analysis, human evaluation where needed, citations, and reviewer-readiness.

## Archived Package References

Former narrow skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with original SKILL.md and support files intact.

## Common Pitfalls

- Treating a model-generated summary as a source.
- Failing to cite URLs/IDs for current claims.
- Losing the distinction between evidence and interpretation.
- Ignoring pagination or rate limits.

## Verification Checklist

- [ ] Source data was actually fetched.
- [ ] Citations/URLs/IDs are included for important claims.
- [ ] The final output matches the requested format and preserves uncertainty.
