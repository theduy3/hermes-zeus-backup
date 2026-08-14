import json, yaml, os
BASE=os.path.expanduser('~/.hermes')
f=os.path.join(BASE,'profiles/zeus/cron/jobs.json')
raw=json.load(open(f))
jobs=raw if isinstance(raw,list) else (raw.get('jobs') or list(raw.values()))
for j in jobs:
    if isinstance(j,dict) and j.get('job_id')=='e6711b998b07':
        print("=== zeus job e6711b998b07 (raw keys) ===")
        print(json.dumps(j, indent=1)[:1400])
        break
cache=json.load(open(os.path.join(BASE,'provider_models_cache.json')))
print("\nnous models in cache:", cache.get('nous',{}).get('models'))
cfg=yaml.safe_load(open(os.path.join(BASE,'config.yaml')))
print("config default model:", cfg['model']['default'])
