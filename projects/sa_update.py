#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys, urllib.request, urllib.error, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from html import unescape

CIK = '0002045724'
CIK_N = str(int(CIK))
VAULT = Path('/vault') if Path('/vault').is_dir() else Path('/Users/theduy/theduyvault')
OUT = VAULT / 'Inbox' / 'Situational Awareness Update.md'
UA = 'Hermes Agent investment-analysis cron contact: user@example.com'
BASE = 'https://data.sec.gov/submissions/CIK0002045724.json'

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def fetch_text(url: str) -> str:
    return fetch(url).decode('utf-8', errors='replace')

def money(v):
    if v is None: return '—'
    sign='-' if v<0 else ''
    v=abs(v)
    return f"{sign}${v:,.0f}"

def num(v):
    if v is None: return '—'
    sign='-' if v<0 else ''
    return sign + f"{abs(v):,}"

def md_escape(s):
    return str(s or '').replace('|','\\|').replace('\n',' ')

def get_recent_filings():
    data = json.loads(fetch_text(BASE))
    recent = data['filings']['recent']
    rows=[]
    n=len(recent['accessionNumber'])
    for i in range(n):
        rows.append({k: recent[k][i] if i < len(recent[k]) else None for k in recent})
    return data, rows

def archive_base(accession):
    acc_nodash = accession.replace('-','')
    return f'https://www.sec.gov/Archives/edgar/data/{CIK_N}/{acc_nodash}'

def find_info_xml(accession):
    idx_url = archive_base(accession) + '/index.json'
    idx = json.loads(fetch_text(idx_url))
    items = idx.get('directory',{}).get('item',[])
    candidates=[]
    for item in items:
        name=item.get('name','')
        low=name.lower()
        if low.endswith('.xml') and ('info' in low or '13f' in low or 'form13f' in low):
            if not low.startswith('primary_doc') and not low.startswith('xsl'):
                candidates.append(name)
    # Prefer infotable XML names
    candidates.sort(key=lambda n: (0 if 'infotable' in n.lower() or 'informationtable' in n.lower() else 1, len(n)))
    if not candidates:
        raise RuntimeError(f'No information table XML found for {accession}: {[i.get("name") for i in items]}')
    return archive_base(accession) + '/' + candidates[0], candidates[0]

def strip_ns(tag): return tag.split('}',1)[-1]

def child_text(elem, name):
    for c in elem.iter():
        if strip_ns(c.tag)==name:
            return (c.text or '').strip()
    return ''

def parse_info_table(accession):
    url, fname = find_info_xml(accession)
    xml = fetch_text(url)
    root = ET.fromstring(xml.encode('utf-8'))
    rows=[]
    for it in root.iter():
        if strip_ns(it.tag) != 'infoTable':
            continue
        issuer=child_text(it,'nameOfIssuer')
        cls=child_text(it,'titleOfClass')
        cusip=child_text(it,'cusip')
        value_txt=child_text(it,'value')
        ssh_txt=child_text(it,'sshPrnamt')
        putcall=child_text(it,'putCall')
        ssh_type=child_text(it,'sshPrnamtType')
        discretion=child_text(it,'investmentDiscretion')
        other=child_text(it,'otherManager')
        # Voting authority direct children are tricky; use generic totals
        sole=child_text(it,'Sole') or child_text(it,'sole')
        shared=child_text(it,'Shared') or child_text(it,'shared')
        none=child_text(it,'None') or child_text(it,'none')
        try: value=int(value_txt.replace(',','')) if value_txt else 0
        except: value=0
        try: shares=int(float(ssh_txt.replace(',',''))) if ssh_txt else 0
        except: shares=0
        rows.append({'issuer':issuer,'class':cls,'cusip':cusip,'putcall':putcall or '', 'value':value, 'shares':shares, 'type':ssh_type, 'discretion':discretion, 'sole':sole, 'shared':shared, 'none':none})
    return url, rows

def key(row):
    return (row['issuer'].upper().strip(), row['class'].upper().strip(), row.get('putcall','').upper().strip())

