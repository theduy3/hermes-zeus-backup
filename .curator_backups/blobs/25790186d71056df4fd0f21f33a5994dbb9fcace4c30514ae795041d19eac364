# fail2ban banaction: iptables vs firewalld (RHEL/Alma + Tailscale)

## Symptom

- `systemctl is-active fail2ban` → active; log says `Server ready`
- `fail2ban-client status sshd` lists Banned IPs
- `/var/log/fail2ban.log` on ban/restore:
  - `FirewallD is not running`
  - action `firewallcmd-rich-rules`
  - `Error banning <ip>`
- `iptables -L f2b-sshd -n` missing or empty of real bans

## Cause

EPEL `fail2ban` often pulls `fail2ban-firewalld` + `firewalld`. Default banaction becomes firewalld rich rules. On Hermes/Bluehost hosts that use raw iptables + Tailscale (`ts-input`), firewalld should stay **masked**. Masked firewalld → every fail2ban ban is a no-op even though the jail looks healthy.

## Fix (verified on hal-server-803171, 2026-08-21)

```bash
cat > /etc/fail2ban/jail.d/00-iptables.conf <<'EOF'
[DEFAULT]
banaction = iptables-multiport
banaction_allports = iptables-allports
EOF

cat > /etc/fail2ban/jail.d/sshd.local <<'EOF'
[sshd]
enabled  = true
backend  = systemd
maxretry = 3
findtime = 10m
bantime  = 1h
banaction = iptables-multiport
EOF

rm -f /etc/fail2ban/jail.d/00-firewalld.conf
systemctl restart fail2ban
sleep 2
fail2ban-client ping
fail2ban-client set sshd banip 203.0.113.1
iptables -L f2b-sshd -n -v
fail2ban-client set sshd unbanip 203.0.113.1
iptables-save > /etc/sysconfig/iptables
```

## Proof bar

- `pong`
- test IP appears under chain `f2b-sshd` as REJECT/DROP
- unban removes it
- no new `FirewallD is not running` lines after restart

Jail DB "Currently banned: N" alone is **not** proof the packet path works.

## Related

- Mask firewalld when inactive after fail2ban install: `systemctl disable --now firewalld; systemctl mask firewalld`
- Re-save iptables after `iptables-services` install (RPM may drop `iptables.rpmnew`)
- Full incident: `references/bluehost-almalinux-ssh-incident.md`
