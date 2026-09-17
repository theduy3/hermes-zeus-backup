import json, os, tempfile, threading, urllib.error, urllib.request
from pathlib import Path
from wsgiref.simple_server import make_server

LIVE_ROOT = Path(__file__).resolve().parents[2]

def request(base, path, method="GET", data=None, bearer=False, token=""):
    r = urllib.request.Request(base + path, method=method)
    if bearer:
        r.add_header("Authorization", "Bearer " + token)
    if data is not None:
        r.add_header("Content-Type", "application/json")
        r.data = json.dumps(data).encode()
    return urllib.request.urlopen(r, timeout=5)

def main():
    requested = os.environ.get("LIFE_OS_ROOT")
    if requested and Path(requested).resolve() == LIVE_ROOT.resolve():
        raise SystemExit("refusing to run test_live.py against the live Life OS tree")
    tmp = Path(tempfile.mkdtemp(prefix="lifeos-live-test-"))
    os.environ["LIFE_OS_ROOT"] = str(tmp)
    (tmp / "life-knowledge-base").mkdir()
    (tmp / "tracker" / "data").mkdir(parents=True)

    sys_path_tracker = str(Path(__file__).resolve().parents[1])
    import sys
    if sys_path_tracker not in sys.path:
        sys.path.insert(0, sys_path_tracker)
    import life_store as s
    s.configure(tmp)
    import app as tracker_app
    tracker_app.DB = tmp / "tracker" / "data" / "tracker.sqlite3"
    tracker_app.init()

    httpd = make_server("127.0.0.1", 0, tracker_app.app)
    port = httpd.server_port
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"
    token = tracker_app.S["AGENT_TOKEN"]
    try:
        try:
            request(base, "/api/today")
        except urllib.error.HTTPError as e:
            assert e.code == 401
        else:
            raise AssertionError("unauthorized access accepted")
        request(base, "/api/habits", "POST", {"id": "habit-focus", "title": "Focused work", "schedule": {"kind": "weekdays", "days": [0, 1, 2, 3, 4]}, "paused": False}, True, token)
        x = json.loads(request(base, "/api/today", bearer=True, token=token).read())
        assert any(i["id"] == "habit-focus" for i in x["items"])
        d = x["date"]
        request(base, "/api/complete", "POST", {"id": "habit-focus", "day": d, "state": "completed"}, True, token)
        x = json.loads(request(base, "/api/today", bearer=True, token=token).read())
        assert next(i for i in x["items"] if i["id"] == "habit-focus")["completed"]
        request(base, "/api/metrics", "POST", {"id": "energy", "label": "Energy", "kind": "rating", "unit": "/10", "min": 1, "max": 10, "aggregation": "mean", "chart": "line", "privacy": "private", "missing": "unknown"}, True, token)
        request(base, "/api/observations", "POST", {"id": "obs-energy-20260812", "metric_id": "energy", "day": d, "value": 7, "estimated": False, "description": "explicit test observation"}, True, token)
        dashboard = json.loads(request(base, "/api/dashboard", bearer=True, token=token).read())
        assert dashboard["metrics"][0]["coverage"] >= 1
        live_ledger = LIVE_ROOT / "life-knowledge-base" / "70-goals" / "events"
        if live_ledger.exists():
            for p in live_ledger.glob("*.md"):
                text = p.read_text(encoding="utf8")
                assert "habit-focus" not in text
                assert "obs-energy-20260812" not in text
        print("live smoke: PASS")
    finally:
        httpd.shutdown()

if __name__ == "__main__":
    main()
