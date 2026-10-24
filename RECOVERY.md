# Pet Bathroom Tracker — Backup and recovery guide

## What is backed up

An app backup includes private app `/data`, which holds `tracker.db` (pet names, icons, archived status, pee/poop trips, notes) and app options. The manifest uses **`backup: cold`** so Home Assistant briefly stops the app while making its backup.

**Important:** If you are running a *Local app*, keep the source ZIP or app directory separately, especially for a partial backup that might not include `local_apps`. Keep the encryption emergency kit secure and independent of your Home Assistant host.

## Verify an existing Home Assistant backup safely

1. Open **Settings → System → Backups** and select the manual backup you made.
2. Under **Select what to restore**, confirm **Pet Bathroom Tracker (Preview)** is listed at the expected version.
3. Confirm the backup is present in at least one trusted location, ideally both local and remote.
4. **Do not press Restore on the production Home Assistant instance** just to test the backup. The list confirms that the app is included; it does **not** demonstrate that all records can be restored.

## Safest real recovery drill — disposable Home Assistant OS

A full restore test needs an *isolated* throwaway Home Assistant OS VM or spare device:

1. Preserve the original backup and its encryption recovery key; make sure you can access the ZIP/app repository source separately.
2. Create a **new disposable Home Assistant OS instance on an isolated test network**, not a clone that runs with the same networking/services as production.
3. Use Home Assistant's supported backup restore wizard, supply the recovery key when required, and select **only the Pet Bathroom Tracker preview app** (and required dependencies). The exact screens can vary by Home Assistant version.
4. Restore/reinstall the matching app source if the local-app repository wasn't included in the backup, keeping the same slug. Do not point the test at the production VM or its live volumes.
5. Open the restored tracker and compare pets, icons, archive status, and several recent trips against a written baseline taken before backing up. Add and edit a test trip **on the disposable instance only**.
6. Destroy or shut down the test instance once verified. Do not attach its data volume to the production app.

**Status — Verified October 23, 2026:** An encrypted Pet Bathroom Tracker app backup was successfully restored to a separate AMD64 Home Assistant OS installation (VM 103). The restored installation retained the test pet, emoji icon, and bathroom history. Subsequent edits persisted after an application restart.

**Additional verification — October 24, 2026:** The restored test environment successfully completed an in-place upgrade from v0.5.4 to v0.5.5. Existing records survived the update and subsequent restart, and adding, editing, and deleting entries worked correctly.

These tests validate the documented recovery and upgrade procedures in the tested AMD64 environment. They do not guarantee successful recovery from every hardware failure, filesystem issue, or unsupported architecture.

## Offline SQLite backup/restore rehearsal (developers)

If you have an unencrypted, authorized copy of the actual `tracker.db` file, run:

```sh
python3 tools/rehearse_recovery.py /safe/path/to/tracker.db
```

The tool opens the source **read-only**, verifies SQLite integrity and foreign keys, uses SQLite's online backup API to create a consistent snapshot, and restores that snapshot into a temporary database, comparing pet/entry records. Its test files are deleted afterward; the source isn't changed. This can work while the source SQLite file is in use, but for a fully representative backup verification prefer a copy extracted from a stopped app.

The tool **does not** read, decrypt, or validate the encrypted Home Assistant backup archive. A passing SQLite rehearsal alone is *not* a passing Supervisor restore test.

## If the database is corrupted

The app performs startup integrity checks and refuses to run if corruption or orphaned entries are found. Do not reset or delete `/data/tracker.db` to silence these errors. Keep the app stopped, preserve a copy of the damaged data, and restore from the latest known-good Home Assistant backup following a cautious recovery process. Avoid exposing private database files publicly.

## Verified Home Assistant OS restore — October 23, 2026

The maintainer tested the following against **a separate Home Assistant OS 18.3 VM (VM 103)**:

1. Created an encrypted manual app backup containing Pet Bathroom Tracker Preview 0.5.0 on a different Home Assistant installation.
2. Uploaded the backup to VM 103 and selected **only** the Pet Bathroom Tracker app for restore. Full Home Assistant settings and automations were not restored.
3. Started the restored app and verified two original test dogs, a third pet with a custom rabbit icon, and previous pee/poop history.
4. Renamed one restored pet and restarted the restored app; the updated name persisted.

**Result:** Restoring app data worked on the tested x86-64 Home Assistant OS environment. This does not yet validate ARM64 or disaster recovery after every possible filesystem failure. Keep a separate copy of your encryption key, and for early source-built releases retain a copy of this repository or source package.
