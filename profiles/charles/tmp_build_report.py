#!/usr/bin/env python3
import json, re

# Parsed from Finviz valuation screener rows (as-of matching Sep 11 2026 prices)
# cols: pe, fwdPE, peg, pfcf, epsNext5Y (where available)
finviz = {
"AAPL": {"pe":"38.09","fwdPE":"34.66","peg":"2.73","pfcf":"35.48"},
"AMZN": {"pe":"20.65","fwdPE":"24.15","peg":"0.98","pfcf":None},
"CRM": {"pe":"22.58","fwdPE":"15.38","peg":"1.12","pfcf":"13.45"},
"CRWV": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"DELL": {"pe":"32.93","fwdPE":"18.36","peg":"0.35","pfcf":"42.14"},
"GOOG": {"pe":"16.85","fwdPE":"22.21","peg":"1.21","pfcf":"77.39"},
"META": {"pe":"24.41","fwdPE":"19.19","peg":"1.03","pfcf":"40.29"},
"MSFT": {"pe":"27.62","fwdPE":"21.11","peg":"1.15","pfcf":"54.94"},
"ORCL": {"pe":"23.56","fwdPE":"13.63","peg":"0.51","pfcf":None},
"PLTR": {"pe":"142.51","fwdPE":"72.93","peg":"1.10","pfcf":"119.67"},
"ASML": {"pe":"52.87","fwdPE":"28.10","peg":"0.73","pfcf":"57.79"},
"HD": {"pe":"21.60","fwdPE":"19.33","peg":"3.43","pfcf":"20.40"},
"INFY": {"pe":"13.57","fwdPE":"13.32","peg":"4.07","pfcf":"11.45"},
"LOW": {"pe":"16.64","fwdPE":"15.16","peg":"3.21","pfcf":"15.78"},
"MELI": {"pe":"51.63","fwdPE":"34.74","peg":"1.38","pfcf":"10.77"},
"NBIS": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"NFLX": {"pe":"24.38","fwdPE":"20.30","peg":"0.93","pfcf":"28.90"},
"TGT": {"pe":"16.17","fwdPE":"16.26","peg":"1.51","pfcf":"15.89"},
"TSLA": {"pe":"339.53","fwdPE":"161.09","peg":"6.81","pfcf":"250.49"},
"WMT": {"pe":"38.82","fwdPE":"33.18","peg":"2.97","pfcf":"62.93"},
"AMD": {"pe":"132.46","fwdPE":"32.58","peg":"0.43","pfcf":"100.27"},
"APLD": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"AVGO": {"pe":"46.21","fwdPE":"18.73","peg":"0.29","pfcf":"43.85"},
"BE": {"pe":"375.73","fwdPE":"55.78","peg":"0.47","pfcf":"129.48"},
"INTC": {"pe":None,"fwdPE":"49.53","peg":"0.53","pfcf":"1581.84"},
"MU": {"pe":"22.08","fwdPE":"6.27","peg":"0.04","pfcf":"42.09"},
"NVDA": {"pe":"27.59","fwdPE":"13.91","peg":"0.22","pfcf":"41.42"},
"SNDK": {"pe":"22.41","fwdPE":"6.27","peg":"0.11","pfcf":"20.81"},
"TE": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"TSM": {"pe":"31.27","fwdPE":"19.75","peg":"0.52","pfcf":"56.31"},
"BTDR": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"BW": {"pe":None,"fwdPE":"18.61","peg":None,"pfcf":None},
"CLSK": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"CORZ": {"pe":None,"fwdPE":"60.77","peg":None,"pfcf":None},
"GLW": {"pe":"76.32","fwdPE":"38.26","peg":"1.15","pfcf":"59.85"},
"HIVE": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"IREN": {"pe":None,"fwdPE":"38.42","peg":None,"pfcf":None},
"PSIX": {"pe":"14.32","fwdPE":"10.79","peg":"1.84","pfcf":"14.73"},
"PUMP": {"pe":None,"fwdPE":"31.20","peg":"0.38","pfcf":None},
"RIOT": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"CRCL": {"pe":"54.53","fwdPE":"64.65","peg":None,"pfcf":"30.22"},
"GLD": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"RKLB": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"SEI": {"pe":"85.66","fwdPE":"29.45","peg":"0.32","pfcf":None},
"SMH": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"SPCX": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"WYFI": {"pe":None,"fwdPE":"61.79","peg":None,"pfcf":None},
"BITF": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
"VFV.TO": {"pe":None,"fwdPE":None,"peg":None,"pfcf":None},
}

with open("/home/hermes/.hermes/profiles/charles/tmp_watchlist_prices.json") as f:
    prices = json.load(f)

def fmt_px(p):
    if p is None: return "—"
    if abs(p) >= 1000: return f"{p:,.2f}"
    if abs(p) >= 100: return f"{p:.2f}"
    if abs(p) >= 10: return f"{p:.2f}"
    return f"{p:.2f}"

def fmt_chg(c):
    if c is None: return "—"
    return f"{c:+.2f}%"

def fmt_pe(x):
    if not x or x == "-" : return "—"
    try:
        return f"{float(x):.1f}"
    except: return "—"

