from pathlib import Path
from textwrap import dedent
R=Path('/home/hermes/.hermes/projects/life-os'); K=R/'life-knowledge-base'; T=R/'tracker'
def w(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(dedent(s).lstrip(),encoding='utf8')
for d in '00-index 01-inbox 10-profile 20-timeline/events/2026 30-health/conditions 30-health/medications 30-health/procedures 30-health/tests 30-health/logs 40-nutrition/logs 50-projects/projects 60-finance 70-goals/goals 75-ideas/ideas 80-interests 85-resources 90-sources/records 90-sources/files 95-system/templates'.split(): (K/d).mkdir(parents=True,exist_ok=True)
w(K/'README.md',f'''# Life Knowledge Base\n\nPortable, private, Markdown-first source of truth. Created 2026-08-12. Dates use America/Toronto. Existing `/vault` is a read-only legacy/source corpus: its `AgentMemory` export is explicitly excluded. See [rules](agent_rules.md) and [index](00-index/master_index.md). No personal histories were imported during setup.\n''')
w(K/'agent_rules.md',f'''# Agent Rules\n\n## Authority\n`{K}` is the detailed personal context authority. Before a personal answer or substantial capture: read this file; lexical-search this directory; read the canonical summary and newer events/entity notes; follow sources for consequential claims. Conversation history and `/vault` are secondary only. Never use `/vault/AgentMemory`.\n\n## Capture and correction\nUse America/Toronto for selected dates; exact ISO date when known, otherwise `date_precision: approximate`. Label claims `fact`, `self_report`, `observation`, `hypothesis`, or `preference`. A correction creates/preserves a superseded record and links it; summaries show only current supported state. Never invent missing facts. Routine capture is one targeted write, one search verification, one concise acknowledgement.\n\n## Privacy\nNever store or send passwords, credentials, cookies, recovery codes, keys, seed phrases, payment authentication, or portal credentials. Do not transmit private KB material to third parties without explicit approval. Resources require inspecting their original URL before a summary.\n''')
w(K/'00-index/master_index.md','''# Master Index\n\n- [Profile](../10-profile/profile.md) · [Timeline](../20-timeline/timeline.md) · [Health](../30-health/health_summary.md) · [Nutrition](../40-nutrition/nutrition_summary.md)\n- [Projects](../50-projects/projects_summary.md) · [Finance](../60-finance/finance_summary.md) · [Goals](../70-goals/goals_summary.md) · [Ideas](../75-ideas/ideas_index.md) · [Interests](../80-interests/interests_summary.md) · [Resources](../85-resources/resources.md)\n- [Schema](../95-system/schema.md) · [Intake](../95-system/intake.md) · [Changelog](../95-system/changelog.md) · [Backups](../95-system/backups.md)\n''')
for p,title,text in [('00-index/open_questions.md','Open questions','No foundation answers were supplied beyond the active timezone.'),('00-index/people_index.md','People index','No person records captured.'),('00-index/projects_index.md','Projects index','No project records captured.'),('00-index/sources_index.md','Sources index','No source records captured.'),('01-inbox/inbox.md','Inbox','Unprocessed material only.'),('10-profile/profile.md','Profile','No profile facts imported.'),('20-timeline/timeline.md','Timeline','No events captured.'),('30-health/health_summary.md','Health summary','No health data captured.'),('40-nutrition/nutrition_summary.md','Nutrition summary','No nutrition data captured.'),('50-projects/projects_summary.md','Projects summary','No projects captured.'),('60-finance/finance_summary.md','Finance summary','No finance data captured.'),('70-goals/goals_summary.md','Goals summary','No goals captured.'),('75-ideas/ideas_index.md','Ideas index','No ideas captured.'),('80-interests/interests_summary.md','Interests summary','No interests captured.'),('85-resources/resources.md','Resources','No saved resources captured.')]:w(K/p,f'# {title}\n\n{text}\n')
w(K/'95-system/schema.md','''# Schema\n\nApplicable YAML fields: `id`, `type`, `subtype`, `record_status`, `epistemic`, `occurred_at`, `date_precision`, `recorded_at`, `source_ids`, `confidence`, `verification`, `needs_verification`, `supersedes`, `aliases`, `tags`. IDs: `evt- src- sym- cond- med- sup- lab- per- org- prj- dec- goal- idea- res-`. Bodies use Summary, Details, Evidence and provenance, Connections, Uncertainty and follow-up. Metrics define type/unit/range/options/aggregation/chart/privacy/missing semantics.\n''')
w(K/'95-system/intake.md','# Intake\n\nSearch existing record; reject secrets; capture provenance; update the smallest authority; update summary only when current state changes; validate and search once.\n')
w(K/'95-system/changelog.md','# Changelog\n\n## 2026-08-12\nCreated private portable KB and tracker; no personal data imported. `/vault/AgentMemory` excluded. Existing vault is referenced as a legacy/source corpus only due to its write boundary.\n')
w(K/'95-system/backups.md',f'# Backups\n\nBack up `{K}` and `{T}/data/tracker.sqlite3` with encrypted filesystem snapshots. Secrets are independently stored at `~/.config/life-tracker/secrets.env` with mode 600. Restore files, run `python3 {T}/tools.py verify`, then restart.\n')
w(K/'95-system/templates/event.md','''---\nid: evt-yyyymmdd-001\ntype: event\nrecord_status: historical\nepistemic: self_report\noccurred_at: yyyy-mm-dd\ndate_precision: exact\nrecorded_at: yyyy-mm-dd\nsource_ids: []\nconfidence: high\nverification: user_reported\nneeds_verification: false\nsupersedes: []\ntags: []\n---\n# Title\n\n## Summary\n\n## Details\n\n## Evidence and provenance\n\n## Connections\n\n## Uncertainty and follow-up\n''')
w(T/'app.py',r"""import os,json,sqlite3,secrets,hashlib,hmac,base64,threading
from pathlib import Path
from datetime import date,datetime
from wsgiref.simple_server import make_server
ROOT=Path(__file__).parent; DB=ROOT/'data/tracker.sqlite3'; LOCK=threading.RLock(); SEC=Path.home()/'.config/life-tracker/secrets.env'
def secrets_file():
 SEC.parent.mkdir(parents=True,exist_ok=True)
 if not SEC.exists(): SEC.write_text('BROWSER_PASSWORD='+secrets.token_urlsafe(18)+'\nAGENT_TOKEN='+secrets.token_urlsafe(30)+'\nSESSION_SECRET='+secrets.token_urlsafe(30)+'\n');os.chmod(SEC,0o600)
 return dict(x.split('=',1) for x in SEC.read_text().splitlines() if '=' in x)
S=secrets_file()
def con():
 c=sqlite3.connect(DB,timeout=5);c.row_factory=sqlite3.Row;c.execute('pragma foreign_keys=on');c.execute('pragma journal_mode=wal');return c
def init():
 c=con();c.executescript('''create table if not exists goals(id text primary key,title text,area text,status text,done text,review_date text);create table if not exists projects(id text primary key,title text,status text,phase text,blocker text,next_action text,goal_id text);create table if not exists habits(id text primary key,title text,schedule text,paused integer default 0,goal_id text,project_id text);create table if not exists completions(id text primary key,habit_id text,day text,state text,unique(habit_id,day));create table if not exists metrics(id text primary key,label text,kind text,unit text,min real,max real,aggregation text,chart text,privacy text,missing text);create table if not exists observations(id text primary key,metric_id text,day text,value text,estimated integer,description text,recorded_at text,deleted integer default 0);''');c.commit();c.close()
def rows(c,s,a=()):return [dict(x) for x in c.execute(s,a)]
def body(e):
 try:return json.loads(e['wsgi.input'].read(int(e.get('CONTENT_LENGTH') or 0)) or '{}')
 except:raise ValueError('invalid json')
def goodid(x):
 if not isinstance(x,str) or not x.replace('-','').replace('_','').isalnum():raise ValueError('bad id')
def auth(e):
 a=e.get('HTTP_AUTHORIZATION','');return a.startswith('Bearer ') and hmac.compare_digest(a[7:],S['AGENT_TOKEN'])
def send(st,status,o,hs=[]):
 b=json.dumps(o).encode();st(status,[('Content-Type','application/json'),('Content-Length',str(len(b))),*hs]);return[b]
def api(e,st):
 p=e['PATH_INFO'];m=e['REQUEST_METHOD'];c=con()
 try:
  if p=='/api/login' and m=='POST':
   if not hmac.compare_digest(str(body(e).get('password','')),S['BROWSER_PASSWORD']):return send(st,'401 Unauthorized',{'error':'bad credentials'})
   raw=base64.urlsafe_b64encode(str(int(datetime.now().timestamp())+86400).encode()).decode();sig=hmac.new(S['SESSION_SECRET'].encode(),raw.encode(),hashlib.sha256).hexdigest();return send(st,'200 OK',{'ok':True},[('Set-Cookie',f'life={raw}.{sig}; HttpOnly; SameSite=Strict; Path=/')])
  if not auth(e):return send(st,'401 Unauthorized',{'error':'agent bearer required'})
  if p=='/api/today' and m=='GET':
   d=date.today().isoformat();its=[]
   for h in rows(c,'select * from habits where paused=0'):
    sch=json.loads(h['schedule']); wd=datetime.strptime(d,'%Y-%m-%d').weekday();ok=sch['kind']=='daily' or(sch['kind']=='weekdays' and wd in sch.get('days',[]))or(sch['kind']=='weekly' and wd==sch.get('weekday',0))or sch['kind']=='minimum_frequency'
    if ok:
     z=c.execute('select state from completions where habit_id=? and day=?',(h['id'],d)).fetchone();its.append({'id':h['id'],'type':'habit','title':h['title'],'completed':bool(z and z[0]=='completed')})
   return send(st,'200 OK',{'date':d,'items':its})
  b=body(e)
  if p=='/api/complete' and m=='POST':
   goodid(b['id']);d=b['day'];datetime.strptime(d,'%Y-%m-%d');state=b['state'];h=c.execute('select * from habits where id=?',(b['id'],)).fetchone()
   if not h:raise ValueError('unknown habit')
   if state not in ('completed','open','skipped'):raise ValueError('bad state')
   c.execute('insert into completions(id,habit_id,day,state)values(?,?,?,?) on conflict(habit_id,day)do update set state=excluded.state',(secrets.token_hex(8),b['id'],d,state));c.commit();return send(st,'200 OK',{'ok':True})
  maps={'/api/goals':('goals',['id','title','area','status','done','review_date']),'/api/projects':('projects',['id','title','status','phase','blocker','next_action','goal_id']),'/api/habits':('habits',['id','title','schedule','paused','goal_id','project_id']),'/api/metrics':('metrics',['id','label','kind','unit','min','max','aggregation','chart','privacy','missing']),'/api/observations':('observations',['id','metric_id','day','value','estimated','description','recorded_at','deleted'])}
  if p=='/api/dashboard' and m=='GET':return send(st,'200 OK',{'goals':rows(c,'select * from goals'),'projects':rows(c,'select * from projects'),'metrics':rows(c,'select m.*,count(o.id) coverage from metrics m left join observations o on o.metric_id=m.id and o.deleted=0 group by m.id')})
  if p not in maps or m!='POST':return send(st,'404 Not Found',{'error':'not found'})
  tab,cols=maps[p]
  if set(b)-set(cols):raise ValueError('unknown fields')
  goodid(b['id'])
  if p=='/api/habits':
   s=b.get('schedule');
   if not isinstance(s,dict) or s.get('kind') not in ('daily','weekdays','weekly','minimum_frequency'):raise ValueError('invalid schedule')
   b['schedule']=json.dumps(s)
  if p=='/api/metrics' and (b.get('kind') not in ('numeric','boolean','categorical','duration','count','rating','text') or b.get('missing') not in ('unknown','zero','not_applicable','incomplete')):raise ValueError('invalid metric')
  if p=='/api/observations':b['recorded_at']=datetime.utcnow().isoformat()+'Z';b['deleted']=0;datetime.strptime(b['day'],'%Y-%m-%d')
  c.execute(f'insert or replace into {tab}({",".join(cols)}) values({",".join("?" for _ in cols)})',[b.get(x) for x in cols]);c.commit();return send(st,'200 OK',{'ok':True,'id':b['id']})
 except (ValueError,KeyError,sqlite3.Error) as x:return send(st,'400 Bad Request',{'error':str(x)})
 finally:c.close()
HTML='''<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Life tracker</title><style>body{font:18px system-ui;max-width:720px;margin:auto;padding:20px;color:#17201c}nav{display:flex;gap:12px;border-bottom:1px solid #ddd;padding-bottom:10px}button,a{min-height:44px;padding:10px;font:inherit;border:1px solid #aaa;border-radius:7px;background:#fff}.row{padding:14px 0;border-bottom:1px solid #ddd;display:flex;justify-content:space-between;gap:12px}button:focus,a:focus{outline:3px solid #1967d2}@media(max-width:400px){body{padding:14px}}</style><nav><a href="#today">Today</a><a href="#goals">Goals</a><a href="#projects">Projects</a><a href="#data">Data</a></nav><main id=a aria-live=polite>Sign in via private API, then reload.</main><script>let v=location.hash.slice(1)||'today';let A=document.querySelector('#a');async function r(){let u=v==='today'?'/api/today':'/api/dashboard',x=await fetch(u).then(x=>x.json());let z=v==='today'?x.items:v==='goals'?x.goals:v==='projects'?x.projects:x.metrics;A.innerHTML='<h1>'+v+'</h1>'+z.map(i=>'<div class=row><span>'+i.title+'</span><span>'+ (i.status||('coverage '+i.coverage))+'</span></div>').join('')||'<p>No data yet.</p>'}addEventListener('hashchange',()=>{v=location.hash.slice(1);r()});r();setInterval(r,60000)</script>'''
def app(e,st):
 if e['PATH_INFO'].startswith('/api/'):return api(e,st)
 if e['PATH_INFO']=='/':st('200 OK',[('Content-Type','text/html')]);return[HTML.encode()]
 st('404 Not Found',[]);return[b'']
if __name__=='__main__':init();make_server('127.0.0.1',8788,app).serve_forever()
""")
w(T/'tools.py',f'''import re,sys,json\nfrom pathlib import Path\nK=Path({str(K)!r}); req=['readme.md','agent_rules.md','00-index/master_index.md','95-system/schema.md','95-system/changelog.md','95-system/intake.md','95-system/backups.md']; ids=[];bad=[]\nfor p in K.rglob('*.md'):\n t=p.read_text(); ids+=re.findall(r'^id: ([^\\s]+)',t,re.M); bad += [str(p.relative_to(K))] if re.search(r'(password|api[_-]?key|seed phrase)\\s*[:=]',t,re.I) else []\nr={{'ok':not bad and not [x for x in req if not(K/x).exists()] and len(ids)==len(set(ids)),'markdown_files':len(list(K.rglob('*.md'))),'possible_secret_files':bad}};print(json.dumps(r));sys.exit(0 if r['ok'] else 1)\n''')
w(T/'README.md',f'''# Private Life Tracker\n\nLocal URL: http://127.0.0.1:8788. Run `python3 app.py`. Browser cookie endpoint exists at `/api/login`; agent bearer endpoints are separate. Secrets are generated only in `~/.config/life-tracker/secrets.env` mode 600 and never printed. SQLite is operational state: Markdown at `{K}` remains knowledge authority. Use HTTPS reverse proxy and set secure cookies before remote exposure.\n''')
print('built',R)
