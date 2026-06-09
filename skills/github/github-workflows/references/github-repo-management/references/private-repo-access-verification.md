# Private repo access verification

Use this when a repository may be private and the auth token’s exact scope is unclear.

## Pattern
1. Check who the token belongs to:
   - `curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user`
2. List repos visible to the token:
   - `curl -s -H "Authorization: token $GITHUB_TOKEN" 'https://api.github.com/user/repos?per_page=100&sort=updated'`
3. Test the actual git transport, because API visibility and git transport can differ for fine-grained PATs:
   - `git ls-remote https://x-access-token:$GITHUB_TOKEN@github.com/OWNER/REPO.git HEAD`
   - If that fails, try a full clone to confirm transport access.
4. Prefer `git ls-remote` / `git clone` over assuming `/repos/OWNER/REPO` proves access.

## Interpretation
- API `404` on `/repos/OWNER/REPO` can mean the token cannot see the repo via REST, even if git transport later works.
- `git ls-remote` `403 write access not granted` means the token is valid but lacks the needed repo permissions.
- A token may still be valid for git clone even when a direct REST repo lookup is misleading.

## Safe handling
- Never paste the token into notes or comments.
- Pass it only in-process (env var or one-shot command).
- Delete any shell history or temp files that may contain the token after use.