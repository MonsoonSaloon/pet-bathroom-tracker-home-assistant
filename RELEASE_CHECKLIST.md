# Release verification checklist

## Automated checks

- [x] Python tests for new SQLite databases, migrations, archived records, invalid/corrupt data and disposable snapshot/restore
- [x] Python, shell, and dashboard JavaScript syntax checks
- [x] App configuration includes Ingress, cold backups, non-admin sidebar access, and Watchdog health URL
- [x] Dashboard version label matches manifest version
- [x] GitHub Actions **Source checks** passed after first publication of v0.5.1
- [x] GitHub Actions passed after v0.5.2 update
- [ ] GitHub Actions passes after v0.5.3 branding update

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
- [ ] Public GitHub-install version: full add/edit/delete/rename/archive workflow rechecked
- [ ] Public GitHub-install version: non-admin account tested
- [ ] Watchdog fault recovery tested intentionally in an isolated instance

## Remaining stability/publication work

- [ ] ARM64 install/build/runtime test
- [ ] Dependency vulnerability review and routine upgrade process
- [x] Custom app icon, logo, and GitHub hero artwork
- [x] Cropped UI screenshots for README (desktop, mobile, pet management; earlier preview test builds)
- [ ] Optional pre-built amd64/aarch64 container images
- [ ] Additional external security review

**Experimental preview:** These remaining checks prevent declaring a stable v1.0 release.
