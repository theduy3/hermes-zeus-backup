# Profile Codex auth repair

Use when a Hermes profile can receive gateway/cron messages but model calls fail with:

```text
RuntimeError: Codex auth is missing access_token. Run `hermes auth` to re-authenticate. Run `hermes model` to re-authenticate.
```

## Pattern

A profile-specific `auth.json` may show an OpenAI Codex credential in `hermes -p <profile> auth list`, but the runtime still fails because the stored provider/token shape is stale, missing `access_token`, or has suppressed/legacy state. If another profile is known to work, replacing the affected profile auth file from the working profile is faster and safer than trying to hand-edit token internals.

## Safe repair recipe

```bash
PROFILE=catthew
JOB_ID=c729ba85e251
TS=$(date -u +%Y%m%dT%H%M%SZ)
SRC="$HOME/.hermes/auth.json"                         # known-working baseline
DST="$HOME/.hermes/profiles/$PROFILE/auth.json"

# Inspect without printing secrets
hermes auth list openai-codex
hermes -p "$PROFILE" auth list openai-codex
hermes -p "$PROFILE" cron list

# Backup and replace
cp "$DST" "$DST.bak.$TS"
cp "$SRC" "$DST"
chmod 600 "$DST"

# Verify profile model auth
hermes -p "$PROFILE" chat -q 'Reply exactly OK' --toolsets '' -Q

# Verify original cron path
hermes -p "$PROFILE" cron run "$JOB_ID"
sleep 75
hermes -p "$PROFILE" cron list | sed -n "/$JOB_ID/,/^$/p"
```

Expected verification:

- `hermes -p <profile> chat ...` prints `OK`.
- The failing cron job's `Last run` changes from the auth RuntimeError to `ok`.

## Pitfalls

- Do not print raw `auth.json` or token values in chat output.
- Always backup the profile `auth.json` before replacement.
- Verify both model auth and the original cron job; a successful `auth list` alone is not enough.
- Treat this as a credential-state repair, not a permanent claim that Codex or the profile is broken.
