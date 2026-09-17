"""Markdown-first Life OS ledger; SQLite is a rebuildable operational cache."""
from __future__ import annotations
import fcntl, hashlib, json, os, re, shutil, sqlite3, threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

WRITE_LOCK = threading.RLock()  # in-process; flock covers cross-process writers

CHARLES_KINDS = frozenset({"position", "thesis", "risk_rule", "decision", "watch"})
DOMAIN_OWNER = {
    "health": "thor",
    "nutrition": "thor",
    "finance": "finance",
    "project": "life",
    "goal": "life",
    "tracker": "tracker",
}
# Must match tracker/app.py init() exactly, including unique(habit_id,day).
OPERATIONAL_SCHEMA = (
    "create table if not exists goals(id text primary key,title text,area text,status text,done text,review_date text);"
    "create table if not exists projects(id text primary key,title text,status text,phase text,blocker text,next_action text,goal_id text);"
    "create table if not exists habits(id text primary key,title text,schedule text,paused integer default 0,goal_id text,project_id text);"
    "create table if not exists completions(id text primary key,habit_id text,day text,state text,unique(habit_id,day));"
    "create table if not exists metrics(id text primary key,label text,kind text,unit text,min real,max real,aggregation text,chart text,privacy text,missing text);"
    "create table if not exists observations(id text primary key,metric_id text,day text,value text,estimated integer,description text,recorded_at text,deleted integer default 0);"
)

ID = re.compile(r"^[a-z][a-z0-9_-]{0,79}$")
LEDGER_DIRS = {
    "health": "30-health/logs",
    "nutrition": "40-nutrition/logs",
    "finance": "60-finance/events",
    "project": "50-projects/events",
    "goal": "70-goals/events",
    "tracker": "70-goals/events",
}

def configure(root=None):
    """Point ROOT/KB/DB at root, or LIFE_OS_ROOT, or this file's project tree."""
    global ROOT, KB, DB
    env = os.environ.get("LIFE_OS_ROOT")
    ROOT = Path(root) if root is not None else Path(env) if env else Path(__file__).resolve().parent.parent
    KB = ROOT / "life-knowledge-base"
    DB = ROOT / "tracker" / "data" / "tracker.sqlite3"

configure()

def utcnow():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def month(day):
    datetime.strptime(day, "%Y-%m-%d")
    return day[:7]

def validate_id(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError("invalid id")

def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def ledger_path(domain, day):
    if domain not in LEDGER_DIRS:
        raise ValueError("invalid domain")
    return KB / LEDGER_DIRS[domain] / f"{month(day)}.md"

def record_id(record):
    return record["id"]

def event_block(record):
    # One JSON object per line makes parsing deterministic; Markdown remains human-readable.
    return "<!-- life-os-event " + canonical_json(record) + " -->\n"

def event_owner(record):
    owner = record.get("owner")
    if owner:
        return owner
    if record.get("kind") in CHARLES_KINDS:
        return "charles"
    return DOMAIN_OWNER.get(record.get("domain"))

def cached_event(event):
    return {k: v for k, v in event.items() if k != "_path"}

def parse_events(text, source_path=None):
    out = []
    for raw in re.findall(r"<!-- life-os-event (.*?) -->", text):
        x = json.loads(raw)
        if source_path is not None:
            x["_path"] = source_path
        out.append(x)
    return out

@contextmanager
def _flock(path, *, exclusive=True):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
    fh = open(path, "a+", encoding="utf8")
    try:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        yield fh
    finally:
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        fh.close()

def write_lock_path():
    p = DB.parent
    p.mkdir(parents=True, exist_ok=True)
    return p / ".write.lock"

def append_event(record, *, locked_fd=None):
    validate_id(record_id(record))
    datetime.strptime(record["selected_date"], "%Y-%m-%d")
    path = ledger_path(record["domain"], record["selected_date"])
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# {record['domain'].title()} ledger — {month(record['selected_date'])}\n\n", encoding="utf8")
    rel = str(path.relative_to(KB))

    def _append(fh):
        fh.seek(0)
        text = fh.read()
        existing = parse_events(text, rel)
        if any(x["id"] == record["id"] for x in existing):
            raise ValueError("duplicate event id")
        fh.seek(0, os.SEEK_END)
        fh.write(event_block(record))
        fh.flush()
        os.fsync(fh.fileno())
        return path

    if locked_fd is not None:
        return _append(locked_fd)
    with _flock(path):
        with path.open("a+", encoding="utf8") as fh:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
            try:
                return _append(fh)
            finally:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)

