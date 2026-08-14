import os, sys, json, urllib.request, re, xml.etree.ElementTree as ET, gzip
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from html import unescape

VAULTS=[Path('/vault'), Path('/Users/theduy/theduyvault')]
vault=next((p for p in VAULTS if p.exists()), None)
if not vault:
    print('BLOCKER: no vault found at /vault or /Users/theduy/theduyvault')
    sys.exit(2)

CIK='0002045724'
CIK_INT=str(int(CIK))
UA='Hermes Charles investment analysis cron contact: duy@example.com'

def fetch(url, accept='application/json'):
    h={'User-Agent':UA,'Accept-Encoding':'gzip, deflate'}
    if accept: h['Accept']=accept
    req=urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
        if r.headers.get('Content-Encoding') == 'gzip' or data[:2] == b'\x1f\x8b':
            data = gzip.decompress(data)
        return data

def fetch_json(url):
    return json.loads(fetch(url).decode('utf-8'))

sub_url=f'https://data.sec.gov/submissions/CIK{CIK}.json'
sub=fetch_json(sub_url)
recent=sub['filings']['recent']
forms=recent['form']; accs=recent['accessionNumber']; dates=recent['filingDate']; prim=recent.get('primaryDocument', ['']*len(forms))
filings=[]
for i, form in enumerate(forms):
    filings.append({'form':form,'accession':accs[i], 'filingDate':dates[i], 'primaryDocument': prim[i] if i < len(prim) else ''})
hr=[f for f in filings if f['form']=='13F-HR'][:2]
if len(hr)<2:
    print('BLOCKER: fewer than two 13F-HR filings found')
    sys.exit(3)

NS_RE=re.compile(r'\{.*\}')
def strip_ns(tag): return NS_RE.sub('', tag)
def text_child(elem, name):
    for c in elem:
        if strip_ns(c.tag)==name:
            return (c.text or '').strip()
    return ''
def find_child(elem, name):
    for c in elem:
        if strip_ns(c.tag)==name:
            return c
    return None

def info_xml_url(f):
    acc_nodash=f['accession'].replace('-','')
    base=f'https://www.sec.gov/Archives/edgar/data/{CIK_INT}/{acc_nodash}/'
    idx=fetch_json(base+'index.json')
    items=idx['directory']['item']
    cands=[it['name'] for it in items if it['name'].lower().endswith('.xml')]
    pref=[n for n in cands if any(s in n.lower() for s in ['infotable','info_table','form13finfo','primary_doc'])]
    for n in pref+cands:
        try:
            b=fetch(base+n, accept='application/xml')
            full=b.decode('utf-8','ignore').lower()
            if 'infotable' in full:
                return base+n, b
        except Exception:
            pass
    raise RuntimeError('No information table XML found for '+f['accession'])

def parse_info(f):
    url,b=info_xml_url(f)
    root=ET.fromstring(b)
    rows=[]
    for elem in root.iter():
        if strip_ns(elem.tag)=='infoTable':
            shrs=0
            ssh=find_child(elem,'shrsOrPrnAmt')
            if ssh is not None:
                shrs_txt=text_child(ssh,'sshPrnamt')
                shrs=int(float(shrs_txt.replace(',',''))) if shrs_txt else 0
            rows.append({
                'issuer': text_child(elem,'nameOfIssuer').upper(),
                'class': text_child(elem,'titleOfClass').upper(),
                'cusip': text_child(elem,'cusip').upper(),
                'putcall': text_child(elem,'putCall').upper(),
                'value': int(float((text_child(elem,'value') or '0').replace(',',''))),
                'shares': shrs,
                'sshType': (text_child(ssh,'sshPrnamtType') if ssh is not None else ''),
                'url': url,
            })
    agg={}
    for r in rows:
        key=(r['issuer'], r['class'], r['putcall'])
        if key not in agg:
            agg[key]=dict(r)
        else:
            agg[key]['value']+=r['value']; agg[key]['shares']+=r['shares']
            if r['cusip'] not in agg[key]['cusip']:
                agg[key]['cusip']+=','+r['cusip']
    return list(agg.values()), url