def compare(latest, prior):
    pm={key(r):r for r in prior}
    lm={key(r):r for r in latest}
    allkeys=sorted(set(pm)|set(lm))
    comps=[]
    for k in allkeys:
        l=lm.get(k); p=pm.get(k)
        if l and not p: sig='NEW/BUY'
        elif p and not l: sig='SELL/EXIT'
        else:
            if l['shares']>p['shares']: sig='ADD'
            elif l['shares']<p['shares']: sig='REDUCE'
            else: sig='HOLD'
        base=l or p
        comps.append({'issuer':base['issuer'],'class':base['class'],'putcall':base.get('putcall',''),
                      'latest_value': l['value'] if l else 0, 'prior_value': p['value'] if p else 0,
                      'delta_value': (l['value'] if l else 0)-(p['value'] if p else 0),
                      'latest_shares': l['shares'] if l else 0, 'prior_shares': p['shares'] if p else 0,
                      'delta_shares': (l['shares'] if l else 0)-(p['shares'] if p else 0), 'signal':sig,
                      'cusip':base.get('cusip','')})
    return comps

def primary_doc_url(accession, primary):
    return archive_base(accession)+'/'+primary

def summarize_ownership(rows):
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=30)
    forms={'SC 13G','SC 13G/A','SC 13D','SC 13D/A','SCHEDULE 13G','SCHEDULE 13D','SCHEDULE 13D/A'}
    out=[]
    for r in rows:
        form=(r.get('form') or '').upper()
        if form not in forms: continue
        fd=datetime.strptime(r['filingDate'],'%Y-%m-%d').date()
        if fd < cutoff: continue
        url=primary_doc_url(r['accessionNumber'], r.get('primaryDocument') or '')
        summary='Beneficial ownership filing; details require primary document review.'
        try:
            txt=fetch_text(url)
            plain=re.sub('<[^>]+>',' ',txt)
            plain=unescape(re.sub(r'\s+',' ',plain))
            # Pull useful snippets around Nebius and percent ownership patterns
            snippets=[]
            for pat in ['Nebius', 'Percent of Class', 'percent of class', '%']:
                m=re.search(pat, plain, re.I)
                if m:
                    snippets.append(plain[max(0,m.start()-160):m.end()+260].strip())
            if snippets:
                summary=' '.join(snippets[:2])[:700]
        except Exception as e:
            summary=f'Could not fetch primary document detail: {e}'
        out.append({'form':r['form'],'date':r['filingDate'],'accession':r['accessionNumber'],'doc':r.get('primaryDocument'),'url':url,'summary':summary})
    return out

def table(rows, limit=None):
    hdr='| Issuer | Class | Put/Call | Signal | Latest value | Prior value | Δ value | Latest sh/ctr | Prior sh/ctr | Δ sh/ctr |\n|---|---|---:|---|---:|---:|---:|---:|---:|---:|'
    lines=[hdr]
    for r in (rows[:limit] if limit else rows):
        lines.append(f"| {md_escape(r['issuer'])} | {md_escape(r['class'])} | {md_escape(r['putcall'] or '—')} | {r['signal']} | {money(r['latest_value'])} | {money(r['prior_value'])} | {money(r['delta_value'])} | {num(r['latest_shares'])} | {num(r['prior_shares'])} | {num(r['delta_shares'])} |")
    if len(lines)==1: lines.append('| — | — | — | — | — | — | — | — | — | — |')
    return '\n'.join(lines)

