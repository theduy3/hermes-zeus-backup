import os, glob, yaml
BASE = os.path.expanduser('~/.hermes')
paths = [os.path.join(BASE, 'config.yaml')] + sorted(glob.glob(os.path.join(BASE, 'profiles', '*', 'config.yaml')))
for p in paths:
    scope = 'DEFAULT' if p == os.path.join(BASE, 'config.yaml') else p.split('/profiles/')[1].split('/')[0]
    try:
        cfg = yaml.safe_load(open(p))
    except Exception as e:
        print(f"[{scope}] parse err {e}"); continue
    m = cfg.get('model', {}) or {}
    print(f"[{scope:8}] provider={m.get('provider')!r:16} default_model={m.get('default')!r:28} fallback={m.get('fallback_providers')!r}")
    # also show credential_pool_strategies for codex
    cps = cfg.get('credential_pool_strategies', {}) or {}
    if 'openai-codex' in cps:
        print(f"           credential_pool_strategies.openai-codex={cps['openai-codex']!r}")