latest, latest_url=parse_info(hr[0])
prior, prior_url=parse_info(hr[1])
prior_map={(r['issuer'],r['class'],r['putcall']):r for r in prior}
latest_map={(r['issuer'],r['class'],r['putcall']):r for r in latest}
comp=[]
for k in sorted(set(prior_map)|set(latest_map)):
    l=latest_map.get(k); p=prior_map.get(k)
    lv=l['value'] if l else 0; pv=p['value'] if p else 0
    ls=l['shares'] if l else 0; ps=p['shares'] if p else 0
    if p is None and l is not None: sig='NEW/BUY'
    elif l is None and p is not None: sig='SELL/EXIT'
    elif ls>ps: sig='ADD'
    elif ls<ps: sig='REDUCE'
    else: sig='HOLD'
    base=l or p
    comp.append({**base, 'latest_value':lv, 'prior_value':pv, 'delta_value':lv-pv, 'latest_shares':ls, 'prior_shares':ps, 'delta_shares':ls-ps, 'signal':sig})

today=datetime.now(ZoneInfo('America/Vancouver')).date()
own=[]
own_forms={'SC 13G','SC 13G/A','SC 13D','SC 13D/A','SCHEDULE 13G','SCHEDULE 13D','SCHEDULE 13D/A'}
for f in filings:
    if f['form'] in own_forms:
        try: fd=datetime.strptime(f['filingDate'],'%Y-%m-%d').date()
        except: continue
        if fd >= today - timedelta(days=30):
            acc_nodash=f['accession'].replace('-','')
            base=f'https://www.sec.gov/Archives/edgar/data/{CIK_INT}/{acc_nodash}/'
            pdoc=f.get('primaryDocument') or ''
            url=base+pdoc if pdoc else base
            summary=f"{f['filingDate']} — {f['form']} — {pdoc or f['accession']}"
            try:
                txt=fetch(url, accept='text/plain').decode('utf-8','ignore')[:200000]
                plain=unescape(re.sub(r'<[^>]+>', ' ', txt))
                plain=re.sub(r'\s+', ' ', plain).strip()
                issuer=''
                m=re.search(r'UNDER THE SECURITIES EXCHANGE ACT OF 1934\s+(.+?)\s+\(Name of Issuer\)', plain, flags=re.I)
                if m: issuer=m.group(1).strip()
                title=''
                m=re.search(r'\(Name of Issuer\)\s+(.+?)\s+\(Title of Class of Securities\)', plain, flags=re.I)
                if m: title=m.group(1).strip()
                amount=''
                m=re.search(r'Aggregate Amount Beneficially Owned by Each Reporting Person\s+([0-9,.]+)', plain, flags=re.I)
                if m: amount=m.group(1).strip()
                pct=''
                m=re.search(r'Percent of class represented by amount in row \(9\)\s+([0-9.]+\s*%)', plain, flags=re.I)
                if m: pct=m.group(1).strip()
                bits=[]
                if issuer: bits.append(issuer)
                if title: bits.append(title)
                if amount: bits.append(f'beneficial ownership {amount} shares/securities')
                if pct: bits.append(f'{pct} of class')
                if bits: summary += ' — ' + ' — '.join(bits)
                if re.search('Nebius|NBIS', plain, re.I): summary += ' — Nebius/NBIS mentioned'
            except Exception as e:
                summary += f' (document fetch failed: {e})'
            own.append({'summary':summary,'url':url})

fmt_money=lambda v: f"${v:,.0f}"
fmt_num=lambda n: f"{n:,.0f}"
def row(r):
    typ = r['putcall'].title() if r['putcall'] else 'Stock'
    return f"| {r['issuer']} | {r['class']} | {typ} | {r['signal']} | {fmt_money(r['latest_value'])} | {fmt_money(r['delta_value'])} | {fmt_num(r['latest_shares'])} | {fmt_num(r['delta_shares'])} |"
