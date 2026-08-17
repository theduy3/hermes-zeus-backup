import json
d=json.load(open('cnbc_all.json'))
fail=[]
for t,v in d.items():
    if not v.get("ok"):
        fail.append(t)
        continue
    fpe=v.get("fpe")
    print(f"{t:7} last={v.get('last')} chg={v.get('chg_pct')} fpe={fpe} pe={v.get('pe')} mcap={v.get('mktcap')} yr[{v.get('yrlo')}-{v.get('yrhi')}] ext={v.get('ext_type')}/{v.get('ext_chg')}")
print("\nFAILED:", fail)
print("\nMissing fpe among OK:", [t for t,v in d.items() if v.get('ok') and v.get('fpe') in (None,0.0)])
