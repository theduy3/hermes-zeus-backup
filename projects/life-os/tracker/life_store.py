"""Markdown-first Life OS ledger; SQLite is a rebuildable operational cache."""
from __future__ import annotations
import hashlib, json, re, shutil, sqlite3, threading
from datetime import datetime, timezone
from pathlib import Path

WRITE_LOCK = threading.RLock()  # serializes append+rebuild so concurrent writes stay consistent

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "life-knowledge-base"
DB = Path(__file__).resolve().parent / "data" / "tracker.sqlite3"
LEDGER_DIRS = {"health": "30-health/logs", "nutrition": "40-nutrition/logs", "finance": "60-finance/events", "project": "50-projects/events", "goal": "70-goals/events", "tracker": "70-goals/events"}
ID = re.compile(r"^[a-z][a-z0-9_-]{0,79}$")

def utcnow(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def month(day): datetime.strptime(day, '%Y-%m-%d'); return day[:7]
def validate_id(value):
    if not isinstance(value, str) or not ID.fullmatch(value): raise ValueError("invalid id")
def canonical_json(value): return json.dumps(value, sort_keys=True, separators=(',',':'), ensure_ascii=False)
def ledger_path(domain, day):
    if domain not in LEDGER_DIRS: raise ValueError("invalid domain")
    return KB / LEDGER_DIRS[domain] / f"{month(day)}.md"
def record_id(record): return record["id"]
def event_block(record):
    # One JSON object per line makes parsing deterministic; Markdown remains human-readable.
    return "<!-- life-os-event " + canonical_json(record) + " -->\n"
def append_event(record):
    validate_id(record_id(record)); datetime.strptime(record['selected_date'], '%Y-%m-%d')
    path = ledger_path(record['domain'], record['selected_date']); path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists(): path.write_text(f"# {record['domain'].title()} ledger — {month(record['selected_date'])}\n\n", encoding='utf8')
    existing = list_events(path)
    if any(x['id'] == record['id'] for x in existing): raise ValueError('duplicate event id')
    with path.open('a', encoding='utf8') as f: f.write(event_block(record))
    return path
def list_events(path=None):
    paths=[path] if path else list(KB.rglob('*.md')); out=[]
    for p in paths:
        if not p.exists(): continue
        for raw in re.findall(r'<!-- life-os-event (.*?) -->', p.read_text(encoding='utf8')):
            x=json.loads(raw); x['_path']=str(p.relative_to(KB)); out.append(x)
    return sorted(out, key=lambda x:(x['selected_date'],x['recorded_at'],x['id']))
def active(events):
    superseded={s for x in events for s in x.get('supersedes',[])}
    return [x for x in events if x['id'] not in superseded and not x.get('deleted',False)]
def init_db(path=None):
    path = DB if path is None else path
    path.parent.mkdir(parents=True,exist_ok=True); c=sqlite3.connect(path); c.execute('pragma journal_mode=wal'); c.execute('pragma foreign_keys=on')
    c.executescript('''create table if not exists cache_events(id text primary key, domain text not null, kind text not null, selected_date text not null, payload text not null, recorded_at text not null, source_path text not null); create table if not exists cache_meta(key text primary key,value text not null);''')
    c.commit(); return c
def rebuild(db=None):
    db = DB if db is None else db
    events=active(list_events()); c=init_db(db); c.execute('begin immediate'); c.execute('delete from cache_events')
    for e in events:
        # Store the full event (incl. source_ids/supersedes/epistemic) so the
        # rebuildable cache preserves provenance, not just the inner payload.
        cached={k:v for k,v in e.items() if k!='_path'}
        c.execute('insert into cache_events values(?,?,?,?,?,?,?)',(e['id'],e['domain'],e['kind'],e['selected_date'],canonical_json(cached),e['recorded_at'],e['_path']))
    c.execute('insert or replace into cache_meta values(?,?)',('ledger_sha256',ledger_digest())); c.commit(); c.close(); return len(events)
def ledger_digest():
    h=hashlib.sha256()
    for p in sorted(KB.rglob('*.md')):
        if 'logs' in p.parts or 'events' in p.parts: h.update(str(p.relative_to(KB)).encode()+b'\0'+p.read_bytes())
    return h.hexdigest()
def reconcile(db=None):
    db = DB if db is None else db
    expected={e['id'] for e in active(list_events())}; c=init_db(db); actual={r[0] for r in c.execute('select id from cache_events')}; stored=c.execute("select value from cache_meta where key='ledger_sha256'").fetchone(); c.close()
    return {'ok':expected==actual and bool(stored) and stored[0]==ledger_digest(),'ledger_only':sorted(expected-actual),'cache_only':sorted(actual-expected),'ledger_count':len(expected),'cache_count':len(actual)}
def write(domain, kind, selected_date, payload, *, event_id, supersedes=(), source_ids=(), estimated=False):
    if not isinstance(payload,dict): raise ValueError('payload must be object')
    r={'id':event_id,'domain':domain,'kind':kind,'selected_date':selected_date,'recorded_at':utcnow(),'payload':payload,'supersedes':list(supersedes),'source_ids':list(source_ids),'estimated':bool(estimated),'epistemic':'self_report'}
    with WRITE_LOCK:
        append_event(r); rebuild()
    return r
def rebuild_tracker(db=None):
    """Recreate operational tables solely from active Markdown events."""
    db = DB if db is None else db; events=active(list_events()); c=sqlite3.connect(db); c.execute('pragma foreign_keys=on')
    tables=['goals','projects','habits','completions','metrics','observations']
    for t in tables: c.execute(f'delete from {t}')
    for e in events:
        p=e['payload']; rid=p.get('record_id')
        if e['kind']=='goals' and rid: c.execute('insert into goals values(?,?,?,?,?,?)',(rid,p.get('title'),p.get('area'),p.get('status'),p.get('done'),p.get('review_date')))
        elif e['kind']=='projects' and rid: c.execute('insert into projects values(?,?,?,?,?,?,?)',(rid,p.get('title'),p.get('status'),p.get('phase'),p.get('blocker'),p.get('next_action'),p.get('goal_id')))
        elif e['kind']=='habits' and rid:
            sched=p.get('schedule')
            if isinstance(sched,dict): sched=canonical_json(sched)
            c.execute('insert into habits values(?,?,?,?,?,?)',(rid,p.get('title'),sched,int(bool(p.get('paused'))),p.get('goal_id'),p.get('project_id')))
        elif e['kind']=='metrics' and rid: c.execute('insert into metrics values(?,?,?,?,?,?,?,?,?,?)',(rid,p.get('label'),p.get('kind'),p.get('unit'),p.get('min'),p.get('max'),p.get('aggregation'),p.get('chart'),p.get('privacy'),p.get('missing')))
        elif e['kind']=='observations' and rid: c.execute('insert into observations values(?,?,?,?,?,?,?,?)',(rid,p.get('metric_id'),p.get('day'),p.get('value'),int(bool(p.get('estimated'))),p.get('description'),p.get('recorded_at'),int(bool(p.get('deleted')))))
        elif e['kind']=='habit_completion': c.execute('insert into completions values(?,?,?,?)',(e['id'],p.get('habit_id'),e['selected_date'],p.get('state')))
    c.commit(); c.close(); rebuild(db); return len(events)

def checkpoint(name):
    validate_id(name); dest=KB.parent/'verification'/'checkpoints'/name; dest.mkdir(parents=True,exist_ok=False)
    shutil.copytree(KB,dest/'life-knowledge-base');
    if DB.exists(): shutil.copy2(DB,dest/'tracker.sqlite3')
    (dest/'manifest.json').write_text(canonical_json({'created_at':utcnow(),'ledger_sha256':ledger_digest(),'sqlite_present':DB.exists()})+'\n'); return dest
