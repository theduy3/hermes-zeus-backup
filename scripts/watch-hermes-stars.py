#!/usr/bin/env python3
"""Zero-token GitHub star watcher for Hermes cron.

Prints nothing unless the watched repository's stargazer count changes.
Designed for cronjob no_agent=True so quiet runs use zero LLM tokens.
"""
import json
import os
import sys
import tempfile
import urllib.request

REPO = "NousResearch/hermes-agent"
STATE = os.path.expanduser("~/.hermes/scripts/.watch-hermes-stars-state.json")
USER_AGENT = "hermes-zero-token-star-watcher"


def fetch_stars() -> int:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}",
        headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return int(data["stargazers_count"])


def load_prev():
    try:
        with open(STATE, "r", encoding="utf-8") as f:
            return json.load(f).get("count")
    except FileNotFoundError:
        return None


def save_curr(count: int) -> None:
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".watch-stars-", dir=os.path.dirname(STATE), text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"repo": REPO, "count": count}, f)
            f.write("\n")
        os.replace(tmp, STATE)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main() -> int:
    prev = load_prev()
    curr = fetch_stars()
    save_curr(curr)

    # Initial baseline and no-change runs stay silent.
    if prev is None or curr == prev:
        return 0

    delta = curr - int(prev)
    sign = "+" if delta > 0 else ""
    print(f"GitHub stars changed for {REPO}: {prev} → {curr} ({sign}{delta})")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"watch-hermes-stars error: {e}", file=sys.stderr)
        raise
