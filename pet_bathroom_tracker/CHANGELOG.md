# Changelog

## 0.5.6 — Input validation and timeline display fixes (release candidate; not yet published)

### Fixed
- Reject fractional, boolean, noncanonical, negative, or out-of-range pet IDs in bathroom-entry requests with a controlled 400 response.
- Reject zero and out-of-range pet/entry IDs in route paths before SQLite operations, returning 404 instead of causing server errors.
- Display saved local bathroom timestamps without browser daylight-saving-time normalization.

### Testing and maintenance
- Add Flask API regression tests for Ingress restrictions, malformed JSON, size limits, pet/entry lifecycle, archived records, and invalid IDs.
- Add JavaScript regressions for daylight-saving-time timestamps and HTML escaping.
- Install application dependencies in the source-check workflow and remove the hard-coded manifest version assertion in release tests.
- All nine GitHub automated checks passed on the `security-v056` pull request, including CodeQL scanning and native AMD64/ARM64 container build and test jobs. CodeQL reported no new alerts in the changes covered by the pull request.

### Home Assistant OS validation (October 24, 2026)
- Installed the v0.5.6 development branch as a separate app on an isolated AMD64 Home Assistant OS VM (VM 103); verified startup, Ingress, pet management, entry editing, date navigation, and historical data.
- Confirmed fresh-install pet-management and persistence regressions, including pet rename, icon changes, archive/restore, and history preservation after restart.
- Tested database compatibility on a disposable copy of an existing v0.5.5 SQLite database; repeated initialization preserved both pets, all four bathroom entries, timestamps, and notes, with passing integrity and foreign-key checks.
- Rehearsed an actual in-place v0.5.5 → v0.5.6 update using a separate `upgrade-rehearsal-v056` branch and Home Assistant's normal Update button, without uninstalling the app.
- Before and after the in-place update, compared the complete `dogs` and `bathroom_entries` table records: both pets and all four entries matched exactly, including IDs, icons, activity flags, timestamps, and notes.
- Confirmed the upgraded app restarted successfully, retained the October 23–24 test history, served the dashboard through Ingress, and returned successful Supervisor health checks. Reviewed application logs contained no observed exceptions or failed HTTP requests.
- Preserved verified pre-upgrade SQLite backups and a Home Assistant backup before the rehearsal.

### Upgrade notes
- No database schema change or data migration is required for this release.
- Back up the existing Home Assistant app before updating; update in place and do not uninstall to upgrade.
- The public release is pending final documentation and merge into `main`; v0.5.5 remains the published version until then.
- The project remains an experimental preview. Full ARM64 Home Assistant OS installation/runtime verification, independent security review, and broader external testing are still outstanding.

## 0.5.5 — Security maintenance

### Fixed
- Resolved six medium-severity CodeQL findings involving potential information disclosure through exception responses.
- Replaced exception-derived responses with consistent, safe validation messages.
- Restricted GitHub Actions workflow permissions to read-only repository access.
- Resolved all seven CodeQL security findings identified in v0.5.4.

### Security and testing
- CodeQL security analysis completed with zero remaining open findings after the fixes.
- Python source checks and automated AMD64/ARM64 container tests passed.
- GitHub Dependabot and secret scanning reported zero open alerts at the time of release preparation.

### Upgrade notes
- No database schema changes or intentional changes to bathroom-tracking behavior.
- Existing pets, icons, archived records, and bathroom history should remain intact.
- Make a Home Assistant backup before updating.
- Update the existing app in place. Do not uninstall it.
- This remains an experimental preview. Real ARM64 Home Assistant OS testing is still outstanding.

## 0.5.4 — Dependency and storage-permissions maintenance

### Security hardening
- Updated pinned Python dependencies to Flask `3.1.3` and Gunicorn `26.2.0`.
- On startup, apply restrictive permissions to persistent SQLite storage (`/data` mode `700`; `tracker.db` and related SQLite files mode `600`) and ensure SQLite file ownership belongs to the unprivileged `dogtracker` account.
- Keep Home Assistant Supervisor's private `options.json` under Supervisor control.

