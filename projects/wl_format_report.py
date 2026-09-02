#!/usr/bin/env python3
import json
from datetime import datetime, timezone

prices = {r["ticker"]: r for r in json.load(open("/home/hermes/.hermes/projects/watchlist_daily_out.json"))}
stats_raw = json.load(open("/home/hermes/.hermes/projects/watchlist_stats.json"))
stats = {r["t"]: r for r in stats_raw["merged"]}

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

def fmt_px(p, cur=None):
    if p is None: return "—"
    if abs(p) >= 1000: s = f"{p:,.0f}"
    elif abs(p) >= 100: s = f"{p:.2f}"
    elif abs(p) >= 10: s = f"{p:.2f}"
    else: s = f"{p:.3f}" if abs(p) < 1 else f"{p:.2f}"
    if cur == "CAD": s += " C$"
    return s

def fmt_chg(c):
    if c is None: return "—"
    return f"{c:+.1f}%"

def fmt_pe(pe):
    if pe is None: return "—"
    if pe < 0: return "neg"
    if pe > 500: return ">500"
    if pe >= 100: return f"{pe:.0f}"
    return f"{pe:.1f}"

def sentiment(t, s, p):
    # ETFs
    if t in ("VFV.TO","GLD","SMH"):
        return "Watch", "ETF"
    peg = s.get("peg")
    fcf = s.get("fcf")
    roe = s.get("roe")
    fpe = s.get("forwardPE")
    g1 = s.get("growth_+1y")

    fcf_pos = fcf is not None and fcf > 0
    fcf_neg = fcf is not None and fcf < 0
    roe_hi = roe is not None and roe >= 0.15
    roe_lo = roe is not None and roe < 0.05
    roe_neg = roe is not None and roe < 0
    peg_attr = peg is not None and peg < 1.0
    peg_ok = peg is not None and peg <= 1.5
    peg_rich = peg is not None and peg > 2.0
    peg_very = peg is not None and peg > 3.5
    fpe_neg = fpe is not None and fpe < 0
    fpe_crazy = fpe is not None and fpe > 80

    # Speculative / pre-profit / thin
    if t in ("CRWV","NBIS","APLD","TE","IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE","RKLB","WYFI","PUMP","BW","SPCX","CRCL","BE","PSIX","SEI"):
        if fcf_neg or fpe_neg or roe_neg or fpe_crazy:
            reason = []
            if fcf_neg: reason.append("neg FCF")
            if fpe_neg: reason.append("neg Fwd P/E")
            if fpe_crazy: reason.append("extreme Fwd P/E")
            if roe_neg: reason.append("neg ROE")
            if not reason: reason.append("thin Big-3")
            return "Watch", "/".join(reason)[:40]
        if peg_attr and fcf_pos and roe_hi:
            return "Buy", f"PEG {peg:.2f}+FCF+ROE"
        return "Watch", "need FCF/ROIC/PEG confirm"

    # Big 3 full names
    if peg_very or (fpe is not None and fpe > 100 and (peg is None or peg > 2)):
        return "Sell", f"PEG/Fwd stretched ({peg if peg else fpe:.0f})"
    if peg_attr and fcf_pos and roe_hi:
        return "Buy", f"PEG {peg:.2f}+FCF+ROE {roe*100:.0f}%"
    if peg_attr and fcf_pos and roe is None:
        return "Buy", f"PEG {peg:.2f}+FCF (ROE n/a)"
    if peg_attr and fcf_neg and roe_hi:
        return "Hold", f"PEG {peg:.2f} but FCF neg"
    if fpe is not None and 0 < fpe < 10 and fcf_pos and (roe_hi or (roe is not None and roe > 0.3)):
        return "Buy", f"cheap Fwd {fpe:.1f}+FCF+ROE"
    if peg_rich and fcf_pos and roe_hi:
        return "Hold", f"rich PEG {peg:.2f}; FCF/ROE OK"
    if peg_ok and fcf_pos and (roe_hi or roe is None or roe > 0.1):
        return "Hold", f"PEG {peg:.2f}+FCF"
    if fcf_neg and roe_neg:
        return "Sell", "neg FCF+ROE"
    if fpe_neg and fcf_neg:
        return "Watch", "neg earnings+FCF"
    if not s.get("ok") and t == "BITF":
        return "Watch", "quote missing"
    if peg is None and fpe is None:
        return "Watch", "data thin"
    if peg_rich:
        return "Hold", f"rich PEG {peg:.2f}"
    if fcf_pos and roe_hi:
        return "Hold", "FCF+ROE; PEG mixed"
    return "Watch", "mixed Big-3"

# print structured for report drafting
print("ASOF chart last bar UTC", datetime.fromtimestamp(1788183000, tz=timezone.utc).isoformat())
print("NOW", datetime.now(timezone.utc).isoformat())
for gname, tickers in groups:
    print(f"\n## {gname}")
    print("Ticker | Price | Chg % | Fwd P/E | Sentiment")
    for t in tickers:
        p = prices.get(t, {})
        s = stats.get(t, {})
        sent, reason = sentiment(t, s, p)
        pe = s.get("forwardPE")
        print(f"{t} | {fmt_px(p.get('price'), p.get('currency'))} | {fmt_chg(p.get('chg'))} | {fmt_pe(pe)} | {sent} ({reason})")
        # extra for analysis
        print(f"   peg={s.get('peg')} fcf={s.get('fcf')} roe={s.get('roe')} g1={s.get('growth_+1y')} rec={s.get('rec')}")
