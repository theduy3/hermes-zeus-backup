import re,sys,json
from pathlib import Path
K=Path('/home/hermes/.hermes/projects/life-os/life-knowledge-base'); req=['README.md','agent_rules.md','00-index/master_index.md','95-system/schema.md','95-system/changelog.md','95-system/intake.md','95-system/backups.md']; ids=[];bad=[]
for p in K.rglob('*.md'):
 t=p.read_text(); ids+=re.findall(r'^id: ([^\s]+)',t,re.M); bad += [str(p.relative_to(K))] if re.search(r'(password|api[_-]?key|seed phrase)\s*[:=]',t,re.I) else []
r={'ok':not bad and not [x for x in req if not(K/x).exists()] and len(ids)==len(set(ids)),'markdown_files':len(list(K.rglob('*.md'))),'possible_secret_files':bad};print(json.dumps(r));sys.exit(0 if r['ok'] else 1)
