"""Release gate tests (Python stdlib only)."""
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT/'pet_bathroom_tracker'
SCRIPT = ROOT/'tools'/'rehearse_recovery.py'
BOOTSTRAP = APP/'bootstrap.py'

def init_database(db):
    opts = db.parent/'options.json'
    opts.write_text(json.dumps({'timezone':'America/New_York'}))
    env = {**os.environ, 'DOG_TRACKER_DATABASE': str(db), 'DOG_TRACKER_OPTIONS': str(opts)}
    subprocess.run([sys.executable, str(BOOTSTRAP)], check=True, env=env, capture_output=True)
    return env

class ReleaseTests(unittest.TestCase):
    def test_manifest_contains_recovery_and_ingress_safeguards(self):
        config = yaml.safe_load((APP/'config.yaml').read_text())
        self.assertEqual(config['version'], '0.5.5')
        self.assertEqual(config['backup'], 'cold')
        self.assertTrue(config['ingress'])
        self.assertFalse(config['panel_admin'])
        self.assertNotIn('ports', config)
        self.assertEqual(config['watchdog'], 'http://[HOST]:[PORT:8099]/health')

    def test_dashboard_version_matches_manifest(self):
        manifest = yaml.safe_load((APP / 'config.yaml').read_text())
        html = (APP / 'templates' / 'index.html').read_text()
        self.assertIn(f'Preview {manifest["version"]}', html)
        self.assertNotIn('Shared through Home Assistant · Preview 0.4.0', html)

    def test_snapshot_restore_rehearsal_preserves_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp)/'tracker.db'
            init_database(db)
            with sqlite3.connect(db) as con:
                con.execute("INSERT INTO dogs (id,name,active,icon) VALUES (1,'Dog',1,'🐶'),(2,'Archived',0,'🐱')")
                con.execute("INSERT INTO bathroom_entries(dog_id,timestamp,pee,poop,notes) VALUES(1,'2026-10-23T17:20:00',1,0,'normal'),(2,'2026-10-23T16:00:00',0,1,'archived trip')")
                con.commit()
            result = subprocess.run([sys.executable, str(SCRIPT), str(db)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('2 pets, 2 trips', result.stdout)
            with sqlite3.connect(db) as con:
                self.assertEqual(con.execute('SELECT COUNT(*) FROM bathroom_entries').fetchone()[0],2)
                self.assertEqual(con.execute('SELECT active,icon FROM dogs WHERE id=2').fetchone(),(0,'🐱'))

    def test_invalid_foreign_key_refuses_startup(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp)/'tracker.db'
            env = init_database(db)
            with sqlite3.connect(db) as con:
                # Deliberately create orphan data as a recovery warning test.
                con.execute("INSERT INTO bathroom_entries(dog_id,timestamp,pee,poop,notes) VALUES(999,'2026-10-23T17:20:00',1,0,'orphan')")
                con.commit()
            result = subprocess.run([sys.executable, str(BOOTSTRAP)], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('orphaned bathroom entries', result.stderr)
            result = subprocess.run([sys.executable,str(SCRIPT), str(db)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('orphaned', result.stderr)

    def test_corrupted_database_is_not_reinitialized(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/'tracker.db'; db.write_bytes(b'not a SQLite database: do not overwrite')
            opts=Path(tmp)/'options.json'; opts.write_text('{}')
            original=db.read_bytes()
            env={**os.environ,'DOG_TRACKER_DATABASE':str(db),'DOG_TRACKER_OPTIONS':str(opts)}
            result=subprocess.run([sys.executable,str(BOOTSTRAP)],capture_output=True,text=True,env=env)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(db.read_bytes(),original)

if __name__ == '__main__': unittest.main()
