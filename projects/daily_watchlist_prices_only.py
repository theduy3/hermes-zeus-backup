#!/usr/bin/env python3
import json, subprocess, time, os

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

UA = "Mozilla/5.0 (compatible; research/1.0)"
out = {}
for i, t in enumerate(tickers):
    path = f"/tmp/yf_c_{t.replace('.', '_')}.json"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d"
    try:
        p = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", "15", "-A", UA, "-o", path, "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=25
        )
        code = p.stdout.strip()
        if code == "200" and os.path.exists(path):
            d = json.load(open(path))
            m = d["chart"]["result"][0]["meta"]
            price = m.get("regularMarketPrice")
            chg = m.get("regularMarketChangePercent")
            if chg is None:
                prev = m.get("chartPreviousClose") or m.get("previousClose")
                if price and prev:
                    chg = (price - prev) / prev * 100.0
            out[t] = {
                "price": price,
                "chg": chg,
                "asof": m.get("regularMarketTime"),
                "currency": m.get("currency"),
                "tz": m.get("timezone"),
                "code": code,
            }
            print(f"OK {t} {price} {chg}", flush=True)
        else:
            out[t] = {"price": None, "chg": None, "code": code, "err": "bad"}
            print(f"BAD {t} {code}", flush=True)
            time.sleep(3)
    except Exception as e:
        out[t] = {"price": None, "chg": None, "err": str(e)}
        print(f"ERR {t} {e}", flush=True)
        time.sleep(2)
    time.sleep(1.5)

with open("/home/hermes/.hermes/projects/daily_watchlist_prices.json", "w") as f:
    json.dump(out, f, indent=2)
ok = sum(1 for v in out.values() if v.get("price") is not None)
print(f"DONE {ok}/{len(tickers)}", flush=True)
