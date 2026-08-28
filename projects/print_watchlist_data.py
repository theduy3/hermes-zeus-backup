#!/usr/bin/env python3
import json
with open("/home/hermes/.hermes/projects/watchlist_data.json") as f:
    d = json.load(f)
for t, v in d.items():
    if "error" in v:
        print("CHART FAIL", t, v.get("error"))
    else:
        print(f"{t}|{v.get('price')}|{v.get('chg_pct')}|{v.get('name')}|{v.get('last_ts')}|{v.get('currency')}")
