#!/usr/bin/env python3
import json, datetime

charts = json.load(open("/tmp/charts_v2.json"))
fv = json.load(open("/tmp/fv_parsed.json"))

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

etfs = {"VFV.TO","GLD","SMH","SPCX"}
# speculative / pre-profit / thin data defaults to Watch
speculative = {
    "CRWV","NBIS","APLD","TE","BW","PUMP","IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE",
    "RKLB","WYFI","CRCL","BE","SNDK"  # SNDK has data but extreme run - still assess
}

def fmt_price(p, ccy=None):
    if p is None: return "—"
    if p >= 1000: return f"{p:,.2f}"
    if p >= 100: return f"{p:.2f}"
    if p >= 10: return f"{p:.2f}"
    return f"{p:.2f}"

def fmt_chg(c):
    if c is None: return "—"
    return f"{c:+.2f}%"

def fmt_pe(x):
    if x is None: return "—"
    if abs(x) >= 100: return f"{x:.0f}"
    return f"{x:.1f}"

def sentiment(t, f, chg):
    """Big 3 lens: PEG, FCF proxy (P/FCF), ROIC unavailable -> use PEG+FCF+quality heuristics.
    Prefer Watch when thin data.
    """
    if t in etfs:
        return "Watch", "ETF — no PEG/FCF/ROIC"
    fwd = f.get("fwdPE") if f else None
    peg = f.get("peg") if f else None
    pfcf = f.get("pfcf") if f else None
    pe = f.get("pe") if f else None
    eps_ny = f.get("epsNextY") if f else None

    # parse eps next y
    epsn = None
    if isinstance(eps_ny, str) and eps_ny not in ("-",""):
        try: epsn = float(eps_ny.replace("%",""))
        except: pass

    thin = (f is None) or (fwd is None and peg is None and pe is None)
    if thin:
        return "Watch", "thin fundamentals / need FCF·ROIC·PEG"

    # FCF health proxy: lower P/FCF better if profitable; null often means neg FCF
    fcf_ok = pfcf is not None and 0 < pfcf < 80
    fcf_rich = pfcf is not None and pfcf >= 80
    fcf_missing_neg = pfcf is None and pe is None  # often unprofitable

    # Extreme valuation sells
    if peg is not None and peg >= 4.0:
        return "Sell", f"PEG {peg:.1f} stretched + rich multiples"
    if fwd is not None and fwd >= 100:
        return "Sell", f"Fwd P/E {fwd:.0f} extreme"
    if pe is not None and pe >= 200 and (peg is None or peg > 2):
        return "Sell", f"P/E {pe:.0f} extreme, growth not priced cleanly"

    # Strong buy: PEG<1 + reasonable FCF + not speculative chaos
    if peg is not None and peg < 1.0 and fcf_ok and (fwd is None or fwd < 35):
        if t in ("NVDA","AVGO","MU","SNDK","ORCL","DELL","AMD","TSM","ASML"):
            # quality compounders with cheap PEG
            if peg < 0.5 and fwd is not None and fwd < 25:
                return "Buy", f"PEG {peg:.2f} + Fwd {fwd:.1f} + FCF ok"
            if peg < 1.0 and fwd is not None and fwd < 20:
                return "Buy", f"PEG {peg:.2f} + Fwd {fwd:.1f}"
        if peg < 0.6 and fwd and fwd < 25:
            return "Buy", f"PEG {peg:.2f} + Fwd {fwd:.1f}"

    # META/NFLX style: PEG ~1, solid FCF
    if peg is not None and peg <= 1.15 and fcf_ok and fwd and 15 <= fwd <= 25:
        return "Hold", f"PEG {peg:.2f} fair, Fwd {fwd:.1f}"

    # MSFT etc fair growth
    if peg is not None and 1.0 <= peg <= 1.6 and fcf_ok and fwd and fwd < 30:
        return "Hold", f"PEG {peg:.2f} fair + Fwd {fwd:.1f}"

    # GOOG value-ish trail but fwd mid
    if peg is not None and peg <= 1.3 and pe is not None and pe < 20:
        return "Hold", f"trail cheap P/E {pe:.1f}, PEG {peg:.2f}"

    # AMZN peg <1 but neg FCF / neg next-year eps print
    if peg is not None and peg < 1.0 and pfcf is None:
        return "Hold", f"PEG {peg:.2f} but FCF thin (P/FCF —)"

    # CRM cheap fwd
    if fwd is not None and fwd < 16 and peg is not None and peg < 1.3 and fcf_ok:
        return "Buy", f"Fwd {fwd:.1f} + PEG {peg:.2f} + FCF"

    # ORCL
    if fwd is not None and fwd < 15 and peg is not None and peg < 0.7:
        return "Buy", f"Fwd {fwd:.1f} + PEG {peg:.2f}"

    # Rich growth holds
    if peg is not None and 1.5 < peg < 3.0 and fcf_ok:
        return "Hold", f"PEG {peg:.2f} elevated, FCF ok"
    if peg is not None and peg >= 2.5 and peg < 4.0:
        return "Hold", f"PEG {peg:.2f} rich vs growth"
    if fwd is not None and fwd > 40 and (peg is None or peg > 1.2):
        if t in speculative or pe is None:
            return "Watch", f"rich/spec Fwd {fwd:.0f}, need FCF·ROIC"
        return "Hold", f"rich Fwd {fwd:.0f}"

    # PLTR rich abs multiples but peg ~1.1
    if fwd and fwd > 50 and peg and peg < 1.5:
        return "Hold", f"PEG {peg:.2f} but Fwd {fwd:.0f} rich abs"

    # unprofitable / no PE
    if pe is None and fwd is None:
        return "Watch", "unprofitable / need FCF·ROIC·PEG"
    if pe is None and fwd and fwd > 40:
        return "Watch", f"pre-earn quality, Fwd {fwd:.0f}"

    # INTC no trailing PE, high fwd
    if pe is None and fwd and fwd > 30:
        return "Watch", f"no trail P/E, Fwd {fwd:.0f}, turnaround"

    # default
    if peg is not None and peg < 1.0:
        return "Hold", f"PEG {peg:.2f} attractive — confirm FCF/ROIC"
    if fwd is not None:
        return "Hold", f"Fwd {fwd:.1f}"
    return "Watch", "need FCF·ROIC·PEG"

