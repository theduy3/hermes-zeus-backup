# CallMeBot voice-call endpoints — verified live 2026-08-21

## Telegram in-app voice call (no key)
`https://api.callmebot.com/start.php`
Params (GET, URL-encoded):
- `source=hermes` (any tag)
- `user=@yourusername` — your Telegram @username (or `+CCphonenumber`)
- `text=<message to speak>`
- `lang=<Voice Name>`, e.g. `en-US-Standard-B`, `en-GB-Standard-A`
No API key. Requires one-time authorization of @CallMeBot to contact the @username.
Activation: https://api2.callmebot.com/txt/auth.php  (or message @CallMeBot / @CallMeBot_API)

## Real PSTN phone call (needs key)
`https://api.callmebot.com/call.php`
Params (GET, URL-encoded):
- `phone=+CCphonenumber` (e.g. +16045551234)
- `text=<message to speak>`
- `lang=<Voice Name>`
- `key=<APIkey>` — get from @CallMeBot_phone bot (one-time)
Probe with a bogus key returns "Wrong APIkey" → confirms endpoint is correct.

## Notes
- Voices: Standard only (Wavenet/premium unsupported). Full list on CallMeBot site.
- Free tier is fair-use (handful of calls/day, short cooldown between same-user calls).
- `web_search`/`web_extract` are unavailable here (no FIRECRAWL_API_KEY); the
  callmebot.com DOC URLs often 404, but the API endpoints above are stable —
  verify endpoints by `curl` probing the live API, not by scraping docs.
- A "not authorized" response for the Telegram mode is expected until the
  one-time @username authorization is completed; it is not a bug.
