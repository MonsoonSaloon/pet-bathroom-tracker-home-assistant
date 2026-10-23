# Pet Bathroom Tracker — Home Assistant App

![Developer preview](https://img.shields.io/badge/status-experimental-orange) ![Home Assistant OS](https://img.shields.io/badge/platform-Home%20Assistant%20OS-blue)

**Preview v0.5.2** — a free, local-first bathroom tracker for multiple pets, shared inside Home Assistant. Record pee, poop, or both; review a color-coded timeline; and edit history from your phone, tablet, or computer.

[![Add Pet Bathroom Tracker repository to your Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FMonsoonSaloon%2Fpet-bathroom-tracker-home-assistant)

> **Experimental preview.** Successfully tested on AMD64 Home Assistant OS: fresh install from this public GitHub repository, first-pet onboarding, saving a trip and retaining it after app restart, non-admin household access in an earlier preview, and a separate encrypted app-backup restore. ARM64 has not been runtime-tested; no independent security review has been completed.

## Features

- **Any number of pets:** custom names, emoji icons, and archiving without deleting history.
- **Fast entry:** pee, poop, or both; timestamp and optional notes.
- **Clear history:** daily totals and editable, color-coded hourly timeline.
- **Mobile friendly:** one-pet timeline selector on narrow displays; all pets on larger screens.
- **Shared household data:** authorized Home Assistant users see the same database through Ingress.
- **Local storage:** private SQLite database, with Home Assistant app backups (`backup: cold`).

## Install in five steps (Home Assistant OS)

1. Use the **Add repository** badge above, or open **Settings → Apps → Install app → ⋮ → Repositories** and add `https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant`.
2. Find **Pet Bathroom Tracker (Preview)** in the app store and choose **Install**.
3. Open **Configuration** and choose your time zone (e.g., `America/New_York`). Save the options.
4. Start the app and select **Open Web UI**. Click **Add your first pet** and choose a name/icon.
5. Select **Show in sidebar** so other non-admin Home Assistant accounts can use the tracker. Optionally enable **Start on boot** and **Watchdog** after verifying operation.

No Proxmox, Samba, extra Linux server, or port forwarding is needed for users running Home Assistant OS. **This is not a HACS integration** and is not an official Home Assistant app.

### Updating safely

1. Create a manual Home Assistant backup containing this app. Save the encryption recovery key in a secure location.
2. On **Settings → Apps**, open its available update and review the changelog.
3. **Update in place**; do not uninstall, as that can remove persistent app data.
4. Verify saved pets and entries remain after the update.

Older **Local app** installations have a different Supervisor app identity: adding the public GitHub repository does **not** automatically transfer their data. Back up first and plan a separate migration.

## How it works

Each pet has an entry form and counts for the selected day. The timeline shows trips with distinct colors for pee, poop and combined events. Entries can be edited or deleted from history. With more pets, the timeline expands on desktop; on phones, choose which pet to display. Archived pets can be restored later, with their records retained.

Data is shared with everyone who can access the app via Home Assistant—there are no per-user permissions. The server doesn't publish a LAN port or require an external account. The database lives at `/data/tracker.db` in persistent app storage.

## Privacy and backup

All tracking data stays on your Home Assistant system unless you back it up to other destinations. Home Assistant Ingress authenticates users. The project does not include third-party telemetry. **Anyone with access to the app can change or delete its data.** Keep backups of the app and its SQLite database; Home Assistant app backup uses `backup: cold` to stop writes during the backup.

**Verified recovery (October 23, 2026):** A manual encrypted app backup was restored to a separate Home Assistant OS VM, recovering pet names, an emoji icon, and bathroom records. An edit persisted after restarting the restored app. This is a successful isolated test, not a guarantee across all configurations.

## Compatibility and status

| Item | Status |
|---|---|
| Home Assistant OS / AMD64 | Tested (installation, use, backup restore) |
| Home Assistant OS / ARM64 | Listed in manifest, **not yet tested** |
| Home Assistant Container / Core | App store installation method not supported |
| GitHub-hosted installation | Tested |
| Built container image | Built on the HA machine; pre-built images not yet available |
| Current release channel | Experimental preview |

**Screenshots:** Representative, cropped screenshots will be added before promoting this experimental preview. Do not publish captures that show private IP addresses, accounts, pet details, or access tokens.

## Documentation and help

- [Home Assistant in-app documentation](pet_bathroom_tracker/DOCS.md)
- [Release history and upgrade notes](CHANGELOG.md)
- [Backup and recovery guide](RECOVERY.md)
- [Security and privacy](SECURITY.md)
- [Release verification checklist](RELEASE_CHECKLIST.md)
- [Publishing and maintenance](PUBLISHING.md)
- [Issues and bug reports](https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/issues)

## Development and automated checks

```bash
python3 -m pip install pyyaml
python3 -m unittest discover -s tests -v
```

The [Source checks workflow](.github/workflows/checks.yml) runs database tests, Python syntax checks, shell syntax checks and a JavaScript syntax check for pushes and pull requests. These checks cannot substitute for testing on multiple Home Assistant OS architectures.

## License

[MIT](LICENSE)
