#!/usr/bin/env python3
import json, urllib.request, ssl, re, time, random, html as htmlmod
from html.parser import HTMLParser

ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self._table = None
        self._row = None
        self._cell = None
        self._in_td = False
        self._in_th = False
        def_attrs = []
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._table = []
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []
            self._in_td = True
        elif tag == "a" and self._in_td:
            href = dict(attrs).get("href", "")
            m = re.search(r"[?&]t=([A-Za-z0-9.\-]+)", href)
            if m:
                self._cell.append(f"TICKER:{m.group(1).upper()}")
    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._row is not None and self._cell is not None:
            text = htmlmod.unescape(re.sub(r"\s+", " ", "".join(self._cell))).strip()
            self._row.append(text)
            self._cell = None
            self._in_td = False
        elif tag == "tr" and self._table is not None and self._row is not None:
            if any(self._row):
                self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            self.tables.append(self._table)
            self._table = None
    def handle_data(self, data):
        if self._in_td and self._cell is not None:
            self._cell.append(data)

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, context=ctx, timeout=40) as r:
        return r.read().decode("utf-8", "ignore")

batches = [
"MSFT,AMZN,GOOG,META,AAPL,CRM,DELL,PLTR,ORCL,CRWV",
"INFY,NBIS,TSLA,NFLX,MELI,HD,LOW,WMT,TGT,ASML",
"AVGO,NVDA,AMD,SNDK,MU,TSM,INTC,BE,APLD,TE",
"PSIX,GLW,BW,PUMP,IREN,CORZ,RIOT,CLSK,BTDR,HIVE",
"RKLB,SEI,WYFI,CRCL,GLD,SMH,SPCX,BITF",
"PSIX,BW,PUMP,TE,APLD,CRWV,NBIS,INFY,SNDK",
]

results = {}
for b in batches:
    url = f"https://finviz.com/screener.ashx?v=121&t={b}"
    try:
        page = fetch(url)
    except Exception as e:
        print("ERR", b, e)
        continue
    p = TableParser()
    p.feed(page)
    print("tables", len(p.tables), "page", len(page))
    for table in p.tables:
        # find header row with Forward
        header_idx = None
        headers = None
        for i, row in enumerate(table):
            joined = " | ".join(row).lower()
            if "forward" in joined and ("p/e" in joined or "pe" in joined):
                header_idx = i
                headers = [h.lower() for h in row]
                break
            if any("TICKER:" in c for c in row) and header_idx is None:
                # data without header detected
                pass
        if header_idx is None:
            # try any row with TICKER:
            for row in table:
                tcell = next((c for c in row if c.startswith("TICKER:")), None)
                if not tcell:
                    continue
                t = tcell.split(":",1)[1]
                # guess columns by scanning numbers - print raw
                print("RAWROW", t, row)
            continue
        # map columns
        def col(*names):
            for n in names:
                for i,h in enumerate(headers):
                    if n in h:
                        return i
            return None
        i_tick = col("ticker")
        i_fwd = col("forward p/e", "forward")
        i_pe = col("p/e")
        i_peg = col("peg")
        i_pfcf = col("p/fcf")
        i_eps5 = col("eps next 5y", "eps next 5")
        i_price = col("price")
        for row in table[header_idx+1:]:
            t = None
            for c in row:
                if c.startswith("TICKER:"):
                    t = c.split(":",1)[1]
                    break
            if not t and i_tick is not None and i_tick < len(row):
                t = row[i_tick].replace("TICKER:","").strip().upper()
            if not t:
                continue
            def get(i):
                if i is None or i >= len(row):
                    return None
                v = row[i].replace("TICKER:","").strip()
                return v if v and v != "-" else None
            results[t] = {
                "fwdPE": get(i_fwd),
                "pe": get(i_pe),
                "peg": get(i_peg),
                "pfcf": get(i_pfcf),
                "epsNext5Y": get(i_eps5),
                "price": get(i_price),
                "src": "finviz",
            }
            print("OK", t, results[t])
    time.sleep(1.2)

