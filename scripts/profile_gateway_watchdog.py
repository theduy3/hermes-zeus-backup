#!/usr/bin/env python3
import os, subprocess
from pathlib import Path

HOME = Path('/home/hermes/.hermes')
PROFILES = ['butter','catthew','charles','finance','thor','zeus']

def run(cmd):
    return subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout

def all_gateway_pids():
    """Return Hermes gateway PIDs.

    Healthy Docker profile gateways usually appear as `hermes gateway run` with
    profile-scoped HERMES_HOME. Mis-started repair attempts can appear as
    `python -m hermes_cli.main --profile <name> gateway run --replace` while
    inheriting the default HERMES_HOME; include those too so the alert points at
    the wrong environment instead of only saying "missing".
    """
    out = run("ps -eo pid=,args= | grep -E '(hermes gateway run|hermes_cli\\.main .*gateway run)' | grep -v grep || true")
    pids=[]
    for line in out.splitlines():
        parts=line.strip().split(None,1)
        if parts and parts[0].isdigit(): pids.append(int(parts[0]))
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

def recent_bad_log(profile):
    lines=last_start_window(profile)
    bad=[]
    patterns=['polling conflict','token already in use','Could not parse your authentication token','auth is missing access_token','Port 8642 already in use']
    for pat in patterns:
        if any(pat in l for l in lines): bad.append(pat)
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
