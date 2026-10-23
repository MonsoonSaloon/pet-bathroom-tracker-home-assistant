# Changelog

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
