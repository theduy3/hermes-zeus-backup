#!/usr/bin/env python3
import json
from datetime import datetime, timezone, timedelta

prices = {r['ticker']: r for r in json.load(open('/home/hermes/.hermes/projects/daily_watchlist_data.json'))}
vals = json.load(open('/home/hermes/.hermes/projects/finviz_vals.json'))
fins = json.load(open('/home/hermes/.hermes/projects/finviz_fin.json'))

# as-of from first good asof
asof = None
for r in prices.values():
    if r.get('asof'):
        asof = r['asof']
        break
# EDT = UTC-4 in Sep
dt = datetime.fromtimestamp(asof, tz=timezone(timedelta(hours=-4))) if asof else None
print('ASOF', dt, 'unix', asof)

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
# portfolio no-add list (context only, not forced sell)
no_add = {"MSFT","AMZN","GOOG","META","NVDA","AVGO","TSLA","ASML","AMD","INTC","NBIS"}

def fmt_px(p):
    if p is None: return "—"
    if abs(p) >= 1000: return f"{p:,.2f}"
    if abs(p) >= 100: return f"{p:.2f}"
    if abs(p) >= 10: return f"{p:.2f}"
    return f"{p:.2f}"

def fmt_chg(c):
    if c is None: return "—"
    sign = "+" if c > 0 else ""
    return f"{sign}{c:.2f}%"

def fmt_pe(p):
    if p is None: return "—"
    return f"{p:.1f}" if p < 100 else f"{p:.0f}"

def sentiment(t):
    v = vals.get(t, {})
    f = fins.get(t, {})
    peg = v.get('peg')
    fpe = v.get('fwdPE')
    pfcf = v.get('pfcf')
    roi = f.get('roi')  # Finviz ROI ~ ROIC
    roe = f.get('roe')
    pe = v.get('pe')

    if t in etfs:
        return "Watch", "ETF — Big 3 N/A"
    if t == "BITF":
        return "Watch", "symbol missing/delisted on Yahoo+Finviz"
    # speculative miners / pre-profit / negative ROIC
    thin = peg is None and fpe is None
    if thin:
        if roi is not None and roi < 0:
            return "Watch", f"thin data, ROI {roi:.0f}% (weak)"
        return "Watch", "need FCF/ROIC/PEG to confirm"

    # SELL signals
    if peg is not None and peg > 2.5:
        if roi is not None and roi < 10:
            return "Sell", f"PEG {peg:.2f} stretched + ROI {roi:.0f}%"
        return "Sell", f"PEG {peg:.2f} stretched vs growth"
    if roi is not None and roi < -5 and (fpe is None or fpe > 25):
        return "Sell", f"ROI {roi:.0f}% eroding + rich/NA fwd"
    if roi is not None and roi < -20:
        return "Sell", f"deeply negative ROI {roi:.0f}%"

    # BUY signals: PEG < 1 + high ROIC + reasonable cash (pfcf not insane if present)
    high_roic = roi is not None and roi >= 15
    ok_cash = pfcf is None or (pfcf > 0 and pfcf < 80)
    if peg is not None and peg < 1.0 and high_roic and ok_cash:
        return "Buy", f"PEG {peg:.2f} + ROI {roi:.0f}% + cash OK"
    if peg is not None and peg < 0.5 and (high_roic or (roe is not None and roe > 20)):
        r = roi if roi is not None else roe
        return "Buy", f"PEG {peg:.2f} + ROI/ROE {r:.0f}%"
    # strong but not full buy
    if peg is not None and peg < 1.0 and (roi is None or roi > 5):
        if fpe is not None and fpe < 20:
            return "Hold", f"cheap PEG {peg:.2f}/Fwd {fpe:.0f}x; need FCF trend"
        return "Hold", f"PEG {peg:.2f} attractive; confirm FCF"

    # HOLD zone
    if peg is not None and 1.0 <= peg <= 2.0 and high_roic:
        return "Hold", f"PEG {peg:.2f} fair + ROI {roi:.0f}%"
    if peg is not None and 1.0 <= peg <= 2.5:
        rtxt = f", ROI {roi:.0f}%" if roi is not None else ""
        return "Hold", f"PEG {peg:.2f}{rtxt}"
    if fpe is not None and fpe < 18 and (roi is None or roi > 10):
        return "Hold", f"Fwd P/E {fpe:.0f}x reasonable"
    if fpe is not None and fpe > 50:
        return "Watch", f"rich Fwd P/E {fpe:.0f}x; need PEG/FCF"
    if pe is not None and pe > 100 and (peg is None or peg > 1.5):
        return "Watch", f"elevated trailing P/E; growth must deliver"

    return "Watch", "mixed pillars — dig deeper"

# print telegram-friendly tables
print("\n===REPORT_START===\n")
for gname, tickers in groups:
    print(f"**{gname}**")
    print("```")
    print(f"{'Ticker':<7} {'Price':>8} {'Chg %':>8} {'Fwd P/E':>7}  Sentiment")
    for t in tickers:
        pr = prices.get(t, {})
        v = vals.get(t, {})
        px = pr.get('price')
        chg = pr.get('chg')
        # fallback finviz price if yahoo missing
        if px is None and v.get('price') is not None:
            px = v['price']
            chg = v.get('chg')
        fpe = v.get('fwdPE')
        sent, reason = sentiment(t)
        print(f"{t:<7} {fmt_px(px):>8} {fmt_chg(chg):>8} {fmt_pe(fpe):>7}  {sent} ({reason})")
    print("```\n")

# best / avoid
print("Pillar notes (PEG/ROI from Finviz; prices Yahoo chart):")
for t in ["MU","SNDK","AVGO","NVDA","ORCL","DELL","META","GOOG","TSM","AMD","MSFT","AAPL","TSLA","PLTR","INTC","BE","IREN"]:
    v=vals.get(t,{}); f=fins.get(t,{})
    print(f"  {t}: PEG={v.get('peg')} FwdPE={v.get('fwdPE')} ROI={f.get('roi')} P/FCF={v.get('pfcf')} ROE={f.get('roe')}")
