#!/usr/bin/env python3
"""Fetch Yahoo key-statistics pages and parse Forward PE, PEG, ROE, FCF, ROA."""
import json, re, ssl, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

tickers = [
"MSFT","AMZN","GOOG","META","AAPL",
"CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS",
"TSLA","NFLX","MELI",
"HD","LOW","WMT","TGT",
"ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC",
"BE","APLD","TE","PSIX","GLW","BW","PUMP",
"IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE",
"VFV.TO","GLD","SMH",
"SPCX","RKLB","SEI","WYFI","CRCL"
]

ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
outdir = Path("/tmp/yh_ks")
outdir.mkdir(exist_ok=True)

def fetch(t):
    url = f"https://finance.yahoo.com/quote/{urllib.parse.quote(t)}/key-statistics"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
            html = r.read().decode("utf-8", errors="replace")
        (outdir / f"{t.replace('.','_')}.html").write_text(html, encoding="utf-8")
        return t, html, None
    except Exception as e:
        return t, None, str(e)

def parse_num(s):
    if s is None:
        return None
    s = s.strip().replace(",", "")
    if s in ("", "--", "—", "N/A", "Infinity"):
        return None
    mult = 1.0
    if s.endswith("%"):
        try:
            return float(s[:-1]) / 100.0
        except:
            return None
    if s[-1:] in "KMBT" and len(s) > 1:
        mult = {"K":1e3,"M":1e6,"B":1e9,"T":1e12}[s[-1]]
        s = s[:-1]
    try:
        return float(s) * mult
    except:
        return None

def extract(html):
    if not html:
        return {}
    out = {}
    # Try JSON embedded root.App.main
    m = re.search(r"root\.App\.main\s*=\s*(\{.*?\});\s*\n", html, re.S)
    if not m:
        m = re.search(r"ytInitialData\s*=\s*(\{.*?\});", html, re.S)
    # Yahoo often embeds quoteSummary in script
    for pat, key in [
        (r'"forwardPE"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "fwd_pe"),
        (r'"trailingPE"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "trail_pe"),
        (r'"pegRatio"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "peg"),
        (r'"returnOnEquity"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "roe"),
        (r'"returnOnAssets"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "roa"),
        (r'"freeCashflow"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "fcf"),
        (r'"operatingCashflow"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "ocf"),
        (r'"profitMargins"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "pm"),
        (r'"recommendationKey"\s*:\s*"([^"]+)"', "rec"),
        (r'"targetMeanPrice"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "target"),
    ]:
        mm = re.search(pat, html)
        if mm:
            val = mm.group(1)
            if key == "rec":
                out[key] = val
            else:
                try:
                    out[key] = float(val)
                except:
                    out[key] = None
    # HTML table fallbacks
    def table_val(label):
        # label then next cell
        patterns = [
            rf">{re.escape(label)}</td><td[^>]*>([^<]+)</td>",
            rf">{re.escape(label)}</span></td><td[^>]*><span[^>]*>([^<]+)</span>",
            rf">{re.escape(label)}</td>\s*<td[^>]*>\s*([^<]+)",
            rf">{re.escape(label)}[^<]{{0,40}}</[^>]+>\s*<[^>]+>([^<]+)",
        ]
        for p in patterns:
            mm = re.search(p, html, re.I)
            if mm:
                return mm.group(1).strip()
        # looser
        mm = re.search(rf"{re.escape(label)}[^0-9\-]{{0,80}}(-?\d[\d,\.]*\%?)", html, re.I)
        if mm:
            return mm.group(1).strip()
        return None

    mapping = {
        "Forward P/E": "fwd_pe",
        "PEG Ratio (5 yr expected)": "peg",
        "PEG Ratio (5yr expected)": "peg",
        "Trailing P/E": "trail_pe",
        "Return on Equity (ttm)": "roe",
        "Return on Assets (ttm)": "roa",
        "Levered Free Cash Flow (ttm)": "fcf",
        "Operating Cash Flow (ttm)": "ocf",
        "Profit Margin": "pm",
    }
    for label, key in mapping.items():
        if key not in out or out[key] is None:
            v = table_val(label)
            if v:
                out[key] = parse_num(v)
                out[f"{key}_raw"] = v
    return out

results = {}
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(fetch, t) for t in tickers]
    for i, f in enumerate(as_completed(futs)):
        t, html, err = f.result()
        if err:
            results[t] = {"error": err}
        else:
            results[t] = extract(html)
            results[t]["html_len"] = len(html)
        time.sleep(0.05)

# also parse any already-cached full extracts if useful
print(json.dumps(results, indent=2, default=str))