### Testing
- GitHub Actions source checks and native AMD64/ARM64 container tests passed after the dependency updates and permissions fix.
- Automated container tests now verify database file permissions during fresh installation and after a restart with previously permissive file modes.
- Full Home Assistant OS installation on ARM64 and a clean-install update-entity test without a Home Assistant Core restart remain to be completed.

### Upgrade notes
- **No API, database schema, pet history, or tracking-behavior changes.** An in-place update is expected to preserve existing entries; verify this on the test installation before considering the release validated.
- Create a Home Assistant backup before updating. **Do not uninstall** the app to update it.
- This remains an experimental preview, not an independently audited stable release.

## 0.5.3 — App icon and public branding

### Added
- New square dog-and-cat tracking icon (`icon.png`) for Home Assistant app listings and installed-app cards.
- Matching landscape app logo (`logo.png`) for the Home Assistant app details page.
- GitHub banner, promotional artwork, and transparent icon in `assets/`.
- Visual branding in the repository README.

### Improved
- Dashboard version label updated to `Preview 0.5.3`.
- In-app troubleshooting documents the possible missing graphical Update control and the Supervisor update entity; **no mandatory Home Assistant restart** is required on install.

### Upgrade notes
- **No API, database schema, or tracking behavior changes.** Existing pets, icons, trips, and archived history should remain unchanged on an in-place update.
- Make a Home Assistant app backup before updating. Do **not uninstall** the existing app to update it.
- ARM64 runtime testing remains outstanding. This is still an experimental preview.

## 0.5.2 — Public installation documentation polish

### Fixed
- Replaced the outdated v0.4.0 placeholder on the Home Assistant app details page with real installation, usage, backup and support information.
- Updated the dashboard label to `Preview 0.5.2` so it matches Home Assistant's installed version.
- Corrected stale development notes that incorrectly said fresh GitHub installation and isolated restore testing were pending.

### Improved
- Added an official **Add repository** shortcut to the GitHub README and populated the public repository URL in `repository.yaml`.
- Clarified GitHub-installed upgrades versus older Local-app previews; they do not share the same app identity or automatically transfer records.
- Updated in-app documentation, release checklist, publishing guide, and troubleshooting information.
- Added `.gitattributes` to preserve LF line endings for Linux scripts even when developing on Windows.

### Upgrade notes
- **No tracking behavior, API, database schema, or saved records changed.** Existing pets and bathroom history should stay intact when updating in place.
- Back up the app before updating. **Do not uninstall it**, since that may delete persistent data.
- Still an **experimental developer preview**. ARM64 runtime and independent security review remain outstanding.

## 0.5.1 — GitHub preview preparation

### Fixed
- Corrected the outdated `Preview 0.4.0` label in the dashboard header. The interface now displays `Preview 0.5.1`.

### Documentation and testing
- Updated recovery documentation with the successful isolated Home Assistant OS restore test: an encrypted app backup was restored to a separate temporary Home Assistant VM, pet records and a custom icon were verified, then an edit survived an app restart.
- Added a GitHub publishing guide and an automated lint/test workflow.
- Documented the distinction between a **source-built preview** and a future pre-built multi-architecture release.

### Upgrade notes
- **No SQLite schema changes and no changes to tracking behavior.** Existing pets, archived status, icons, and trips should remain intact.
- Make an app backup before any upgrade. Do not uninstall an existing preview instance when updating in place.
- The app remains **experimental**, not a stable 1.0 release. ARM64 runtime testing and a clean GitHub-repository installation are still pending.

## 0.5.0 — Database readiness and recovery tooling

