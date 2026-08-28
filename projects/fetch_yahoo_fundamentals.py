#!/usr/bin/env python3
"""Fetch Yahoo fundamentals using cookie + crumb auth."""
import json
import re
import ssl
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.cookiejar import CookieJar
from datetime import datetime, timezone

ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

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


class YahooSession:
    def __init__(self):
        self.cj = CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cj),
            urllib.request.HTTPSHandler(context=ctx),
        )
        self.crumb = None

    def _req(self, url, timeout=20):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,text/html"})
        with self.opener.open(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace"), r.geturl()

    def init(self):
        # seed cookies
        try:
            self._req("https://fc.yahoo.com")
        except Exception:
            pass
        try:
            body, _ = self._req("https://finance.yahoo.com/")
        except Exception as e:
            print("HOME_ERR", e)
            body = ""
        # crumb endpoint
        try:
            crumb_body, _ = self._req("https://query1.finance.yahoo.com/v1/test/getcrumb")
            if crumb_body and "html" not in crumb_body.lower() and len(crumb_body) < 200:
                self.crumb = crumb_body.strip()
        except Exception as e:
            print("CRUMB_EP_ERR", e)
        if not self.crumb:
            # scrape from html
            m = re.search(r'"CrumbStore":\{"crumb":"([^"]+)"\}', body)
            if not m:
                m = re.search(r'"crumb"\s*:\s*"([^"]+)"', body)
            if m:
                self.crumb = m.group(1)
        print("CRUMB", self.crumb)
        print("COOKIES", len(list(self.cj)))

    def get_json(self, url, timeout=20):
        if self.crumb and "crumb=" not in url:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}crumb={urllib.parse.quote(self.crumb)}"
        body, _ = self._req(url, timeout=timeout)
        return json.loads(body)


def raw(x):
    if x is None:
        return None
    if isinstance(x, dict):
        return x.get("raw", x.get("fmt"))
    return x


def main():
    ys = YahooSession()
    ys.init()

    results = {}

    # Try batch quote first
    if ys.crumb:
        # batch in chunks of 10
        for i in range(0, len(tickers), 10):
            chunk = tickers[i : i + 10]
            syms = ",".join(chunk)
            url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(syms)}"
            try:
                data = ys.get_json(url)
                for q in (data.get("quoteResponse") or {}).get("result") or []:
                    sym = q.get("symbol")
                    results.setdefault(sym, {})
                    results[sym].update(
                        {
                            "forwardPE": q.get("forwardPE"),
                            "trailingPE": q.get("trailingPE"),
                            "price": q.get("regularMarketPrice"),
                            "chg": q.get("regularMarketChangePercent"),
                            "marketCap": q.get("marketCap"),
                            "fiftyTwoWeekLow": q.get("fiftyTwoWeekLow"),
                            "fiftyTwoWeekHigh": q.get("fiftyTwoWeekHigh"),
                            "averageAnalystRating": q.get("averageAnalystRating"),
                        }
                    )
                err = (data.get("quoteResponse") or {}).get("error")
                if err:
                    print("QUOTE_ERR_CHUNK", chunk[0], err)
            except Exception as e:
                print("QUOTE_FAIL", chunk, e)
            time.sleep(0.2)

    # quoteSummary per ticker for PEG/FCF/ROE
    def fetch_summary(t):
        modules = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}"
        try:
            data = ys.get_json(url, timeout=25)
            res = (data.get("quoteSummary") or {}).get("result") or []
            if not res:
                err = (data.get("quoteSummary") or {}).get("error")
                return t, {"error": str(err)}
            res = res[0]
            dks = res.get("defaultKeyStatistics") or {}
            fd = res.get("financialData") or {}
            sd = res.get("summaryDetail") or {}
            et = res.get("earningsTrend") or {}
            out = {
                "forwardPE": raw(dks.get("forwardPE")) or raw(sd.get("forwardPE")),
                "trailingPE": raw(dks.get("trailingPE")) or raw(sd.get("trailingPE")),
                "pegRatio": raw(dks.get("pegRatio")),
                "freeCashflow": raw(fd.get("freeCashflow")),
                "operatingCashflow": raw(fd.get("operatingCashflow")),
                "recommendation": fd.get("recommendationKey"),
                "targetMeanPrice": raw(fd.get("targetMeanPrice")),
                "earningsGrowth": raw(fd.get("earningsGrowth")),
                "revenueGrowth": raw(fd.get("revenueGrowth")),
                "returnOnEquity": raw(fd.get("returnOnEquity")),
                "returnOnAssets": raw(fd.get("returnOnAssets")),
                "profitMargins": raw(fd.get("profitMargins")),
            }
            for tr in et.get("trend") or []:
                if tr.get("period") == "+1y":
                    g = raw(tr.get("growth"))
                    if g is not None:
                        out["nextYearGrowth"] = g
            return t, out
        except Exception as e:
            return t, {"error": str(e)}

    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(fetch_summary, t) for t in tickers]
        for fut in as_completed(futs):
            t, d = fut.result()
            results.setdefault(t, {})
            # don't overwrite good forwardPE with None
            for k, v in d.items():
                if v is not None or k not in results[t]:
                    results[t][k] = v

    # derive peg
    for t, d in results.items():
        peg = d.get("pegRatio")
        fpe = d.get("forwardPE")
        g = d.get("nextYearGrowth", d.get("earningsGrowth"))
        if peg is not None:
            d["pegDerived"] = peg
        elif fpe and g and isinstance(g, (int, float)) and g != 0:
            growth_pct = g * 100.0 if abs(g) < 2 else g
            if growth_pct > 0:
                d["pegDerived"] = fpe / growth_pct

    out_path = "/home/hermes/.hermes/projects/watchlist_fundamentals.json"
    with open(out_path, "w") as fh:
        json.dump(
            {"fetched_at_utc": datetime.now(timezone.utc).isoformat(), "crumb": ys.crumb, "tickers": results},
            fh,
            indent=2,
            default=str,
        )

    for t in tickers:
        d = results.get(t, {})
        fpe = d.get("forwardPE")
        peg = d.get("pegDerived")
        fcf = d.get("freeCashflow")
        roe = d.get("returnOnEquity")
        eg = d.get("earningsGrowth")
        nyg = d.get("nextYearGrowth")
        rec = d.get("recommendation")
        err = d.get("error")
        def fmt(x, nd=1):
            if isinstance(x, (int, float)):
                return f"{x:.{nd}f}"
            return "—"
        print(
            f"{t}|fpe={fmt(fpe,1)}|peg={fmt(peg,2)}|fcf={fmt(fcf,0)}|roe={fmt(roe,3)}|eg={fmt(eg,3)}|nyg={fmt(nyg,3)}|rec={rec}|err={err}"
        )
    print("WROTE", out_path)


if __name__ == "__main__":
    main()
