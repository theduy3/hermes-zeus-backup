#!/usr/bin/env python3
import os, subprocess, re
from datetime import datetime, timezone
from pathlib import Path

HOME = Path('/home/hermes/.hermes')
PROFILES = ['butter','catthew','charles','finance','thor','zeus']

def run(cmd):
    return subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout

def _gateway_action(rest):
    """Return True if argv tail is gateway run/restart after optional profile flags.

    Accepts:
      gateway run|restart
      -p NAME gateway run|restart
      --profile NAME gateway run|restart
      ... plus optional --replace anywhere before gateway
    """
    i = 0
    while i < len(rest):
        tok = rest[i]
        if tok in ('-p', '--profile') and i + 1 < len(rest):
            i += 2
            continue
        if tok == '--replace':
            i += 1
            continue
        break
    return rest[i:i+2] in (['gateway', 'run'], ['gateway', 'restart'])

def all_gateway_pids():
    """Return only real Hermes gateway process PIDs.

    Do not use ``ps | grep`` here: a cron/tool shell command can contain the
    literal text ``hermes gateway run`` or ``--profile <name>`` in its script
    body while inheriting ``HERMES_HOME=/home/hermes/.hermes``. That produced
    false wrong-HERMES_HOME alerts for profile gateways even though the live
    profile Python processes were healthy. Inspect /proc cmdline tokens instead
    and accept only actual Hermes/Python launcher shapes.

    Profile supervisor launches:
      python3 .../hermes -p <name> gateway run
    so gateway/run are NOT always argv[2:4] — strip -p/--profile first.
    """
    pids=[]
    for name in os.listdir('/proc'):
        if not name.isdigit():
            continue
        pid=int(name)
        argv=cmdline(pid).split()
        if not argv:
            continue
        exe=Path(argv[0]).name
        is_gateway = False
        # python3 .../hermes [ -p NAME | --profile NAME ] gateway run|restart
        if exe.startswith('python') and len(argv) >= 4 and Path(argv[1]).name == 'hermes':
            is_gateway = _gateway_action(argv[2:])
        # hermes [ -p NAME | --profile NAME ] gateway run|restart
        elif exe == 'hermes' and len(argv) >= 3:
            is_gateway = _gateway_action(argv[1:])
        # Module shape used by some repair commands:
        #   python -m hermes_cli.main [ -p NAME ] gateway run|restart
        elif exe.startswith('python') and '-m' in argv and 'hermes_cli.main' in argv:
            idx = argv.index('hermes_cli.main')
            is_gateway = _gateway_action(argv[idx+1:])
        if is_gateway:
            pids.append(pid)
    return pids

def cmdline(pid):
    try:
        return Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0', b' ').decode(errors='ignore')
    except Exception:
        return ''

def env(pid, key):
    try:
        data=Path(f'/proc/{pid}/environ').read_bytes().split(b'\0')
        pref=(key+'=').encode()
        for item in data:
            if item.startswith(pref): return item[len(pref):].decode(errors='ignore')
    except Exception:
        pass
    return ''

def last_start_window(profile):
    log = HOME/'logs/gateway.log' if profile=='default' else HOME/'profiles'/profile/'logs/gateway.log'
    if not log.exists(): return []
    try:
        lines=log.read_text(errors='ignore').splitlines()
    except Exception:
        return ['log unreadable']
    start=0
    for i,l in enumerate(lines):
        if 'Starting Hermes Gateway' in l:
            start=i
    return lines[start:][-300:]

def _line_age_seconds(line):
    m = re.search(r'(20\d\d-\d\d-\d\d \d\d:\d\d:\d\d)', line)
    if not m:
        return None
    try:
        # Container logs are local time; use naive delta to avoid timezone config drift.
        return (datetime.now() - datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S')).total_seconds()
    except Exception:
        return None

def recent_bad_log(profile):
    lines=last_start_window(profile)
    bad=[]

    # True startup blockers. Do not include model/cron auth strings here: they can
    # appear in gateway.log but are not gateway startup failures.
    blocker_patterns=['token already in use','Port 8642 already in use']
    for pat in blocker_patterns:
        if any(pat in l for l in lines): bad.append(pat)

    # Telegram can emit one transient 409 when an old long-poll session is still
    # expiring, then continue normally. Alert only if conflicts are recent or
    # repeated in the current startup window.
    conflict_lines=[l for l in lines if 'polling conflict' in l]
    recent_conflicts=[]
    for l in conflict_lines:
        age=_line_age_seconds(l)
        # Untimestamped duplicate console lines are not enough to make an old
        # conflict current; rely on timestamped log lines or repeated conflicts.
        if age is not None and age <= 20*60:
            recent_conflicts.append(l)
    if len(conflict_lines) >= 3 or recent_conflicts:
        bad.append('polling conflict')

    # If it connected after a startup retry, do not keep stale startup conflict as active.
    if any('✓ telegram connected' in l or 'Connected to Telegram' in l for l in lines):
        bad=[b for b in bad if b not in ('token already in use',)]
    return bad

problems=[]
gateway_pids=all_gateway_pids()
def_pids=[pid for pid in gateway_pids if env(pid,'HERMES_HOME') == str(HOME)]
if not def_pids:
    problems.append('default gateway missing')

for p in PROFILES:
    expected=str(HOME/'profiles'/p)
    pids=[pid for pid in gateway_pids if env(pid,'HERMES_HOME') == expected]
    if not pids:
        wrong=[pid for pid in gateway_pids if f'--profile {p}' in cmdline(pid) or f'-p {p}' in cmdline(pid)]
        if wrong:
            for pid in wrong:
                hh=env(pid,'HERMES_HOME')
                problems.append(f'{p}: wrong HERMES_HOME pid={pid} got={hh or "<unset>"} expected={expected}')
        else:
            problems.append(f'{p}: gateway missing')
        continue
    for pid in pids:
        hh=env(pid,'HERMES_HOME')
        if hh != expected:
            problems.append(f'{p}: wrong HERMES_HOME pid={pid} got={hh or "<unset>"} expected={expected}')
    bad=recent_bad_log(p)
    if bad:
        problems.append(f'{p}: current startup log issue: {", ".join(bad)}')

if problems:
    print('Hermes profile watchdog found issues:\n' + '\n'.join('- '+x for x in problems))
