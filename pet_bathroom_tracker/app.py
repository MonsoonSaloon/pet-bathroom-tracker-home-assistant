import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from zoneinfo import ZoneInfo

from flask import Flask, jsonify, render_template, request, abort

app = Flask(__name__)
# Avoid accepting unexpectedly large JSON payloads on write endpoints.
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024
PET_ICONS = ('🐶', '🐱', '🐰', '🐹', '🐦', '🐢', '🐾', '🐴', '🐸', '🐠')
SQLITE_MAX_ID = 2**63 - 1
# Storage survives Home Assistant app restarts and updates.
DATABASE = os.environ.get('DOG_TRACKER_DATABASE', '/data/tracker.db')
TZ = ZoneInfo(os.environ.get('DOG_TRACKER_TIMEZONE', 'America/New_York'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@contextmanager
def get_db():
    # Unlike sqlite3.Connection's context manager, this closes the database
    # connection on every request, including failed writes.
    db = sqlite3.connect(DATABASE, timeout=10)
    try:
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
        db.execute('PRAGMA busy_timeout = 10000')
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.url_value_preprocessor
def reject_invalid_url_ids(endpoint, values):
    # Werkzeug's integer URL converter accepts non-negative Python integers,
    # including numbers larger than SQLite's signed 64-bit INTEGER type.
    # Reject those IDs before any query attempts to bind them.
    if not values:
        return
    for key in ('dog_id', 'entry_id'):
        value = values.get(key)
        if value is not None and not (1 <= value <= SQLITE_MAX_ID):
            abort(404)


@app.before_request
def ingress_only():
    # HA Supervisor's Ingress proxy is the only allowed source in production.
    # No host port is exposed in the app manifest. Dev tests can set this to 0.
    if os.environ.get('DOG_TRACKER_INGRESS_ONLY', '1') == '1':
        if request.remote_addr != '172.30.32.2':
            abort(403)


@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


def parse_date(value):
    if not isinstance(value, str):
        raise ValueError('Date must be YYYY-MM-DD')
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError('Date must be YYYY-MM-DD') from exc
    if parsed.isoformat() != value:
        raise ValueError('Date must be YYYY-MM-DD')
    return parsed


def parse_timestamp(value):
    """Store a local wall-clock timestamp as YYYY-MM-DDTHH:MM:SS.

    The date/time input is intentionally local, so a late entry can be edited easily.
    """
    if not isinstance(value, str):
        raise ValueError('timestamp must be a local ISO date and time')
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError('timestamp must be YYYY-MM-DDTHH:MM') from exc
    if parsed.tzinfo is not None:
        raise ValueError('timestamp must be local time without a timezone offset')
    if parsed.second or parsed.microsecond:
        raise ValueError('timestamp must use minute precision')
    if len(value) != 16 or value[10] != 'T':
        raise ValueError('timestamp must be YYYY-MM-DDTHH:MM')
    return parsed.strftime('%Y-%m-%dT%H:%M:%S')


def parse_pet_id(value):
    # JSON floating-point values must never be silently truncated to pet IDs.
    # Accept integer IDs and canonical decimal strings for API compatibility.
    if type(value) is int:
        pet_id = value
    elif isinstance(value, str) and re.fullmatch(r'[1-9][0-9]*', value) and len(value) <= 19:
        pet_id = int(value)
    else:
        raise ValueError('Valid dog_id is required')
    if not (1 <= pet_id <= SQLITE_MAX_ID):
        raise ValueError('Valid dog_id is required')
    return pet_id


def validate_entry(payload):
    if not isinstance(payload, dict):
        raise ValueError('Expected a JSON object')
    dog_id = parse_pet_id(payload.get('dog_id'))
    pee, poop = payload.get('pee'), payload.get('poop')
    if type(pee) is not bool or type(poop) is not bool:
        raise ValueError('pee and poop must be true or false')
    if not (pee or poop):
        raise ValueError('Select pee, poop, or both')
    timestamp = parse_timestamp(payload.get('timestamp'))
    notes = payload.get('notes', '')
    if notes is None:
        notes = ''
    if not isinstance(notes, str) or len(notes) > 1000:
        raise ValueError('notes must be text of at most 1000 characters')
    return dog_id, timestamp, int(pee), int(poop), notes.strip()


def present_entry(row):
    entry = dict(row)
    entry['pee'] = bool(entry['pee'])
    entry['poop'] = bool(entry['poop'])
    return entry


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error='Invalid request'), 400


@app.route('/health', methods=['GET'])
def health():
    # Supervisor may call this URL for Watchdog checks. A running web server
    # with a missing/unreadable database must not appear healthy.
    try:
        if not os.path.isfile(DATABASE):
            return jsonify(status='unavailable'), 503
        with get_db() as db:
            db.execute('SELECT id FROM dogs LIMIT 1').fetchone()
            db.execute('SELECT id FROM bathroom_entries LIMIT 1').fetchone()
    except sqlite3.Error:
        app.logger.exception('Health check failed: database unavailable')
        return jsonify(status='unavailable'), 503
    return jsonify(status='ok', application='Pet Bathroom Tracker')


@app.route('/api/dogs', methods=['GET'])
def dogs():
    with get_db() as db:
        rows = db.execute('SELECT id, name, active, icon FROM dogs ' +
                          ('' if request.args.get('include_inactive') == '1' else 'WHERE active = 1 ') +
                          'ORDER BY id').fetchall()
    return jsonify([dict(row) for row in rows])




def validate_pet_name(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get('name'), str):
        raise ValueError('Pet name is required')
    name = payload['name'].strip()
    if not 1 <= len(name) <= 60:
        raise ValueError('Pet name must contain 1–60 characters')
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in name):
        raise ValueError('Pet name contains invalid characters')
    return name


