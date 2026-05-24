#!/usr/bin/env python3
"""Refresh Strava OAuth token, cache it, print current active token as JSON.

Usage: python3 strava_refresh.py
Output: JSON with access_token and expires_at on stdout.
Side effects: updates secrets/strava.json and cache/strava_active.json.

Requires secrets file at ~/.hermes/profiles/thor/secrets/strava.json:
{"client_id":"...","client_secret":"...","refresh_token":"..."}

First-time setup: user must authorize at strava.com/oauth/authorize,
then exchange the code for a refresh token via POST /oauth/token.
"""
import json, os, sys, urllib.request, urllib.parse

SECRETS = os.path.expanduser("~/.hermes/profiles/thor/secrets/strava.json")
CACHE = os.path.expanduser("~/.hermes/profiles/thor/cache/strava_active.json")
os.makedirs(os.path.dirname(CACHE), exist_ok=True)

with open(SECRETS) as f:
    cfg = json.load(f)

# Try cached token first (with 60s buffer)
if os.path.exists(CACHE):
    with open(CACHE) as f:
        tok = json.load(f)
    if tok.get("expires_at", 0) > __import__("time").time() + 60:
        print(json.dumps(tok))
        sys.exit(0)

# Refresh via Strava OAuth
data = urllib.parse.urlencode({
    "client_id": cfg["client_id"],
    "client_secret": cfg["client_secret"],
    "grant_type": "refresh_token",
    "refresh_token": cfg["refresh_token"]
}).encode()

req = urllib.request.Request("https://www.strava.com/oauth/token", data=data)
with urllib.request.urlopen(req) as r:
    tok = json.loads(r.read())

# Update secrets file with new tokens
cfg["access_token"] = tok["access_token"]
cfg["refresh_token"] = tok.get("refresh_token", cfg["refresh_token"])
cfg["expires_at"] = tok["expires_at"]
with open(SECRETS, "w") as f:
    json.dump(cfg, f, indent=2)

# Cache active token
with open(CACHE, "w") as f:
    json.dump({"access_token": tok["access_token"], "expires_at": tok["expires_at"]}, f)

print(json.dumps(tok))
