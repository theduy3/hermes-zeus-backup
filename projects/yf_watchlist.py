import yfinance as yf, json, re, math
from datetime import datetime
WATCH='/vault/System/Stock Watchlist.md'
lines=open(WATCH).read().splitlines()
sections=[]; current=None; in_watch=False
for line in lines:
    if line.startswith('Watchlist:'):
        in_watch=True; continue
    if in_watch:
        if line.startswith('## '):
            current=line[3:].strip(); sections.append([current,[]]); continue
        m=re.match(r'\s*-\s*([A-Za-z0-9.^=\-]+)', line)
        if m and current: sections[-1][1].append(m.group(1).strip())
tickers=[t for _,ts in sections for t in ts]
out={}
for t in tickers:
    r={'symbol':t}
    try:
        tk=yf.Ticker(t)
        fi={}
        try:
            fi=tk.fast_info
            # Lazy dict
            for k in ['last_price','lastPrice','previous_close','previousClose','year_high','year_low','market_cap']:
                try:
                    if k in fi: r[k]=fi[k]
                except Exception: pass
        except Exception as e: r['fast_error']=repr(e)
        hist=tk.history(period='5d', interval='1d', auto_adjust=False, prepost=False)
        if not hist.empty:
            last=float(hist['Close'].dropna().iloc[-1])
            prev=float(hist['Close'].dropna().iloc[-2]) if len(hist['Close'].dropna())>1 else None
            r['price']=last
            if prev: r['chgPct']=(last-prev)/prev*100
        # info modules
        try:
            info=tk.get_info()
            for k in ['trailingPE','forwardPE','marketCap','sector','industry','shortName','longName','averageAnalystRating','targetMeanPrice','fiftyTwoWeekLow','fiftyTwoWeekHigh','quoteType']:
                if info.get(k) is not None: r[k]=info.get(k)
            # override price if live available
            for pk in ['currentPrice','regularMarketPrice']:
                if info.get(pk) is not None: r['price']=info.get(pk)
            if info.get('regularMarketChangePercent') is not None: r['chgPct']=info.get('regularMarketChangePercent')
        except Exception as e: r['info_error']=repr(e)
    except Exception as e: r['error']=repr(e)
    out[t]=r
print(json.dumps({'date':datetime.now().strftime('%Y-%m-%d'), 'sections':sections, 'data':out}, default=str))
