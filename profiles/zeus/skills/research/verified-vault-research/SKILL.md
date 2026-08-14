---
name: verified-vault-research
description: Use when turning one research question into a verified, dated, source-backed intelligence note in the vault. Splits the question, fans out across practitioner/social surfaces and official/web sources, extracts full-text receipts, runs a skeptic pass, and writes only surviving claims with expiry dates.
version: 1.0.0
author: Zeus
license: MIT
metadata:
  hermes:
    tags: [research, obsidian, vault, verification, last30days, receipts]
    related_skills: [last30days, youtube-content, obsidian, xurl, mcporter]
---

# Verified Vault Research Workflow

## Overview

This workflow turns one research question into vault intelligence instead of chatbot scrollback.

The goal is not to produce a confident-sounding answer. The goal is to create dated, linked, expiring research pages where every important claim has a receipt and weak claims are visibly labeled.

The core loop:

1. One question goes in.
2. Split it into 3-5 sub-questions.
3. Parallel agents search different surfaces.
4. Every finding becomes a receipt: claim, source link, source type, retrieved date.
5. A fresh skeptic agent attacks the claims and tries to kill them.
6. Verified survivors land in the vault as dated notes with expiry dates.

Use this especially for fast-moving domains where official docs lag reality: AI tools, model serving, creator workflows, growth tactics, dev tooling, automations, ads, commerce ops, and niche practitioner playbooks.

## When to Use

Use this when:

- The user asks for research that should become reusable knowledge.
- The topic changes quickly and stale advice is dangerous.
- Practitioner reality matters more than official positioning.
- You need to compare what people are actually running now against docs, pricing, and vendor claims.
- The output should feed an Obsidian vault, wiki, weekly intelligence brief, or decision memo.

Do not use this for:

- Simple factual lookups where one authoritative current source is enough.
- Private/personal tasks that do not need multi-source research.
- Pure writing/editing tasks after research is already complete.
- Legal, medical, tax, or financial advice without explicit caveats and authoritative sources.

## Default Stack

Use the best available tools in this order. If a tool is unavailable, state the gap and continue with the closest substitute.

### Practitioner Layer

- `last30days` powered by ScrapeCreators: sweep Reddit, X, YouTube, Instagram, TikTok and other surfaces for recent practitioner talk.
- Official X MCP or X CLI (`xurl`) when live posts, bookmarks, or threads are needed from source.
- YouTube transcripts via `yt-dlp` or the `youtube-content` skill.
- Instagram/TikTok via ScrapeCreators when short-form workflows are likely to surface first.

### Official / Web Layer

- Perplexity Deep Research or equivalent cited web research for long-read synthesis.
- Official docs, changelogs, pricing pages, GitHub repos, release notes, API docs.
- Firecrawl for full clean markdown extraction from pages worth keeping.

### Vault Layer

- Use the `obsidian` skill when writing or updating vault notes.
- Store durable output as dated notes with clear titles, source links, claim receipts, and expiry dates.
- Do not dump raw transcripts into core notes. Link or attach raw material separately if needed.

## Research Shape

### 1. Define the Research Question

Rewrite the question into a precise decision-oriented form.

Good:

- "What are practitioners using in July 2026 to automate short-form video clipping for podcasts, and what breaks?"
- "Which local LLM serving stack should a small team choose now for high-throughput OpenAI-compatible inference?"

Bad:

- "Research AI video tools."
- "Tell me about LLM serving."

Capture:

- Topic
- Decision to support
- Time window
- Geography or market, if relevant
- Intended audience
- Excluded areas

### 2. Split Into 3-5 Sub-Questions

Default split:

1. Practitioner reality: what are people actually using right now?
2. Failure modes: what breaks, disappoints, or wastes time?
3. Official facts: docs, pricing, limits, policies, roadmap, changelog.
4. Comparative options: viable alternatives and trade-offs.
5. Adoption signal: momentum, repeated mentions, real examples, counter-signals.

Adjust the split to the niche. Keep each sub-question small enough for one agent or pass.

### 3. Fan Out Across Surfaces

Run parallel searches when possible. Assign each surface a distinct job so findings are independent.

Suggested worker briefs:

#### Social / Practitioner Worker

Goal: Find what real users are doing in the last 30 days.

Look for:

- Reddit threads with comments from practitioners.
- X posts and threads with concrete workflows.
- YouTube walkthroughs, tutorials, demos, comments if accessible.
- TikTok/Instagram clips showing emerging workflows.
- Hacker News, GitHub issues, Discord/forum mirrors when relevant.

