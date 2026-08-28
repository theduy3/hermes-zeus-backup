#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

ctx = ssl.create_default_context()
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

tickers = [
    "MSFT", "AMZN", "GOOG", "META", "AAPL",
    "CRM", "DELL", "PLTR", "ORCL", "CRWV", "INFY", "NBIS",
    "TSLA", "NFLX", "MELI",
    "HD", "LOW", "WMT", "TGT",
    "ASML", "AVGO", "NVDA", "AMD", "SNDK", "MU", "TSM", "INTC",
    "BE", "APLD", "TE", "PSIX", "GLW", "BW", "PUMP",
    "IREN", "CORZ", "RIOT", "CLSK", "BITF", "BTDR", "HIVE",
    "VFV.TO", "GLD", "SMH",
    "SPCX", "RKLB", "SEI", "WYFI", "CRCL",
]


def fetch_json(url, timeout=15):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, context=ctx, timeout=timeout) as r:
        return json.loads(r.read().decode())


def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    try:
        data = fetch_json(url)
        result = data["chart"]["result"][0]
        meta = result["meta"]
        quote = (result.get("indicators") or {}).get("quote", [{}])[0]
        closes = quote.get("close") or []
        pairs = [c for c in closes if c is not None]
        price = meta.get("regularMarketPrice") or (pairs[-1] if pairs else None)
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        if prev is None and len(pairs) >= 2:
            prev = pairs[-2]
        chg = None
        if price is not None and prev:
            chg = (price - prev) / prev * 100.0
        return t, {
            "price": price,
            "prev": prev,
            "chg": chg,
            "currency": meta.get("currency"),
            "exchange": meta.get("exchangeName"),
            "asof": meta.get("regularMarketTime"),
            "symbol": meta.get("symbol"),
        }
    except Exception as e:
        return t, {"error": str(e)}


def fetch_fundamentals(t):
    """Forward PE, trailing PE, PEG-ish fields via quoteSummary modules."""
    modules = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
    url = (
        "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"
        f"{urllib.parse.quote(t)}?modules={modules}"
    )
    out = {
        "forwardPE": None,
        "trailingPE": None,
        "pegRatio": None,
        "roe": None,
        "profitMargins": None,
        "freeCashflow": None,
        "operatingCashflow": None,
        "recommendation": None,
        "targetMeanPrice": None,
        "earningsGrowth": None,
        "revenueGrowth": None,
        "returnOnEquity": None,
        "returnOnAssets": None,
    }
    try:
        data = fetch_json(url, timeout=20)
        res = data["quoteSummary"]["result"][0]
        dks = res.get("defaultKeyStatistics") or {}
        fd = res.get("financialData") or {}
        sd = res.get("summaryDetail") or {}
        et = res.get("earningsTrend") or {}

        def raw(x):
            if x is None:
                return None
            if isinstance(x, dict):
                return x.get("raw", x.get("fmt"))
            return x

        out["forwardPE"] = raw(dks.get("forwardPE")) or raw(sd.get("forwardPE"))
        out["trailingPE"] = raw(dks.get("trailingPE")) or raw(sd.get("trailingPE"))
        out["pegRatio"] = raw(dks.get("pegRatio"))
        out["freeCashflow"] = raw(fd.get("freeCashflow"))
        out["operatingCashflow"] = raw(fd.get("operatingCashflow"))
        out["recommendation"] = raw(fd.get("recommendationKey")) or fd.get("recommendationKey")
        out["targetMeanPrice"] = raw(fd.get("targetMeanPrice"))
        out["earningsGrowth"] = raw(fd.get("earningsGrowth"))
        out["revenueGrowth"] = raw(fd.get("revenueGrowth"))
        out["returnOnEquity"] = raw(fd.get("returnOnEquity"))
        out["returnOnAssets"] = raw(fd.get("returnOnAssets"))
        out["profitMargins"] = raw(fd.get("profitMargins"))

        # try earnings trend for growth / forward pe alternate
        trends = et.get("trend") or []
        for tr in trends:
            if tr.get("period") == "0y":
                g = raw((tr.get("growth") or {})) if isinstance(tr.get("growth"), dict) else raw(tr.get("growth"))
                if g is not None and out["earningsGrowth"] is None:
                    out["earningsGrowth"] = g
            if tr.get("period") == "+1y":
                # earnings estimate growth already in growth field sometimes
                g = raw(tr.get("growth")) if not isinstance(tr.get("growth"), dict) else raw(tr.get("growth"))
                if isinstance(tr.get("growth"), dict):
                    g = raw(tr.get("growth"))
                if g is not None:
                    out["nextYearGrowth"] = g
        return t, out
    except Exception as e:
        out["error"] = str(e)
        return t, out


