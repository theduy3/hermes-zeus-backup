# Newsletter IMAP ingestion

Use this when the user wants newsletters sent to a mailbox to become vault knowledge.

## Durable facts from setup

- Dedicated newsletter mailbox: `theduy.newsletter@gmail.com`.
- Preferred credential method: Gmail app password (16-character password created at <https://myaccount.google.com/apppasswords> after enabling 2FA).

## Why not the Hermes Email Gateway for newsletters

The Email Gateway adapter is designed for email conversations with the agent. It intentionally filters many automated/bulk messages, including common newsletter signals such as:

- `List-Unsubscribe`
- `Precedence: bulk`
- noreply / no-reply / mailer-daemon style senders
- auto-submitted headers

For newsletters, use a mailbox poller/capture job instead of relying on gateway delivery.

## Recommended workflow

1. Connect to Gmail over IMAP with:
   - host: `imap.gmail.com`
   - port: `993`
   - SSL/TLS enabled
   - login: `theduy.newsletter@gmail.com`
   - password: Gmail app password, not the Google account password
2. Poll `UNSEEN` messages periodically (for example every 10–15 minutes).
3. For each new message, extract:
   - From / sender
   - Subject
   - Date
   - Message-ID when available
   - Plain-text body, or stripped HTML body if HTML-only
   - Source URLs from the message body where useful
4. Write a timestamped Markdown source under `/vault/Inbox/`, for example:
   `Inbox/YYYY-MM-DD-HHMM-newsletter-<sender-or-subject-slug>.md`.
5. Include frontmatter/provenance and then the body, e.g.:

```markdown
---
type: newsletter
source: email
author: "Sender Name <sender@example.com>"
received: YYYY-MM-DDTHH:MM:SSZ
message_id: "<...>"
---

# Subject line

Original body text...
```

6. Run `wiki-ingest` normally.
7. Mark the email as seen only after the Markdown source was successfully written. If capture or ingest fails, leave it unseen or label it for retry rather than losing the source.

## Setup and verification pattern

Use the support script `scripts/newsletter_imap_capture.py` as a starting point for the profile-level cron script. Install it under the profile scripts directory, for example:

```bash
mkdir -p ~/.hermes/profiles/wiki/scripts
cp <skill-dir>/scripts/newsletter_imap_capture.py ~/.hermes/profiles/wiki/scripts/newsletter_imap_capture.py
```

Store credentials in the active profile `.env` using shell-safe quoting for values with spaces:

```bash
NEWSLETTER_EMAIL_ADDRESS=theduy.newsletter@gmail.com
NEWSLETTER_EMAIL_PASSWORD='xxxx xxxx xxxx xxxx'
NEWSLETTER_IMAP_HOST=imap.gmail.com
NEWSLETTER_IMAP_PORT=993
```

Then set restrictive permissions:

```bash
chmod 600 ~/.hermes/profiles/wiki/.env
```

Verify IMAP before scheduling. Gmail app passwords work either with spaces or with the spaces removed, but the value in `.env` must be quoted if spaces are present. If auth fails, test both forms directly against IMAP before asking for another password:

```python
import imaplib
email = "theduy.newsletter@gmail.com"
for label, password in [("with-spaces", pw), ("no-spaces", pw.replace(" ", ""))]:
    try:
        m = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=20)
        m.login(email, password)
        print(label, "OK")
        m.logout()
    except Exception as e:
        print(label, "FAILED", e)
```

Create a silent no-agent cron job so empty polls send nothing:

```text
schedule: every 15m
script: newsletter_imap_capture.py
no_agent: true
```

Run it once after creation and confirm it succeeds.

## Filtering setup noise

A brand-new Gmail mailbox often contains Google account/security notices (`Security alert`, `2-Step Verification turned on`, `Finish setting up your new Google Account`, welcome messages). Do not ingest these as wiki knowledge. Either filter them in the capture script and mark them seen, or move any already-captured setup emails out of `/vault/Inbox/` before the next `wiki-ingest` run.

## Pitfalls

- Do not store or hardcode the app password in a skill. Put it in the profile `.env` or another secret store.
- Do not use the user's personal inbox for this workflow unless explicitly asked; the dedicated newsletter mailbox avoids privacy leakage and accidental ingestion.
- Do not mark messages seen before the Inbox source exists.
- Do not fabricate article content from subject lines alone. If a newsletter contains only links/snippets, archive what was actually present and let later web extraction happen from the captured URLs if available.
- If `/vault/Sources` is root-owned, do not move setup-noise captures there; use an allowed writable vault folder such as `/vault/System/<setup-folder>/` only to keep them out of Inbox, and report the permission issue when relevant.
