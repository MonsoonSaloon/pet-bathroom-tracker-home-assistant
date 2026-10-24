"""Flask API security and lifecycle regression tests; disposable databases only."""
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / 'pet_bathroom_tracker'
APP_PATH = APP_DIR / 'app.py'
BOOTSTRAP = APP_DIR / 'bootstrap.py'
MAX_SQLITE_ID = 2**63 - 1
TRUSTED = {'environ_overrides': {'REMOTE_ADDR': '172.30.32.2'}}
UNTRUSTED = {'environ_overrides': {'REMOTE_ADDR': '127.0.0.1'}}


class APITests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.db_file = Path(self.folder.name) / 'tracker.db'
        options = Path(self.folder.name) / 'options.json'
        options.write_text(json.dumps({'timezone': 'America/New_York'}), encoding='utf-8')
        env = {
            **os.environ,
            'DOG_TRACKER_DATABASE': str(self.db_file),
            'DOG_TRACKER_OPTIONS': str(options),
            'DOG_TRACKER_TIMEZONE': 'America/New_York',
            'DOG_TRACKER_INGRESS_ONLY': '1',
        }
        subprocess.run([sys.executable, str(BOOTSTRAP)], env=env,
                       check=True, capture_output=True, text=True)
        module_name = 'tracker_api_under_test_' + self._testMethodName
        spec = importlib.util.spec_from_file_location(module_name, APP_PATH)
        module = importlib.util.module_from_spec(spec)
        # Flask resolves its template directory through the imported module.
        sys.modules[module_name] = module
        self.addCleanup(lambda: sys.modules.pop(module_name, None))
        with patch.dict(os.environ, env):
            spec.loader.exec_module(module)
        module.app.testing = True
        self.client = module.app.test_client()

    def get(self, path, trusted=True):
        return self.client.get(path, **(TRUSTED if trusted else UNTRUSTED))

    def send(self, method, path, payload=None, trusted=True, **extra):
        kwargs = dict(TRUSTED if trusted else UNTRUSTED)
        kwargs.update(extra)
        if payload is not None:
            kwargs['json'] = payload
        return self.client.open(path, method=method, **kwargs)

    def make_pet(self, name='Biscuit', icon='🐶'):
        response = self.send('POST', '/api/dogs', {'name': name, 'icon': icon})
        self.assertEqual(response.status_code, 201, response.get_data(as_text=True))
        return response.json['id']

    def make_trip(self, dog_id, **changes):
        payload = {
            'dog_id': dog_id, 'timestamp': '2026-10-23T19:29',
            'pee': True, 'poop': False, 'notes': 'Normal entry',
        }
        payload.update(changes)
        response = self.send('POST', '/api/entries', payload)
        self.assertEqual(response.status_code, 201, response.get_data(as_text=True))
        return response.json['id']

    def test_ingress_blocks_untrusted_requests_including_mutations(self):
        self.assertEqual(self.get('/health', trusted=False).status_code, 403)
        self.assertEqual(self.get('/', trusted=False).status_code, 403)
        self.assertEqual(self.get('/api/dogs', trusted=False).status_code, 403)
        result = self.send('POST', '/api/dogs', {'name': 'Should Not Exist'}, trusted=False)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(self.get('/api/dogs').json, [])

    def test_health_and_response_security_headers(self):
        result = self.get('/health')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['status'], 'ok')
        self.assertEqual(result.headers['Cache-Control'], 'no-store')
        self.assertEqual(result.headers['X-Content-Type-Options'], 'nosniff')

    def test_health_unavailable_if_database_is_missing(self):
        self.db_file.unlink()
        result = self.get('/health')
        self.assertEqual(result.status_code, 503)
        self.assertEqual(result.json['status'], 'unavailable')

    def test_pet_creation_listing_rename_and_duplicate_detection(self):
        pet_id = self.make_pet()
        self.assertEqual(self.get('/api/dogs').json[0]['id'], pet_id)
        self.assertEqual(self.send('POST', '/api/dogs', {'name': 'biscuit'}).status_code, 409)
        changed = self.send('PATCH', f'/api/dogs/{pet_id}',
                            {'name': 'Biscuit Junior', 'icon': '🐱'})
        self.assertEqual(changed.status_code, 200)
        self.assertEqual(self.get('/api/dogs').json[0]['icon'], '🐱')
        self.assertEqual(self.get('/api/dogs').json[0]['name'], 'Biscuit Junior')

    def test_pet_name_icon_and_json_validation(self):
        for payload in ({}, [], {'name': ''}, {'name': 'x' * 61},
                        {'name': 'Bad\nName'}, {'name': 'Valid', 'icon': 'not-icon'}):
            with self.subTest(payload=payload):
                result = self.send('POST', '/api/dogs', payload)
                self.assertEqual(result.status_code, 400)
        malformed = self.client.post('/api/dogs', data='{',
                                     content_type='application/json', **TRUSTED)
        self.assertEqual(malformed.status_code, 400)
        self.assertNotIn('Traceback', malformed.get_data(as_text=True))

    def test_request_payload_size_limit(self):
        result = self.client.post('/api/dogs', data='x' * (64 * 1024 + 1),
                                  content_type='application/json', **TRUSTED)
        self.assertEqual(result.status_code, 413)

    def test_json_numeric_dog_ids_reject_floats_booleans_and_overflows(self):
        pet_id = self.make_pet()
        good = {
            'dog_id': pet_id, 'timestamp': '2026-10-23T19:29',
            'pee': True, 'poop': False, 'notes': '',
        }
        for bad in (True, False, 0, -1, 1.9, float('inf'), float('nan'),
                    MAX_SQLITE_ID + 1, 10**60, '01', '1.0', '-1', 'bad', ''):
            with self.subTest(dog_id=repr(bad)):
                result = self.send('POST', '/api/entries', {**good, 'dog_id': bad})
                self.assertEqual(result.status_code, 400, result.get_data(as_text=True))
        self.assertEqual(self.get('/api/entries?date=2026-10-23').json, [])

    def test_canonical_decimal_string_id_is_supported(self):
        pet_id = self.make_pet()
        self.make_trip(str(pet_id))
        entries = self.get('/api/entries?date=2026-10-23').json
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['dog_id'], pet_id)

    def test_invalid_url_identifiers_return_404_not_500(self):
        pet_id = self.make_pet()
        trip_id = self.make_trip(pet_id)
        oversized = str(MAX_SQLITE_ID + 1)
        for method, path, body in (
            ('PATCH', '/api/dogs/' + oversized, {'name': 'Other'}),
            ('DELETE', '/api/dogs/' + oversized, None),
            ('POST', '/api/dogs/' + oversized + '/restore', None),
            ('PUT', '/api/entries/' + oversized, {'dog_id': pet_id}),
            ('DELETE', '/api/entries/' + oversized, None),
            ('PATCH', '/api/dogs/0', {'name': 'Other'}),
            ('DELETE', '/api/entries/0', None),
        ):
            with self.subTest(method=method, path=path):
                response = self.send(method, path, body)
                self.assertEqual(response.status_code, 404, response.get_data(as_text=True))
        self.assertEqual(self.get('/api/dogs').json[0]['name'], 'Biscuit')
        self.assertEqual(len(self.get('/api/entries?date=2026-10-23').json), 1)

    def test_trip_field_validation(self):
        pet_id = self.make_pet()
        valid = {'dog_id': pet_id, 'timestamp': '2026-10-23T19:29',
                 'pee': True, 'poop': False, 'notes': ''}
        for change in (
            {'timestamp': '2026-10-23T19:29:01'},
            {'timestamp': '2026-10-23T19:29Z'},
            {'timestamp': 'not-a-date'},
            {'timestamp': '2026-13-23T19:29'},
            {'pee': 1}, {'poop': 'false'}, {'pee': False, 'poop': False},
            {'notes': ['array']}, {'notes': 'z' * 1001},
        ):
            with self.subTest(change=change):
                result = self.send('POST', '/api/entries', {**valid, **change})
                self.assertEqual(result.status_code, 400, result.get_data(as_text=True))

    def test_invalid_dates_are_rejected_on_read_endpoints(self):
        for path in ('/api/entries?date=2026-02-30', '/api/summary?date=2026-10-1'):
            self.assertEqual(self.get(path).status_code, 400)

    def test_unknown_pet_is_not_accepted_for_new_entry(self):
        self.assertEqual(self.send('POST', '/api/entries', {
            'dog_id': 100, 'timestamp': '2026-10-23T19:29',
            'pee': True, 'poop': False, 'notes': '',
        }).status_code, 404)

    def test_pet_archiving_restoring_and_trip_retention(self):
        first = self.make_pet()
        second = self.make_pet('Whiskers', '🐱')
        trip = self.make_trip(first)
        self.assertEqual(self.send('DELETE', f'/api/dogs/{first}').status_code, 200)
        active_ids = [p['id'] for p in self.get('/api/dogs').json]
        self.assertEqual(active_ids, [second])
        self.assertEqual(len(self.get('/api/dogs?include_inactive=1').json), 2)
        self.assertEqual(len(self.get('/api/entries?date=2026-10-23').json), 1)
        # Editing an archived pet's existing entry is allowed, but creating
        # another entry while it is archived is not.
        invalid_new = self.send('POST', '/api/entries', {
            'dog_id': first, 'timestamp': '2026-10-23T19:30',
            'pee': True, 'poop': False, 'notes': '',
        })
        self.assertEqual(invalid_new.status_code, 404)
        edit = self.send('PUT', f'/api/entries/{trip}', {
            'dog_id': first, 'timestamp': '2026-10-23T19:29',
            'pee': False, 'poop': True, 'notes': 'Archived history retained',
        })
        self.assertEqual(edit.status_code, 200)
        self.assertEqual(self.send('POST', f'/api/dogs/{first}/restore').status_code, 200)
        self.assertEqual(len(self.get('/api/dogs').json), 2)
        self.assertEqual(self.get('/api/entries?date=2026-10-23').json[0]['notes'],
                         'Archived history retained')

    def test_last_active_pet_cannot_be_archived(self):
        pet_id = self.make_pet()
        self.assertEqual(self.send('DELETE', f'/api/dogs/{pet_id}').status_code, 409)

    def test_trip_create_edit_delete_and_summary_latest(self):
        pet_id = self.make_pet()
        trip_id = self.make_trip(pet_id, pee=True, poop=True)
        summary = self.get('/api/summary?date=2026-10-23').json['dogs'][0]
        self.assertEqual((summary['pee_count'], summary['poop_count'], summary['trip_count']),
                         (1, 1, 1))
        latest = self.get('/api/latest').json[0]
        self.assertEqual(latest['last_pee'], '2026-10-23T19:29:00')
        self.assertEqual(latest['last_poop'], '2026-10-23T19:29:00')
        self.assertEqual(self.send('PUT', f'/api/entries/{trip_id}', {
            'dog_id': pet_id, 'timestamp': '2026-10-23T20:00',
            'pee': False, 'poop': True, 'notes': 'Updated',
        }).status_code, 200)
        self.assertEqual(self.send('DELETE', f'/api/entries/{trip_id}').status_code, 200)
        self.assertEqual(self.send('DELETE', f'/api/entries/{trip_id}').status_code, 404)
        self.assertEqual(self.get('/api/entries?date=2026-10-23').json, [])

    def test_script_like_text_is_stored_without_executing(self):
        name = '<img src=x onerror=alert(1)>'
        pet_id = self.make_pet(name=name)
        notes = '<script>alert(1)</script> & "quote"'
        self.make_trip(pet_id, notes=notes)
        history = self.get('/api/entries?date=2026-10-23').json
        self.assertEqual(history[0]['dog_name'], name)
        self.assertEqual(history[0]['notes'], notes)
        # Rendering safety is tested separately by tests/test_dashboard.js.


if __name__ == '__main__':
    unittest.main()
