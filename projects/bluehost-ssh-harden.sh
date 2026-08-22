#!/usr/bin/env bash
#
# bluehost-ssh-harden.sh
# SSH brute-force remediation + hardening for RHEL/Alma/CentOS-ish hosts.
# Run as root ON THE SERVER:  bash bluehost-ssh-harden.sh
#
# SAFE: will NOT disable password auth unless ~/.ssh/authorized_keys exists
#       for the current user.
#
set -u

echo "=== SSH Hardening & Brute-force Remediation ==="
echo "Run date: $(date -u)"
echo

if [[ $EUID -ne 0 ]]; then
  echo "ERROR: must run as root." >&2
  exit 1
fi

AUTHLOG=""
for f in /var/log/secure /var/log/auth.log; do
  [[ -r "$f" ]] && { AUTHLOG="$f"; break; }
done
[[ -z "$AUTHLOG" ]] && echo "WARN: no auth log found; audit steps skipped." >&2

if command -v dnf >/dev/null 2>&1; then PM=dnf
elif command -v yum >/dev/null 2>&1; then PM=yum
elif command -v apt-get >/dev/null 2>&1; then PM=apt
else PM=unknown
fi
echo "Package manager: $PM"

echo
echo "--- [1] Recent SUCCESSFUL logins (verify these are YOU) ---"
[[ -n "$AUTHLOG" ]] && grep -E "Accepted (publickey|password)" "$AUTHLOG" | tail -n 20

echo
echo "--- [1b] Top source IPs of FAILED sshd attempts ---"
if [[ -n "$AUTHLOG" ]]; then
  grep -E "Failed password|authentication failure|Invalid user|Connection closed by authenticating" "$AUTHLOG" \
    | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" \
    | sort | uniq -c | sort -rn | head -n 25
  echo
  echo "Total 'Failed password' lines: $(grep -cE 'Failed password' "${AUTHLOG:-/dev/null}" || true)"
fi

KEY_OK=0
if [[ -s "$HOME/.ssh/authorized_keys" ]]; then
  KEY_OK=1
  echo "OK: authorized_keys present for $(whoami) -> will allow key-only auth"
else
  echo "WARN: no authorized_keys for $(whoami); password auth will be LEFT ON"
fi

# ---------------------------------------------------------------------------
# 3. Harden sshd via drop-in (RHEL: first-obtained value wins; Include is first)
# ---------------------------------------------------------------------------
SSHD_DIR=/etc/ssh/sshd_config.d
SSHD_DROPIN="${SSHD_DIR}/00-hardening.conf"
mkdir -p "$SSHD_DIR"
cp -a /etc/ssh/sshd_config "/etc/ssh/sshd_config.bak.$(date +%s)" 2>/dev/null || true
[[ -f "$SSHD_DROPIN" ]] && cp -a "$SSHD_DROPIN" "${SSHD_DROPIN}.bak.$(date +%s)"

if [[ $KEY_OK -eq 1 ]]; then
  cat > "$SSHD_DROPIN" <<'EOF'
# Managed by bluehost-ssh-harden.sh — key-only SSH
PermitRootLogin prohibit-password
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2
EOF
  echo "Wrote $SSHD_DROPIN (password auth DISABLED, key-only)."
else
  cat > "$SSHD_DROPIN" <<'EOF'
# Managed by bluehost-ssh-harden.sh — keys missing, password left enabled
PermitRootLogin yes
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2
EOF
  echo "WARN: partial hardening only; password auth LEFT ON (no authorized_keys)."
fi

# Comment out conflicting directives elsewhere so order cannot re-enable passwords.
for f in /etc/ssh/sshd_config "$SSHD_DIR"/*.conf; do
  [[ -f "$f" ]] || continue
  [[ "$f" == "$SSHD_DROPIN" ]] && continue
  sed -ri \
    -e 's/^[[:space:]]*PasswordAuthentication[[:space:]].*/#&  # neutralized by harden/' \
    -e 's/^[[:space:]]*KbdInteractiveAuthentication[[:space:]].*/#&  # neutralized by harden/' \
    -e 's/^[[:space:]]*ChallengeResponseAuthentication[[:space:]].*/#&  # neutralized by harden/' \
    -e 's/^[[:space:]]*PermitRootLogin[[:space:]].*/#&  # neutralized by harden/' \
    -e 's/^[[:space:]]*AuthenticationMethods[[:space:]].*/#&  # neutralized by harden/' \
    "$f" 2>/dev/null || true
done

if sshd -t 2>/tmp/sshd-t.err; then
  systemctl restart sshd && echo "sshd restarted OK"
  echo "Effective:"
  sshd -T | grep -E '^(passwordauthentication|permitrootlogin|kbdinteractiveauthentication|pubkeyauthentication|authenticationmethods) '
