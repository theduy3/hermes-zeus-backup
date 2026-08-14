from pathlib import Path

root = Path('/home/hermes/.hermes/projects/life-os')
required = [
    'life-knowledge-base/README.md',
    'life-knowledge-base/agent_rules.md',
    'life-knowledge-base/00-index/master_index.md',
    'life-knowledge-base/95-system/schema.md',
    'tracker/app.py', 'tracker/tools.py', 'tracker/README.md', 'tracker/tests/test_live.py',
]
missing = [item for item in required if not (root / item).exists()]
if missing:
    raise SystemExit('artifact check: FAIL ' + repr(missing))
print('artifact check: PASS')
