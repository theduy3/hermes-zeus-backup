# Google Calendar sync for Catthew briefings

Session-derived workflow for connecting Catthew to a family Google Calendar.

## Preferred OAuth path

1. Ask for a Desktop OAuth client JSON, or have Sir upload the JSON in Telegram if the local macOS path is not reachable from the Linux container.
2. Save it with the Google Workspace setup script:
   ```bash
   python3 /home/hermes/.hermes/profiles/catthew/skills/productivity/google-workspace/scripts/setup.py --client-secret /path/to/client_secret.json
   ```
3. If the consent app is in Testing and Google returns `access_denied`, tell Sir to add `duynt1989@gmail.com` under Google Cloud Console → OAuth consent screen / Audience → Test users.
4. For Catthew morning briefings, prefer **calendar read-only** scope first. Full Workspace scopes can make Google consent slow or fail for this lightweight use case.
5. If the helper script only emits the full-scope URL, generate a read-only URL manually with `google_auth_oauthlib.flow.Flow` using:
   - scope: `https://www.googleapis.com/auth/calendar.readonly`
   - redirect_uri: preferably the exact redirect in the JSON, commonly `http://localhost`; if that fails try `http://localhost:1`.
   - persist `state`, `code_verifier`, and `redirect_uri` to `/home/hermes/.hermes/profiles/catthew/google_oauth_pending.json` so `setup.py --auth-code` can exchange the code.
6. Tell Sir to open the auth URL in **Safari/Chrome directly**, not Telegram’s in-app browser.
7. Sir should paste the full redirect URL, e.g. `http://localhost/?state=...&code=...&scope=https://www.googleapis.com/auth/calendar.readonly`.
8. Exchange and verify:
   ```bash
   python3 /home/hermes/.hermes/profiles/catthew/skills/productivity/google-workspace/scripts/setup.py --auth-code 'FULL_REDIRECT_URL'
   python3 /home/hermes/.hermes/profiles/catthew/skills/productivity/google-workspace/scripts/setup.py --check-live
   ```

## Consent pitfalls

- Warning “Google hasn’t verified this app” is expected for Testing apps. Sir must choose Advanced / continue to the app if shown.
- If consent spins or returns Google 500, reduce scope to calendar read-only and use the JSON’s exact `redirect_uri` (`http://localhost` worked in-session where `http://localhost:1` caused issues).
- If the address bar shows only `http://localhost/?code=` with no code value, treat it as failed and generate a fresh auth URL.

## Fallback: iCal URL

If OAuth remains blocked, ask Sir for Google Calendar → Settings → Integrate calendar → **Secret address in iCal format**. This gives read-only calendar access for briefings without OAuth.