charts = {}
funds = {}

with ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(fetch_chart, t): ("chart", t) for t in tickers}
    futs.update({ex.submit(fetch_fundamentals, t): ("fund", t) for t in tickers})
    for fut in as_completed(futs):
        kind, _ = futs[fut]
        t, d = fut.result()
        if kind == "chart":
            charts[t] = d
        else:
            funds[t] = d

combined = {}
for t in tickers:
    c = charts.get(t, {})
    f = funds.get(t, {})
    combined[t] = {**c, **{k: v for k, v in f.items() if k != "error" or "error" not in c}}
    if "error" in c:
        combined[t]["chart_error"] = c["error"]
    if "error" in f:
        combined[t]["fund_error"] = f["error"]

# derive PEG if possible: forwardPE / (growth*100) if growth is decimal
for t, d in combined.items():
    peg = d.get("pegRatio")
    fpe = d.get("forwardPE")
    g = d.get("nextYearGrowth", d.get("earningsGrowth"))
    if peg is None and fpe and g and g > 0:
        # g as decimal e.g. 0.15 = 15%
        growth_pct = g * 100.0 if g < 1.5 else g
        if growth_pct > 0:
            d["pegDerived"] = fpe / growth_pct
    elif peg is not None:
        d["pegDerived"] = peg

out_path = "/home/hermes/.hermes/projects/watchlist_data.json"
with open(out_path, "w") as fh:
    json.dump(
        {
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
            "tickers": combined,
        },
        fh,
        indent=2,
        default=str,
    )

# human summary lines
print(f"FETCHED_AT={datetime.now(timezone.utc).isoformat()}")
for t in tickers:
    d = combined[t]
    if d.get("chart_error"):
        print(f"{t}|ERR|{d['chart_error']}")
        continue
    p = d.get("price")
    c = d.get("chg")
    fpe = d.get("forwardPE")
    peg = d.get("pegDerived")
    fcf = d.get("freeCashflow")
    roe = d.get("returnOnEquity")
    eg = d.get("earningsGrowth")
    ny = d.get("nextYearGrowth")
    rec = d.get("recommendation")
    ps = f"{p:.2f}" if isinstance(p, (int, float)) else "—"
    cs = f"{c:+.2f}" if isinstance(c, (int, float)) else "—"
    fpes = f"{fpe:.1f}" if isinstance(fpe, (int, float)) else "—"
    pegs = f"{peg:.2f}" if isinstance(peg, (int, float)) else "—"
    fcfs = f"{fcf:.0f}" if isinstance(fcf, (int, float)) else "—"
    roes = f"{roe:.3f}" if isinstance(roe, (int, float)) else "—"
    egs = f"{eg:.3f}" if isinstance(eg, (int, float)) else "—"
    nys = f"{ny:.3f}" if isinstance(ny, (int, float)) else "—"
    print(f"{t}|{ps}|{cs}|{fpes}|peg={pegs}|fcf={fcfs}|roe={roes}|eg={egs}|nyg={nys}|rec={rec}|asof={d.get('asof')}")

print("WROTE", out_path)