Return only claims with source URLs and dates.

#### Official / Docs Worker

Goal: Establish current official facts.

Look for:

- Pricing pages.
- API docs.
- Changelogs and release notes.
- Model/tool/version docs.
- Rate limits, region limits, licensing, usage restrictions.
- GitHub README/issues/releases if open source.

Return quote-level citations where possible.

#### Full-Text Extraction Worker

Goal: Pull clean text from important sources so the vault keeps more than a link.

Use Firecrawl or equivalent to extract:

- Blog posts.
- Docs pages.
- Tutorials.
- Case studies.
- Long forum posts.
- YouTube transcripts.

Return markdown snippets and original URLs.

#### Optional Market / Pricing Worker

Use when buying decisions are involved.

Look for:

- Current pricing.
- Free tier limits.
- Enterprise requirements.
- Hidden costs.
- Competitor pricing.
- Recent pricing changes.

#### Optional Skeptic Prep Worker

Use when the topic is noisy. This worker does not synthesize; it only collects contradictions, debunks, and complaints.

## Receipt Format

Every meaningful finding must become a receipt.

Use this compact schema:

```markdown
- claim: <specific claim, one sentence>
  status: unverified | single-source | supported | contradicted | stale-risk
  source: <url>
  source_type: official_docs | pricing | changelog | reddit | x | youtube | tiktok | instagram | github | blog | forum | other
  source_date: YYYY-MM-DD or unknown
  retrieved_date: YYYY-MM-DD
  evidence: "<short quote or paraphrase>"
  confidence: low | medium | high
  expiry_date: YYYY-MM-DD
```

Rules:

- No source link, no durable claim.
- One receipt should support one claim.
- Avoid vague claims like "users like it". Use concrete claims like "multiple Reddit users reported failed exports above 30 minutes."
- Label unknown source dates. Do not pretend retrieval date equals publication date.
- Prefer primary sources over summaries.

## Skeptic Gate

The skeptic must be a fresh agent or fresh pass that did not do the initial collection.

Skeptic job:

1. Attack every important claim.
2. Look for contradictions and missing context.
3. Downgrade hype based on single-source evidence.
4. Separate official claims from practitioner outcomes.
5. Flag stale or unverifiable claims.
6. Kill unsupported claims before vault write.

Skeptic prompt:

```text
You are the skeptic gate for this research. You did not collect these findings.
Your job is to kill weak claims, not to make the report sound good.

For each claim:
- Is the source primary, secondary, anecdotal, or unclear?
- Is there a date? Is it recent enough for this topic?
- Is the claim supported by the evidence, or stronger than the source allows?
- Are there contradictions in the evidence set?
- Is it single-source hype?
- What would make this claim false?

Return:
- survivors: claims safe to publish
- downgraded: claims that need weaker wording
- killed: claims that should not enter the vault
- contradictions: conflicts the final note must surface
- missing checks: searches that should be run before relying on this
```

Survival rules:

- Official pricing/API limits can survive with one current official source.
- Practitioner claims need repeated signal or explicit labeling as anecdotal.
- Vendor claims about performance, reliability, or adoption need independent support.
- Anything from a viral post without corroboration is `single-source` at best.
- If the claim depends on a fast-moving product, assign a short expiry.

## Expiry Dates

Every vault page and every important claim needs an expiry date.

Default expiry windows:

- AI model/tool pricing: 14-30 days.
- API capabilities/rate limits: 14-30 days.
- Practitioner workflow/tooling: 30-45 days.
- Social sentiment: 14-30 days.
- Stable concepts/frameworks: 90-180 days.
- Legal/compliance/policy: 14-30 days unless sourced from official current policy.

Use shorter expiry when:

- The product is in beta.
- The source is social only.
- The vendor is shipping weekly.
- Pricing, availability, or rate limits drive the decision.

Use longer expiry only when:

- The source is stable documentation.
- The claim is conceptual, not operational.
- Multiple sources agree across time.

## Vault Output Template

Create one main note per research question. Use clean markdown.

