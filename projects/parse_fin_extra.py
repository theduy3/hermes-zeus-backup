#!/usr/bin/env python3
import re, json, html
from pathlib import Path

def parse_rows(path, kind='fin'):
    text = Path(path).read_text(errors='ignore')
    rows = {}
    trs = re.findall(r'<tr[^>]*class=\"styled-row[^\"]*\"[^>]*>(.*?)</tr>', text, flags=re.I|re.S)
    for tr in trs:
        m = re.search(r'data-boxover-ticker=\"([A-Z0-9.\-]+)\"', tr)
        if not m:
            m = re.search(r'class=\"tab-link\">([A-Z0-9.\-]+)</a>', tr)
        if not m:
            continue
        t = m.group(1)
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, flags=re.I|re.S)
        cells = []
        for td in tds:
            c = re.sub(r'<[^>]+>', ' ', td)
            c = html.unescape(c)
            c = re.sub(r'\s+', ' ', c).strip()
            cells.append(c)
        ti = None
        for i, c in enumerate(cells):
            if t in c.split() or c == t:
                ti = i
                break
        if ti is None:
            continue
        rest = cells[ti+1:]
        rows[t] = rest
    return rows

def num(s):
    if s is None: return None
    s = str(s).replace(',', '').replace('%', '').strip()
    if s in ('', '-', '—', 'N/A'): return None
    try: return float(s)
    except: return None

# Financial view v=161 columns typically:
# No Ticker Market Cap Dividend ROA ROE ROI Curr R Quick LT D/E Debt/Eq Gross M Op M Profit M Earnings Price Change Volume
fin = {}
for p in ['/tmp/fv_fin1.html','/tmp/fv_fin2.html']:
    fin.update(parse_rows(p))
print('fin rows', len(fin))
fin_out = {}
for t, rest in fin.items():
    # rest: mcap, dividend, roa, roe, roi, curr, quick, ltdebteq, debteq, gross, oper, profit, earnings, price, chg, vol
    fin_out[t] = {
        'mcap': rest[0] if rest else None,
        'div': rest[1] if len(rest)>1 else None,
        'roa': num(rest[2]) if len(rest)>2 else None,
        'roe': num(rest[3]) if len(rest)>3 else None,
        'roi': num(rest[4]) if len(rest)>4 else None,  # ROIC proxy on Finviz
        'grossM': num(rest[9]) if len(rest)>9 else None,
        'opM': num(rest[10]) if len(rest)>10 else None,
        'profitM': num(rest[11]) if len(rest)>11 else None,
        'raw': rest[:16],
    }
    print(t, 'roe', fin_out[t]['roe'], 'roi', fin_out[t]['roi'], 'raw0-6', rest[:6])

with open('/home/hermes/.hermes/projects/finviz_fin.json','w') as f:
    json.dump(fin_out, f, indent=2)

# extract remaining yahoo chart files
import os, json as J
from datetime import datetime, timezone
extra = {}
for t in ['HIVE','VFV.TO','GLD','SMH','SPCX','SEI','WYFI','CRCL','BITF']:
    path = f'/tmp/c_{t}.json'
    if not os.path.exists(path):
        continue
    try:
        d = J.load(open(path))
        if not d.get('chart',{}).get('result'):
            print(t, 'no result')
            continue
        m = d['chart']['result'][0]['meta']
        extra[t] = {
            'price': m.get('regularMarketPrice'),
            'chg': m.get('regularMarketChangePercent'),
            'asof': m.get('regularMarketTime'),
            'currency': m.get('currency'),
            'tz': m.get('timezone'),
        }
        print('chart', t, extra[t])
    except Exception as e:
        print(t, e)
with open('/home/hermes/.hermes/projects/extra_charts.json','w') as f:
    J.dump(extra, f, indent=2)
