#!/bin/bash
# Fetch stock quotes from Yahoo Finance v8 chart API — sequential, no & backgrounding.
# Maps Yahoo URL-encoded tickers to the JSON filenames parse_stocks.py expects.
# Usage: bash fetch_stocks.sh
# Timeout: ~10s per ticker × 11 tickers ≈ 120s recommended.

TICKERS=(
  '%5EGSPC:spx'
  '%5EVIX:vix'
  '%5ETNX:tnx'
  'TSLA:TSLA'
  'NVDA:NVDA'
  'AAPL:AAPL'
  'META:META'
  'GOOGL:GOOGL'
  'AMZN:AMZN'
  'MSFT:MSFT'
  'PLTR:PLTR'
)

UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

for entry in "${TICKERS[@]}"; do
  ticker="${entry%%:*}"
  fname="${entry##*:}"
  curl -sS -L -m 10 -H "User-Agent: $UA" \
    "https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=1d" \
    -o "/tmp/${fname}.json"
done
echo "done"