# Sentiment using Big 3 lens; missing FCF trend/ROIC => avoid forced Buy
def sentiment(t, chg, f):
    etf = t in ("VFV.TO","GLD","SMH")
    miner = t in ("IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE")
    speculative = t in ("CRWV","NBIS","APLD","TE","BW","PUMP","SPCX","RKLB","WYFI","CRCL","SEI","BE","PSIX","SNDK")
    fwd = f.get("fwdPE"); peg = f.get("peg"); pfcf = f.get("pfcf")
    try: pegf = float(peg) if peg else None
    except: pegf = None
    try: fwdf = float(fwd) if fwd else None
    except: fwdf = None
    try: pfcff = float(pfcf) if pfcf else None
    except: pfcff = None

    if etf:
        return "Watch", "ETF — no PEG/FCF/ROIC"
    if t == "BITF":
        return "Watch", "quote missing (Yahoo 404)"
    if miner:
        return "Watch", "miner/BTC beta; need FCF/ROIC"
    if t == "TSLA":
        return "Sell", f"PEG {peg} >>2 + rich Fwd P/E"
    if t == "PLTR":
        return "Hold", f"PEG~{peg} but Fwd P/E {fmt_pe(fwd)} rich"
    if t == "AAPL":
        return "Hold", f"PEG {peg} stretched; quality franchise"
    if t == "WMT":
        return "Hold", f"PEG {peg} rich vs growth"
    if t in ("HD","LOW"):
        return "Hold", f"PEG {peg} elevated; solid FCF proxy"
    if t == "INFY":
        return "Hold", f"cheap Fwd {fmt_pe(fwd)} but PEG {peg} weak growth"
    if t == "CRCL":
        return "Watch", f"Fwd {fmt_pe(fwd)} rich; sharp down day"
    if t == "BE":
        return "Watch", f"PEG {peg} but parabolic + tape; thin FCF"
    if t == "INTC":
        return "Watch", f"Fwd {fmt_pe(fwd)}; PEG {peg} but P/FCF stretched"
    if t == "AMD":
        return "Hold", f"PEG {peg} attractive; Fwd {fmt_pe(fwd)} still full"
    if t in ("MU","SNDK"):
        return "Watch", f"PEG {peg}/Fwd {fmt_pe(fwd)} cheap — cycle risk; need ROIC/FCF confirm"
    if t in ("NVDA","AVGO","ORCL","DELL","TSM","ASML"):
        # attractive PEG quality semis/infra — still missing full ROIC series => Hold not Buy
        return "Hold", f"PEG {peg} + Fwd {fmt_pe(fwd)}; quality but confirm FCF/ROIC"
    if t in ("META","NFLX","CRM","MSFT","GOOG","AMZN"):
        if pegf is not None and pegf <= 1.2 and fwdf and fwdf < 30:
            return "Hold", f"PEG {peg} reasonable; FCF/ROIC not fully verified"
        if pegf and pegf > 2:
            return "Hold", f"PEG {peg} elevated"
        return "Hold", f"Fwd {fmt_pe(fwd)}; PEG {peg or '—'}"
    if t == "MELI":
        return "Hold", f"growth PEG {peg}; Fwd {fmt_pe(fwd)}"
    if t == "TGT":
        return "Hold", f"Fwd {fmt_pe(fwd)}; PEG {peg}"
    if t == "PSIX":
        return "Watch", f"Fwd {fmt_pe(fwd)} / PEG {peg}; small-cap, need ROIC"
    if t == "GLW":
        return "Hold", f"PEG {peg}; Fwd {fmt_pe(fwd)} full after spike"
    if t == "SEI":
        return "Watch", f"PEG {peg} + spike; need FCF/ROIC"
    if t in ("CORZ","IREN") and fwdf:
        return "Watch", f"Fwd {fmt_pe(fwd)}; crypto-infra, no full pillars"
    if t in ("PUMP","BW") and fwdf:
        return "Watch", f"Fwd {fmt_pe(fwd)}; thin data"
    if t == "WYFI":
        return "Watch", f"Fwd {fmt_pe(fwd)} speculative"
    # default speculative
    if speculative or not fwd:
        return "Watch", "need FCF/ROIC/PEG to confirm"
    return "Watch", f"Fwd {fmt_pe(fwd)}; incomplete pillars"

sections = [
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

rows_out = []
for sec, ticks in sections:
    print(f"\n### {sec}")
    print("| Ticker | Price | Chg % | Fwd P/E | Sentiment |")
    print("|---|---:|---:|---:|---|")
    for t in ticks:
        p = prices.get(t) or {}
        f = finviz.get(t) or {}
        price = p.get("price")
        chg = p.get("chg_pct")
        if t == "BITF":
            price = None; chg = None
        sent, reason = sentiment(t, chg, f)
        px = fmt_px(price) if price is not None else "—"
        if t == "VFV.TO" and price is not None:
            px = f"C${price:.2f}"
        line = f"| {t} | {px} | {fmt_chg(chg) if chg is not None else '—'} | {fmt_pe(f.get('fwdPE'))} | {sent} ({reason}) |"
        print(line)
        rows_out.append((t, price, chg, f, sent, reason))

with open("/home/hermes/.hermes/profiles/charles/tmp_watchlist_report_rows.json","w") as f:
    json.dump([{"t":a,"price":b,"chg":c,"fund":d,"sent":e,"reason":g} for a,b,c,d,e,g in rows_out], f)
print("\nDONE")
