import os,json,sqlite3,secrets,hashlib,hmac,base64,threading
from pathlib import Path
from datetime import date,datetime
from wsgiref.simple_server import make_server
from life_store import write as ledger_write
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
def browser(e):
 cookie=e.get('HTTP_COOKIE',''); token=next((x.strip()[5:] for x in cookie.split(';') if x.strip().startswith('life=')), '')
 try:
  raw,sig=token.split('.',1); good=hmac.compare_digest(sig,hmac.new(S['SESSION_SECRET'].encode(),raw.encode(),hashlib.sha256).hexdigest()); return good and int(base64.urlsafe_b64decode(raw).decode())>int(datetime.now().timestamp())
 except Exception:return False
def auth(e):
 a=e.get('HTTP_AUTHORIZATION','');return a.startswith('Bearer ') and hmac.compare_digest(a[7:],S['AGENT_TOKEN'])
def read_auth(e): return auth(e) or browser(e)
def send(st,status,o,hs=[]):
 b=json.dumps(o).encode();st(status,[('Content-Type','application/json'),('Content-Length',str(len(b))),*hs]);return[b]
def api(e,st):
 p=e['PATH_INFO'];m=e['REQUEST_METHOD'];c=con()
 try:
  if p=='/api/login' and m=='POST':
   if not hmac.compare_digest(str(body(e).get('password','')),S['BROWSER_PASSWORD']):return send(st,'401 Unauthorized',{'error':'bad credentials'})
   raw=base64.urlsafe_b64encode(str(int(datetime.now().timestamp())+86400).encode()).decode();sig=hmac.new(S['SESSION_SECRET'].encode(),raw.encode(),hashlib.sha256).hexdigest();return send(st,'200 OK',{'ok':True},[('Set-Cookie',f'life={raw}.{sig}; HttpOnly; SameSite=Strict; Path=/')])
  if not read_auth(e):return send(st,'401 Unauthorized',{'error':'authentication required'})
  if p=='/api/today' and m=='GET':
   d=date.today().isoformat();its=[]
   for h in rows(c,'select * from habits where paused=0'):
    sch=json.loads(h['schedule']); wd=datetime.strptime(d,'%Y-%m-%d').weekday();ok=sch['kind']=='daily' or(sch['kind']=='weekdays' and wd in sch.get('days',[]))or(sch['kind']=='weekly' and wd==sch.get('weekday',0))or sch['kind']=='minimum_frequency'
    if ok:
     z=c.execute('select state from completions where habit_id=? and day=?',(h['id'],d)).fetchone();its.append({'id':h['id'],'type':'habit','title':h['title'],'completed':bool(z and z[0]=='completed')})
   return send(st,'200 OK',{'date':d,'items':its})
  if p=='/api/dashboard' and m=='GET':return send(st,'200 OK',{'goals':rows(c,'select * from goals'),'projects':rows(c,'select * from projects'),'metrics':rows(c,'select m.*,count(o.id) coverage from metrics m left join observations o on o.metric_id=m.id and o.deleted=0 group by m.id')})
  b=body(e)
  if p not in ('/api/complete',) and not auth(e):return send(st,'401 Unauthorized',{'error':'agent bearer required'})
  if p=='/api/complete' and m=='POST':
   goodid(b['id']);d=b['day'];datetime.strptime(d,'%Y-%m-%d');state=b['state'];h=c.execute('select * from habits where id=?',(b['id'],)).fetchone()
   if not h:raise ValueError('unknown habit')
   if state not in ('completed','open','skipped'):raise ValueError('bad state')
   ledger_write('tracker','habit_completion',d,{'habit_id':b['id'],'state':state},event_id='evt-'+secrets.token_hex(12))
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
  domain={'/api/goals':'goal','/api/projects':'project','/api/habits':'tracker','/api/metrics':'tracker','/api/observations':'health'}[p]
  selected=b.get('day') or date.today().isoformat()
  ledger_payload={k:b.get(k) for k in cols if k not in ('id','recorded_at')}; ledger_payload['record_id']=b['id']
  ledger_write(domain,tab,selected,ledger_payload,event_id='evt-'+secrets.token_hex(12))
  c.execute(f'insert or replace into {tab}({",".join(cols)}) values({",".join("?" for _ in cols)})',[b.get(x) for x in cols]);c.commit();return send(st,'200 OK',{'ok':True,'id':b['id']})
 except (ValueError,KeyError,sqlite3.Error) as x:return send(st,'400 Bad Request',{'error':str(x)})
 finally:c.close()
HTML='''<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Life tracker</title><style>body{font:18px system-ui;max-width:720px;margin:auto;padding:20px;color:#17201c}nav{display:flex;gap:12px;border-bottom:1px solid #ddd;padding-bottom:10px}button,a{min-height:44px;padding:10px;font:inherit;border:1px solid #aaa;border-radius:7px;background:#fff}.row{padding:14px 0;border-bottom:1px solid #ddd;display:flex;justify-content:space-between;gap:12px}button:focus,a:focus{outline:3px solid #1967d2}@media(max-width:400px){body{padding:14px}}</style><nav><a href="#today">Today</a><a href="#goals">Goals</a><a href="#projects">Projects</a><a href="#data">Data</a></nav><main id=a aria-live=polite>Sign in via private API, then reload.</main><script>let v=location.hash.slice(1)||'today';let A=document.querySelector('#a');async function r(){let u=v==='today'?'/api/today':'/api/dashboard',x=await fetch(u).then(x=>x.json());let z=v==='today'?x.items:v==='goals'?x.goals:v==='projects'?x.projects:x.metrics;A.innerHTML='<h1>'+v+'</h1>'+z.map(i=>'<div class=row><span>'+i.title+'</span><span>'+ (i.status||('coverage '+i.coverage))+'</span></div>').join('')||'<p>No data yet.</p>'}addEventListener('hashchange',()=>{v=location.hash.slice(1);r()});r();setInterval(r,60000)</script>'''
def app(e,st):
 if e['PATH_INFO'].startswith('/api/'):return api(e,st)
 if e['PATH_INFO']=='/':st('200 OK',[('Content-Type','text/html')]);return[HTML.encode()]
 st('404 Not Found',[]);return[b'']
if __name__=='__main__':init();make_server('127.0.0.1',8788,app).serve_forever()
