# Release verification checklist

## Automated checks

- [x] Python tests for new SQLite databases, migrations, archived records, invalid/corrupt data and disposable snapshot/restore
- [x] Python, shell, and dashboard JavaScript syntax checks
- [x] App configuration includes Ingress, cold backups, non-admin sidebar access, and Watchdog health URL
- [x] Dashboard version label matches manifest version
- [x] GitHub Actions **Source checks** passed after first publication of v0.5.1
- [x] GitHub Actions passed after v0.5.2 update
- [x] GitHub Actions passes after v0.5.3 branding update (verified by subsequent successful builds)

## Real-world Home Assistant OS (AMD64)

- [x] Earlier preview upgrades preserved pets, emoji icons, and history across restarts
- [x] Mobile pet selector tested on a Samsung phone
- [x] Non-admin household account accessed the app through sidebar
- [x] Home Assistant update changelog displayed correctly
- [x] Encrypted app backup restored to a separate Home Assistant OS VM; existing entries/icons appeared, and subsequent edit persisted after reboot
- [x] Public GitHub repository installed successfully on clean Home Assistant OS; welcome screen appeared
- [x] New GitHub installation added a pet and pee/poop entry; entries survived restart
- [x] Watchdog enabled on the earlier preview without immediate reported issues
- [x] In-place v0.5.1 → v0.5.2 upgrade tested with existing records via Home Assistant CLI; Test pet 1 and 7:29 PM combined trip preserved
- [x] v0.5.2 → v0.5.3 GUI update tested without CLI or Core restart; installed version, logo and saved Test pet 1 / trip verified
- [x] Public GitHub-install version: pet creation, renaming, archiving, and restoring tested; bathroom history preserved
- [x] Public GitHub-install version: bathroom entries can be added, edited, and deleted
- [x] Public GitHub-install version: non-admin account tested successfully on VM 103 with v0.5.5; sidebar access, shared pet records, entry creation, and administrator visibility verified
- [x] Watchdog fault recovery tested on isolated Home Assistant OS VM 103 (v0.5.5); Supervisor confirmed automatic restart after container exit code 137, with dashboard functionality and saved pet history preserved

## v0.5.5 — Security maintenance release verification (October 24, 2026)

### Security

- [x] Resolved six CodeQL information-exposure findings in Python exception handling
- [x] Resolved one GitHub Actions workflow permissions finding
- [x] CodeQL confirmed zero remaining open findings after the fixes
- [x] Dependabot reported zero open vulnerability alerts
- [x] Secret scanning reported zero open alerts
- [x] Secret protection and push protection enabled

### Automated testing

- [x] GitHub Actions Source checks #18 passed
- [x] GitHub Actions Container architecture tests #8 passed
- [x] GitHub Actions CodeQL #3 passed
- [x] App configuration, dashboard, documentation, and recovery test updated to v0.5.5
- [x] Windows tests investigated; remaining failures involve temporary SQLite database file locks (WinError 32)
- [x] GitHub Actions native AMD64 and ARM64 container architecture tests passed on main; both jobs completed successfully

### Home Assistant OS upgrade testing (AMD64)

- [x] Created Proxmox VM 103 snapshot: before-pet-tracker-v055
- [x] v0.5.5 detected and installed through Home Assistant's normal app update process
- [x] Existing test pet and bathroom history preserved during v0.5.4 → v0.5.5 upgrade
- [x] Adding, editing, and deleting bathroom entries tested successfully
- [x] Dashboard displays Preview 0.5.5
- [x] Application restarted successfully and existing records remained intact

### Publication

- [x] v0.5.5 committed and pushed to GitHub
- [x] GitHub v0.5.5 release published
- [x] Release remains designated as an experimental preview
- [ ] Independent ARM64 Home Assistant OS runtime testing
- [ ] Independent external security review

## Remaining stability/publication work

- [x] Native ARM64 container build and runtime tests passed on GitHub Actions ubuntu-24.04-arm runner; health, database operations, permissions, and restart persistence verified
- [ ] Full ARM64 Home Assistant OS installation, Ingress, and runtime verification
- [x] Dependency vulnerability review and routine upgrade process
- [x] Custom app icon, logo, and GitHub hero artwork
- [x] Cropped UI screenshots for README (desktop, mobile, pet management; earlier preview test builds)
- [ ] Optional pre-built amd64/aarch64 container images
- [ ] Additional external security review

