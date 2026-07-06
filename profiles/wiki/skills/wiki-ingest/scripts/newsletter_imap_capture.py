#!/usr/bin/env python3
"""Capture unseen newsletter emails from Gmail IMAP into /vault/Inbox.

Template/support script for the wiki-ingest newsletter IMAP workflow.
Copy into the profile scripts directory and configure NEWSLETTER_* keys in the
active profile .env. Prints nothing when there are no new messages, so it is
safe for cron no_agent=True. Marks messages seen only after the Inbox Markdown
file is written successfully.
"""
from __future__ import annotations

import email
import imaplib
import os
import re
import shlex
import sys
from datetime import datetime, timezone
from email.message import Message
from email.policy import default
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path

ENV_PATH = Path(os.environ.get("HERMES_PROFILE_ENV", "/home/hermes/.hermes/profiles/wiki/.env"))
INBOX_DIR = Path(os.environ.get("NEWSLETTER_CAPTURE_INBOX", "/vault/Inbox"))


def load_env(path: Path) -> dict[str, str]:
    env = dict(os.environ)
    if not path.exists():
        return env
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        try:
            parts = shlex.split(val, posix=True)
            val = parts[0] if parts else ""
        except ValueError:
            val = val.strip().strip('"').strip("'")
        env[key.strip()] = val
    return env


class HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in {"script", "style", "noscript"}:
            self.skip += 1
        if tag in {"p", "br", "div", "li", "tr", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.parts.append(f" [link: {href}] ")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in {"script", "style", "noscript"} and self.skip:
            self.skip -= 1
        if tag in {"p", "div", "li", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

    def text(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def html_to_text(html: str) -> str:
    parser = HTMLTextExtractor()
    parser.feed(html)
    return parser.text()


def decode_part(part: Message) -> str:
    payload = part.get_payload(decode=True)
    if payload is None:
        raw = part.get_payload()
        return raw if isinstance(raw, str) else ""
    charset = part.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def extract_body(msg: Message) -> tuple[str, str]:
    plain: list[str] = []
    html: list[str] = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = (part.get("Content-Disposition") or "").lower()
            if "attachment" in disp:
                continue
            if ctype == "text/plain":
                plain.append(decode_part(part))
            elif ctype == "text/html":
                html.append(decode_part(part))
    else:
        if msg.get_content_type() == "text/html":
            html.append(decode_part(msg))
        else:
            plain.append(decode_part(msg))
    if "\n".join(plain).strip():
        return "plain", "\n\n".join(p.strip() for p in plain if p.strip()).strip()
    return "html-stripped", html_to_text("\n\n".join(html))


def header(msg: Message, name: str) -> str:
    return str(msg.get(name, "")).strip()


def yaml_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def slugify(value: str, max_len: int = 72) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (value or "newsletter")[:max_len].strip("-") or "newsletter"


def received_dt(msg: Message) -> datetime:
    raw = header(msg, "Date")
    if raw:
        try:
            dt = parsedate_to_datetime(raw)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            pass
    return datetime.now(timezone.utc)


def unique_path(base: Path) -> Path:
    if not base.exists():
        return base
    for i in range(2, 1000):
        p = base.with_name(f"{base.stem}-{i}{base.suffix}")
        if not p.exists():
            return p
    raise RuntimeError(f"could not allocate unique path for {base}")


def should_ignore_setup_mail(from_: str, subject: str) -> bool:
    """Skip mailbox administration/security notices, not newsletters."""
    f = from_.lower()
    s = subject.lower()
    google_sender = "google" in f or "accounts.google.com" in f or "no-reply@accounts.google.com" in f
    setup_subject = any(
        needle in s
        for needle in [
            "security alert",
            "2-step verification",
            "finish setting up your new google account",
            "welcome to",
        ]
    )
    return google_sender and setup_subject


def main() -> int:
    env = load_env(ENV_PATH)
    addr = env.get("NEWSLETTER_EMAIL_ADDRESS")
    pw = env.get("NEWSLETTER_EMAIL_PASSWORD")
    host = env.get("NEWSLETTER_IMAP_HOST", "imap.gmail.com")
    port = int(env.get("NEWSLETTER_IMAP_PORT", "993"))
    if not addr or not pw:
        print("Newsletter IMAP capture not configured: missing NEWSLETTER_EMAIL_ADDRESS or NEWSLETTER_EMAIL_PASSWORD", file=sys.stderr)
        return 2

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    captured: list[str] = []
    with imaplib.IMAP4_SSL(host, port, timeout=30) as imap:
        imap.login(addr, pw)
        imap.select("INBOX")
        typ, data = imap.search(None, "UNSEEN")
        if typ != "OK":
            raise RuntimeError(f"IMAP search failed: {typ} {data}")
        for msg_id in (data[0].split() if data and data[0] else []):
            typ, fetch_data = imap.fetch(msg_id, "(RFC822)")
            if typ != "OK" or not fetch_data:
                continue
            raw_msg = next((item[1] for item in fetch_data if isinstance(item, tuple)), None)
            if not raw_msg:
                continue
            msg = email.message_from_bytes(raw_msg, policy=default)
            subject = header(msg, "Subject") or "Untitled Newsletter"
            from_ = header(msg, "From") or "Unknown sender"
            if should_ignore_setup_mail(from_, subject):
                imap.store(msg_id, "+FLAGS", "\\Seen")
                continue
            to = header(msg, "To")
            message_id = header(msg, "Message-ID")
            received_iso = received_dt(msg).isoformat().replace("+00:00", "Z")
            body_kind, body = extract_body(msg)
            body = body.strip() or "(No readable text body extracted.)"
            stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
            path = unique_path(INBOX_DIR / f"{stamp}-newsletter-{slugify(subject or from_)}.md")
            md = "\n".join([
                "---",
                "type: newsletter",
                "source: email",
                f"mailbox: {yaml_quote(addr)}",
                f"author: {yaml_quote(from_)}",
                f"to: {yaml_quote(to)}",
                f"received: {yaml_quote(received_iso)}",
                f"message_id: {yaml_quote(message_id)}",
                f"body_format: {yaml_quote(body_kind)}",
                "---",
                "",
                f"# {subject}",
                "",
                f"- From: {from_}",
                f"- To: {to}",
                f"- Received: {received_iso}",
                f"- Message-ID: `{message_id}`",
                "",
                "## Body",
                "",
                body,
                "",
            ])
            path.write_text(md, encoding="utf-8")
            imap.store(msg_id, "+FLAGS", "\\Seen")
            captured.append(str(path))
        imap.logout()
    if captured:
        print("Captured newsletter email(s) to /vault/Inbox:")
        for p in captured:
            print(f"- {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
