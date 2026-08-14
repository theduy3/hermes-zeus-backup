# Catthew Google Calendar OAuth setup notes

Use this reference when syncing Catthew household briefings with Google Calendar.

## Flow that worked

1. Load/use the `google-workspace` skill for OAuth commands, but keep Catthew-specific delivery/briefing rules in `household-task-briefings`.
2. Save the Google OAuth client JSON into the active profile with:
   ```bash
   python3 /home/hermes/.hermes/profiles/catthew/skills/productivity/google-workspace/scripts/setup.py --client-secret /path/to/client_secret.json
   ```
3. Generate an auth URL with:
   ```bash
   python3 /home/hermes/.hermes/profiles/catthew/skills/productivity/google-workspace/scripts/setup.py --auth-url
   ```
4. Send Sir the exact URL and ask him to paste the full final `http://localhost:1/?code=...` URL after approval.
5. Exchange the pasted URL/code with:
   ```bash
   python3 /home/hermes/.hermes/profiles/catthew/skills/productivity/google-workspace/scripts/setup.py --auth-code 'PASTED_URL_OR_CODE'
   ```
6. Verify before claiming success:
   ```bash
   python3 /home/hermes/.hermes/profiles/catthew/skills/productivity/google-workspace/scripts/setup.py --check
   python3 /home/hermes/.hermes/profiles/catthew/skills/productivity/google-workspace/scripts/google_api.py calendar list
   ```

## Pitfalls from this session

- A macOS path such as `/Users/theduy/Downloads/client_secret...json` may not exist inside the Linux/container runtime. If missing, ask Sir to upload the JSON document to Telegram and use the cached uploaded path.
- The current setup script in this profile may not support `--services` or `--format`; use `--auth-url` alone if those args fail.
- For testing-mode Google Cloud apps, `Error 403: access_denied` means Sir must add `duynt1989@gmail.com` as a test user in Google Cloud Console → OAuth consent screen/Audience → Test users. Then generate a fresh auth URL.
- “Google hasn’t verified this app” is expected for a testing OAuth client. Tell Sir to tap **Advanced → Go to Hermes-Catthew (unsafe)**, then continue/allow and paste the final localhost redirect.

## Catthew-specific policy

- After auth succeeds, morning briefings may include Google Calendar events relevant to Sir, Madam, and Victoria.
- Do not create calendar events without confirmation.
- Google tasks/task lists are not part of Catthew task briefings unless mirrored as `/vault/Tasks` files tagged `#catthew`.
