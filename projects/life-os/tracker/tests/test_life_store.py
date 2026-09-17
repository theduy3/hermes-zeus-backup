import json, os, sqlite3, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import life_store as s

def _write(*a, **k):
    k.setdefault("owner", "thor")
    return s.write(*a, **k)

class LifeStoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.old_kb, self.old_db = s.KB, s.DB
        s.configure(root)
        s.KB.mkdir()
        s.DB.parent.mkdir(parents=True, exist_ok=True)
        c = sqlite3.connect(s.DB)
        c.executescript(s.OPERATIONAL_SCHEMA)
        c.close()

    def tearDown(self):
        s.KB, s.DB = self.old_kb, self.old_db
        self.tmp.cleanup()

    def test_rebuild_from_markdown_and_restore(self):
        _write("health", "metric", "2026-08-12", {"metric_id": "weight", "value": 75.4}, event_id="evt-weight-1", source_ids=["src-thor-weight"])
        self.assertTrue(s.reconcile()["ok"])
        self.assertEqual(s.rebuild(), 1)
        os.unlink(s.DB)
        self.assertEqual(s.rebuild(), 1)
        self.assertTrue(s.reconcile()["ok"])

    def test_correction_supersedes_without_erasing_history(self):
        _write("health", "metric", "2026-08-12", {"value": 75.4}, event_id="evt-one")
        _write("health", "metric", "2026-08-12", {"value": 75.0}, event_id="evt-two", supersedes=["evt-one"])
        self.assertEqual([x["id"] for x in s.active(s.list_events())], ["evt-two"])
        self.assertEqual(len(s.list_events()), 2)

    def test_invalid_id_rejected_and_cache_tamper_detected(self):
        with self.assertRaises(ValueError):
            _write("health", "metric", "2026-08-12", {}, event_id="../bad")
        _write("goal", "goal", "2026-08-12", {"title": "x"}, event_id="goal-one", owner="life")
        c = sqlite3.connect(s.DB)
        c.execute("delete from cache_events")
        c.commit()
        c.close()
        self.assertFalse(s.reconcile()["ok"])

    def test_rebuild_operational_tracker_from_markdown(self):
        _write(
            "tracker",
            "metrics",
            "2026-08-12",
            {"record_id": "energy", "label": "Energy", "kind": "rating", "unit": "/10", "min": 1, "max": 10, "aggregation": "mean", "chart": "line", "privacy": "private", "missing": "unknown"},
            event_id="evt-metric",
            owner="tracker",
        )
        self.assertEqual(s.rebuild_tracker(), 1)
        c = sqlite3.connect(s.DB)
        self.assertEqual(c.execute("select count(*) from metrics").fetchone()[0], 1)
        c.close()

    def test_checkpoint(self):
        _write("finance", "event", "2026-08-12", {"description": "test"}, event_id="evt-finance-one", owner="finance")
        p = s.checkpoint("phase12-test-" + Path(self.tmp.name).name)
        self.assertTrue((p / "manifest.json").exists())
        self.assertTrue((p / "tracker" / "life_store.py").exists())

    def test_backup_restore_roundtrip(self):
        _write("goal", "goal", "2026-08-12", {"title": "G1", "area": "health", "status": "active", "done": "0", "review_date": "2026-09-01"}, event_id="goal-restore-1", owner="life")
        _write("tracker", "habits", "2026-08-12", {"record_id": "h1", "title": "Walk", "schedule": {"kind": "daily"}, "paused": False}, event_id="habit-restore-1", owner="tracker")
        s.rebuild_tracker()
        cp = s.checkpoint("phase12-backup-" + Path(self.tmp.name).name)
        sha_before = s.ledger_digest()
        import shutil
        shutil.rmtree(s.KB)
        os.unlink(s.DB)
        s.KB = cp / "life-knowledge-base"
        shutil.copy2(cp / "tracker.sqlite3", s.DB)
        self.assertEqual(s.ledger_digest(), sha_before)
        self.assertTrue(s.reconcile()["ok"])
        self.assertEqual(s.rebuild_tracker(), 2)
        c = sqlite3.connect(s.DB)
        self.assertEqual(c.execute("select count(*) from habits").fetchone()[0], 1)
        c.close()

    def test_interrupted_write_no_partial_cache(self):
        _write("health", "metric", "2026-08-12", {"value": 74.0}, event_id="evt-int-1")
        before = s.reconcile()
        self.assertTrue(before["ok"])
        real = s.append_event
        def boom(r, **_k):
            raise OSError("disk full simulated")
        s.append_event = boom
        with self.assertRaises(OSError):
            _write("health", "metric", "2026-08-12", {"value": 75.0}, event_id="evt-int-2")
        s.append_event = real
        self.assertTrue(s.reconcile()["ok"])
        c = sqlite3.connect(s.DB)
        n = c.execute("select count(*) from cache_events where id='evt-int-2'").fetchone()[0]
        c.close()
        self.assertEqual(n, 0)

    def test_concurrent_writes_no_duplicate_ids(self):
        import concurrent.futures as cf
        def w(i):
            try:
                _write("health", "metric", "2026-08-12", {"value": 70 + i}, event_id=f"evt-conc-{i}")
            except Exception as e:
                return f"err:{e}"
            return "ok"
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(w, range(20)))
        with self.assertRaises(ValueError):
            _write("health", "metric", "2026-08-12", {"value": 999}, event_id="evt-conc-0")
        self.assertTrue(s.reconcile()["ok"])
        self.assertEqual(len([x for x in s.active(s.list_events())]), 20)

    def test_provenance_source_link_recorded(self):
        _write("finance", "event", "2026-08-12", {"description": "rent obligation", "amount": 1800}, event_id="evt-prov-1", owner="finance", source_ids=["src-lease-2026", "vault:Finance/lease.pdf"])
        ev = [x for x in s.list_events() if x["id"] == "evt-prov-1"][0]
        self.assertEqual(set(ev["source_ids"]), {"src-lease-2026", "vault:Finance/lease.pdf"})
        self.assertEqual(ev["domain"], "finance")
        self.assertEqual(ev["epistemic"], "self_report")
        self.assertEqual(ev["owner"], "finance")
        s.rebuild()
        c = sqlite3.connect(s.DB)
        row = c.execute("select payload from cache_events where id='evt-prov-1'").fetchone()[0]
        c.close()
        self.assertIn("src-lease-2026", json.loads(row)["source_ids"])

    def test_production_schema_has_habit_day_unique(self):
        self.assertIn("unique(habit_id,day)", s.OPERATIONAL_SCHEMA)
        info = sqlite3.connect(s.DB).execute("pragma index_list(completions)").fetchall()
        self.assertTrue(info)

    def test_habit_toggled_twice_then_rebuild_tracker(self):
        _write("tracker", "habits", "2026-08-12", {"record_id": "h-walk", "title": "Walk", "schedule": {"kind": "daily"}, "paused": False}, event_id="habit-h-walk", owner="tracker")
        _write("tracker", "habit_completion", "2026-08-12", {"habit_id": "h-walk", "state": "completed"}, event_id="evt-complete-1", owner="tracker")
        _write("tracker", "habit_completion", "2026-08-12", {"habit_id": "h-walk", "state": "open"}, event_id="evt-complete-2", owner="tracker")
        self.assertEqual(s.rebuild_tracker(), 3)
        c = sqlite3.connect(s.DB)
        rows = list(c.execute("select id, habit_id, day, state from completions"))
        c.close()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][3], "open")
        self.assertEqual(rows[0][0], "evt-complete-2")

    def test_reconcile_detects_tampered_cache_payload(self):
        _write("health", "observation", "2026-08-13", {"weight_kg": 74.0}, event_id="thor-2026-08-13")
        self.assertTrue(s.reconcile()["ok"])
        c = sqlite3.connect(s.DB)
        payload = json.loads(c.execute("select payload from cache_events where id='thor-2026-08-13'").fetchone()[0])
        payload["payload"]["weight_kg"] = 999.0
        c.execute("update cache_events set payload=? where id='thor-2026-08-13'", (s.canonical_json(payload),))
        c.commit()
        c.close()
        rec = s.reconcile()
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["payload_mismatch"], ["thor-2026-08-13"])

    def test_reconcile_detects_tampered_summary(self):
        _write("health", "observation", "2026-08-13", {"weight_kg": 74.0}, event_id="thor-2026-08-13")
        self.assertTrue(s.reconcile()["ok"])
        summary = s.KB / "health_summary.md"
        summary.write_text("weight 9999 kg\n", encoding="utf8")
        rec = s.reconcile()
        self.assertFalse(rec["ok"])
        self.assertFalse(rec["digest_ok"])

    def test_ledger_digest_covers_all_kb_files(self):
        _write("health", "observation", "2026-08-13", {"weight_kg": 74.0}, event_id="thor-2026-08-13")
        extra = s.KB / "00-index"
        extra.mkdir()
        (extra / "master_index.md").write_text("# index\n", encoding="utf8")
        self.assertFalse(s.reconcile()["ok"])

    def test_owner_required_and_cross_owner_supersede_rejected(self):
        with self.assertRaises(TypeError):
            s.write("finance", "observation", "2026-08-13", {"liquid_cad": 0}, event_id="fin-1")
        _write("finance", "observation", "2026-08-13", {"liquid_cad": 0, "monthly_in_cad": 5952.92}, event_id="fin-1", owner="finance")
        with self.assertRaises(ValueError):
            _write("finance", "position", "2026-08-13", {"liquid_cad": 1}, event_id="charles-1", owner="charles", supersedes=["fin-1"])
        with self.assertRaises(ValueError):
            _write("finance", "observation", "2026-08-13", {"liquid_cad": 1}, event_id="fin-ghost", owner="finance", supersedes=["does-not-exist"])

    def test_correction_merges_predecessor_payload(self):
        _write(
            "finance",
            "observation",
            "2026-08-13",
            {"liquid_cad": 0.0, "monthly_in_cad": 5952.92, "liabilities": ["mortgage"], "goals": ["buffer"], "review_cadence": "monthly"},
            event_id="fin-2026-08-13",
            owner="finance",
        )
        rec = _write(
            "finance",
            "observation",
            "2026-08-13",
            {"monthly_out_cad": 2050.0, "note": "rent"},
            event_id="fin-2026-08-13-v2",
            owner="finance",
            supersedes=["fin-2026-08-13"],
        )
        self.assertEqual(rec["payload"]["monthly_out_cad"], 2050.0)
        self.assertEqual(rec["payload"]["liquid_cad"], 0.0)
        self.assertEqual(rec["payload"]["monthly_in_cad"], 5952.92)
        self.assertEqual(rec["payload"]["liabilities"], ["mortgage"])
        self.assertEqual(rec["payload"]["goals"], ["buffer"])
        replaced = _write(
            "finance",
            "observation",
            "2026-08-13",
            {"monthly_out_cad": 2100.0},
            event_id="fin-2026-08-13-v3",
            owner="finance",
            supersedes=["fin-2026-08-13-v2"],
            replace=True,
        )
        self.assertEqual(replaced["payload"], {"monthly_out_cad": 2100.0})

    def test_rebuild_refuses_to_drop_cache_only(self):
        _write("health", "observation", "2026-08-13", {"weight_kg": 74.0}, event_id="keep-1")
        c = sqlite3.connect(s.DB)
        c.execute("insert into cache_events values(?,?,?,?,?,?,?)", ("ghost-1", "health", "observation", "2026-08-13", "{}", "2026-08-13T00:00:00Z", "x.md"))
        c.commit()
        c.close()
        rec = s.reconcile()
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["cache_only"], ["ghost-1"])
        with self.assertRaises(ValueError):
            s.rebuild()
        self.assertEqual(s.rebuild(drop_cache_only=True), 1)
        self.assertTrue(s.reconcile()["ok"])

    def test_write_requires_owner(self):
        with self.assertRaises(ValueError):
            s.write("health", "observation", "2026-08-13", {"n": 1}, event_id="evt-x", owner="Thor")

