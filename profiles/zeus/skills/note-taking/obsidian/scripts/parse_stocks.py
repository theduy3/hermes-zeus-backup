#!/usr/bin/env python3
"""Parse Yahoo Finance v8 chart JSON files and print ticker prices with % change.

Reads JSON files from /tmp/<ticker>.json (or /tmp/spx.json for ^GSPC, etc.).
Prints tickers sorted by absolute % change, descending.
Only tickers with >2% change are printed unless --all is passed.

Usage:
    python3 scripts/parse_stocks.py              # >2% movers only
    python3 scripts/parse_stocks.py --all        # all tickers
    python3 scripts/parse_stocks.py --top 8      # top N by abs change
"""
import json, os, sys

# Ticker → JSON file mapping (Yahoo Finance v8 chart API)
TICKER_FILES = {
    '^GSPC': '/tmp/spx.json',
    '^VIX':  '/tmp/vix.json',
    '^TNX':  '/tmp/tnx.json',
    'TSLA':  '/tmp/TSLA.json',
    'NVDA':  '/tmp/NVDA.json',
    'AAPL':  '/tmp/AAPL.json',
    'META':  '/tmp/META.json',
    'GOOGL': '/tmp/GOOGL.json',
    'AMZN':  '/tmp/AMZN.json',
    'MSFT':  '/tmp/MSFT.json',
    'PLTR':  '/tmp/PLTR.json',
}

def parse_stocks(min_pct=0.0, top_n=None):
    results = []
    for sym, path in TICKER_FILES.items():
        if not os.path.exists(path):
            continue
        try:
            with open(path) as f:
                data = json.load(f)
            meta = data['chart']['result'][0]['meta']
            price = meta.get('regularMarketPrice', 0)
            prev = meta.get('chartPreviousClose', price or 1)
            if prev and prev != 0:
                chg = ((price - prev) / prev) * 100
            else:
                chg = 0
            if abs(chg) >= min_pct:
                results.append((abs(chg), sym, price, chg))
        except Exception as e:
            print(f"ERR {sym}: {e}", file=sys.stderr)

    results.sort(key=lambda x: x[0], reverse=True)
    if top_n:
        results = results[:top_n]

    for _, sym, price, chg in results:
        sign = '+' if chg >= 0 else ''
        print(f"{sym} ${price:.2f} ({sign}{chg:.1f}%)")


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--all', action='store_true', help='Show all tickers, not just >2%')
    p.add_argument('--top', type=int, default=None, help='Limit to top N by abs change')
    args = p.parse_args()

    min_pct = 0.0 if args.all else 2.0
    parse_stocks(min_pct=min_pct, top_n=args.top)
