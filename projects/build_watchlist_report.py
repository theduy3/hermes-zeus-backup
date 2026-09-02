#!/usr/bin/env python3
"""Assemble daily watchlist report rows from cached JSON + manual Big3 overlays."""
import json
from datetime import datetime, timezone

prices = json.load(open("/home/hermes/.hermes/projects/watchlist_data.json"))
funds = json.load(open("/home/hermes/.hermes/projects/watchlist_fundamentals.json"))
# SEI price fix from later fetch
prices["results"]["SEI"]["chart"] = {
    "price": 49.30,
    "chg_pct": -2.90,
    "as_of": "2026-09-01T16:00:00+00:00",
}
# BITF -> KEEL redomicile
prices["results"]["BITF"]["chart"] = {
    "price": 3.12,
    "chg_pct": -1.07,
    "as_of": "2026-09-01T16:00:00+00:00",
    "note": "Yahoo BITF 404; KEEL (Bitfarms redomicile) used",
}

# Big3 overlays from Yahoo key-stats / FinanceCharts (as of ~2026-09-01)
# fcf_trend: rising | stable | shrinking | negative | unknown
# roic_proxy: high | mid | low | unknown  (ROE/ROIC qualitative)
big3 = {
    "MSFT": {"roe": 34.0, "roa": 14.1, "fcf_trend": "shrinking", "roic": 20.2, "note": "FCF TTM ~$67B -6% YoY; ROIC high but off peak"},
    "AMZN": {"roe": 30.6, "roa": 6.6, "fcf_trend": "negative", "roic": 10.1, "note": "FCF TTM ~-$11.6B; ROIC declining on AI capex"},
    "GOOG": {"roe": 48.7, "roa": 13.0, "fcf_trend": "shrinking", "roic": 21.7, "note": "FCF TTM ~$53B -20% YoY; PEG <1"},
    "META": {"roe": 29.9, "roa": 14.6, "fcf_trend": "shrinking", "roic": 27.6, "note": "FCF TTM ~$41B -18% YoY; PEG 0.85"},
    "AAPL": {"roe": 148.8, "roa": 27.1, "fcf_trend": "stable", "roic": None, "note": "ROE extreme; PEG 2.54 stretched"},
    "CRM": {"roe": 19.4, "roa": 5.7, "fcf_trend": "stable", "roic": None, "note": "Levered FCF ~$17.7B; PEG ~1.05"},
    "DELL": {"roe": None, "roa": None, "fcf_trend": "rising", "roic": 54.9, "note": "Yahoo Scout ROIC ~55%; FCF growth strong; PEG 0.77"},
    "PLTR": {"roe": 38.1, "roa": 17.3, "fcf_trend": "rising", "roic": None, "note": "FCF positive; Fwd P/E ~115 stretched"},
    "ORCL": {"roe": None, "roa": None, "fcf_trend": "negative", "roic": None, "note": "Scout: FCF growth severely negative on AI build"},
    "TSLA": {"roe": 4.7, "roa": 1.9, "fcf_trend": "stable", "roic": None, "note": "ROE low; PEG 5.2 + Fwd P/E 182"},
    "NFLX": {"roe": 49.5, "roa": 16.1, "fcf_trend": "rising", "roic": None, "note": "Levered FCF ~$25.4B; ROE high"},
    "NVDA": {"roe": 117.2, "roa": 53.6, "fcf_trend": "rising", "roic": 87.0, "note": "FCF TTM ~$127B +76% YoY; PEG 0.63"},
    "MU": {"roe": 66.6, "roa": 34.9, "fcf_trend": "rising", "roic": None, "note": "OCF ~$51B; levered FCF ~$7.6B; PEG 0.14"},
    "TSM": {"roe": 40.0, "roa": 19.0, "fcf_trend": "rising", "roic": None, "note": "Strong ROE; PEG ~1.0"},
    "AVGO": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "PEG 0.42; earnings ~Sep 3"},
    "MELI": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "Growth name; rich Fwd P/E"},
    "HD": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "Housing-sensitive"},
    "LOW": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "Cheaper than HD on Fwd P/E"},
    "WMT": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "PEG 3.91 stretched"},
    "TGT": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "PEG 2.61"},
    "AMD": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "Fwd P/E 64 rich vs peers"},
    "ASML": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "PEG >2"},
    "INTC": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "Turnaround; Fwd P/E 70 on depressed base"},
    "INFY": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "PEG 2.04"},
    "GLW": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "PEG 1.14; optical/AI glass"},
    "BE": {"roe": None, "roa": None, "fcf_trend": "unknown", "roic": None, "note": "Fwd P/E 84 speculative"},
}

