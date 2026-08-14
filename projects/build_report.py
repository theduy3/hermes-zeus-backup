import json, datetime

data = json.load(open('/home/hermes/.hermes/projects/watchlist_data.json'))
inds = json.loads('''{"^VIX":{"price":14.69,"chg":-1.4093959731543682},"^TNX":{"price":4.641,"chg":-0.4077253218884147},"^GSPC":{"price":7783.78,"chg":0.9574628143336632},"^RUT":{"price":3047.36,"chg":1.5262114574136678},"CAD=X":{"price":1.3936,"chg":-0.5565862708719872},"CADUSD=X":{"price":0.7176,"chg":0.5605381165919288},"BTC-USD":{"price":63390.78,"chg":-2.2424389451091242},"GC=F":{"price":4421.6,"chg":1.370993626484483}}''')

SECTIONS = {
    "Mega-cap AI / Platforms": ["MSFT","AMZN","GOOG","META","AAPL"],
    "AI Infrastructure / Cloud": ["CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS"],
    "Consumer / Internet": ["TSLA","NFLX","MELI"],
    "Semiconductors": ["ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC"],
    "Data Centers / Power": ["BE","APLD","TE","PSIX","GLW","BW","PUMP"],
    "Crypto Miners / Bitcoin Infrastructure": ["IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE"],
    "ETFs / Funds": ["VFV.TO","GLD","SMH"],
    "Other / Unresolved": ["SPCX","RKLB","SEI","WYFI"],
}

SENT = {
    "MSFT":("Hold","fair Fwd P/E ~25x, mild pullback"),
    "AMZN":("Hold","fair Fwd P/E ~29x, soft tape"),
    "GOOG":("Hold","fair Fwd P/E ~25x, weak tape -3.7%"),
    "META":("Buy","cheap Fwd P/E ~18x"),
    "AAPL":("Hold","rich Fwd P/E ~33x, weak tape"),
    "CRM":("Buy","cheap Fwd P/E ~14x + positive tape"),
    "DELL":("Hold","fair Fwd P/E ~26x, +14% spike = chase risk"),
    "PLTR":("Watch","very rich Fwd P/E ~90x, momentum froth"),
    "ORCL":("Buy","cheap Fwd P/E ~19x + strong tape"),
    "CRWV":("Watch","no Fwd P/E, speculative, +27% spike"),
    "INFY":("Buy","cheap Fwd P/E ~15x (ADR)"),
    "NBIS":("Watch","no Fwd P/E, speculative, +36% spike"),
    "TSLA":("Watch","extreme Fwd P/E ~169x, speculative"),
    "NFLX":("Buy","reasonable Fwd P/E ~21x + positive tape"),
    "MELI":("Hold","rich Fwd P/E ~43x, flat tape"),
    "ASML":("Hold","rich-ish Fwd P/E ~32x, strong tape"),
    "AVGO":("Hold","fair Fwd P/E ~26x"),
    "NVDA":("Buy","reasonable Fwd P/E ~22x + strong tape"),
    "AMD":("Hold","rich Fwd P/E ~43x"),
    "SNDK":("Buy","cheap Fwd P/E ~7x, explosive tape"),
    "MU":("Buy","cheap Fwd P/E ~6x + strong tape"),
    "TSM":("Buy","cheap Fwd P/E ~20x + strong tape"),
    "INTC":("Watch","rich Fwd P/E ~61x, turnaround uncertainty"),
    "BE":("Watch","rich Fwd P/E ~69x, speculative"),
    "APLD":("Watch","no Fwd P/E, speculative"),
    "TE":("Watch","no Fwd P/E, weak tape -11%"),
    "PSIX":("Buy","cheap Fwd P/E ~13x, strong tape"),
    "GLW":("Hold","rich Fwd P/E ~45x"),
    "BW":("Watch","rich Fwd P/E ~50x, small-cap"),
    "PUMP":("Watch","rich Fwd P/E ~50x"),
    "IREN":("Watch","no Fwd P/E, speculative, +20% on BTC weakness"),
    "CORZ":("Watch","no meaningful Fwd P/E (~663x), distressed"),
    "RIOT":("Watch","no Fwd P/E, weak tape"),
    "CLSK":("Watch","no Fwd P/E, weak tape"),
    "BITF":("Watch","data unavailable (source 404)"),
    "BTDR":("Watch","no Fwd P/E, weak tape -15%"),
    "HIVE":("Watch","no Fwd P/E, weak tape"),
    "VFV.TO":("Watch","ETF; no Fwd P/E; CAD-denominated"),
    "GLD":("Watch","ETF; gold proxy +1.4%"),
    "SMH":("Watch","ETF; semis exposure +4.1%"),
    "SPCX":("Watch","rich Fwd P/E ~61x, unresolved/SPAC"),
    "RKLB":("Watch","no Fwd P/E, speculative"),
    "SEI":("Watch","rich Fwd P/E ~77x"),
    "WYFI":("Watch","no Fwd P/E, speculative/new"),
}