def validate_pet_icon(payload):
    icon = payload.get('icon', '🐶')
    if not isinstance(icon, str) or icon not in PET_ICONS:
        raise ValueError('Choose one of the available pet icons')
    return icon


def name_exists(db, name, exclude_id=None):
    if exclude_id is None:
        row = db.execute('SELECT id FROM dogs WHERE name = ? COLLATE NOCASE', (name,)).fetchone()
    else:
        row = db.execute('SELECT id FROM dogs WHERE name = ? COLLATE NOCASE AND id != ?',
                         (name, exclude_id)).fetchone()
    return row is not None


@app.route('/api/dogs', methods=['POST'])
def add_dog():
    try:
        payload = request.get_json(silent=True)
        name = validate_pet_name(payload)
        icon = validate_pet_icon(payload)
    except ValueError:
        return jsonify(error='Invalid pet name or icon'), 400
    with get_db() as db:
        if name_exists(db, name):
            return jsonify(error='A pet with that name already exists, including archived pets'), 409
        cur = db.execute('INSERT INTO dogs(name, active, icon) VALUES (?, 1, ?)', (name, icon))
        db.commit()
        row_id = cur.lastrowid
    return jsonify(id=row_id, name=name, active=1, icon=icon), 201


@app.route('/api/dogs/<int:dog_id>', methods=['PATCH'])
def rename_dog(dog_id):
    try:
        payload = request.get_json(silent=True)
        name = validate_pet_name(payload)
        icon = validate_pet_icon(payload)
    except ValueError:
        return jsonify(error='Invalid pet name or icon'), 400
    with get_db() as db:
        if not db.execute('SELECT id FROM dogs WHERE id=?', (dog_id,)).fetchone():
            return jsonify(error='Pet not found'), 404
        if name_exists(db, name, dog_id):
            return jsonify(error='A pet with that name already exists'), 409
        db.execute('UPDATE dogs SET name=?, icon=? WHERE id=?', (name, icon, dog_id))
        db.commit()
    return jsonify(id=dog_id, name=name, icon=icon, message='Pet updated')


@app.route('/api/dogs/<int:dog_id>', methods=['DELETE'])
def archive_dog(dog_id):
    with get_db() as db:
        row = db.execute('SELECT active FROM dogs WHERE id=?', (dog_id,)).fetchone()
        if not row:
            return jsonify(error='Pet not found'), 404
        if not row['active']:
            return jsonify(error='Pet is already archived'), 409
        count = db.execute('SELECT COUNT(*) FROM dogs WHERE active=1').fetchone()[0]
        if count <= 1:
            return jsonify(error='Keep at least one active pet'), 409
        db.execute('UPDATE dogs SET active=0 WHERE id=?', (dog_id,))
        db.commit()
    # The existing bathroom entries are never deleted.
    return jsonify(id=dog_id, message='Pet archived; past trips preserved')


@app.route('/api/dogs/<int:dog_id>/restore', methods=['POST'])
def restore_dog(dog_id):
    with get_db() as db:
        row = db.execute('SELECT active FROM dogs WHERE id=?', (dog_id,)).fetchone()
        if not row:
            return jsonify(error='Pet not found'), 404
        if row['active']:
            return jsonify(error='Pet is already active'), 409
        db.execute('UPDATE dogs SET active=1 WHERE id=?', (dog_id,))
        db.commit()
    return jsonify(id=dog_id, message='Pet restored')


