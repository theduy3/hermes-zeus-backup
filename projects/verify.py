import json, urllib.request, time
from datetime import datetime, timezone

UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")

for t in ["NFLX","MU","SNDK","BITF","BITF.C"]:
    try:
        raw = fetch("https://query1.finance.yahoo.com/v8/finance/chart/%s?range=5d&interval=1d" % t)
        j = json.loads(raw)
        meta = j["chart"]["result"][0]["meta"]
        closes = [c for c in j["chart"]["result"][0]["indicators"]["quote"][0]["close"] if c is not None]
        ts = meta.get("regularMarketTime")
        dt = datetime.fromtimestamp(ts, tz=timezone.utc) if ts else None
        print("%-8s price=%.2f closes=%s name=%s exch=%s t=%s" % (t, meta.get("regularMarketPrice"), closes[-3:], meta.get("shortName"), meta.get("exchangeName"), dt))
    except Exception as e:
        print("%-8s FAIL %s" % (t, e))
    time.sleep(0.3)