# print tables
ts = None
for t,c in charts.items():
    if c.get("ok") and c.get("ts"):
        ts = c["ts"]
        break
asof = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M UTC") if ts else "unknown"
print(f"ASOF|{asof}")
print(f"NOTE|Markets closed (Sun). Prices = Fri 2026-09-11 regular-session close (Yahoo chart). Fwd P/E/PEG = Finviz live pull.")

rows_out = []
for gname, tickers in groups:
    print(f"\n## {gname}")
    print("Ticker | Price | Chg % | Fwd P/E | Sentiment")
    print("--- | --- | --- | --- | ---")
    for t in tickers:
        c = charts.get(t) or {}
        f = fv.get(t) or {}
        if t == "BITF" or not c.get("ok"):
            price, chg = None, None
            if not c.get("ok"):
                sent, reason = "Watch", "price N/A (Yahoo 404)"
                print(f"{t} | — | — | {fmt_pe(f.get('fwdPE'))} | {sent} ({reason})")
                rows_out.append((t, None, None, f.get("fwdPE"), sent, reason, gname, f))
                continue
        price = c.get("price")
        chg = c.get("chg")
        ccy = c.get("ccy")
        pstr = fmt_price(price)
        if ccy == "CAD":
            pstr = f"C${pstr}"
        sent, reason = sentiment(t, f, chg)
        print(f"{t} | {pstr} | {fmt_chg(chg)} | {fmt_pe(f.get('fwdPE'))} | {sent} ({reason})")
        rows_out.append((t, price, chg, f.get("fwdPE"), sent, reason, gname, f))

# Best / Avoid
buys = [r for r in rows_out if r[4]=="Buy"]
sells = [r for r in rows_out if r[4]=="Sell"]
watches_rich = [r for r in rows_out if r[4] in ("Watch","Hold") and r[7] and ((r[7].get("peg") or 0) > 2.5 or (r[7].get("fwdPE") or 0) > 80)]
# also avoid high flyers with weak pillars
print("\n## BEST")
for r in sorted(buys, key=lambda x: (x[7] or {}).get("peg") or 99):
    f=r[7] or {}
    print(f"BUY|{r[0]}|PEG {f.get('peg')}|Fwd {f.get('fwdPE')}|P/FCF {f.get('pfcf')}|{r[5]}")

print("\n## AVOID")
for r in sells:
    f=r[7] or {}
    print(f"SELL|{r[0]}|PEG {f.get('peg')}|Fwd {f.get('fwdPE')}|{r[5]}")

# top movers
valid = [r for r in rows_out if r[2] is not None]
up = sorted(valid, key=lambda x: -x[2])[:5]
dn = sorted(valid, key=lambda x: x[2])[:5]
print("\n## MOVERS_UP")
for r in up: print(f"{r[0]}|{r[2]:+.2f}%")
print("## MOVERS_DN")
for r in dn: print(f"{r[0]}|{r[2]:+.2f}%")

# missing fv
all_t = [t for _,ts in groups for t in ts]
miss = [t for t in all_t if t not in fv]
print("MISSING_FV", miss)
missc = [t for t in all_t if not (charts.get(t) or {}).get("ok")]
print("MISSING_CHART", missc)