@app.route('/api/entries', methods=['GET'])
def entries():
    try:
        chosen = parse_date(request.args.get('date', datetime.now(TZ).date().isoformat()))
    except ValueError:
        return jsonify(error='Invalid date; use YYYY-MM-DD'), 400
    with get_db() as db:
        rows = db.execute('''
            SELECT e.id, e.dog_id, d.name AS dog_name, e.timestamp,
                   e.pee, e.poop, e.notes, e.created_at, e.updated_at
              FROM bathroom_entries e JOIN dogs d ON d.id = e.dog_id
             WHERE substr(e.timestamp, 1, 10) = ?
             ORDER BY e.timestamp ASC, e.id ASC
        ''', (chosen.isoformat(),)).fetchall()
    return jsonify([present_entry(row) for row in rows])


@app.route('/api/entries', methods=['POST'])
def add_entry():
    try:
        dog_id, timestamp, pee, poop, notes = validate_entry(request.get_json(silent=True))
    except ValueError:
        return jsonify(error='Invalid trip details; check pet, time, pee/poop, and notes'), 400
    with get_db() as db:
        dog = db.execute('SELECT id FROM dogs WHERE id = ? AND active = 1', (dog_id,)).fetchone()
        if not dog:
            return jsonify(error='Pet not found'), 404
        cur = db.execute('''
            INSERT INTO bathroom_entries (dog_id, timestamp, pee, poop, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (dog_id, timestamp, pee, poop, notes))
        db.commit()
        new_id = cur.lastrowid
    return jsonify(id=new_id, message='Entry saved'), 201


@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
def edit_entry(entry_id):
    try:
        dog_id, timestamp, pee, poop, notes = validate_entry(request.get_json(silent=True))
    except ValueError:
        return jsonify(error='Invalid trip details; check pet, time, pee/poop, and notes'), 400
    with get_db() as db:
        existing = db.execute('SELECT dog_id FROM bathroom_entries WHERE id=?', (entry_id,)).fetchone()
        if not existing:
            return jsonify(error='Entry not found'), 404
        target = db.execute('SELECT active FROM dogs WHERE id=?', (dog_id,)).fetchone()
        # Past records of archived pets remain editable, but new records cannot
        # be reassigned to an archived pet.
        if not target or (not target['active'] and dog_id != existing['dog_id']):
            return jsonify(error='Pet is archived or not found'), 404
        cur = db.execute('''
            UPDATE bathroom_entries
               SET dog_id = ?, timestamp = ?, pee = ?, poop = ?, notes = ?,
                   updated_at = CURRENT_TIMESTAMP
             WHERE id = ?
        ''', (dog_id, timestamp, pee, poop, notes, entry_id))
        db.commit()
        if not cur.rowcount:
            return jsonify(error='Entry not found'), 404
    return jsonify(id=entry_id, message='Entry updated')


@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    with get_db() as db:
        cur = db.execute('DELETE FROM bathroom_entries WHERE id = ?', (entry_id,))
        db.commit()
        if not cur.rowcount:
            return jsonify(error='Entry not found'), 404
    return jsonify(id=entry_id, message='Entry deleted')


@app.route('/api/summary', methods=['GET'])
def summary():
    try:
        chosen = parse_date(request.args.get('date', datetime.now(TZ).date().isoformat()))
    except ValueError:
        return jsonify(error='Invalid date; use YYYY-MM-DD'), 400
    with get_db() as db:
        rows = db.execute('''
            SELECT d.id AS dog_id, d.name AS dog_name,
                   COALESCE(SUM(e.pee), 0) AS pee_count,
                   COALESCE(SUM(e.poop), 0) AS poop_count,
                   COUNT(e.id) AS trip_count
              FROM dogs d
              LEFT JOIN bathroom_entries e ON e.dog_id = d.id
                    AND substr(e.timestamp, 1, 10) = ?
             WHERE d.active = 1
             GROUP BY d.id, d.name
             ORDER BY d.id
        ''', (chosen.isoformat(),)).fetchall()
    return jsonify(date=chosen.isoformat(), dogs=[dict(row) for row in rows])


@app.route('/api/latest', methods=['GET'])
def latest():
    with get_db() as db:
        dogs = db.execute('SELECT id, name FROM dogs WHERE active = 1 ORDER BY id').fetchall()
        result = []
        for dog in dogs:
            pee = db.execute('''
                SELECT timestamp FROM bathroom_entries
                 WHERE dog_id = ? AND pee = 1
                 ORDER BY timestamp DESC, id DESC LIMIT 1
            ''', (dog['id'],)).fetchone()
            poop = db.execute('''
                SELECT timestamp FROM bathroom_entries
                 WHERE dog_id = ? AND poop = 1
                 ORDER BY timestamp DESC, id DESC LIMIT 1
            ''', (dog['id'],)).fetchone()
            result.append(dict(dog_id=dog['id'], dog_name=dog['name'],
                               last_pee=pee['timestamp'] if pee else None,
                               last_poop=poop['timestamp'] if poop else None))
    return jsonify(result)