### Added
- Optional Home Assistant Watchdog URL (`/health`) that checks that the SQLite database and its essential tables are readable, instead of reporting success merely because the web server is running.
- Startup validation for existing SQLite databases **before** schema migrations, plus a foreign-key integrity check after initialization. Damaged or orphaned databases now fail startup instead of silently appearing healthy.
- Read-only SQLite recovery rehearsal utility (`tools/rehearse_recovery.py`). It takes a consistent database snapshot, restores it into a disposable temporary database, and checks that pets and trips match the source.
- Dedicated recovery, security, and release-testing guides; automated tests for corrupt databases and orphaned records.

### Changed
- Database connections are explicitly closed after each web request; failures roll back uncommitted writes.
- HTTP JSON request size capped at 64 KiB.
- Updated preview documentation with clear distinctions between offline SQLite testing and **actual Home Assistant encrypted backup restoration**.

### Backups and upgrade notes
- **No database schema changes or record deletion.** Existing pets, icons, archives, and trips should remain unchanged across the update.
- `backup: cold` was already present in v0.4.0 and remains enabled; Home Assistant stops this app during its app-data backup. The backup process may briefly interrupt access.
- To activate deep monitoring, enable **Watchdog** in the app Info page after verifying that the app starts correctly.
- Keep a separate copy of the source package or published repository URL. A backup containing app data alone may not reproduce a missing local-app source folder.
- Take a Home Assistant backup before updating; do not uninstall the preview. **Real Home Assistant OS backup restoration is not yet tested.**

## 0.4.0 — First-time setup and pet icons

### Added
- Welcome screen with **Add your first pet** for clean installations. No automatic Dog 1/Dog 2 profiles.
- Selectable pet icons (dogs, cats, rabbits, birds, and more) when creating or editing pets.
- Pet icons are shown on entry forms, day summaries, and timeline navigation.

### Changed
- **Manage pets** now saves both names and icons from a single row.
- Deprecated initial `dog_1_name` and `dog_2_name` options; they are not used to seed pets on new installations. Existing saved options remain accepted for upgrade compatibility.

### Upgrade and migration
- Adds a persistent `icon` column to the SQLite pets table. Existing pets automatically retain the original 🐶 icon, existing names, archive states, and bathroom records.
- No entries or pets are deleted. **Take a Home Assistant backup before upgrading.**
- This is a preview build; test first-run onboarding and an in-place upgrade before public release.

## 0.3.1 — Home Assistant release notes fix

- Fix packaging so Home Assistant displays release notes in its app update dialog.
- Keep the repository-level changelog and app-level `CHANGELOG.md` in sync.
- No changes to tracking behavior, mobile layout, database, or app settings.

## 0.3.0 — Phone timeline preview

- Show one pet at a time in the hourly timeline on narrow mobile screens (560 CSS pixels and below).
- Add a pet selector that changes timeline columns without reloading or touching stored entries.
- Preserve full multi-pet columns for wider screens, including horizontal scrolling with many pets.
- Keep all-pet daily totals and event history visible on mobile.
- No server, database, or configuration changes besides the preview version.

**Test status:** automated syntax/database tests passed; real phone UI and in-place upgrade still need user testing.


## 0.2.0 — Multi-pet preview

- Add, rename, archive and restore pets using the **Manage pets** dialog.
- Support more than two active pets. The timeline scrolls horizontally when needed.
- Preserve historical bathroom trips when archiving a pet. Archived pet entries can still be edited from the history list.
- Preserve user-entered names and archived status across app restarts and upgrades; configured initial pet names now apply only to a brand-new database.
- Retain Home Assistant Ingress login, existing SQLite records and the familiar tracking interface.

**Test status:** Python/JavaScript syntax checks and bootstrap migration tests passed. Upgrade and UI testing on Home Assistant OS still required before release.

## 0.1.0 — First standalone preview

- Initial Home Assistant OS app packaging.
- Two pet profiles from app settings, pee/poop tracking, daily timeline, editing and history.
- Local-first SQLite and Home Assistant Ingress.
