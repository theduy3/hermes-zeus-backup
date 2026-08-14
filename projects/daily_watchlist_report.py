import re, sys, time, contextlib, io
from datetime import datetime
from pathlib import Path
import yfinance as yf

WATCH = Path('/vault/System/Stock Watchlist.md')
if not WATCH.exists():
    WATCH = Path('/Users/theduy/theduyvault/System/Stock Watchlist.md')
if not WATCH.exists():
    print('BLOCKER: watchlist not found')
    sys.exit(2)

lines = WATCH.read_text().splitlines()
in_watch = False
groups = []
current_group = 'Ungrouped'
for line in lines:
    if line.startswith('Watchlist:'):
        in_watch = True
        continue
    if not in_watch:
        continue
    if line.startswith('Indicators:'):
        break
    if line.startswith('## '):
        current_group = line[3:].strip()
        groups.append((current_group, []))
        continue
    m = re.match(r'^-\s*([A-Za-z0-9.^=-]+)', line.strip())
    if m:
        if not groups:
            groups.append((current_group, []))
        groups[-1][1].append(m.group(1).upper())

def safe_float(x):
    try:
        if x is None: return None
        return float(x)
    except Exception:
        return None

def fmt_num(x):
    x=safe_float(x)
    return 'N/A' if x is None else f'{x:.1f}'

def fmt_price(x, cur=None):
    x=safe_float(x)
    if x is None: return 'N/A'
    s = f'{x:,.0f}' if x>=1000 else (f'{x:.1f}' if x>=100 else f'{x:.2f}')
    return ('C$' if cur == 'CAD' else '$') + s

def change_str(x):
    x=safe_float(x)
    return 'N/A' if x is None else f'{x:+.1f}%'

def get_data(sym):
    d={'ticker':sym}
    try:
        t=yf.Ticker(sym)
        # yfinance can print provider warnings; silence them in report generation.
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            info=t.info or {}
        d.update(info)
        price=safe_float(info.get('regularMarketPrice') or info.get('currentPrice'))
        prev=safe_float(info.get('regularMarketPreviousClose') or info.get('previousClose'))
        chg=safe_float(info.get('regularMarketChangePercent'))
        if chg is not None and abs(chg) > 100: # sometimes returned as fraction or bps inconsistently
            chg = chg/100
        if chg is None and price is not None and prev:
            chg=(price/prev-1)*100
        if price is None:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                hist=t.history(period='5d', interval='1d', auto_adjust=False)
            if not hist.empty:
                close=hist['Close'].dropna()
                if len(close): price=safe_float(close.iloc[-1])
                if len(close)>=2 and safe_float(close.iloc[-2]): chg=(safe_float(close.iloc[-1])/safe_float(close.iloc[-2])-1)*100
        d['price']=price
        d['chg']=chg
    except Exception as e:
        d['error']=repr(e)
    return d

all_syms=[s for _,lst in groups for s in lst]
data={}
for sym in all_syms:
    data[sym]=get_data(sym)
    time.sleep(0.15)

def sentiment(sym, q, group):
    price=safe_float(q.get('price'))
    chg=safe_float(q.get('chg'))
    f=safe_float(q.get('forwardPE'))
    target=safe_float(q.get('targetMeanPrice'))
    upside=(target/price-1)*100 if target and price else None
    if price is None:
        return 'Watch (data missing)'
    if group == 'ETFs / Funds' or sym in {'GLD','SMH','VFV.TO','SPCX'}:
        return 'Watch (ETF/fund)'
    speculative_groups={'Crypto Miners / Bitcoin Infrastructure','Data Centers / Power','Other / Unresolved'}
    if f is None or f <= 0:
        if group in speculative_groups:
            return 'Watch (speculative + weak tape)' if chg is not None and chg < -3 else 'Watch (speculative/no Fwd P/E)'
        return 'Watch (Fwd P/E missing)'
    high_growth = group in {'Mega-cap AI / Platforms','Semiconductors','AI Infrastructure / Cloud','Consumer / Internet'}
    reasonable = f < (32 if high_growth else 24)
    stretched = f > (45 if high_growth else 35)
    if reasonable and (chg is None or chg > -1.5) and (upside is None or upside > -5):
        return 'Buy (reasonable Fwd P/E + stable tape)'
    if upside is not None and upside > 15 and (chg is None or chg > -2) and not stretched:
        return 'Buy (target upside + stable tape)'
    if stretched and chg is not None and chg < -2:
        return 'Sell (rich valuation + weak tape)'
    if chg is not None and chg < -4:
        return 'Watch (weak tape)'
    if stretched:
        return 'Hold (rich Fwd P/E)'
    return 'Hold (neutral tape)'

