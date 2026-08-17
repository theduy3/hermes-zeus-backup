#!/usr/bin/env python3
import json

d = json.load(open('cnbc_all.json'))

groups = {
    "Mega-cap AI / Platforms": ["MSFT","AMZN","GOOG","META","AAPL"],
    "AI Infrastructure / Cloud": ["CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS"],
    "Consumer / Internet": ["TSLA","NFLX","MELI"],
    "Semiconductors": ["ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC"],
    "Data Centers / Power": ["BE","APLD","TE","PSIX","GLW","BW","PUMP"],
    "Crypto Miners / Bitcoin Infrastructure": ["IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE"],
    "ETFs / Funds": ["VFV.TO","GLD","SMH"],
    "Other / Unresolved": ["SPCX","RKLB","SEI","WYFI"],
}

sent = {
 "MSFT": ("Hold", "fair fwd PE ~25, quality compounder"),
 "AMZN": ("Hold", "reasonable fwd PE ~28, slight pullback"),
 "GOOG": ("Buy", "cheap TTM PE 17, fwd PE ~26"),
 "META": ("Buy", "cheapest mega-cap fwd PE ~20"),
 "AAPL": ("Hold", "rich fwd PE ~33"),
 "CRM": ("Buy", "cheap fwd PE ~14 + momentum"),
 "DELL": ("Hold", "reasonable fwd PE ~26"),
 "PLTR": ("Watch", "extreme fwd PE ~104, speculative"),
 "ORCL": ("Buy", "reasonable fwd PE ~19"),
 "CRWV": ("Watch", "unprofitable, fwd PE N/M"),
 "INFY": ("Buy", "cheap fwd PE ~15"),
 "NBIS": ("Watch", "unprofitable, fwd PE N/M"),
 "TSLA": ("Watch", "extreme fwd PE ~180, speculative"),
 "NFLX": ("Hold", "reasonable fwd PE ~23, strong tape"),
 "MELI": ("Hold", "rich fwd PE ~42, quality"),
 "ASML": ("Hold", "rich fwd PE ~34, monopoly moat"),
 "AVGO": ("Hold", "reasonable fwd PE ~27"),
 "NVDA": ("Buy", "reasonable fwd PE ~22 for AI leader"),
 "AMD": ("Hold", "rich fwd PE ~43"),
 "SNDK": ("Buy", "very cheap fwd PE ~7 (big +13.7% move)"),
 "MU": ("Buy", "very cheap fwd PE ~6.6"),
 "TSM": ("Buy", "reasonable fwd PE ~22, AI foundry"),
 "INTC": ("Watch", "unprofitable TTM, turnaround"),
 "BE": ("Watch", "unprofitable, speculative"),
 "APLD": ("Watch", "unprofitable, fwd PE N/M"),
 "TE": ("Watch", "unprofitable, fwd PE N/M"),
 "PSIX": ("Watch", "cheap fwd PE but weak tape, small-cap"),
 "GLW": ("Hold", "rich fwd PE ~43, weak tape"),
 "BW": ("Watch", "weak tape, small-cap"),
 "PUMP": ("Watch", "extreme fwd PE ~214, small-cap"),
 "IREN": ("Watch", "unprofitable, BTC-linked"),
 "CORZ": ("Watch", "unprofitable TTM, weak tape"),
 "RIOT": ("Watch", "unprofitable, weak tape"),
 "CLSK": ("Watch", "unprofitable, weak tape"),
 "BITF": ("Watch", "data missing"),
 "BTDR": ("Watch", "unprofitable, fwd PE N/M"),
 "HIVE": ("Watch", "unprofitable, weak tape"),
 "VFV.TO": ("Watch", "ETF (S&P 500 CAD-hedged)"),
 "GLD": ("Watch", "ETF (gold)"),
 "SMH": ("Watch", "ETF (semiconductors)"),
 "SPCX": ("Watch", "ETF/unclear, weak tape"),
 "RKLB": ("Watch", "unprofitable, speculative"),
 "SEI": ("Watch", "rich fwd PE ~47, small-cap"),
 "WYFI": ("Watch", "unprofitable, recent listing"),
}

def fpe_disp(v):
    if v is None: return "—"
    if v <= 0: return "N/M"
    return f"{v:.1f}"

def price_disp(v):
    if v is None: return "—"
    return f"{v:,.2f}"

def chg_disp(v):
    if v is None: return "—"
    return f"{v:+.2f}%"

lines = []
lines.append("# Daily Watchlist Report — Fri Aug 14, 2026")
lines.append("")
lines.append("**Data as-of:** Most recent regular session close = Thu Aug 13, 2026. Pre-market context from Fri Aug 14, 2026 ~9:04 AM EDT.")
lines.append("**Source:** CNBC quote webservice (live). *Facts* below (Price, Chg %, Fwd P/E) are market data; *Sentiment* is my analysis, not a recommendation.")
lines.append("**Fwd P/E legend:** `—` = not available (ETF / no data); `N/M` = not meaningful (company unprofitable, negative forward earnings).")
lines.append("")
lines.append("**Pre-market snapshot (9:04 AM EDT):** Mega-caps roughly flat; semiconductors firm (SNDK, MU, NVDA up in pre-mkt); crypto miners and small-caps soft.")
lines.append("")

for g, tickers in groups.items():
    lines.append(f"## {g}")
    lines.append("")
    lines.append("| Ticker | Price | Chg % | Fwd P/E | Sentiment |")
    lines.append("|---|---|---|---|---|")
    for t in tickers:
        v = d.get(t, {})
        if not v.get("ok"):
            lines.append(f"| {t} | — | — | — | Watch (data missing) |")
            continue
        sl, sr = sent.get(t, ("Watch", ""))
        lines.append(f"| {t} | {price_disp(v.get('last'))} | {chg_disp(v.get('chg_pct'))} | {fpe_disp(v.get('fpe'))} | {sl} ({sr}) |")
    lines.append("")

lines.append("## Best opportunities today")
lines.append("- **MU** — fwd P/E ~6.6, memory-cycle recovery; **SNDK** — fwd P/E ~7.1 (note the +13.7% session pop, may be partly priced in).")
lines.append("- **GOOG / META** — mega-cap quality at fwd P/E ~26 / ~20 (META cheapest of the group; GOOG also cheap on TTM).")
lines.append("- **CRM / ORCL / INFY** — fwd P/E ~14–19, reasonable entry on infrastructure/cloud.")
lines.append("- **NVDA / TSM** — fwd P/E ~22, best-in-class AI exposure at a (now) sane multiple.")
lines.append("")
lines.append("## Avoid / wait")
lines.append("- **Crypto miners** (RIOT −5.5%, CLSK −5.4%, BTDR −2.9%, HIVE −5.8%, IREN, CORZ) — unprofitable, weak tape; BTC-linked downside persists.")
lines.append("- **PLTR** (fwd P/E ~104) and **TSLA** (fwd P/E ~180) — priced for perfection; wait for a better entry.")
lines.append("- **Unprofitable / speculative small-caps** (RKLB, WYFI, BE, APLD, TE, PUMP, INTC turnaround, NBIS) — need earnings proof before committing.")
lines.append("- **BITF** — quote unavailable from both Yahoo and CNBC; monitor, do not act on missing data.")
lines.append("")

out = "\n".join(lines)
open('report.md','w').write(out)
print(out)
