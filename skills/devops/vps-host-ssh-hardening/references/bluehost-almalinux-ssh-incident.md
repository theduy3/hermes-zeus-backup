# Bluehost AlmaLinux SSH brute-force incident (hal-server)

## Context

- Host: `hal-server-803171` (Alma/RHEL 9 family, `dnf`, `/var/log/secure`)
- Hermes: Docker container `hermes`, volume `hermes_hermes-data` → `/home/hermes/.hermes`
- User SSH alias: `bluehost` from Mac; normal source IP pattern `64.46.26.208`
- Tailscale present (`ts-input` chain); no firewalld/ufw preinstalled

## What "231 failed attempts" meant

- Failed password/auth noise from internet scanners, not proof of breach.
- Breach test = `Accepted` lines + key inventory, not failure counts.
- Log scale can be huge (example: ~18k `Failed password` lines; top sources 176.53.159.197/198 at 2.6k each).

## Successful login inventory (clean pattern)

- Dominant: `Accepted publickey for root from 64.46.26.208` key `SHA256:a2gSGJyaNmh4pbh7IBUFCb9dGGFtfyWbkJrW5uZi3b8` (comment `duynt1989@gmail.com`)
- Secondary: `147.93.116.94` key `SHA256:VnuLapVKcqjAnED+f0yYV/5UkLJ+B01V46PorIA3OFQ` (comment `root@srv1300679` — prior Hermes/Paperclip VPS)
- No password Accepts in the reviewed window → brute force not successful

## authorized_keys fingerprints seen

| Comment | Fingerprint | Notes |
|---------|-------------|--------|
| duynt1989@gmail.com | a2gSGJ… | Mac — keep |
| root@srv1300679 | VnuLap… | Old VPS — keep if still used |
| access@hal | KDk27Y… | Confirm with user |
| (no comment), duplicated | UFSLOks… | Confirm or remove after user OK |

## Dead ends

- `echo 'sshd: IP' >> /etc/hosts.deny` — **ignored** (`ldd $(which sshd)` has no libwrap)
- `firewall-cmd` / `ufw` — not installed on minimal image
- Agent path `/home/hermes/.hermes/projects/...` — **missing on host**; use `docker cp hermes:/home/hermes/.hermes/projects/bluehost-ssh-harden.sh /root/`

## What worked

1. `iptables -I INPUT -s <ip> -j DROP` (immediate)
2. fail2ban install + jail `sshd` (banned scanners within minutes)
3. Drop-in `/etc/ssh/sshd_config.d/00-hardening.conf` + neutralize other PasswordAuthentication lines + `sshd -T` verify
4. `iptables-save > /etc/sysconfig/iptables` + plan `iptables-services` for reboot

## Script bug (do not repeat)

First harden script used over-escaped stream-edit patterns against `sshd_config`, printed "password auth DISABLED", restarted sshd, but effective config stayed:

```text
permitrootlogin yes
passwordauthentication yes
```

Always gate success on `sshd -T`, not on script echo. Prefer drop-in + neutralize + `sshd -T` over in-place stream edits of the main file alone.

## Side effect

`dnf install fail2ban` pulled `firewalld` (enabled but inactive). Mask/disable if not intentionally used so next reboot does not replace the iptables/Tailscale path.

## User interaction lesson

User repeatedly pasted assistant prose (`show installed keys…`, `then run the fixed script:`) into bash. Deliver **only** executable lines inside copy fences.