rows=[]
for group,lst in groups:
    for sym in lst:
        q=data.get(sym,{})
        q['group']=group
        q['sentiment']=sentiment(sym,q,group)
        rows.append(q)

print(f'Daily Watchlist - {datetime.now().strftime("%Y-%m-%d")}')
print(f'Data source: yfinance/Yahoo Finance; fetched {datetime.now().strftime("%Y-%m-%d %H:%M local")}.')
print()
for group,lst in groups:
    print(f'**{group}**')
    print('| Ticker | Price | Chg % | Fwd P/E | Sentiment |')
    print('|---|---:|---:|---:|---|')
    for sym in lst:
        r=data.get(sym,{})
        print(f"| {sym} | {fmt_price(r.get('price'), r.get('currency'))} | {change_str(r.get('chg'))} | {fmt_num(r.get('forwardPE'))} | {r.get('sentiment','Watch (data missing)')} |")
    print()

# Rank opportunities: buy first, then lower-FPE holds with stable tape.
def score_best(r):
    f=safe_float(r.get('forwardPE')) or 999
    c=safe_float(r.get('chg')) or 0
    s=10 if str(r.get('sentiment','')).startswith('Buy') else (3 if str(r.get('sentiment','')).startswith('Hold') else 0)
    return (s, min(c,5), -f)
choices=[r for r in rows if str(r.get('sentiment','')).startswith(('Buy','Hold'))]
choices.sort(key=score_best, reverse=True)
print('**Best opportunities today** *(analysis, not financial advice)*')
for r in choices[:5]:
    print(f"- {r['ticker']}: {r['sentiment']}; {change_str(r.get('chg'))}, Fwd P/E {fmt_num(r.get('forwardPE'))}.")
if not choices:
    print('- None compelling on today’s data; most names are Watch due to missing/negative forward P/E or weak tape.')
print()

avoid=[r for r in rows if str(r.get('sentiment','')).startswith(('Sell','Watch'))]
avoid.sort(key=lambda r: (safe_float(r.get('chg')) if safe_float(r.get('chg')) is not None else -999))
print('**Avoid / wait**')
for r in avoid[:5]:
    print(f"- {r['ticker']}: {r['sentiment']}; {change_str(r.get('chg'))}, Fwd P/E {fmt_num(r.get('forwardPE'))}.")
print()

valid=[r for r in rows if safe_float(r.get('chg')) is not None]
valid.sort(key=lambda r: safe_float(r.get('chg')))
missing=[r['ticker'] for r in rows if safe_float(r.get('price')) is None or safe_float(r.get('forwardPE')) is None]
print('**Notes**')
if valid:
    print(f"- Biggest gainer: {valid[-1]['ticker']} ({change_str(valid[-1].get('chg'))}); biggest loser: {valid[0]['ticker']} ({change_str(valid[0].get('chg'))}).")
if missing:
    print('- Missing price/Fwd P/E: ' + ', '.join(missing[:12]) + (', ...' if len(missing)>12 else '') + '.')
print('- Watch ratings mean the evidence is incomplete, speculative, or risk/reward is not yet attractive.')
print()
print('This is analysis, not financial advice.')
