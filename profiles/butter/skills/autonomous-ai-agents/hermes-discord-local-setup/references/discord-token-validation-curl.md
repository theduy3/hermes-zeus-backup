# Discord Token Validation: curl vs Python urllib

## The pitfall

Python's `urllib.request` can return **false-negative HTTP 403 with error code 1010** for valid Discord bot tokens. The token works fine with curl and the Discord gateway, but Python reports it as rejected.

## Reproduction

```python
import json, urllib.request
tok = "MTUwMzk4MzE2NzI4MTgyMzgyNA.G51H_x.6gJyJML03O_HRqqwCaXDBQTtfAPv217qEiUUdY"
req = urllib.request.Request("https://discord.com/api/v10/users/@me",
    headers={"Authorization": f"Bot {tok}"})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.load(r)
    print(data["username"])  # Would work
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()}")
    # Returns: HTTP 403: error code: 1010  (FALSE NEGATIVE)
```

## The fix

Always use `curl` for Discord token validation:

```bash
curl -s -H "Authorization: Bot <TOKEN>" "https://discord.com/api/v10/users/@me"
```

Valid response includes: `{"id":"...","username":"...","bot":true,...}`

## Why

Discord's API appears to behave differently depending on the TLS/client fingerprint when certain tokens are involved. `curl` (linked against macOS Security framework) succeeds where Python's `ssl` module (OpenSSL-based) gets rejected. This has been observed consistently across multiple bot tokens on macOS.
