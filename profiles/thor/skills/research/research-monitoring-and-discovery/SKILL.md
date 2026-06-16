---
name: research-monitoring-and-discovery
description: "Use when discovering, monitoring, or querying external research/intelligence sources such as arXiv, blogs/RSS feeds, prediction markets, or topic-specific knowledge bases."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, monitoring, discovery, arxiv, rss, markets]
    related_skills: [arxiv, llm-wiki, research-paper-writing]
---

# Research Monitoring and Discovery

## Overview

Use this umbrella for class-level research discovery and monitoring. It covers deciding which source to query, fetching real results, filtering for relevance, and reporting provenance. Narrow historical procedures are preserved in:

- `references/blogwatcher.md`

Specialist skills with scripts or large template packages, such as arXiv search, Polymarket, LLM Wiki, and research paper writing, can remain related skills when their support files are needed.

## When to Use

- The user asks what is new on a topic, blog, RSS feed, paper stream, or market.
- The task requires source monitoring rather than one-off web search.
- You need a repeatable source-specific discovery workflow.

## Source Routing

| Source class | Use for | Output standard |
|---|---|---|
| arXiv/papers | Scientific literature discovery | Titles, authors, dates, links, short relevance notes. |
| Blogs/RSS | Ongoing topic or author monitoring | Feed item title, URL, date, why it matters. |
| Prediction markets | Current beliefs/prices | Market title, price, timestamp, source link. |
| Knowledge bases | Focused domain recall | Cite note/source path and separate fact from synthesis. |

## Verification Checklist

- [ ] Results came from a real query/fetch, not memory.
- [ ] Dates/timestamps are included for current monitoring.
- [ ] URLs or stable IDs are included for follow-up.
- [ ] Summary separates source facts from interpretation.
