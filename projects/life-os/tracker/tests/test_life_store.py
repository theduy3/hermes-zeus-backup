import os, sqlite3, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import life_store as s

class LifeStoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); root=Path(self.tmp.name); self.old_kb,self.old_db=s.KB,s.DB
        s.KB=root/'kb';s.DB=root/'tracker.sqlite3';s.KB.mkdir()
        c=sqlite3.connect(s.DB); c.executescript('''create table goals(id text primary key,title text,area text,status text,done text,review_date text);create table projects(id text primary key,title text,status text,phase text,blocker text,next_action text,goal_id text);create table habits(id text primary key,title text,schedule text,paused integer,goal_id text,project_id text);create table completions(id text primary key,habit_id text,day text,state text);create table metrics(id text primary key,label text,kind text,unit text,min real,max real,aggregation text,chart text,privacy text,missing text);create table observations(id text primary key,metric_id text,day text,value text,estimated integer,description text,recorded_at text,deleted integer);''');c.close()
    def tearDown(self): s.KB,s.DB=self.old_kb,self.old_db;self.tmp.cleanup()
    def test_rebuild_from_markdown_and_restore(self):
        s.write('health','metric','2026-08-12',{'metric_id':'weight','value':75.4},event_id='evt-weight-1',source_ids=['src-thor-weight'])
        self.assertTrue(s.reconcile()['ok']); self.assertEqual(s.rebuild(),1)
        os.unlink(s.DB); self.assertEqual(s.rebuild(),1); self.assertTrue(s.reconcile()['ok'])
    def test_correction_supersedes_without_erasing_history(self):
        s.write('health','metric','2026-08-12',{'value':75.4},event_id='evt-one')
        s.write('health','metric','2026-08-12',{'value':75.0},event_id='evt-two',supersedes=['evt-one'])
        self.assertEqual([x['id'] for x in s.active(s.list_events())],['evt-two']); self.assertEqual(len(s.list_events()),2)
    def test_invalid_id_rejected_and_cache_tamper_detected(self):
        with self.assertRaises(ValueError): s.write('health','metric','2026-08-12',{},event_id='../bad')
        s.write('goal','goal','2026-08-12',{'title':'x'},event_id='goal-one')
        c=sqlite3.connect(s.DB);c.execute("delete from cache_events");c.commit();c.close(); self.assertFalse(s.reconcile()['ok'])
    def test_rebuild_operational_tracker_from_markdown(self):
        s.write('tracker','metrics','2026-08-12',{'record_id':'energy','label':'Energy','kind':'rating','unit':'/10','min':1,'max':10,'aggregation':'mean','chart':'line','privacy':'private','missing':'unknown'},event_id='evt-metric')
        self.assertEqual(s.rebuild_tracker(),1)
        c=sqlite3.connect(s.DB); self.assertEqual(c.execute('select count(*) from metrics').fetchone()[0],1);c.close()
    def test_checkpoint(self):
        s.write('finance','event','2026-08-12',{'description':'test'},event_id='evt-finance-one')
        p=s.checkpoint('phase12-test-'+Path(self.tmp.name).name); self.assertTrue((p/'manifest.json').exists())

    def test_backup_restore_roundtrip(self):
        # Phase 1.3 backup/restore: a checkpoint preserves ledger + cache and
        # restoring it reproduces the same operational tracker state.
        s.write('goal','goal','2026-08-12',{'title':'G1','area':'health','status':'active','done':'0','review_date':'2026-09-01'},event_id='goal-restore-1')
        s.write('tracker','habits','2026-08-12',{'record_id':'h1','title':'Walk','schedule':{'kind':'daily'},'paused':False},event_id='habit-restore-1')
        s.rebuild_tracker()
        cp=s.checkpoint('phase12-backup-'+Path(self.tmp.name).name)
        sha_before=s.ledger_digest()
        # Simulate total loss of live state, then restore from checkpoint.
        import shutil
        shutil.rmtree(s.KB); os.unlink(s.DB)
        s.KB=cp/'life-knowledge-base'; shutil.copy2(cp/'tracker.sqlite3',s.DB)
        self.assertEqual(s.ledger_digest(),sha_before)
        self.assertTrue(s.reconcile()['ok'])
        self.assertEqual(s.rebuild_tracker(),2)
        c=sqlite3.connect(s.DB); self.assertEqual(c.execute('select count(*) from habits').fetchone()[0],1); c.close()

    def test_interrupted_write_no_partial_cache(self):
        # Phase 1.3 interrupted-write: if the Markdown ledger write fails,
        # the SQLite cache must NOT be updated (no partial/orphaned cache rows).
        s.write('health','metric','2026-08-12',{'value':74.0},event_id='evt-int-1')
        before=s.reconcile(); self.assertTrue(before['ok'])
        real=s.append_event
        def boom(r):
            raise OSError('disk full simulated')
        s.append_event=boom
        with self.assertRaises(OSError):
            s.write('health','metric','2026-08-12',{'value':75.0},event_id='evt-int-2')
        s.append_event=real
        # Cache must still be consistent with the surviving Markdown (no evt-int-2).
        self.assertTrue(s.reconcile()['ok'])
        c=sqlite3.connect(s.DB); n=c.execute("select count(*) from cache_events where id='evt-int-2'").fetchone()[0]; c.close()
        self.assertEqual(n,0)

    def test_concurrent_writes_no_duplicate_ids(self):
        # Phase 1.3 concurrency: parallel writes with distinct ids and one
        # duplicate must leave the ledger and cache consistent and reject the dup.
        import concurrent.futures as cf
        def w(i):
            try: s.write('health','metric','2026-08-12',{'value':70+i},event_id=f'evt-conc-{i}')
            except Exception as e: return f'err:{e}'
            return 'ok'
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(w,range(20)))
        # Now attempt a duplicate id — must be rejected, not silently overwritten.
        with self.assertRaises(ValueError):
            s.write('health','metric','2026-08-12',{'value':999},event_id='evt-conc-0')
        self.assertTrue(s.reconcile()['ok'])
        self.assertEqual(len([x for x in s.active(s.list_events())]),20)

    def test_provenance_source_link_recorded(self):
        # Phase 2 provenance: every consequential record must carry a source id
        # and be reconstructable from its Markdown ledger block.
        s.write('finance','event','2026-08-12',{'description':'rent obligation','amount':1800},event_id='evt-prov-1',source_ids=['src-lease-2026','vault:Finance/lease.pdf'])
        ev=[x for x in s.list_events() if x['id']=='evt-prov-1'][0]
        self.assertEqual(set(ev['source_ids']),{'src-lease-2026','vault:Finance/lease.pdf'})
        self.assertEqual(ev['domain'],'finance'); self.assertEqual(ev['epistemic'],'self_report')
        # Rebuild must preserve the source link in the cache payload.
        s.rebuild()
        c=sqlite3.connect(s.DB); row=c.execute("select payload from cache_events where id='evt-prov-1'").fetchone()[0]; c.close()
        import json as _j
        self.assertIn('src-lease-2026',_j.loads(row)['source_ids'])

if __name__=='__main__': unittest.main()
