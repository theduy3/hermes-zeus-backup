#!/usr/bin/env python3
"""Parse wttr.in JSON forecast files for today + tomorrow in compact format.

Expects /tmp/wx_mtl.json, /tmp/wx_laval.json, /tmp/wx_qc.json from:
    curl -sS "https://wttr.in/Montreal?format=j1" -o /tmp/wx_mtl.json
    curl -sS "https://wttr.in/Laval,Quebec?format=j1" -o /tmp/wx_laval.json
    curl -sS "https://wttr.in/Quebec+City?format=j1" -o /tmp/wx_qc.json

Output: pipe-delimited rows suitable for the compact briefing weather table.
"""
import json, sys

FILES = [
    ('/tmp/wx_mtl.json', 'Montreal'),
    ('/tmp/wx_laval.json', 'Laval'),
    ('/tmp/wx_qc.json', 'Quebec City'),
]

for path, city in FILES:
    try:
        with open(path) as f:
            data = json.load(f)
        today = data['weather'][0]
        tomorrow = data['weather'][1]
        t_hi = today['maxtempC']
        t_lo = today['mintempC']
        t_cond = today['hourly'][4]['weatherDesc'][0]['value']
        tm_hi = tomorrow['maxtempC']
        tm_lo = tomorrow['mintempC']
        tm_cond = tomorrow['hourly'][4]['weatherDesc'][0]['value']
        print(f'{city} | {t_hi}/{t_lo} {t_cond} | {tm_hi}/{tm_lo} {tm_cond}')
    except Exception as e:
        print(f'{city} | ERR: {e}', file=sys.stderr)