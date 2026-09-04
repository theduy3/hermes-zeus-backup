#!/usr/bin/env python3
import json, re
from pathlib import Path

outdir = Path("/tmp/yh_ks")
# map file stem to ticker
files = list(outdir.glob("*.html"))

def parse_num(s):
    if s is None: return None
    s = s.strip().replace(",","").replace("\xa0","")
    if s in ("","--","—","N/A","Infinity"): return None
    if s.endswith("%"):
        try: return float(s[:-1])/100.0
        except: return None
    mult=1.0
    if s[-1:] in "KMBT" and re.match(r"^-?\d", s):
        mult={"K":1e3,"M":1e6,"B":1e9,"T":1e12}[s[-1]]
        s=s[:-1]
    try: return float(s)*mult
    except: return None

def extract_deep(html):
    out={}
    # Find valuation table rows via various HTML structures
    labels = {
        "Forward P/E": "fwd_pe",
        "Trailing P/E": "trail_pe",
        "PEG Ratio (5yr expected)": "peg",
        "PEG Ratio (5 yr expected)": "peg",
        "Return on Equity (ttm)": "roe",
        "Return on Assets (ttm)": "roa",
        "Levered Free Cash Flow (ttm)": "fcf",
        "Operating Cash Flow (ttm)": "ocf",
        "Profit Margin": "pm",
        "Operating Margin (ttm)": "opm",
    }
    # strip tags helper patterns: look for label text near numbers in table
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    # keep some structure
    plain = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    plain = re.sub(r"</tr>", "\n", plain, flags=re.I)
    plain = re.sub(r"</p>", "\n", plain, flags=re.I)
    plain = re.sub(r"<[^>]+>", " ", plain)
    plain = re.sub(r"[ \t]+", " ", plain)
    plain = re.sub(r"\n+", "\n", plain)

    for label, key in labels.items():
        # e.g. "Forward P/E 24.45 19.19 ..."
        m = re.search(re.escape(label) + r"\s+([-\d\.,]+%?|N/A|--)", plain)
        if m:
            out[key] = parse_num(m.group(1))
            out[key+"_s"] = m.group(1)

    # JSON raw fields again more thoroughly
    for pat, key in [
        (r'"forwardPE"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "fwd_pe"),
        (r'"trailingPE"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "trail_pe"),
        (r'"pegRatio"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "peg"),
        (r'"returnOnEquity"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "roe"),
        (r'"returnOnAssets"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "roa"),
        (r'"freeCashflow"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "fcf"),
        (r'"operatingCashflow"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "ocf"),
        (r'"profitMargins"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "pm"),
    ]:
        matches = re.findall(pat, html)
        if matches:
            try:
                out[key] = float(matches[0])
            except:
                pass
    return out, plain

results={}
for f in files:
    stem=f.stem
    ticker = stem.replace("_",".") if stem.endswith("_TO") else stem.replace("_",".")
    # VFV_TO -> VFV.TO
    if stem.endswith("_TO"):
        ticker = stem[:-3].replace("_",".") + ".TO"
    html=f.read_text(encoding="utf-8", errors="replace")
    out, plain = extract_deep(html)
    # debug snippet for ROE
    idx = plain.find("Return on Equity")
    snip = plain[idx:idx+80] if idx>=0 else None
    out["roe_snip"]=snip
    idx2 = plain.find("Levered Free Cash Flow")
    out["fcf_snip"]=plain[idx2:idx2+90] if idx2>=0 else None
    results[ticker]=out

print(json.dumps(results, indent=2, default=str)[:50000])
# summary
print("---SUMMARY---")
for t in sorted(results):
    v=results[t]
    print(f"{t}\tfwd={v.get('fwd_pe')}\tpeg={v.get('peg')}\troe={v.get('roe')}\troa={v.get('roa')}\tfcf={v.get('fcf')}\tocf={v.get('ocf')}\tpm={v.get('pm')}")
