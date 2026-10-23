#!/usr/bin/env python3
"""Read-only verification + disposable SQLite backup/restore rehearsal.

Usage: python3 tools/rehearse_recovery.py /path/to/tracker.db

This does not decrypt Home Assistant backups or exercise Supervisor restore.
Do not submit your personal tracker.db to bug reports.
"""
import argparse
import sqlite3
import tempfile
from pathlib import Path

def inspect_database(db):
    integrity = db.execute('PRAGMA integrity_check').fetchall()
    if len(integrity) != 1 or integrity[0][0] != 'ok':
        raise RuntimeError('SQLite integrity check failed')
    if db.execute('PRAGMA foreign_key_check').fetchall():
        raise RuntimeError('Database contains orphaned records')
    pets = db.execute('SELECT id, name, active, icon FROM dogs ORDER BY id').fetchall()
    trips = db.execute('SELECT id, dog_id, timestamp, pee, poop, notes FROM bathroom_entries ORDER BY id').fetchall()
    return pets, trips

def run(source_path):
    source_path = Path(source_path).expanduser().resolve(strict=True)
    if not source_path.is_file():
        raise ValueError('Not a database file')
    # URI read-only protects the original database, even if run as root.
    with sqlite3.connect(source_path.as_uri() + '?mode=ro', uri=True) as source:
        before = inspect_database(source)
        with tempfile.TemporaryDirectory(prefix='pet-tracker-restore-') as temp:
            temp = Path(temp)
            snapshot_file = temp / 'snapshot.db'
            restored_file = temp / 'restored.db'
            with sqlite3.connect(snapshot_file) as snapshot:
                source.backup(snapshot)
                assert inspect_database(snapshot) == before, 'Backup snapshot differs from source'
            # Restore into a different disposable database, never the original.
            with sqlite3.connect(snapshot_file) as snapshot, sqlite3.connect(restored_file) as restored:
                snapshot.backup(restored)
                assert inspect_database(restored) == before, 'Restored data differs from snapshot'
    pets, trips = before
    print(f'PASS: integrity, foreign keys, snapshot and disposable restore ({len(pets)} pets, {len(trips)} trips).')
    print('Source database left unchanged. This does NOT validate a Home Assistant encrypted backup archive.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('database', help='An extracted/copy of tracker.db (not an encrypted HA backup)')
    args = parser.parse_args()
    try:
        run(args.database)
    except (sqlite3.Error, OSError, RuntimeError, ValueError, AssertionError) as error:
        parser.exit(1, f'FAIL: {error}\n')
