---
name: last30days
description: Safely research a topic over the last 30 days using available web/search tools and produce concise, source-linked findings.
version: 1.0.0
metadata:
  hermes:
    tags: [research, news, last30days, web]
    homepage: https://github.com/mvanhorn/last30days-skill
    source_note: "Local safe replacement created because the community repository was blocked by Hermes security scan as DANGEROUS."
---

# last30days — safe local research workflow

Use this skill when the user asks for `/last30days`, `last30`, or wants recent developments on a topic/company/ticker over roughly the last 30 days.

## Inputs

Parse the user's request into:
1. Topic or ticker(s)
2. Desired angle: news, recommendations, prompt ideas, product/company updates, risks, opportunities, or general overview
3. Output destination/format if stated

If the request is clear enough, do not ask clarification.

## Research workflow

1. Establish today's date with a tool when date math matters.
2. Search the web for the topic plus recency terms such as `last 30 days`, current month/year, `news`, `earnings`, `guidance`, `launch`, `lawsuit`, `analyst`, `partnership`, or other domain-specific terms.
3. Prefer primary or high-quality sources:
   - company IR/newsroom filings for public companies;
   - reputable financial/business media;
   - official blogs/docs for technical topics;
   - Reddit/X/YouTube only as sentiment or discussion signals, not as sole factual proof.
4. For each major claim, keep a source URL and date when available.
5. Filter out stale items older than 30 days unless they are needed for context and clearly labeled as background.

## Output for stock/company watchlist updates

For each ticker/company:

```markdown
### TICKER — Company Name
- YYYY-MM-DD — concise factual update. [Source](URL)
- YYYY-MM-DD — concise factual update. [Source](URL)

Why it matters: one sentence tying the updates to business quality, growth, risk, valuation, or watchlist thesis.
```

Guidelines:
- 2-4 bullets per ticker is enough.
- Focus on company-specific developments: earnings/guidance, major customers, product launches, regulatory/legal issues, M&A, financing/capex, analyst moves, management changes, or material stock-moving context.
- Avoid generic market-wide updates unless directly tied to the company.
- If research fails, write `Research unavailable` and state the tool/source limitation; do not invent facts.

## Verification

Before finalizing:
- Confirm every non-obvious factual claim has a source or is labeled as unsourced/context.
- Confirm dates are within the requested window.
- Confirm the final answer matches the requested destination/format.