# Portfolio policy from memory
NO_ADD = {"MSFT","AMZN","GOOG","META","NVDA","AVGO","TSLA","ASML","AMD","INTC","NBIS"}

groups = [
    ("Mega-cap AI / Platforms", ["MSFT","AMZN","GOOG","META","AAPL"]),
    ("AI Infrastructure / Cloud", ["CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS"]),
    ("Consumer / Internet", ["TSLA","NFLX","MELI"]),
    ("Retail", ["HD","LOW","WMT","TGT"]),
    ("Semiconductors", ["ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC"]),
    ("Data Centers / Power", ["BE","APLD","TE","PSIX","GLW","BW","PUMP"]),
    ("Crypto Miners / Bitcoin Infrastructure", ["IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE"]),
    ("ETFs / Funds", ["VFV.TO","GLD","SMH"]),
    ("Other / Unresolved", ["SPCX","RKLB","SEI","WYFI","CRCL"]),
]

ETFS = {"VFV.TO","GLD","SMH"}
SPEC = {"CRWV","NBIS","APLD","TE","PSIX","BE","BW","PUMP","IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE","SPCX","RKLB","WYFI","CRCL","SNDK","SEI"}


def fmt_price(p):
    if p is None:
        return "—"
    p = float(p)
    if p >= 1000:
        return f"{p:,.0f}"
    if p >= 100:
        return f"{p:.2f}"
    if p >= 10:
        return f"{p:.2f}"
    return f"{p:.2f}"


def fmt_chg(c):
    if c is None:
        return "—"
    return f"{c:+.2f}%"


def fmt_fpe(v):
    if v is None:
        return "—"
    v = float(v)
    if v > 200:
        return f"{v:.0f}"
    return f"{v:.1f}"


def sentiment(t, fpe, peg, b3):
    # ETFs / thin data / speculative
    if t in ETFS:
        return "Watch", "ETF — no Big 3"
    if t in SPEC and (fpe is None or (fpe is not None and fpe > 80) or peg is None):
        if t == "BITF":
            return "Watch", "now KEEL; miner/spec"
        if fpe is None:
            return "Watch", "need FCF/ROIC/PEG"
        if fpe and fpe > 100:
            return "Watch", f"spec Fwd P/E {fpe:.0f}"
        return "Watch", "thin Big 3 / speculative"

    fcf = (b3 or {}).get("fcf_trend")
    roe = (b3 or {}).get("roe")
    roic = (b3 or {}).get("roic")
    high_roic = (roic is not None and roic >= 15) or (roe is not None and roe >= 20)
    rising_fcf = fcf == "rising"
    shrinking_fcf = fcf in ("shrinking", "negative")
    neg_fcf = fcf == "negative"

    # SELL signals
    if peg is not None and peg >= 4.0 and (roe is not None and roe < 10):
        return "Sell", f"PEG {peg:.1f} + weak ROE"
    if peg is not None and peg >= 5.0:
        return "Sell", f"PEG {peg:.1f} stretched"
    if neg_fcf and peg is not None and peg > 1.5:
        return "Watch", "neg FCF + PEG mid"

    # BUY signals (full Big 3)
    if peg is not None and peg < 1.0 and rising_fcf and high_roic:
        label = "Buy"
        why = f"PEG {peg:.2f}+rising FCF+high ROE/ROIC"
        if t in NO_ADD:
            # still show analytical Buy but note size — user preference is no-add; use Hold for portfolio-constrained
            return "Hold", f"Big3 Buy but no-add/conc. ({why})"
        return label, why

    if peg is not None and peg < 0.5 and high_roic and fcf in ("rising", "stable", "unknown", None):
        if t == "MU":
            return "Buy", f"PEG {peg:.2f}+ROE 67%+FCF up (cycle risk)"
        if t == "AVGO":
            return "Hold", f"PEG {peg:.2f} attractive; earn Sep3 / no-add"
        if t == "DELL":
            return "Buy", f"PEG {peg:.2f}+ROIC~55%+FCF up"
        if t in NO_ADD:
            return "Hold", f"PEG {peg:.2f} cheap vs growth; no-add list"

    if peg is not None and peg < 1.0 and high_roic and shrinking_fcf:
        return "Hold", f"PEG {peg:.2f}+high ROE; FCF soft (AI capex)"

    if peg is not None and peg < 1.0 and rising_fcf:
        if t in NO_ADD:
            return "Hold", f"PEG {peg:.2f}+FCF up; no-add/size"
        return "Buy", f"PEG {peg:.2f}+FCF rising"

    if peg is not None and peg > 2.5 and fpe is not None and fpe > 30:
        return "Hold", f"rich PEG {peg:.1f}"
    if peg is not None and peg > 2.0:
        return "Hold", f"PEG {peg:.1f} elevated"
    if fpe is not None and fpe > 50 and (peg is None or peg > 1.5):
        return "Watch", f"rich Fwd P/E {fpe:.0f}"
    if fpe is not None and fpe > 80:
        return "Watch", f"spec Fwd P/E {fpe:.0f}"

    if peg is not None and 0.8 <= peg <= 1.5:
        return "Hold", f"PEG {peg:.2f} balanced"
    if peg is not None and peg < 0.8:
        return "Hold", f"PEG {peg:.2f}; confirm FCF"
    if fpe is not None and fpe < 20:
        return "Hold", f"Fwd P/E {fpe:.1f}"
    if fpe is not None:
        return "Hold", f"Fwd P/E {fpe:.1f}"
    return "Watch", "data thin"


