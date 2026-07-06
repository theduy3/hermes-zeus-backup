#!/usr/bin/env python3
"""Capture the latest After Earnings transcript into /vault/Inbox if new.

No-agent cron pattern: prints a short message only when a new transcript is
captured; prints nothing if the latest transcript was already captured.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BLOG_URL = "https://www.afterearnings.com/blog/"
STATE_PATH = Path("/home/hermes/.hermes/profiles/wiki/state/afterearnings_latest.json")
INBOX_DIR = Path("/vault/Inbox")
UA = "Mozilla/5.0 (compatible; theduyvault-wiki-ingest/1.0)"


def slugify(text: str, max_len: int = 80) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return (text or "afterearnings-transcript")[:max_len].strip("-") or "afterearnings-transcript"


def yaml_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def clean_text(el) -> str:
    text = el.get_text("\n")
    lines = [ln.strip() for ln in text.splitlines()]
    out = []
    blank = False
    for ln in lines:
        if not ln:
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(ln)
            blank = False
    text = "\n".join(out).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def latest_post() -> tuple[str, str]:
    r = requests.get(BLOG_URL, timeout=30, headers={"User-Agent": UA})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        title = " ".join(a.get_text(" ", strip=True).split())
        if not title or title.lower() == "view more":
            continue
        if "/blog/" in href and href.rstrip("/") not in {"/blog", BLOG_URL.rstrip("/")}:
            return title, urljoin(BLOG_URL, href)
    raise RuntimeError("No After Earnings transcript link found on blog page")


def extract_post(url: str) -> dict[str, str]:
    r = requests.get(url, timeout=30, headers={"User-Agent": UA})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    title = ""
    if soup.find("h1"):
        title = soup.find("h1").get_text(" ", strip=True)
    title = title or (soup.title.string.strip() if soup.title and soup.title.string else "After Earnings Transcript")
    desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        desc = meta["content"].strip()
    body_el = soup.select_one(".blog-post") or soup.select_one("article") or soup.select_one("main")
    if body_el is None:
        raise RuntimeError("No transcript body found on post page")
    body = clean_text(body_el)
    date = ""
    m = re.search(r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}", body)
    if m:
        date = m.group(0)
    return {"title": title, "description": desc, "body": body, "date": date}


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for i in range(2, 1000):
        candidate = path.with_name(f"{path.stem}-{i}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not allocate unique path for {path}")


def main() -> int:
    title, url = latest_post()
    state = {}
    if STATE_PATH.exists():
        try:
            state = json.loads(STATE_PATH.read_text())
        except Exception:
            state = {}
    if state.get("latest_url") == url:
        return 0

    post = extract_post(url)
    fingerprint = hashlib.sha256((url + "\n" + post["body"][:2000]).encode()).hexdigest()[:16]
    if state.get("latest_fingerprint") == fingerprint:
        return 0

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    path = unique_path(INBOX_DIR / f"{stamp}-afterearnings-{slugify(post['title'])}.md")
    captured_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    md = "\n".join([
        "---",
        "type: transcript",
        "source: " + yaml_quote(url),
        "site: " + yaml_quote("After Earnings"),
        "captured: " + yaml_quote(captured_at),
        "published: " + yaml_quote(post.get("date", "")),
        "---",
        "",
        "# " + post["title"],
        "",
        "Source: " + url,
        "",
        "## Description",
        "",
        post.get("description", ""),
        "",
        "## Transcript",
        "",
        post["body"],
        "",
    ])
    path.write_text(md, encoding="utf-8")
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({
        "latest_url": url,
        "latest_title": post["title"],
        "latest_fingerprint": fingerprint,
        "captured_at": captured_at,
        "inbox_path": str(path),
    }, indent=2) + "\n")
    print(f"Captured latest After Earnings transcript: {post['title']} -> {path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"After Earnings capture failed: {type(e).__name__}: {e}", file=sys.stderr)
        raise