# stockanalysis key pages for FCF/ROE via financials ratios if possible
def sa_full(t):
    out = {}
    for path in [f"https://stockanalysis.com/stocks/{t.lower()}/statistics/", f"https://stockanalysis.com/stocks/{t.lower()}/financials/ratios/"]:
        try:
            page = fetch(path)
        except Exception as e:
            out.setdefault("errors", []).append(str(e))
            continue
        # strip tags lightly for line search
        text = re.sub(r"<script[\s\S]*?</script>", " ", page, flags=re.I)
        text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
        # pair td
        pairs = re.findall(r"<t[dh][^>]*>([\s\S]*?)</t[dh]>\s*<t[dh][^>]*>([\s\S]*?)</t[dh]>", text, re.I)
        clean_pairs = []
        for a,b in pairs:
            a = htmlmod.unescape(re.sub(r"<[^>]+>", "", a))
            b = htmlmod.unescape(re.sub(r"<[^>]+>", "", b))
            a = re.sub(r"\s+", " ", a).strip()
            b = re.sub(r"\s+", " ", b).strip()
            clean_pairs.append((a,b))
        mapping = {
            "Forward PE": "forwardPE",
            "PE Ratio": "pe",
            "PEG Ratio": "peg",
            "Return on Equity (ttm)": "roe",
            "Return on Equity": "roe",
            "Return on Capital (ttm)": "roic",
            "Return on Capital": "roic",
            "Return on Assets (ttm)": "roa",
            "Free Cash Flow": "fcf",
            "Levered Free Cash Flow": "fcf_lev",
            "Profit Margin": "margin",
            "Operating Margin": "opmargin",
            "P/FCF Ratio": "pfcf",
            "FCF Yield": "fcf_yield",
        }
        for a,b in clean_pairs:
            if a in mapping and mapping[a] not in out:
                if b and b.lower() not in ("n/a", "-", "—"):
                    out[mapping[a]] = b.rstrip(".")
        # prose fallbacks
        m = re.search(r"forward PE ratio is ([0-9.]+)", page, re.I)
        if m and "forwardPE" not in out:
            out["forwardPE"] = m.group(1)
        m = re.search(r"PEG ratio is ([0-9.]+)", page, re.I)
        if m and "peg" not in out:
            out["peg"] = m.group(1)
        m = re.search(r"trailing PE ratio is ([0-9.]+)", page, re.I)
        if m and "pe" not in out:
            out["pe"] = m.group(1)
    return out

# merge prior SA
prior = {}
try:
    with open("/home/hermes/.hermes/profiles/charles/tmp_watchlist_fundamentals.json") as f:
        prior = json.load(f)
except Exception:
    pass
sa_prior = prior.get("stockanalysis") or {}

extra = ["MSFT","NVDA","MU","ORCL","CRM","DELL","META","GOOG","AVGO","TSM","INTC","CRWV","NBIS","BE","PSIX","GLW","SEI","NFLX","AAPL","AMZN","PLTR","TSLA","WMT","HD","LOW","TGT","MELI","SNDK","AMD","ASML","INFY","CRCL","WYFI","IREN","APLD","BW","PUMP","TE"]
sa = dict(sa_prior)
for t in extra:
    d = sa_full(t)
    # clean trailing dots from old
    for k,v in list(d.items()):
        if isinstance(v, str):
            d[k] = v.rstrip(".")
    if d:
        # merge prefer new non-null
        base = sa.get(t) or {}
        for k,v in d.items():
            if v is not None:
                base[k] = v if not (isinstance(v,str) and v.endswith('.')) else v.rstrip('.')
        # cleanup old dotted
        for k,v in list(base.items()):
            if isinstance(v, str):
                base[k] = v.rstrip('.')
                if base[k] == '1' and k in ('forwardPE','pe') and t in ('CRWV','NBIS','INTC','APLD','IREN','CORZ','RIOT','CLSK','BTDR','HIVE','RKLB'):
                    # suspicious single-digit 1 from bad parse - drop
                    base[k] = None
        sa[t] = base
        print("SA2", t, {k: base.get(k) for k in ["forwardPE","pe","peg","roe","roic","fcf","pfcf","fcf_yield"]})
    time.sleep(0.5)

out = {"finviz": results, "stockanalysis": sa}
with open("/home/hermes/.hermes/profiles/charles/tmp_watchlist_fundamentals.json","w") as f:
    json.dump(out, f, indent=1)
print("finviz count", len(results))