def table(rows):
    head='| Issuer | Class | Type | Signal | Latest value | Δ value | Latest sh/contracts | Δ sh/contracts |\n|---|---:|---:|---:|---:|---:|---:|---:|'
    if not rows: return head+'\n| None |  |  |  |  |  |  |  |'
    return head+'\n'+'\n'.join(row(r) for r in rows)

buy=sorted([r for r in comp if r['signal'] in ('NEW/BUY','ADD')], key=lambda r: abs(r['delta_value']), reverse=True)
hold=sorted([r for r in comp if r['signal']=='HOLD'], key=lambda r: r['latest_value'], reverse=True)
red=sorted([r for r in comp if r['signal'] in ('REDUCE','SELL/EXIT')], key=lambda r: abs(r['delta_value']), reverse=True)
full=sorted([r for r in comp if r['latest_value']>0], key=lambda r: r['latest_value'], reverse=True)
updated=datetime.now(ZoneInfo('America/Vancouver')).strftime('%Y-%m-%d %H:%M America/Vancouver')
latest_date=hr[0]['filingDate']; prior_date=hr[1]['filingDate']
exec_bul=[
 f"Latest SEC 13F-HR filing is dated {latest_date}; comparison baseline is prior 13F-HR dated {prior_date}.",
 f"Latest information table contains {len(latest)} holdings rows after grouping by issuer, class, and put/call; total reported 13F value is {fmt_money(sum(r['value'] for r in latest))}.",
 f"Largest buy/add signals by reported value change: {', '.join([r['issuer']+' '+('('+r['signal']+')') for r in buy[:3]]) or 'none'}.",
 f"Largest reduce/sell signals by reported value change: {', '.join([r['issuer']+' '+('('+r['signal']+')') for r in red[:3]]) or 'none'}.",
]
exec_bul.append(f"Found {len(own)} Schedule 13D/13G-related filing(s) in the last 30 days; see beneficial ownership section." if own else "No Schedule 13D/13G-related filings by this CIK were found in the latest 30 days of the SEC submissions feed.")
own_md='\n'.join(f"- {o['summary']} — [SEC document]({o['url']})" for o in own) if own else '- None found in the latest 30 days in the SEC submissions feed.'
links=f"- SEC submissions JSON: {sub_url}\n- Latest 13F-HR ({latest_date}, accession {hr[0]['accession']}): {latest_url}\n- Prior 13F-HR ({prior_date}, accession {hr[1]['accession']}): {prior_url}"
content=f"""# Situational Awareness Update
Updated: {updated}

## Executive summary
""" + '\n'.join(f"- {b}" for b in exec_bul) + f"""

## Buy / Add signals
{table(buy)}

## Hold signals
{table(hold)}

## Reduce / Sell signals
{table(red)}

## Full latest holdings
{table(full)}

## Beneficial ownership / activist filings
{own_md}

## Filing links
{links}

## Notes and caveats
- Source: SEC EDGAR submissions and filing documents retrieved during this run.
- SEC 13F `value` figures are displayed as reported in the retrieved XML information table; for this filing they reconcile to approximate market values in dollars.
- 13F option rows are not equivalent to cash equity exposure. Put and Call rows are kept separate from stock rows and should not be interpreted as direct equity ownership.
- 13F data is delayed and only reflects reportable U.S.-listed securities as of the filing's reporting period; it is not a real-time portfolio.
- This is analysis, not financial advice. Consult a qualified advisor before making investment decisions. Past performance does not guarantee future results.
"""
out=vault/'Inbox'/'Situational Awareness Update.md'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(content, encoding='utf-8')
print(json.dumps({'path':str(out),'latest_date':latest_date,'prior_date':prior_date,'holdings':len(latest),'buy_top':[r['issuer']+' '+r['signal'] for r in buy[:5]],'red_top':[r['issuer']+' '+r['signal'] for r in red[:5]],'ownership_count':len(own),'ownership':[o['summary'] for o in own[:3]]}, indent=2))
