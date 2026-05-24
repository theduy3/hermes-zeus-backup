# Common Vault Write Errors in Docker Containers

## Error: /root is 0700 (traversal denied)

```
ls: cannot open directory '/root/': Permission denied
chmod: changing permissions of '/root': Operation not permitted
```

**What it means:** `/root` is `drwx------`, the `hermes` user (uid 1500) cannot traverse it.
**Fix runs on:** VPS host (as root)
**Fix command:** `chmod o+x /root`
**Agent action:** Report error + required fix. Do NOT attempt chmod/setfacl — they will fail.

## Error: /vault/ bind mount is read-only

```
/usr/bin/bash: line N: /vault/Notes/...: Read-only file system
```

**What it means:** The vault subdirectories are mounted `ro` from `/dev/sda1`.
**Check:** `mount | grep vault` — look for `(ro,...)` in the mount options.
**Fix runs on:** VPS host
**Fix:** Change bind mount to `rw` in `docker-compose.yml`, OR use the `/root/theduyvault` path instead (after fixing /root permissions).
**Agent action:** Report error. Do NOT attempt to remount — container lacks privileges.

## Error: /root/theduyvault path missing (combined failure)

```
Checking: /root/theduyvault
  missing
  not writable
```

Combined with `/root` being 0700: the directory can't even be checked for existence because traversal is blocked. Both `/root` and `/root/theduyvault` errors must be fixed together on the host.

## Agent workflow when writes fail

1. Check both paths (`/vault/` and `/root/theduyvault/`)
2. Identify which error pattern(s) match
3. Write note content to `/home/hermes/<descriptive-name>.md` as fallback
4. Report: exact error messages, which host-level fix is needed, and the fallback file path
5. Do NOT claim success — the note was not written to the vault
