#!/usr/bin/env python3
import json
d = json.load(open("/tmp/fv_parsed.json"))
print("COUNT", len(d))
for k, v in sorted(d.items()):
    print(f"{k}|fwd={v.get('fwdPE')}|peg={v.get('peg')}|pfcf={v.get('pfcf')}|epsNY={v.get('epsNextY')}|pe={v.get('pe')}")