else
  echo "ERROR: sshd -t failed — restoring prior drop-in if any." >&2
  cat /tmp/sshd-t.err >&2 || true
  last_bak=$(ls -1t "${SSHD_DROPIN}".bak.* 2>/dev/null | head -1 || true)
  if [[ -n "${last_bak:-}" ]]; then
    cp -a "$last_bak" "$SSHD_DROPIN"
  else
    rm -f "$SSHD_DROPIN"
  fi
  systemctl restart sshd 2>/dev/null || true
fi

# ---------------------------------------------------------------------------
# 4. fail2ban
# ---------------------------------------------------------------------------
if command -v fail2ban-server >/dev/null 2>&1; then
  echo "fail2ban already installed"
else
  echo "Installing fail2ban via $PM ..."
  case $PM in
    dnf|yum) "$PM" -y install epel-release >/dev/null 2>&1; "$PM" -y install fail2ban ;;
    apt)     apt-get update >/dev/null 2>&1; apt-get -y install fail2ban ;;
    *)       echo "WARN: no package manager — install fail2ban manually" ;;
  esac
fi

# Prefer nft/iptables backend action; do NOT force-start firewalld (breaks Tailscale/iptables).
mkdir -p /etc/fail2ban/jail.d
cat > /etc/fail2ban/jail.d/sshd.local <<'EOF'
[sshd]
enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/secure
maxretry = 3
findtime = 10m
bantime  = 1h
backend  = systemd
EOF
[[ "${AUTHLOG:-}" == "/var/log/auth.log" ]] \
  && sed -i 's#/var/log/secure#/var/log/auth.log#' /etc/fail2ban/jail.d/sshd.local

# Stop firewalld from auto-starting on boot if it was pulled in as a dependency.
if systemctl list-unit-files firewalld.service >/dev/null 2>&1; then
  if ! systemctl is-active --quiet firewalld; then
    systemctl disable firewalld 2>/dev/null || true
    systemctl mask firewalld 2>/dev/null || true
    echo "firewalld disabled/masked (was inactive; keeps iptables/Tailscale intact)."
  else
    echo "WARN: firewalld is active — ensure ssh is allowed: firewall-cmd --add-service=ssh"
  fi
fi

systemctl enable --now fail2ban 2>/dev/null || fail2ban-client start 2>/dev/null
systemctl restart fail2ban 2>/dev/null
echo "fail2ban status:"
fail2ban-client status sshd 2>/dev/null || echo "(fail2ban not running — check manually)"

# ---------------------------------------------------------------------------
# 5. Firewall: drop top offenders + light SSH rate limit via iptables
# ---------------------------------------------------------------------------
mapfile -t WORST_IPS < <(
  grep -E "Failed password|Invalid user" "${AUTHLOG:-/dev/null}" \
    | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" \
    | sort | uniq -c | sort -rn | head -n 25 \
    | awk '$1 >= 20 {print $2}'
)

if command -v iptables >/dev/null 2>&1; then
  echo "iptables — dropping top offender IPs + SSH rate limit"
  # Rate limit new SSH (best-effort; ignore if modules missing)
  iptables -C INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 10 -j DROP 2>/dev/null \
    || iptables -I INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 10 -j DROP 2>/dev/null \
    || echo "WARN: recent/conntrack rate-limit not applied"
  iptables -C INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set 2>/dev/null \
    || iptables -I INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set 2>/dev/null \
    || true
  for ip in "${WORST_IPS[@]:-}"; do
    [[ -z "${ip:-}" ]] && continue
    iptables -C INPUT -s "$ip" -j DROP 2>/dev/null \
      || iptables -I INPUT -s "$ip" -j DROP
    echo "  dropped: $ip"
  done
  mkdir -p /etc/sysconfig
  if command -v iptables-save >/dev/null 2>&1; then
    iptables-save > /etc/sysconfig/iptables
    echo "Saved /etc/sysconfig/iptables ($(wc -l < /etc/sysconfig/iptables) lines)"
  fi
  # Ensure rules restore on boot if iptables-services available
  if ! systemctl list-unit-files iptables.service 2>/dev/null | grep -q iptables; then
    case $PM in
      dnf|yum) "$PM" -y install iptables-services >/dev/null 2>&1 || true ;;
    esac
  fi
  if systemctl list-unit-files iptables.service 2>/dev/null | grep -q iptables; then
    systemctl enable iptables 2>/dev/null || true
    service iptables save 2>/dev/null || iptables-save > /etc/sysconfig/iptables
    echo "iptables service enabled for boot restore"
  else
    echo "WARN: install iptables-services later so DROPs survive reboot"
  fi
else
  echo "WARN: iptables not found"
fi

echo
echo "=== Summary ==="
echo "Effective sshd:"
sshd -T | grep -E '^(passwordauthentication|permitrootlogin|kbdinteractiveauthentication|pubkeyauthentication|authenticationmethods) ' || true
echo
echo "fail2ban banned:"
fail2ban-client status sshd 2>/dev/null | sed -n '/Banned IP list/,/^$/p' || true
echo
echo "IMPORTANT: open a NEW ssh session (key) in a second window BEFORE closing this one."
echo "If locked out, use rescue console and remove $SSHD_DROPIN or restore sshd_config.bak.*"