class CrossProcessLockTest(unittest.TestCase):
    def test_concurrent_processes_no_duplicate_ids(self):
        import subprocess, textwrap
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "life-knowledge-base").mkdir()
        (root / "tracker" / "data").mkdir(parents=True)
        worker = textwrap.dedent(
            """
            import os, sys
            sys.path.insert(0, os.environ['LIFE_STORE_DIR'])
            import life_store as s
            s.configure(os.environ['LIFE_OS_ROOT'])
            start = int(sys.argv[1]); n = int(sys.argv[2])
            ok = err = 0
            for i in range(start, start + n):
                try:
                    s.write('health','metric','2026-08-12',{'value': i}, event_id=f'dup-{i % 30}', owner='thor')
                    ok += 1
                except Exception:
                    err += 1
            print(f'{ok} {err}')
            """
        )
        script = root / "worker.py"
        script.write_text(worker, encoding="utf8")
        env = os.environ.copy()
        env["LIFE_OS_ROOT"] = str(root)
        env["LIFE_STORE_DIR"] = str(Path(__file__).resolve().parents[1])
        ps = [
            subprocess.Popen([sys.executable, str(script), "0", "30"], env=env, stdout=subprocess.PIPE, text=True),
            subprocess.Popen([sys.executable, str(script), "0", "30"], env=env, stdout=subprocess.PIPE, text=True),
        ]
        outs = [p.communicate()[0] for p in ps]
        self.assertTrue(all(p.returncode == 0 for p in ps), outs)
        s.configure(root)
        events = s.list_events()
        ids = [e["id"] for e in events]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(s.reconcile()["ok"])
        tmp.cleanup()

if __name__ == "__main__":
    unittest.main()