**Experimental preview:** These remaining checks prevent declaring a stable v1.0 release.

## v0.5.6 — Security and dashboard maintenance release verification (October 24, 2026)

### Security and automated testing

- [x] Improved pet-ID validation to reject invalid, fractional, and oversized values
- [x] Added Flask API security and input-validation regression tests
- [x] Added dashboard JavaScript regression tests, including daylight-saving-time display corrections
- [x] GitHub Actions source checks passed on `security-v056`
- [x] Native AMD64 and ARM64 container architecture tests passed
- [x] CodeQL reported no newly introduced findings on Pull Request #4
- [x] All 9 automated checks passed on the development pull request
- [x] All 9 automated checks passed on the isolated upgrade-rehearsal pull request

### Fresh Home Assistant OS installation (AMD64)

- [x] v0.5.6 installed successfully from `security-v056` on isolated Home Assistant OS VM 103
- [x] Application initialized its database and started successfully
- [x] Home Assistant Ingress and Open Web UI functioned correctly
- [x] Pet management, daily timeline, historical navigation, and entry editing tested
- [x] Pet renaming, icon changes, archiving, and restoring tested
- [x] Historical records and timestamps preserved across restart
- [x] Application logs reviewed with no observed Python exceptions, database failures, or HTTP errors

### Database compatibility verification

- [x] Verified original v0.5.5 database containing 2 pets and 4 bathroom entries
- [x] SQLite integrity and foreign-key consistency checks passed
- [x] Database backup copied outside the container and verified using SHA-256
- [x] Confirmed v0.5.5 and v0.5.6 database initialization code matched
- [x] Isolated database initialization completed successfully twice
- [x] All pet records, bathroom entries, timestamps, and notes preserved
- [x] Original database and preserved backup left unchanged during compatibility testing

### Actual in-place upgrade rehearsal (AMD64)

- [x] Created temporary `upgrade-rehearsal-v056` branch from v0.5.5
- [x] Installed a third, isolated Pet Bathroom Tracker instance on VM 103
- [x] Created 2 test pets and 4 bathroom entries across October 23–24, 2026
- [x] Created test notes and verified historical dates and daily totals
- [x] Preserved a verified pre-upgrade SQLite database backup
- [x] Merged v0.5.6 changes into the temporary rehearsal branch through Pull Request #5
- [x] Home Assistant detected v0.5.6 as an available update
- [x] Performed the v0.5.5 → v0.5.6 upgrade using the normal Home Assistant Update button
- [x] Existing installation identity and database storage preserved
- [x] Application restarted successfully and opened through Home Assistant Ingress
- [x] Both pets and all 4 historical bathroom entries remained visible
- [x] Both notes and the original entry dates remained visible
- [x] Exact SQLite comparison confirmed all pet and bathroom entry records unchanged
- [x] Post-upgrade database integrity and foreign-key checks passed
- [x] Additional application restart completed successfully
- [x] Post-upgrade logs reviewed; successful startup, Ingress requests, and Supervisor health checks confirmed
- [x] No Python exceptions, database errors, or failed HTTP requests observed in the reviewed logs

### Release preparation and publication

- [x] v0.5.6 successfully tested on isolated Home Assistant OS AMD64 VM 103
- [x] Genuine in-place v0.5.5 → v0.5.6 upgrade completed before public release
- [x] Verified pre-upgrade database backup and encrypted Home Assistant backup preserved
- [x] v0.5.6 remains designated as an experimental preview
- [ ] Update README, changelogs, and publishing documentation to reflect completed validation
- [ ] Confirm final GitHub Actions checks pass after documentation updates
- [ ] Merge official Pull Request #4 from `security-v056` into `main`
- [ ] Verify v0.5.6 is available through the normal Home Assistant app update process
- [ ] Publish the official GitHub v0.5.6 release and release notes
- [ ] Confirm published release documentation reflects the completed tests and remaining limitations

### Outstanding limitations

- [ ] Independent testing on ARM64 Home Assistant OS hardware
- [ ] Independent external security review
- [ ] Broader real-world testing beyond the current development environment

**Release status:** v0.5.6 passed automated checks, fresh Home Assistant OS AMD64 installation testing, database compatibility testing, and an isolated in-place upgrade rehearsal. Official publication remains pending. ARM64 Home Assistant OS verification and independent security review remain outstanding; the release continues as an experimental preview rather than a stable v1.0 release.
