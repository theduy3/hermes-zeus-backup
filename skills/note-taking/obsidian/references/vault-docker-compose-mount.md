# Vault Bind Mounts for docker-compose.yml

Add these under the `gateway` service's `volumes:` key so cron workers (spawned as separate containers from the same image) inherit vault access.

```yaml
services:
  gateway:
    volumes:
      - ~/.hermes:/opt/data
      # Obsidian vault — 9 subdirectory bind mounts (read-only from host)
      - /root/theduyvault/Tasks:/vault/Tasks:ro
      - /root/theduyvault/Notes:/vault/Notes:ro
      - /root/theduyvault/Inbox:/vault/Inbox:ro
      - /root/theduyvault/Daily:/vault/Daily:ro
      - /root/theduyvault/Projects:/vault/Projects:ro
      - /root/theduyvault/Attachments:/vault/Attachments:ro
      - /root/theduyvault/Templates:/vault/Templates:ro
      - /root/theduyvault/Sources:/vault/Sources:ro
      - /root/theduyvault/MOCs:/vault/MOCs:ro
```

After updating, recreate:
```bash
cd /root/hermes-agent
docker compose down && docker compose up -d
```

**Why individual subdirectory mounts?** The host path `/root/theduyvault` is inside `/root` (mode `0700`). Mounting the top-level directory would require `chmod o+x /root` which weakens host security. Individual subdirectory mounts bypass this — Docker bind-mounts resolve at the host kernel level, not through the directory tree, so `hermes` UID 1500 can access `/vault/Tasks` directly without needing `x` on `/root`.

**Why read-only?** The vault syncs from the user's MacBook. Writes from the VPS container would create sync conflicts. The obsidian skill is read-only in container environments — create/update notes from the Mac Hermes session instead.

## Alternative: direct partition mount (rw)

Some VPS deployments use a direct ext4 partition mount instead of bind mounts:

```bash
# mount example
/dev/sda1[/root/theduyvault] on /vault type ext4 (rw,relatime,discard,errors=remount-ro)
```

With this pattern the entire vault is writable (`rw`). Agents write to `/vault/Inbox/` as the capture zone — the Obsidian wiki pipeline ingests from Inbox later. Always test writability first (`touch /vault/Inbox/.test`) before relying on it.
