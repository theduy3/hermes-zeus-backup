#!/usr/bin/env python3
"""Monitor @ClaudeDevs for Claude limit-reset posts.

Fetches the public Nitter RSS feed, records seen tweet IDs, and prints a
Telegram-ready alert only when a new tweet looks like a limit-reset notice.
Cron runs this as no_agent=True, so empty stdout stays silent.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

STATE_DIR = pathlib.Path("/home/hermes/.hermes/profiles/zeus/x_monitors")
STATE_PATH = STATE_DIR / "claudedevs_limit_reset.json"
FEEDS = [
    "https://nitter.net/ClaudeDevs/rss",
    "https://nitter.poast.org/ClaudeDevs/rss",
]
USER_AGENT = "Mozilla/5.0 Hermes Zeus ClaudeDevs monitor"
MAX_SEEN = 300


def fetch_feed() -> bytes:
    last_error: Exception | None = None
    for url in FEEDS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - try fallback feed
            last_error = exc
    raise RuntimeError(f"all feeds failed; last error: {last_error}")


def strip_html(text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def parse_items(feed: bytes) -> list[dict]:
    root = ET.fromstring(feed)
    channel = root.find("channel")
    if channel is None:
        return []
    items: list[dict] = []
    for item in channel.findall("item"):
        title = item.findtext("title") or ""
        desc = item.findtext("description") or ""
        link = item.findtext("link") or ""
        guid = item.findtext("guid") or link or title
        pub = item.findtext("pubDate") or ""
        try:
            ts = parsedate_to_datetime(pub).isoformat() if pub else ""
        except Exception:
            ts = pub
        text = strip_html(title + "\n" + desc)
        items.append({"id": guid, "title": strip_html(title), "text": text, "link": link, "published": ts})
    return items


def is_limit_reset_notice(item: dict) -> bool:
    text = (item.get("text") or "").lower()
    # Main trigger: reset + limit in the same post, with Claude context from the account/name.
    if "reset" in text and "limit" in text:
        return True
    # Common phrasings that may omit exact words.
    patterns = [
        r"usage\s+has\s+reset",
        r"limits?\s+(?:are\s+)?back",
        r"quota\s+(?:has\s+)?reset",
        r"rate\s+limit\s+(?:has\s+)?reset",
        r"credits?\s+(?:have\s+)?reset",
    ]
    return any(re.search(p, text) for p in patterns)


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"seen": [], "alerts": []}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"seen": [], "alerts": []}


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    seen = list(dict.fromkeys(state.get("seen", [])))[:MAX_SEEN]
    state["seen"] = seen
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    init = "--init" in sys.argv
    feed = fetch_feed()
    items = parse_items(feed)
    if not items:
        return 0

    state = load_state()
    seen_set = set(state.get("seen", []))

    if not STATE_PATH.exists() or init:
        state["seen"] = [i["id"] for i in items][:MAX_SEEN]
        state["initialized_at"] = int(time.time())
        save_state(state)
        return 0

    new_items = [i for i in items if i["id"] not in seen_set]
    if not new_items:
        return 0

    alerts = [i for i in reversed(new_items) if is_limit_reset_notice(i)]
    state["seen"] = [i["id"] for i in new_items] + list(state.get("seen", []))
    if alerts:
        state.setdefault("alerts", [])
        state["alerts"] = ([{"id": a["id"], "published": a.get("published"), "link": a.get("link")} for a in alerts]
                            + state.get("alerts", []))[:50]
    save_state(state)

    if alerts:
        chunks = []
        for a in alerts:
            title = a.get("title") or "ClaudeDevs posted a limit reset"
            link = (a.get("link") or "").replace("https://nitter.net/", "https://x.com/")
            chunks.append(f"ClaudeDevs limit reset alert\n{title}\n{link}".strip())
        print("\n\n".join(chunks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
