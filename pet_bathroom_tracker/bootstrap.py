"""Initialize or migrate a persistent tracker database, preserving existing records.

New installations start with zero pets and use the welcome screen.
"""
import json
import os
import sqlite3
from pathlib import Path
from zoneinfo import ZoneInfo

database = Path(os.environ.get('DOG_TRACKER_DATABASE', '/data/tracker.db'))
options_path = Path(os.environ.get('DOG_TRACKER_OPTIONS', '/data/options.json'))
options = json.loads(options_path.read_text()) if options_path.exists() else {}
tz_name = str(options.get('timezone', 'America/New_York')).strip()
ZoneInfo(tz_name)  # fail clearly on invalid timezone
database.parent.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(database) as connection:
    connection.execute('PRAGMA foreign_keys = ON')
    # Detect damaged existing databases before attempting any schema migration.
    if database.exists() and database.stat().st_size > 0:
        preflight = connection.execute('PRAGMA integrity_check').fetchall()
        if len(preflight) != 1 or preflight[0][0] != 'ok':
            raise RuntimeError('Existing SQLite database failed its integrity check; restore from backup')
    connection.executescript('''
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS bathroom_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dog_id INTEGER NOT NULL REFERENCES dogs(id),
            timestamp TEXT NOT NULL,
            pee INTEGER NOT NULL CHECK (pee IN (0,1)),
            poop INTEGER NOT NULL CHECK (poop IN (0,1)),
            notes TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_entries_timestamp ON bathroom_entries(timestamp);
        CREATE INDEX IF NOT EXISTS idx_entries_dog_timestamp ON bathroom_entries(dog_id, timestamp);
    ''')
    # Upgrade existing 0.1–0.3 databases in-place. Existing pets receive the
    # original dog icon; neither names nor archive status nor entries change.
    columns = {row[1] for row in connection.execute('PRAGMA table_info(dogs)')}
    if 'icon' not in columns:
        connection.execute("ALTER TABLE dogs ADD COLUMN icon TEXT NOT NULL DEFAULT '🐶'")
    # No automatic pets on new installs; the welcome screen handles setup.
    connection.commit()
    results = connection.execute('PRAGMA integrity_check').fetchall()
    if len(results) != 1 or results[0][0] != 'ok':
        raise RuntimeError('SQLite integrity check failed after initialization')
    orphan_rows = connection.execute('PRAGMA foreign_key_check').fetchall()
    if orphan_rows:
        raise RuntimeError('SQLite has orphaned bathroom entries; restore from backup')

print('Pet Bathroom Tracker database ready', flush=True)
