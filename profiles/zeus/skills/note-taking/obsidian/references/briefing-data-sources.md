# External Data Sources for Daily Briefings

Working sources as of 2026-05. All tested from Docker Hermes environment.

## Stocks — Yahoo Finance v8 Chart API

The v6/v7 quote endpoints return 401/rate-limit. Use the v8 chart API instead:

```bash
# Always set a browser User-Agent header
curl -sS -L -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=1d" \
  -o /tmp/spx.json
```

Parse: `data['chart']['result'][0]['meta']` → `regularMarketPrice`, `chartPreviousClose` (NOT `previousClose` — that key doesn't exist in v8 API).

**Ticker URL-encoding:** `^GSPC` → `%5EGSPC`, `^VIX` → `%5EVIX`, `^TNX` → `%5ETNX`. Regular tickers (TSLA, NVDA, etc.) need no encoding.

**Pitfall:** Yahoo RSS feed (`feeds.finance.yahoo.com/rss/...`) returns a "Will be right back" error page — don't use it.

**Reusable parser:** `scripts/parse_stocks.py` — pass `--all` for all tickers, `--top N` to limit. Only tickers with >2% change print by default.

**Finding the script in cron/Docker:** The script lives inside the skill directory. In the cron container `HOME` is often `/home/hermes/.hermes/profiles/zeus/home`, so `~/` paths resolve differently. Find it with:

```bash
find /home/hermes -name "parse_stocks.py" -path "*/obsidian/*" 2>/dev/null | head -1
```

If the script can't be found, write a minimal one to `/tmp/parse_stocks.py` using `write_file`, then run it with `python3 /tmp/parse_stocks.py --all`. The key parsing logic: load JSON → `data['chart']['result'][0]['meta']` → `regularMarketPrice` / `chartPreviousClose` → compute % change.

**Fetching all tickers:** The `&` background operator is blocked in foreground terminal commands. Write a shell script to `/tmp/fetch_stocks.sh` that loops over tickers with sequential `curl` calls, then run it with `bash /tmp/fetch_stocks.sh` (timeout 120s for 11 tickers). See `scripts/fetch_stocks.sh` for the canned script.

## Weather — wttr.in

```bash
# Current conditions
curl -sS "https://wttr.in/Montreal?format=%C+%t+%h+%w"

# JSON forecast (2+ days)
curl -sS "https://wttr.in/Montreal?format=j1" -o /tmp/wx.json
```

Parse JSON: `data['weather'][i]` → `date`, `maxtempC`, `mintempC`, `hourly[4]['weatherDesc'][0]['value']`.

**Reusable parser:** `scripts/parse_weather.py` — reads the three standard temp files and prints pipe-delimited rows. Find it the same way as parse_stocks.py (search under the obsidian skill directory).

**CRITICAL pitfall — city disambiguation:** `wttr.in/Laval` returns Laval, **France**. Use `wttr.in/Laval,Quebec` for the Montreal suburb. Quebec City is `wttr.in/Quebec+City`.

## News — NYT RSS

Working and returns today's headlines:

```bash
curl -sS "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml" -o /tmp/nyt.xml
# Extract titles: grep -oP '<title>[^<]+</title>' /tmp/nyt.xml
```

## Horoscope — horoscope.com

Static content partially available; the full text is loaded dynamically:

```bash
curl -sS -L "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=9" \
  -o /tmp/horo.html
# Sign 9 = Sagittarius. Extract: grep "MAY 15, 2026" /tmp/horo.html
```

The page truncates with "Read full overview" link — only the first sentence is available via static scrape. Use what's available plus astrological context (moon sign, aspects) for a reasonable 1-2 sentence summary.

## Moon phase

```bash
curl -sS "https://wttr.in/Montreal?format=%m"
```
Returns emoji: 🌑 new, 🌒 waxing crescent, 🌓 first quarter, 🌔 waxing gibbous, 🌕 full, 🌖 waning gibbous, 🌗 last quarter, 🌘 waning crescent.