def fmt_price(t, p):
    if p is None: return "—"
    if t == "VFV.TO": return f"C${p:.2f}"
    return f"${p:.2f}"

def fmt_chg(c):
    if c is None: return "—"
    return f"{c:+.2f}%"

def fmt_pe(fp):
    if fp is None: return "—"
    return f"{fp:.1f}"

lines = []
lines.append("📊 **Daily Watchlist Report — Thu Aug 13, 2026**")
lines.append("")
lines.append("**Market Context (facts, Yahoo Finance):**")
lines.append(f"S&P 500 {fmt_chg(inds['^GSPC']['chg'])} @ {inds['^GSPC']['price']:.0f} · Russell 2000 {fmt_chg(inds['^RUT']['chg'])} · VIX {inds['^VIX']['price']:.2f} ({fmt_chg(inds['^VIX']['chg'])}) · 10Y {inds['^TNX']['price']:.2f}% · Gold {fmt_chg(inds['GC=F']['chg'])} · BTC {fmt_chg(inds['BTC-USD']['chg'])} @ ${inds['BTC-USD']['price']:,.0f} · USD/CAD {inds['CAD=X']['price']:.4f}")
lines.append("*Read: risk-on rotation — small caps leading, VIX low, gold up, but BTC soft (-2.2%) while miners spike (idiosyncratic, not BTC-driven). Mega-caps (MSFT/AMZN/GOOG/AAPL) lag while semis/AI-infra/miners rip.*")
lines.append("")

for sec, tickers in SECTIONS.items():
    lines.append(f"**{sec}**")
    lines.append("| Ticker | Price | Chg % | Fwd P/E | Sentiment |")
    lines.append("|---|---|---|---|---|")
    for t in tickers:
        d = data.get(t, {})
        lab, reason = SENT.get(t, ("Watch","—"))
        lines.append(f"| {t} | {fmt_price(t,d.get('price'))} | {fmt_chg(d.get('chg'))} | {fmt_pe(d.get('fwdpe'))} | {lab} ({reason}) |")
    lines.append("")

lines.append("**Best opportunities today** (cheap/reasonable Fwd P/E + positive tape):")
lines.append("META (18x), CRM (14x), ORCL (19x), NVDA (22x), TSM (20x), MU (6x), SNDK (7x), PSIX (13x), INFY (15x), NFLX (21x).")
lines.append("")
lines.append("**Avoid / wait:**")
lines.append("- Rich/frothy multiples: PLTR (~90x), TSLA (~169x), SEI (~77x), SPCX (~61x), INTC (~61x), BE (~69x).")
lines.append("- Weak tape + no earnings visibility: BTDR (-15%), TE (-11%), RIOT, CLSK, HIVE, CORZ.")
lines.append("- Data gap: BITF quote unavailable on all sources (marked —).")
lines.append("- Divergence flag: miners up hard while BTC -2.2% — moves look idiosyncratic (AI/datacenter news), not a BTC proxy; treat spikes as event-driven, not trend.")
lines.append("")
lines.append("—")
lines.append("**Data as-of:** Thu Aug 13, 2026 ~12:05 PM EDT (market open, regular session). **Sources:** Yahoo Finance chart API (prices, daily change, 52-wk range), StockAnalysis (forward P/E). VFV.TO quoted in CAD; all others USD. Forward P/E shown `—` where not meaningful (ETFs) or not published (unprofitable/speculative names). BITF could not be resolved on any live source.")
lines.append("")
lines.append("This is analysis, not financial advice. Consult a qualified advisor before making investment decisions. Past performance does not guarantee future results.")

print("\n".join(lines))
with open('/home/hermes/.hermes/projects/watchlist_report.md','w') as f:
    f.write("\n".join(lines))