def list_events(path=None):
    paths = [path] if path else list(KB.rglob("*.md"))
    out = []
    for p in paths:
        if not p.exists():
            continue
        try:
            rel = str(p.relative_to(KB))
        except ValueError:
            rel = str(p)
        out.extend(parse_events(p.read_text(encoding="utf8"), rel))
    return sorted(out, key=lambda x: (x["selected_date"], x["recorded_at"], x["id"]))

def active(events):
    superseded = {s for x in events for s in x.get("supersedes", [])}
    return [x for x in events if x["id"] not in superseded and not x.get("deleted", False)]

def init_db(path=None):
    path = DB if path is None else path
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path)
    c.execute("pragma journal_mode=wal")
    c.execute("pragma foreign_keys=on")
    c.executescript(
        "create table if not exists cache_events(id text primary key, domain text not null, kind text not null, selected_date text not null, payload text not null, recorded_at text not null, source_path text not null);"
        "create table if not exists cache_meta(key text primary key,value text not null);"
    )
    c.commit()
    return c

def rebuild(db=None, *, drop_cache_only=False):
    db = DB if db is None else db
    all_events = list_events()
    events = active(all_events)
    c = init_db(db)
    actual = {r[0] for r in c.execute("select id from cache_events")}
    ledger_ids = {e["id"] for e in all_events}
    cache_only = sorted(actual - ledger_ids)
    if cache_only and not drop_cache_only:
        c.close()
        raise ValueError("rebuild would drop cache_only rows %s; pass drop_cache_only=True" % cache_only)
    c.execute("begin immediate")
    c.execute("delete from cache_events")
    for e in events:
        # Store the full event (incl. source_ids/supersedes/epistemic) so the
        # rebuildable cache preserves provenance, not just the inner payload.
        cached = cached_event(e)
        c.execute(
            "insert into cache_events values(?,?,?,?,?,?,?)",
            (e["id"], e["domain"], e["kind"], e["selected_date"], canonical_json(cached), e["recorded_at"], e["_path"]),
        )
    c.execute("insert or replace into cache_meta values(?,?)", ("ledger_sha256", ledger_digest()))
    c.commit()
    c.close()
    return len(events)

def ledger_digest():
    h = hashlib.sha256()
    if not KB.exists():
        return h.hexdigest()
    for p in sorted(KB.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(KB)).encode() + b"\0" + p.read_bytes())
    return h.hexdigest()

def reconcile(db=None):
    db = DB if db is None else db
    events = active(list_events())
    expected = {e["id"]: canonical_json(cached_event(e)) for e in events}
    c = init_db(db)
    actual = {r[0]: r[1] for r in c.execute("select id, payload from cache_events")}
    stored = c.execute("select value from cache_meta where key='ledger_sha256'").fetchone()
    c.close()
    payload_mismatch = sorted(i for i in expected if i in actual and actual[i] != expected[i])
    digest_ok = bool(stored) and stored[0] == ledger_digest()
    return {
        "ok": set(expected) == set(actual) and not payload_mismatch and digest_ok,
        "ledger_only": sorted(set(expected) - set(actual)),
        "cache_only": sorted(set(actual) - set(expected)),
        "payload_mismatch": payload_mismatch,
        "digest_ok": digest_ok,
        "ledger_count": len(expected),
        "cache_count": len(actual),
    }

def _merge_payload(predecessors, payload, *, replace):
    if replace:
        return dict(payload)
    merged = {}
    for pred in predecessors:
        src = pred.get("payload") or {}
        if not isinstance(src, dict):
            raise ValueError("predecessor payload must be object")
        merged.update(src)
    for key, value in payload.items():
        if value is None:
            merged.pop(key, None)
        else:
            merged[key] = value
    return merged