rows_out = []
print(f"Daily Watchlist Report — Tue Sep 1, 2026")
print(f"As-of: market open / live ~12:00 EDT (America/Toronto trip context); prices Yahoo chart API; Fwd P/E & PEG Yahoo key-statistics scrape; Big 3 FCF/ROE overlays Yahoo + FinanceCharts.")
print(f"Sources timestamp: prices {prices['fetched_at_utc'][:19]}Z; fundamentals {funds['fetched_at_utc'][:19]}Z")
print()

best = []
avoid = []

for gname, tickers in groups:
    print(f"**{gname}**")
    print("| Ticker | Price | Chg % | Fwd P/E | Sentiment |")
    print("|--------|------:|------:|--------:|-----------|")
    for t in tickers:
        c = prices["results"].get(t, {}).get("chart", {})
        f = funds["results"].get(t, {})
        price = c.get("price")
        chg = c.get("chg_pct")
        fpe = f.get("forwardPE")
        peg = f.get("pegRatio")
        b3 = big3.get(t)
        sent, why = sentiment(t, fpe, peg, b3)
        # overrides for clarity
        if t == "NVDA":
            sent, why = "Hold", "Big3 strong (PEG 0.63+FCF↑+ROIC~87%); ~36% conc / no-add"
        if t == "TSLA":
            sent, why = "Sell", "PEG 5.2 + ROE ~5% + Fwd P/E 182"
        if t == "MU":
            sent, why = "Buy", "PEG 0.14 + ROE 67% + FCF rising (cycle peak risk)"
        if t == "DELL":
            sent, why = "Buy", "PEG 0.77 + ROIC~55% + FCF rising"
        if t == "GOOG":
            sent, why = "Hold", "PEG 0.92 + ROE 49%; FCF −20% YoY / no-add"
        if t == "META":
            sent, why = "Hold", "PEG 0.85 + ROE 30%; FCF soft / no-add"
        if t == "AVGO":
            sent, why = "Hold", "PEG 0.42 attractive; earnings Sep3 / no-add"
        if t == "AMZN":
            sent, why = "Watch", "neg FCF TTM + ROIC↓; PEG 1.36 / no-add"
        if t == "ORCL":
            sent, why = "Watch", "PEG 0.86 but FCF severely neg (AI build)"
        if t == "PLTR":
            sent, why = "Hold", "ROE 38% + FCF up; Fwd P/E 115 / PEG 2.5"
        if t == "AAPL":
            sent, why = "Hold", "ROE elite; PEG 2.54 stretched"
        if t == "MSFT":
            sent, why = "Hold", "ROE 34% + ROIC~20%; FCF −6% / PEG 1.64 / no-add"
        if t == "NFLX":
            sent, why = "Hold", "ROE 50% + FCF solid; PEG 1.79"
        if t == "WMT":
            sent, why = "Hold", "quality; PEG 3.91 rich"
        if t == "BITF":
            sent, why = "Watch", "ticker→KEEL; miner/spec"
        if t in ETFS:
            sent, why = "Watch", "ETF — no Big 3"
        if t in ("CRWV","NBIS","APLD","TE","PSIX","PUMP","SPCX","RKLB","SEI","WYFI","CRCL","SNDK"):
            if fpe is None:
                sent, why = "Watch", "need FCF/ROIC/PEG"
            elif fpe > 100:
                sent, why = "Watch", f"spec Fwd P/E {fpe:.0f}"
        if t in ("IREN","CORZ","RIOT","CLSK","BTDR","HIVE"):
            sent, why = "Watch", "miner/spec — need FCF/ROIC"
        if t == "BE":
            sent, why = "Watch", "Fwd P/E 84; growth/spec"
        if t == "BW":
            sent, why = "Watch", "Fwd P/E 141; thin quality"
        if t == "GLW":
            sent, why = "Hold", "PEG 1.14; AI fiber/glass"
        if t == "INTC":
            sent, why = "Watch", "turnaround; Fwd P/E 70 / no-add"
        if t == "AMD":
            sent, why = "Hold", "PEG ~1.0 but Fwd P/E 65 rich / no-add"
        if t == "ASML":
            sent, why = "Hold", "PEG 2.07 elevated / no-add"
        if t == "CRM":
            sent, why = "Hold", "PEG 1.05 + FCF solid"
        if t == "INFY":
            sent, why = "Hold", "Fwd P/E 14.9; PEG 2.0"
        if t == "MELI":
            sent, why = "Hold", "growth; Fwd P/E 46 / PEG 1.4"
        if t == "HD":
            sent, why = "Hold", "PEG 1.83; housing tape"
        if t == "LOW":
            sent, why = "Hold", "Fwd P/E 16.6 / PEG 1.4"
        if t == "TGT":
            sent, why = "Hold", "Fwd P/E 17.2; PEG 2.6"
        if t == "TSM":
            sent, why = "Hold", "PEG 1.02 + ROE 40%"
        if t == "BTDR" and fpe == 1.0:
            sent, why = "Watch", "miner; FPE unreliable"

        fpe_s = fmt_fpe(fpe)
        print(f"| {t} | {fmt_price(price)} | {fmt_chg(chg)} | {fpe_s} | {sent} ({why}) |")
        rows_out.append((t, price, chg, fpe, sent, why, gname))
        if sent == "Buy":
            best.append((t, why, peg, b3))
        if sent in ("Sell",) or (sent == "Watch" and "neg FCF" in why):
            avoid.append((t, why))
        if t in ("TSLA",) and sent == "Sell":
            pass
        if t in ("PLTR", "AAPL", "WMT", "ASML") and "rich" in why or "stretched" in why or "elevated" in why:
            if (t, why) not in avoid:
                avoid.append((t, why + " — wait for better entry"))
    print()

