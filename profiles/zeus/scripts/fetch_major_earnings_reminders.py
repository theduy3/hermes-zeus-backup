#!/usr/bin/env python3
"""Fetch major + watchlist US-listed earnings dates and create Obsidian task reminders.

Runs quarterly near the beginning of Jan/Apr/Jul/Oct. Creates one task per
major earnings report and per ticker in /vault/System/Stock Watchlist.md under
/vault/Tasks/tasks. Existing reminders are left unchanged for idempotency.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import yfinance as yf
except Exception:  # optional fallback only
    yf = None

TZ = ZoneInfo("America/Vancouver")
TASK_DIR = Path("/vault/Tasks/tasks")
WATCHLIST_PATH = Path("/vault/System/Stock Watchlist.md")

# Always include these if found, even if Nasdaq market-cap formatting is odd.
CORE_TICKERS = {
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "AVGO", "AMD", "NFLX",
    "JPM", "BAC", "WFC", "C", "GS", "MS", "V", "MA", "AXP", "PYPL", "COIN",
    "WMT", "COST", "HD", "LOW", "TGT", "MCD", "SBUX", "NKE",
    "UNH", "LLY", "JNJ", "ABBV", "MRK", "PFE", "TMO", "DHR",
    "XOM", "CVX", "CAT", "BA", "GE", "ORCL", "CRM", "ADBE", "INTC", "QCOM", "MU", "TXN", "IBM",
    "PEP", "KO", "PG", "DIS", "UBER", "SHOP", "PLTR", "NOW", "INTU", "SNOW",
}
# Keep reminder volume useful: mega-cap by default, plus explicit CORE_TICKERS and Duy's watchlist.
MAJOR_MARKET_CAP = 250_000_000_000
# Nasdaq sometimes omits newly public/special watchlist names; use yfinance fallback only for these.
YFINANCE_FALLBACK_TICKERS = {"SPCX"}
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"



def load_watchlist_tickers() -> set[str]:
    """Read Duy's watchlist tickers from /vault/System/Stock Watchlist.md.

    Only the Watchlist section is included, not macro indicators. Canadian .TO
    tickers and ETFs are kept in the set; Nasdaq simply won't return earnings
    rows for instruments without earnings.
    """
    tickers: set[str] = set()
    if not WATCHLIST_PATH.exists():
        return tickers
    in_watchlist = False
    ticker_re = re.compile(r"^-\s+(\^?[A-Z][A-Z0-9.*=/-]{0,11})\s*$")
    for raw in WATCHLIST_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if line.startswith("Indicators:"):
            in_watchlist = False
            continue
        if line.startswith("Watchlist:"):
            in_watchlist = True
            continue
        if not in_watchlist:
            continue
        m = ticker_re.match(line)
        if not m:
            continue
        sym = m.group(1).upper()
        if sym.startswith("^") or "=" in sym or "-" in sym:
            continue
        tickers.add(sym.split(".", 1)[0])
    return tickers


@dataclass(frozen=True)
class Earnings:
    symbol: str
    name: str
    day: date
    session: str
    market_cap: int
    eps: str
    fiscal: str


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")[:90] or "earnings-reminder"


def parse_market_cap(raw: str) -> int:
    digits = re.sub(r"[^0-9]", "", raw or "")
    return int(digits) if digits else 0


def session_label(raw: str) -> str:
    raw = (raw or "").lower()
    if "pre" in raw:
        return "Before market open"
    if "after" in raw:
        return "After market close"
    return "Time not confirmed"


def fetch_day(day: date, watchlist: set[str]) -> list[Earnings]:
    url = f"https://api.nasdaq.com/api/calendar/earnings?date={day.isoformat()}"
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.nasdaq.com",
        "Referer": "https://www.nasdaq.com/market-activity/earnings",
    })
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=25).read().decode("utf-8"))
    except Exception:
        return []
    rows = ((data.get("data") or {}).get("rows") or [])
    out: list[Earnings] = []
    for r in rows:
        symbol = (r.get("symbol") or "").strip().upper()
        if not symbol or "." in symbol or "^" in symbol:
            continue
        cap = parse_market_cap(r.get("marketCap") or "")
        if symbol not in CORE_TICKERS and symbol not in watchlist and cap < MAJOR_MARKET_CAP:
            continue
        out.append(Earnings(
            symbol=symbol,
            name=(r.get("name") or symbol).strip(),
            day=day,
            session=session_label(r.get("time") or ""),
            market_cap=cap,
            eps=(r.get("epsForecast") or "").strip(),
            fiscal=(r.get("fiscalQuarterEnding") or "").strip(),
        ))
    return out


def existing_for(symbol: str, day: date) -> Path | None:
    needle1 = f"earnings_symbol: {symbol}\n"
    needle2 = f"due_date: {day.isoformat()}"
    for p in TASK_DIR.glob(f"earnings-{symbol.lower()}-*.md"):
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if needle1 in txt and needle2 in txt:
            return p
    return None


def yfinance_watchlist_earnings(watchlist: set[str], start: date, end: date) -> list[Earnings]:
    """Fallback for watchlist tickers missing from Nasdaq calendar rows."""
    if yf is None:
        return []
    out: list[Earnings] = []
    for symbol in sorted(watchlist & YFINANCE_FALLBACK_TICKERS):
        try:
            ticker = yf.Ticker(symbol)
            cal = ticker.calendar or {}
            raw = cal.get("Earnings Date")
            if isinstance(raw, (list, tuple)):
                raw = raw[0] if raw else None
            if isinstance(raw, datetime):
                day = raw.date()
            elif isinstance(raw, date):
                day = raw
            elif raw:
                day = date.fromisoformat(str(raw)[:10])
            else:
                continue
            if not (start <= day <= end):
                continue
            info = getattr(ticker, "info", {}) or {}
            out.append(Earnings(
                symbol=symbol,
                name=(info.get("shortName") or info.get("longName") or symbol).strip(),
                day=day,
                session="Time not confirmed",
                market_cap=int(info.get("marketCap") or 0),
                eps=str(cal.get("Earnings Average") or "").strip(),
                fiscal="",
            ))
        except Exception:
            continue
    return out


def write_task(e: Earnings, dry_run: bool = False) -> Path | None:
    if existing_for(e.symbol, e.day):
        return None
    title = f"Earnings: {e.symbol} — {e.name}"
    path = TASK_DIR / f"earnings-{e.symbol.lower()}-{e.day.isoformat()}.md"
    body = "\n".join([
        "---",
        "type: event",
        f"due_date: {e.day.isoformat()}",
        f"due_time: \"{e.session}\"",
        "status: pending",
        "time_block: fixed",
        "estimated_minutes: 10",
        "energy: low",
        "priority: normal",
        "company: finance",
        "tags: [finance, stocks, earnings]",
        f"earnings_symbol: {e.symbol}",
        f"earnings_session: \"{e.session}\"",
        f"earnings_fiscal_quarter: \"{e.fiscal}\"",
        "source: nasdaq-earnings-calendar",
        "---",
        "",
        f"# {title}",
        "",
        f"Date: {e.day.isoformat()}",
        f"Time: {e.session}",
        f"Ticker: {e.symbol}",
        f"Company: {e.name}",
        f"Fiscal quarter: {e.fiscal or 'n/a'}",
        f"EPS forecast: {e.eps or 'n/a'}",
        "",
        "Event reminder: check earnings preview, options/volatility, and post-earnings reaction.",
        "",
    ])
    if dry_run:
        print(f"would create {path.name}: {e.symbol} {e.day} {e.session}")
    else:
        TASK_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="", help="YYYY-MM-DD; default today Vancouver")
    ap.add_argument("--days", type=int, default=70)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    start = date.fromisoformat(args.start) if args.start else datetime.now(TZ).date()
    created = skipped = found = 0
    watchlist = load_watchlist_tickers()
    seen: set[tuple[str, date]] = set()
    for i in range(args.days):
        d = start + timedelta(days=i)
        for e in fetch_day(d, watchlist):
            seen.add((e.symbol, e.day))
            found += 1
            if write_task(e, args.dry_run):
                created += 1
            else:
                skipped += 1
    end = start + timedelta(days=args.days - 1)
    for e in yfinance_watchlist_earnings(watchlist, start, end):
        if (e.symbol, e.day) in seen:
            continue
        found += 1
        if write_task(e, args.dry_run):
            created += 1
        else:
            skipped += 1
    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}major/watchlist earnings reminders: {created} created, {skipped} existing, {found} found; watchlist={len(watchlist)} tickers; window={start}..{end}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
