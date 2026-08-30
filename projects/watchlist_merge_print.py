#!/usr/bin/env python3
import json
with open("/home/hermes/.hermes/projects/watchlist_daily_data.json") as f:
    prices = json.load(f)
with open("/home/hermes/.hermes/projects/watchlist_fundamentals.json") as f:
    fund = json.load(f)
y = fund["yahoo"]
print("asof", prices["asof_utc"])
for row in prices["rows"]:
    t = row["ticker"]
    f = y.get(t, {})
    p = row.get("price")
    c = row.get("chg_pct")
    pe = f.get("fwd_pe")
    peg = f.get("peg")
    fcf = f.get("fcf")
    roa = f.get("roa")
    roe = f.get("roe")
    g = f.get("earn_growth")

    def fmt(x, pct=False, b=False):
        if x is None:
            return "—"
        if b and isinstance(x, (int, float)):
            return f"{x/1e9:.2f}B"
        if pct and isinstance(x, (int, float)):
            return f"{x*100:.1f}%"
        if isinstance(x, (int, float)):
            return f"{x:.2f}"
        return str(x)

    print(
        f"{t}\tp={fmt(p)}\tc={fmt(c)}\tfwdPE={fmt(pe)}\tPEG={fmt(peg)}\tFCF={fmt(fcf,b=True)}\tROA={fmt(roa,pct=True)}\tROE={fmt(roe,pct=True)}\tg={fmt(g,pct=True)}"
    )
