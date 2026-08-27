#!/usr/bin/env python3
"""Task button dispatcher — Done (zt:), Delay (delay:), Delete (del:)."""
import pathlib, json, datetime, zoneinfo, re, sys
REG = pathlib.Path("/home/hermes/.hermes/profiles/zeus/task_buttons/registry.json")
VAULT = pathlib.Path("/vault/Tasks/tasks")

def reg():
    return json.loads(REG.read_text()) if REG.exists() else {}

def handle_done(digest):
    r = reg(); entry = r.get(digest)
    if not entry: return 1
    fp = pathlib.Path(entry.get("file_path",""))
    if not fp.exists(): return 1
    t = fp.read_text()
    t = t.replace("status: pending", "status: completed")
    if "completed_date:" not in t:
        t = t.replace("# ", "completed_date: " + datetime.datetime.now(zoneinfo.ZoneInfo("America/Vancouver")).strftime("%Y-%m-%d") + "\n# ", 1)
    t = t.replace("- [ ] ", "- [x] ", 1)
    fp.write_text(t)
    return 0

def handle_delay(digest, reply_text):
    r = reg(); entry = r.get(digest)
    fp = pathlib.Path(entry.get("file_path","")) if entry else pathlib.Path("")
    if not fp.exists(): return 1
    m = re.search(r"(\d{4}-\d{2}-\d{2})", reply_text)
    if not m: return 1
    fp.write_text(fp.read_text().replace(str(entry.get("due_date","")), m.group(1)))
    return 0

def handle_delete(digest):
    r = reg(); entry = r.get(digest)
    fp = pathlib.Path(entry.get("file_path","")) if entry else pathlib.Path("")
    if fp.exists(): fp.unlink()
    if digest in r: del r[digest]
    REG.write_text(json.dumps(r))
    return 0

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv)>1 else ""
    digest = sys.argv[2] if len(sys.argv)>2 else ""
    reply = sys.argv[3] if len(sys.argv)>3 else ""
    if cmd=="done": print(handle_done(digest))
    elif cmd=="delay": print(handle_delay(digest, reply))
    elif cmd=="delete": print(handle_delete(digest))
    else: print("usage: done|delay|delete <digest> [reply_date]")
