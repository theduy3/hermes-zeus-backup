# Profile watchdog polling-conflict false positives

## When this applies

A script-only profile gateway watchdog reports profiles as broken with:

```text
Hermes profile watchdog found issues:
- <profile>: current startup log issue: polling conflict
```

but live gateway status shows the profile is running, `HERMES_HOME` is profile-scoped, token hashes are unique, Telegram `getMe` works, and webhook state is empty.

## Durable lesson

A single Telegram `polling conflict (1/5)` can be a transient long-poll handoff after restart or network recovery. If it remains in the latest startup log window, a naive watchdog that matches any `polling conflict` will keep alerting forever even after the profile recovered.

## Verification checklist

Before changing tokens or restarting everything:

1. Check `hermes -p <profile> gateway status`.
2. Inspect the live process environment via `/proc/<pid>/environ`; profile gateways must have `HERMES_HOME=/home/hermes/.hermes/profiles/<profile>`.
3. Compare redacted token hashes across profiles; they must be unique.
4. Validate suspect tokens with Telegram `getMe` without printing tokens.
5. Check `getWebhookInfo`; polling profiles should have `url=''` and no pending webhook conflict.
6. Inspect the latest startup window, not the entire historical log.

## Watchdog rule

For `polling conflict`, alert only when it is current or persistent:

- recent timestamped conflict, e.g. within ~20 minutes, or
- repeated conflicts in the current startup window, e.g. 3+ matching lines.

Ignore old one-off conflicts and untimestamped duplicate console lines by themselves.

## Related pitfall

Do not classify `Could not parse your authentication token` or `auth is missing access_token` as gateway startup issues just because they appear in `gateway.log`. When nearby lines mention cron/model provider execution, track them under cron/model auth health instead of profile gateway health.
