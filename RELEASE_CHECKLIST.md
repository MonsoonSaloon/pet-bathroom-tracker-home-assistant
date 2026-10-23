# Release verification checklist

## Automated checks — local

- [x] `python3 -m unittest discover -s tests -v` (fresh DB, migrations, archive retention, corrupted/orphaned DB refusal, snapshot/restore, app configuration)
- [x] Python syntax compilation and shell script syntax
- [x] UI JavaScript syntax
- [x] Changelog present in app root and at repository root
- [x] App manifest: Ingress enabled, no published host port, non-admin panel, cold backups, Watchdog URL

## User tests — completed in prior previews

- [x] v0.4.0 upgrade preserved pets, icons and trips, including after restart
- [x] v0.3.0 mobile timeline pet selector tested on phone
- [x] v0.2.0 archive/restore/rename tested
- [x] Non-admin Home Assistant account tested
- [x] v0.3.1 changelog shown in HA update dialog
- [x] HA manual backup included Pet Bathroom Tracker v0.4.0 and was copied to local and OneDrive destinations

## Home Assistant OS tests — completed / remaining

- [x] Update in place from v0.4.0 to v0.5.0 with manual backup enabled
- [x] Verify app startup and existing trips, pet icons, archived status
- [x] Enable Watchdog; verify stable uptime (no restart loop)
- [ ] Re-test the full add/edit/delete trip cycle specifically after the v0.5.1 update
- [x] Create a new v0.5.0 manual app backup and confirm the app is listed
- [x] Full restore in **isolated disposable Home Assistant OS**; confirm records and user access
- [ ] Clean install from zero pets on a different Home Assistant OS instance
- [ ] Build and launch on `aarch64` (only `amd64` has been tested by the project owner)
- [ ] Review package versions/security advisories and implement release automation
- [ ] Screenshots/brand assets and permanent GitHub repository URL

**Do not call this a production-ready v1.0.0 until clean repository installation, cross-architecture builds, and the outstanding security/release tests pass.**

## Version-label regression check

- [x] Automated test confirms that the dashboard preview label matches the app manifest version.
