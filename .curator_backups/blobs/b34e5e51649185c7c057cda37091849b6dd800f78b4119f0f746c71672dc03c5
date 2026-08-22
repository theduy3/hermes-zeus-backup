---
name: vps-host-ssh-hardening
description: "Use when hardening SSH/brute-force on RHEL/Alma VPS hosts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ssh, security, vps, iptables, fail2ban, bluehost, almalinux, hardening]
    related_skills: [hermes-operations-troubleshooting, hermes-github-backup-restore]
---

# VPS Host SSH Hardening

## Overview

Respond to SSH brute-force and harden OpenSSH on minimal RHEL/Alma/CentOS-style VPS images (Bluehost KVM and similar) where Hermes often runs in Docker. Prefer packet-level blocks + key-only auth + fail2ban. Never trust a script's "Applied" line without reading effective `sshd -T`.

## When to Use

- User pastes `Last failed login` / N failed attempts since last successful login
- Active scanners on `/var/log/secure`, password auth still on, or root SSH exposed
- Need a ready-to-run harden script or clean root copy-paste blocks for the host
- Hermes lives in Docker on the same box and host paths differ from container paths

## User delivery rules (critical)

1. **Commands-only blocks.** Put runnable shell in fenced blocks with zero prose labels inside the fence. Do not prefix with `bash`, section titles, or "then run…". The user pastes whole blocks into root shells; narrative inside the fence becomes syntax errors.
2. **One block = one paste.** Keep verification, fix, and second-window test as separate blocks.
3. **Terse status outside fences.** Short verdict + what to paste next. No long essays between commands unless they ask.
4. You usually **cannot** run host-root commands from the Hermes container. Ship artifacts + exact host commands; use `docker cp` when the script lives in the Hermes volume.

## Compromise triage (before hardening)

Run on the host as root (give as a clean block):

```bash
grep -E "Accepted (publickey|password)" /var/log/secure | tail -20
awk -F: '$3>=1000 && $3<65534 {print $1, $3}' /etc/passwd
ldd $(which sshd) | grep -i wrap || echo "NO libwrap — hosts.deny is ignored"
ls -la /etc/cron.d/ /var/spool/cron/
while read -r line; do
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  printf '%s  ' "$(echo "$line" | awk '{print $NF}')"
  echo "$line" | ssh-keygen -lf -
done < /root/.ssh/authorized_keys
```

Interpret:

| Signal | Meaning |
|--------|---------|
| Only `Accepted publickey` for known IPs/keys | Brute force failed; not a password breach |
| Any `Accepted password` from unknown IP | Treat as compromised; rotate keys/passwords, deep audit |
| `NO libwrap` | `/etc/hosts.deny` is a no-op — do not recommend it as a block |
| Unknown `authorized_keys` fingerprints | Confirm with user before delete; remove only known-bad |

Known-good patterns on this user's fleet (confirm still true in-session): Mac key comment `duynt1989@gmail.com`; old VPS key `root@srv1300679`. Do not auto-delete `access@hal` or uncommented keys without asking.

## Hardening workflow

1. **Immediate DROP** of the active attacker IP with iptables (firewalld/ufw often absent):
   ```bash
   iptables -I INPUT -s ATTACKER_IP -j DROP
   iptables -L INPUT -n --line-numbers | head -20
   ```
2. **Key-only sshd via drop-in** (RHEL: first-obtained value wins; `Include sshd_config.d/*.conf` is early):
   - Write `/etc/ssh/sshd_config.d/00-hardening.conf` with `PasswordAuthentication no`, `PermitRootLogin prohibit-password`, `AuthenticationMethods publickey`, etc.
   - Comment conflicting directives in main config and other drop-ins.
   - `sshd -t && systemctl restart sshd`
   - **Mandatory verify:** `sshd -T | grep -E 'passwordauthentication|permitrootlogin|pubkeyauthentication|authenticationmethods'`
   - Expect `passwordauthentication no`. If still `yes`, the change did not stick — fix config order, do not declare success.
3. **fail2ban** jail `sshd`, `backend = systemd`, logpath `/var/log/secure` on RHEL-family.
4. **firewalld trap:** `dnf install fail2ban` may pull `firewalld` + `fail2ban-firewalld`. If firewalld was inactive, **disable and mask** it so reboot does not clobber Tailscale/iptables. Do not enable firewalld just because the package landed.
5. **Persist iptables:** `iptables-save > /etc/sysconfig/iptables`, install/enable `iptables-services` when available. A bare save file without a restore unit dies on reboot.
6. **Second window before disconnect:** from the user's Mac, `ssh host 'echo OK; sshd -T | grep passwordauthentication'`. Keep the original root session until that works.

## Hermes-on-Docker path mapping

On this topology the Hermes data volume is often:

- Container: `/home/hermes/.hermes`
- Host volume: `/var/lib/docker/volumes/hermes_hermes-data/_data`
- Container name: `hermes`

Script handoff from agent → host:

```bash
docker cp hermes:/home/hermes/.hermes/projects/bluehost-ssh-harden.sh /root/bluehost-ssh-harden.sh
bash /root/bluehost-ssh-harden.sh
```

Discover mounts if needed:

```bash
docker inspect hermes --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'
```

Canonical script path inside Hermes home: `~/.hermes/projects/bluehost-ssh-harden.sh` (agent-maintained). After fixing the script in the container volume, re-`docker cp` before re-run on the host.

## Script / sed pitfalls

- Do **not** drive sshd changes only with fragile `sed` on `sshd_config`. Over-escaped `\\s` patterns silently fail while the script still prints "Applied" and restarts sshd.
- Prefer drop-in `00-hardening.conf` + neutralize conflicting lines + **always** print `sshd -T` effective values in the script summary.
- Rate-limit via `iptables` `recent`/`conntrack` is best-effort; core protection is DROP list + key-only + fail2ban.
- Policy ACCEPT with explicit DROP sources is fine; do not flush Tailscale's `ts-input` chain.

## Verification checklist

- [ ] `sshd -T` shows `passwordauthentication no` and key-only root policy
- [ ] New SSH session from a second client succeeds with the user's key
- [ ] `fail2ban-client status sshd` shows jail + bans
- [ ] Attacker IPs present in `iptables -L INPUT -n`
- [ ] `/etc/sysconfig/iptables` saved and `iptables` service enabled if package exists
- [ ] `firewalld` inactive and not enabled (unless user intentionally uses it with ssh allowed)
- [ ] `authorized_keys` fingerprints reviewed with the user

## References

- `references/bluehost-almalinux-ssh-incident.md` — concrete incident pattern (brute-force counts, key inventory, fail2ban+firewalld side effect, broken sed lesson)
- Host script maintained at `~/.hermes/projects/bluehost-ssh-harden.sh` (copy to host via `docker cp`)
