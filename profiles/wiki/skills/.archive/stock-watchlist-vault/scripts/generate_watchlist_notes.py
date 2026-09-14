#!/usr/bin/env python3
"""
Starter generator for /vault/Notes/Stock Watchlist/ company evaluation pages.

Run from any cwd on the wiki profile host:
    python3 generate_watchlist_notes.py

This is intentionally a starter script: update MANUAL_NAMES and ALIASES as the
watchlist changes. It writes under /vault/Notes/Stock Watchlist and appends a
wiki-log entry.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

VAULT = Path("/vault")
NOTES = VAULT / "Notes"
OUT = NOTES / "Stock Watchlist"
CONFIG = VAULT / "System" / "Stock Watchlist.md"
TODAY = datetime.now(ZoneInfo("America/Vancouver")).date().isoformat()

MANUAL_NAMES = {
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "GOOG": "Alphabet / Google",
    "META": "Meta Platforms",
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA",
    "PLTR": "Palantir Technologies",
    "TSM": "Taiwan Semiconductor Manufacturing / TSMC",
    "ASML": "ASML Holding",
    "AVGO": "Broadcom",
    "AMD": "Advanced Micro Devices",
    "ORCL": "Oracle",
    "CRM": "Salesforce",
    "DELL": "Dell Technologies",
    "NFLX": "Netflix",
    "MELI": "MercadoLibre",
}

ALIASES = {
    "MSFT": ["Microsoft", "Azure", "OpenAI"],
    "AMZN": ["Amazon", "AWS"],
    "GOOG": ["Google", "Alphabet", "Gemini"],
    "META": ["Meta", "Facebook", "Instagram"],
    "AAPL": ["Apple", "iPhone"],
    "TSLA": ["Tesla", "Elon Musk"],
    "NVDA": ["NVIDIA", "Nvidia", "GPU"],
    "PLTR": ["Palantir"],
    "TSM": ["TSMC", "Taiwan Semiconductor"],
    "ASML": ["ASML"],
    "AVGO": ["Broadcom"],
    "AMD": ["AMD", "Advanced Micro Devices"],
    "ORCL": ["Oracle"],
    "CRM": ["Salesforce"],
    "DELL": ["Dell"],
    "NFLX": ["Netflix"],
    "MELI": ["MercadoLibre"],
}


def parse_watchlist() -> list[str]:
    tickers = []
    current = None
    for line in CONFIG.read_text().splitlines():
        s = line.strip()
        if s.startswith("Indicators:"):
            current = "indicators"
            continue
        if s.startswith("Watchlist:"):
            current = "watchlist"
            continue
        if current == "watchlist" and s.startswith("- "):
            tickers.append(s[2:].strip())
    return tickers


def fetch_watchlist_json() -> dict[str, dict]:
    proc = subprocess.run(
        ["python3", str(VAULT / "System/scripts/fetch_watchlist.py"), "--json"],
        capture_output=True,
        text=True,
        timeout=300,
    )
    start = proc.stdout.find("{")
    if start < 0:
        return {}
    data = json.loads(proc.stdout[start:])
    return {d.get("ticker"): d for d in data.get("watchlist", [])}


def fmt_money(x):
    if x is None:
        return "N/A"
    try:
        x = float(x)
    except Exception:
        return str(x)
    if abs(x) >= 1e12:
        return f"${x/1e12:.2f}T"
    if abs(x) >= 1e9:
        return f"${x/1e9:.1f}B"
    if abs(x) >= 1e6:
        return f"${x/1e6:.1f}M"
    return f"${x:,.0f}"


def fmt_num(x, suffix="", nd=1):
    if x is None:
        return "N/A"
    try:
        return f"{float(x):.{nd}f}{suffix}"
    except Exception:
        return str(x)


def suggestion(d: dict) -> str:
    if not d or "error" in d:
        return "Hold / Watch"
    up = d.get("upside_pct")
    pe = d.get("forward_pe")
    if up is not None and up < 0:
        return "Reduce / Avoid adding"
    if pe is not None and pe > 100 and (up is None or up < 20):
        return "Reduce / Wait for pullback"
    if up is not None and up >= 35 and (pe is None or pe < 80):
        return "Add on weakness"
    if up is not None and up >= 15:
        return "Hold / Opportunistic add"
    if up is None:
        return "Hold / Research further"
    return "Hold"


def note_stem(ticker: str, name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9 .&-]+", "", f"{ticker} {name}").strip()
    return re.sub(r"\s+", " ", safe)[:90]


def load_docs():
    docs = []
    for p in NOTES.rglob("*.md"):
        if OUT in p.parents:
            continue
        try:
            docs.append((p, p.read_text(errors="ignore")))
        except Exception:
            pass
    return docs


def find_links(ticker: str, docs) -> list[tuple[int, str]]:
    terms = []
    bare = ticker.replace(".TO", "")
    if len(bare) >= 3:
        terms += [re.escape(bare), re.escape(ticker)]
    for alias in ALIASES.get(ticker, []):
        if len(alias) >= 3:
            terms.append(re.escape(alias))
    terms = list(dict.fromkeys(terms))
    if not terms:
        return []
    pat = re.compile(r"(?i)(?<![A-Za-z0-9])(" + "|".join(terms) + r")(?![A-Za-z0-9])")
    hits = []
    for p, text in docs:
        count = len(list(pat.finditer(text)))
        if count:
            hits.append((count, p.stem))
    return sorted(hits, key=lambda x: (-x[0], x[1].lower()))


def write_company_page(ticker: str, d: dict, links: list[tuple[int, str]]):
    name = MANUAL_NAMES.get(ticker, ticker)
    sug = suggestion(d)
    stem = note_stem(ticker, name)
    related = "\n".join(
        f"- [[{stem}]] ({count} mention{'s' if count != 1 else ''})"
        for count, stem in links
    ) or "- No existing Notes/ links found yet."
    sources = "\n" + "\n".join(f'  - "[[{stem}]]"' for _, stem in links[:10]) if links else "[]"
    data_issue = f"\nData issue: {d.get('error')}\n" if d.get("error") else ""
    content = f"""---
