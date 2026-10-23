"""Database setup and idempotent schema migration tests; stdlib only."""
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BOOTSTRAP = Path(__file__).resolve().parents[1] / 'pet_bathroom_tracker' / 'bootstrap.py'

class DatabaseTests(unittest.TestCase):
    def run_bootstrap(self, database, options):
        env = {**os.environ, 'DOG_TRACKER_DATABASE': str(database),
               'DOG_TRACKER_OPTIONS': str(options)}
        subprocess.run([sys.executable, str(BOOTSTRAP)], check=True,
                       env=env, capture_output=True)

    def test_new_install_starts_empty_and_uses_icon_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file, options = Path(tmp) / 'tracker.db', Path(tmp) / 'options.json'
            options.write_text(json.dumps({'timezone':'America/New_York'}))
            for _ in range(2):
                self.run_bootstrap(db_file, options)
            with sqlite3.connect(db_file) as con:
                self.assertEqual(con.execute('SELECT COUNT(*) FROM dogs').fetchone()[0], 0)
                columns={row[1] for row in con.execute('PRAGMA table_info(dogs)')}
                self.assertIn('icon', columns)
                self.assertEqual(con.execute('PRAGMA integrity_check').fetchone()[0],'ok')

    def test_upgrade_old_database_preserves_pets_status_and_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file, options = Path(tmp) / 'tracker.db', Path(tmp) / 'options.json'
            options.write_text(json.dumps({'dog_1_name':'Old Dog', 'dog_2_name':'Other',
                                           'timezone':'America/New_York'}))
            with sqlite3.connect(db_file) as con:
                con.executescript("""
                  CREATE TABLE dogs (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
                         active INTEGER NOT NULL DEFAULT 1);
                  CREATE TABLE bathroom_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dog_id INTEGER NOT NULL REFERENCES dogs(id),
                    timestamp TEXT NOT NULL, pee INTEGER NOT NULL CHECK(pee IN (0,1)),
                    poop INTEGER NOT NULL CHECK(poop IN (0,1)), notes TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
                  INSERT INTO dogs(id,name,active) VALUES (1,'Renamed',1),(2,'Archive Me',0),(3,'Buddy',1);
                  INSERT INTO bathroom_entries(dog_id,timestamp,pee,poop,notes)
                    VALUES (1,'2026-10-23T18:00:00',1,0,'preserve'),
                           (2,'2026-10-23T18:05:00',0,1,'archived trip');
                """)
            for _ in range(2):
                self.run_bootstrap(db_file, options)
            with sqlite3.connect(db_file) as con:
                self.assertEqual(con.execute('SELECT name,active,icon FROM dogs ORDER BY id').fetchall(),
                                 [('Renamed',1,'🐶'),('Archive Me',0,'🐶'),('Buddy',1,'🐶')])
                self.assertEqual(con.execute('SELECT notes FROM bathroom_entries ORDER BY id').fetchall(),
                                 [('preserve',),('archived trip',)])
                self.assertEqual(con.execute('PRAGMA integrity_check').fetchone()[0], 'ok')

    def test_new_icon_persists_across_repeated_bootstraps(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file, options = Path(tmp) / 'tracker.db', Path(tmp) / 'options.json'
            options.write_text('{}')
            self.run_bootstrap(db_file, options)
            with sqlite3.connect(db_file) as con:
                con.execute("INSERT INTO dogs(name,active,icon) VALUES ('Cat',1,'🐱')")
                con.commit()
            for _ in range(2):
                self.run_bootstrap(db_file, options)
            with sqlite3.connect(db_file) as con:
                self.assertEqual(con.execute('SELECT name,icon FROM dogs').fetchall(), [('Cat','🐱')])

if __name__=='__main__':unittest.main()