def write(domain, kind, selected_date, payload, *, event_id, owner, supersedes=(), source_ids=(), estimated=False, replace=False):
    if not isinstance(payload, dict):
        raise ValueError("payload must be object")
    validate_id(owner)
    validate_id(event_id)
    supersedes = list(supersedes)
    r = {
        "id": event_id,
        "domain": domain,
        "kind": kind,
        "selected_date": selected_date,
        "recorded_at": utcnow(),
        "payload": payload,
        "supersedes": supersedes,
        "source_ids": list(source_ids),
        "estimated": bool(estimated),
        "epistemic": "self_report",
        "owner": owner,
    }
    path = ledger_path(domain, selected_date)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# {domain.title()} ledger — {month(selected_date)}\n\n", encoding="utf8")
    with WRITE_LOCK:
        with _flock(write_lock_path()):
            with _flock(path) as ledger_fh:
                events = list_events()
                by_id = {e["id"]: e for e in events}
                if event_id in by_id:
                    raise ValueError("duplicate event id")
                predecessors = []
                for sid in supersedes:
                    if sid not in by_id:
                        raise ValueError("supersedes id does not exist: %s" % sid)
                    target = by_id[sid]
                    target_owner = event_owner(target)
                    if target_owner and target_owner != owner:
                        raise ValueError("cross-owner supersede rejected: %s owned by %s, writer is %s" % (sid, target_owner, owner))
                    predecessors.append(target)
                r["payload"] = _merge_payload(predecessors, payload, replace=replace)
                append_event(r, locked_fd=ledger_fh)
                rebuild()
    return r

def rebuild_tracker(db=None):
    """Recreate operational tables solely from active Markdown events."""
    db = DB if db is None else db
    events = active(list_events())
    c = sqlite3.connect(db)
    c.execute("pragma foreign_keys=on")
    c.executescript(OPERATIONAL_SCHEMA)
    tables = ["goals", "projects", "habits", "completions", "metrics", "observations"]
    for t in tables:
        c.execute(f"delete from {t}")
    for e in events:
        p = e["payload"]
        rid = p.get("record_id")
        if e["kind"] == "goals" and rid:
            c.execute("insert into goals values(?,?,?,?,?,?)", (rid, p.get("title"), p.get("area"), p.get("status"), p.get("done"), p.get("review_date")))
        elif e["kind"] == "projects" and rid:
            c.execute("insert into projects values(?,?,?,?,?,?,?)", (rid, p.get("title"), p.get("status"), p.get("phase"), p.get("blocker"), p.get("next_action"), p.get("goal_id")))
        elif e["kind"] == "habits" and rid:
            sched = p.get("schedule")
            if isinstance(sched, dict):
                sched = canonical_json(sched)
            c.execute("insert into habits values(?,?,?,?,?,?)", (rid, p.get("title"), sched, int(bool(p.get("paused"))), p.get("goal_id"), p.get("project_id")))
        elif e["kind"] == "metrics" and rid:
            c.execute("insert into metrics values(?,?,?,?,?,?,?,?,?,?)", (rid, p.get("label"), p.get("kind"), p.get("unit"), p.get("min"), p.get("max"), p.get("aggregation"), p.get("chart"), p.get("privacy"), p.get("missing")))
        elif e["kind"] == "observations" and rid:
            c.execute("insert into observations values(?,?,?,?,?,?,?,?)", (rid, p.get("metric_id"), p.get("day"), p.get("value"), int(bool(p.get("estimated"))), p.get("description"), p.get("recorded_at"), int(bool(p.get("deleted")))))
        elif e["kind"] == "habit_completion":
            c.execute(
                "insert into completions(id,habit_id,day,state) values(?,?,?,?) on conflict(habit_id,day) do update set state=excluded.state, id=excluded.id",
                (e["id"], p.get("habit_id"), e["selected_date"], p.get("state")),
            )
    c.commit()
    c.close()
    rebuild(db)
    return len(events)

def checkpoint(name):
    validate_id(name)
    dest = KB.parent / "verification" / "checkpoints" / name
    dest.mkdir(parents=True, exist_ok=False)
    shutil.copytree(KB, dest / "life-knowledge-base")
    if DB.exists():
        shutil.copy2(DB, dest / "tracker.sqlite3")
    code_dest = dest / "tracker"
    code_dest.mkdir()
    src_tracker = Path(__file__).resolve().parent
    copied = []
    for p in sorted(src_tracker.glob("*.py")):
        shutil.copy2(p, code_dest / p.name)
        copied.append(p.name)
    (dest / "manifest.json").write_text(
        canonical_json(
            {
                "created_at": utcnow(),
                "ledger_sha256": ledger_digest(),
                "sqlite_present": DB.exists(),
                "tracker_py": copied,
            }
        )
        + "\n"
    )
    return dest