print("**Best opportunities today**")
# curated
print("- MU — Buy: PEG 0.14 + ROE ~67% + rising FCF (memory-cycle peak / mean-reversion risk remains)")
print("- DELL — Buy: PEG ~0.77 + ROIC ~55% + rising FCF (not on AI no-add list; tape −4% today)")
print("- NVDA — analytically Big3 Buy (PEG 0.63 + FCF +76% + ROIC ~87%) but portfolio: Hold/no-add at ~36% concentration")
print("- META / GOOG — closest mega-cap PEG <1 with high ROE; FCF soft on AI capex → Hold, not new-buy under no-add policy")
print()
print("**Avoid / wait**")
print("- TSLA — Sell/avoid adds: PEG 5.2 + ROE ~5% + Fwd P/E ~182")
print("- AMZN — Wait: negative FCF TTM and ROIC down on AI spend (no-add)")
print("- ORCL — Wait: FCF severely negative on AI build despite PEG <1")
print("- PLTR / AAPL / WMT — Wait for better entry (rich PEG or Fwd P/E)")
print("- Crypto miners + CRWV/NBIS/APLD/BE — Watch only (spec / incomplete Big 3)")
print("- AVGO — attractive PEG 0.42 but earnings Sep 3 + no-add; don’t chase pre-print")
print()
print("**Portfolio flags (context, not new advice)**")
print("- No-add AI/semi list still active: MSFT AMZN GOOG META NVDA AVGO TSLA ASML AMD INTC NBIS")
print("- NVDA concentration ~36% — size risk dominates ticker-level Big3 Buy signal")
print("- CAD cash ~$92.7k reserved (cards/tax/strata/etc.) — not free dry powder")
print("- BITF Yahoo symbol 404; Bitfarms redomiciled — trading as KEEL ~$3.12 (−1.1%)")
print()
print("Facts: live Yahoo prices/key-stats as timestamped above. Judgment: Sentiment column and Best/Avoid bullets.")
print("This is analysis, not financial advice. Consult a qualified advisor before making investment decisions. Past performance does not guarantee future results.")