def main():
    if not VAULT.is_dir():
        raise SystemExit('BLOCKER: vault not found at /vault or /Users/theduy/theduyvault')
    data, filings = get_recent_filings()
    f13=[r for r in filings if r.get('form')=='13F-HR']
    if len(f13)<2: raise RuntimeError('Fewer than two 13F-HR filings found')
    latest_f, prior_f = f13[0], f13[1]
    latest_url, latest_rows = parse_info_table(latest_f['accessionNumber'])
    prior_url, prior_rows = parse_info_table(prior_f['accessionNumber'])
    comps = compare(latest_rows, prior_rows)
    buys=sorted([c for c in comps if c['signal'] in ('NEW/BUY','ADD')], key=lambda r: (r['delta_value'], r['delta_shares']), reverse=True)
    holds=sorted([c for c in comps if c['signal']=='HOLD'], key=lambda r: r['latest_value'], reverse=True)
    sells=sorted([c for c in comps if c['signal'] in ('REDUCE','SELL/EXIT')], key=lambda r: (r['delta_value'], r['delta_shares']))
    full=sorted([c for c in comps if c['latest_shares']>0], key=lambda r: r['latest_value'], reverse=True)
    ownership=summarize_ownership(filings)
    now=datetime.now(ZoneInfo('America/Vancouver')).strftime('%Y-%m-%d %H:%M America/Vancouver')
    opt_count=sum(1 for r in latest_rows if r.get('putcall'))
    top_b=', '.join([f"{r['issuer']} ({r['signal']}, {num(r['delta_shares'])})" for r in buys[:3]]) or 'None'
    top_s=', '.join([f"{r['issuer']} ({r['signal']}, {num(r['delta_shares'])})" for r in sells[:3]]) or 'None'
    own_bullets='\n'.join([f"- **{o['date']} {o['form']}** [{o['accession']}]({o['url']}): {md_escape(o['summary'])}" for o in ownership]) or '- No SC 13G / SC 13D / SC 13D/A filings by this CIK found in the latest 30 days from the SEC submissions feed.'
    links=f"- SEC submissions JSON: {BASE}\n- Latest 13F-HR ({latest_f['filingDate']}, accession {latest_f['accessionNumber']}): {primary_doc_url(latest_f['accessionNumber'], latest_f.get('primaryDocument') or '')}\n- Latest 13F information table XML: {latest_url}\n- Prior 13F-HR ({prior_f['filingDate']}, accession {prior_f['accessionNumber']}): {primary_doc_url(prior_f['accessionNumber'], prior_f.get('primaryDocument') or '')}"
    md=f"""# Situational Awareness Update

Updated: {now}

## Executive summary

- SEC source: latest 13F-HR filing dated **{latest_f['filingDate']}** compared with prior 13F-HR dated **{prior_f['filingDate']}** for Situational Awareness LP (CIK {CIK}).
- Latest information table contains **{len(latest_rows)} rows**; **{len(full)} current rows** remain after excluding prior-only exits. Option rows in latest filing: **{opt_count}**.
- Top buy/add signals by reported 13F value/share delta: {md_escape(top_b)}.
- Top reduce/sell signals by reported 13F value/share delta: {md_escape(top_s)}.
- Beneficial ownership check: **{len(ownership)}** SC 13G / SC 13D / SC 13D/A filing(s) by this CIK found in the latest 30 days.

## Buy / Add signals

{table(buys)}

## Hold signals

{table(holds)}

## Reduce / Sell signals

{table(sells)}

## Full latest holdings

{table(full)}

## Beneficial ownership / activist filings

{own_bullets}

## Filing links

{links}

## Notes and caveats

- Tables show the SEC information-table `value` field as reported in the retrieved XML filing.
- **Important:** 13F option rows are not equivalent to cash equity exposure. Put and Call rows are kept separate from common/share rows and should not be summed as direct stock exposure.
- Signals are mechanical comparisons of reported share/contract counts between the latest and prior 13F: NEW/BUY, ADD, HOLD, REDUCE, SELL/EXIT. They are not a recommendation by themselves.
- 13F filings are delayed and may omit non-13F securities, shorts, many derivatives, and intraperiod trades.
- This is analysis, not financial advice. Consult a qualified advisor before making investment decisions.
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(md, encoding='utf-8')
    print(json.dumps({'out':str(OUT),'latest_date':latest_f['filingDate'],'prior_date':prior_f['filingDate'],'holdings':len(latest_rows),'current_rows':len(full),'top_buy_add':top_b,'top_reduce_sell':top_s,'ownership_count':len(ownership),'ownership_nebius': any('nebius' in (o['summary']+' '+o.get('doc','')).lower() for o in ownership)}, indent=2))

if __name__=='__main__': main()