```markdown
---
type: research
status: verified
created: YYYY-MM-DD
updated: YYYY-MM-DD
expires: YYYY-MM-DD
topic: <topic>
tags: [research, <topic-tag>]
sources_count: <n>
confidence: low | medium | high
---

# <Research Question> — YYYY-MM-DD

## Answer

<5-10 bullet executive answer. Include uncertainty.>

## What changed recently

- <fresh finding with source link>

## Verified findings

### <Finding group>

- <claim> [source](url) — retrieved YYYY-MM-DD, expires YYYY-MM-DD.

## Practitioner layer

- What people are using:
- What breaks:
- Repeated complaints:
- Workarounds:

## Official facts

- Pricing:
- Limits:
- Docs/changelog:
- Requirements:

## Contradictions and caveats

- <contradiction or uncertainty>

## Receipts

<paste compact receipt list or link to companion receipt note>

## Killed or downgraded claims

- Killed: <claim> — reason.
- Downgraded: <claim> — safer wording.

## Next refresh

Refresh by YYYY-MM-DD. Re-check: <specific things likely to change>.
```

For large research, split into:

- Main synthesis note.
- `Sources - <topic> - YYYY-MM-DD` receipt note.
- `Raw extracts - <topic> - YYYY-MM-DD` note or folder.

## Writing Rules

- Write claims like intelligence, not marketing.
- Keep uncertainty visible.
- Prefer "Evidence suggests" over "This proves" unless proof is strong.
- Preserve contradictions; do not smooth them away.
- Include dates in the prose for fast-moving claims.
- Separate official capabilities from real-world practitioner outcomes.
- Do not cite a source you did not actually inspect.
- Do not use dead scrollback as the final artifact; write the vault note.

## Hermes Execution Pattern

For a full run inside Hermes:

1. Load relevant skills:
   - `last30days` for recent practitioner/social sweep.
   - `youtube-content` for transcripts.
   - `obsidian` for vault writes.
   - `xurl` or MCP skills if X is needed.
2. Use `delegate_task` for parallel independent workers when the research is broad.
3. Keep worker outputs receipt-shaped.
4. Run a separate skeptic worker or fresh pass.
5. Write verified output to the vault.
6. Report final path, confidence, expiry date, and top caveats.

Example delegation set:

```text
Worker A: Search social/practitioner layer from the last 30 days. Return only receipts.
Worker B: Search official docs/pricing/changelogs. Return only receipts.
Worker C: Extract full text/transcripts from the 5-10 best sources. Return markdown excerpts and receipts.
Worker D: Skeptic pass after A-C complete. Attack every claim and produce survivors/kills/contradictions.
```

Do not let the same agent that collected findings be the only validator.

## Weekly Research Machine

For recurring niche intelligence:

- Run once per week per niche.
- Keep the same question family so changes are comparable.
- Add a `What changed since last run` section.
- Expire or update old pages instead of silently accumulating stale notes.
- Promote repeated patterns into evergreen notes only after they survive multiple runs.

Weekly output should include:

- New verified findings.
- Changed pricing/API/doc facts.
- New practitioner workflows.
- Repeated failures/complaints.
- Contradictions.
- Items to watch next week.

## Common Pitfalls

1. One-prompt research. A single chatbot answer is not research. Split the question and collect receipts.

2. Social hype laundering. Viral posts are signals, not facts. Label them as single-source unless corroborated.

3. Stale official docs. Official docs can lag shipped reality, especially in AI tooling. Compare against recent practitioner evidence.

4. Source-date confusion. Retrieval date is not publication date. Track both when possible.

5. Dead links as knowledge. A URL alone is not a receipt. Capture the claim and evidence quote/snippet.

6. Over-synthesis. Do not flatten contradictions into a clean answer. Contradictions are often the most valuable output.

7. No expiry date. If a note does not expire, stale knowledge will look current.

8. Same-agent validation. A model reviewing its own research will often preserve its own mistakes. Use a fresh skeptic.

9. Raw transcript dumping. Transcripts are inputs. The vault page should contain verified claims and links to raw extracts.

10. Treating practitioner anecdotes as universal. Anecdotes are useful but must be labeled, clustered, and checked.

## Verification Checklist

Before finishing a research run:

- [ ] The original question was rewritten into a precise research objective.
- [ ] It was split into 3-5 sub-questions.
- [ ] Practitioner/social surfaces were searched for recent evidence.
- [ ] Official docs/pricing/changelog sources were checked when relevant.
- [ ] Important pages/videos were extracted or summarized from full text/transcripts.
- [ ] Every important claim has a source link and retrieved date.
- [ ] Single-source claims are labeled.
- [ ] Contradictions are surfaced.
- [ ] A fresh skeptic pass killed or downgraded weak claims.
- [ ] The final vault note has created/updated/expires dates.
- [ ] The answer includes caveats and refresh instructions.
- [ ] The user receives the note path, confidence, expiry date, and top caveats.