tags:
  - finance
  - watchlist
  - stocks
type: entity
created: {TODAY}
updated: {TODAY}
ticker: {ticker}
suggestion: "{sug}"
sources: {sources}
wiki_status: draft
---

# {ticker} — {name}

> Working investment note, not financial advice. Update after earnings, major news, or thesis changes.

## Snapshot

| Field | Value |
|---|---:|
| Ticker | {ticker} |
| Company / Instrument | {name} |
| Price | {fmt_money(d.get('price'))} |
| Daily change | {fmt_num(d.get('change_pct'), '%')} |
| 52W range | {fmt_money(d.get('week52_low'))} – {fmt_money(d.get('week52_high'))} |
| Forward P/E | {fmt_num(d.get('forward_pe'))} |
| Market cap | {fmt_money(d.get('market_cap'))} |
| Analyst target | {fmt_money(d.get('target_mean'))} |
| Implied upside | {fmt_num(d.get('upside_pct'), '%')} |

## Suggestion

**{sug}.**

Reasoning: automatically generated triage from current watchlist data, valuation, analyst-target upside, and vault context. Replace with manual conviction after review.
{data_issue}
## Evaluation

- Business / exposure: {name} is tracked in the personal stock watchlist.
- Valuation check: forward P/E is **{fmt_num(d.get('forward_pe'))}** and analyst-target upside is **{fmt_num(d.get('upside_pct'), '%')}**.
- Vault context: {len(links)} existing note(s) mention this company/instrument or a close alias.

## Scenarios

### Base
Monitor execution versus current market expectations.

### Bull
Revenue growth, margins, and/or market narrative improve faster than expected and the stock moves toward or above the analyst target.

### Bear
Guidance disappoints, valuation multiple compresses, or company-specific news weakens the thesis.

## Decision Rules

- **Add** if new evidence strengthens the bull case and valuation/risk are acceptable.
- **Hold** if thesis is intact but upside is moderate, data is incomplete, or position sizing is already full.
- **Reduce** if the bear case starts playing out, valuation becomes unsupported, or better watchlist opportunities appear.

## Related Notes Mentioning This Company

{related}

## Open Questions

- What is the one-sentence thesis for owning this rather than only watching it?
- What event would make this an Add?
- What event would force a Reduce or removal from the watchlist?
- What position size is appropriate relative to conviction and downside?

## Related

- [[Stock Watchlist Index]]
- [[Finance MOC]]
- [[Stock Trading Masterplan]]
- [[Stock Market Trading Rules]]
"""
    (OUT / f"{stem}.md").write_text(content)
    return stem, sug, len(links), name


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tickers = parse_watchlist()
    data = fetch_watchlist_json()
    docs = load_docs()
    rows = []
    for ticker in tickers:
        stem, sug, nlinks, name = write_company_page(ticker, data.get(ticker, {}), find_links(ticker, docs))
        rows.append((ticker, name, sug, nlinks, stem))
    index = [
        "---", "tags:", "  - finance", "  - watchlist", "  - stocks", "type: synthesis",
        f"created: {TODAY}", f"updated: {TODAY}", "sources:", '  - "[[Stock Watchlist]]"',
        "wiki_status: draft", "---", "", "# Stock Watchlist Index", "",
        "| Ticker | Company / Instrument | Suggestion | Linked Notes | Page |",
        "|---|---|---|---:|---|",
    ]
    for ticker, name, sug, nlinks, stem in rows:
        index.append(f"| {ticker} | {name} | {sug} | {nlinks} | [[{stem}]] |")
    (OUT / "Stock Watchlist Index.md").write_text("\n".join(index) + "\n")
    with (VAULT / "System/wiki-log.md").open("a") as f:
        f.write(f"\n## [{TODAY}] enhance | Stock Watchlist company evaluation folder\n\n")
        f.write(f"- Created/updated `/vault/Notes/Stock Watchlist/` with {len(tickers)} ticker pages plus [[Stock Watchlist Index]].\n")


if __name__ == "__main__":
    main()
