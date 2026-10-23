# Pet Bathroom Tracker — Home Assistant App

![Status: Developer preview](https://img.shields.io/badge/status-developer%20preview-orange) ![Home Assistant OS](https://img.shields.io/badge/platform-Home%20Assistant%20OS-blue)

**Preview v0.5.1** — free, local-first bathroom tracking for pets, right inside Home Assistant. Supports any number of pets, optional notes, pee/poop/both entries, editable history, an hourly timeline, a mobile-friendly pet selector, and shared access through Home Assistant's existing accounts.

> **Preview warning:** This release is experimental. It has been tested on one `amd64` Home Assistant OS deployment, with an encrypted app backup restored successfully to a separate Home Assistant OS VM. ARM64 builds, a fresh installation via a public GitHub repository, and third-party security review are still pending. Please keep independent backups.

## Installation (Home Assistant OS)

This repository is a **Home Assistant app repository**, **not** a HACS integration. It contains `repository.yaml` at the root and `pet_bathroom_tracker/config.yaml` underneath. Home Assistant OS supports adding community repositories from **Settings → Apps → Install app → ⋮ → Repositories**.

1. Copy the **HTTPS URL of this GitHub repository** from the GitHub **Code** menu.
2. In Home Assistant, open **Settings → Apps → Install app → ⋮ → Repositories**, paste the copied URL, and choose **Add**.
3. Find **Pet Bathroom Tracker (Preview)**, install it, and select your time zone in the app configuration.
4. Start the app and select **Open Web UI**. Add your first pet from the welcome screen.
5. Enable **Show in sidebar** to make the app accessible to non-admin household members. If it works reliably, optionally enable **Start on boot** and **Watchdog**.

The preview has no pre-built registry image configured, so Home Assistant currently **builds the Dockerfile locally during installation**. This can take longer and has not yet been tested on ARM64 hardware. Future stable releases should provide pre-built images. This source-built approach is supported for development. See [Home Assistant's app publishing guidance](https://contributors.home-assistant.io/apps/guides/publishing/).

### Updating an existing preview

Create a manual Home Assistant backup with this app selected, then update through Home Assistant when a new release is published. **Do not uninstall** the app, because that can remove its persistent data. If you're still running an old Local-app installation, keep using its existing folder and apply new source files there; a GitHub-installed app is a separate app identity from `local_pet_bathroom_tracker` and does **not** automatically migrate the local app's database.

## Using the tracker

- Add pets with custom names and emoji; rename, archive and restore pets without losing their existing trip history.
- Record pee, poop, or both with a timestamp and optional note. New-entry time stays current unless manually adjusted.
- Switch dates to see daily totals, hourly trips, and editable history.
- On phones, select one pet for the timeline; on larger screens, see multiple pet columns at once.
- All authenticated Home Assistant accounts with access to the app share the **same data**, including the ability to edit and delete records. This is not a per-user private journal.

## Data and backups

Pet records are stored locally in the app's private persistent `/data/tracker.db` (SQLite). Home Assistant Ingress provides authentication; **no LAN port or separate cloud service is required**.

The app declares `backup: cold`, so Home Assistant stops it briefly while copying persistent data during an app backup. Keep the backup encryption recovery key in a safe place. For recovery details see [RECOVERY.md](RECOVERY.md).

**Recovery test completed (Oct 23, 2026):** A Home Assistant encrypted app backup from the preview was uploaded to a separate Home Assistant OS VM (VM 103) and the preview app was restored **without restoring production settings**. Existing pets, icons, and bathroom history were present; changing a pet name then restarting the restored app preserved the change. This provides direct restore evidence on the tested `amd64` environment, not a guarantee for every Home Assistant version and device.

## Development

```bash
python3 -m pip install pyyaml
python3 -m unittest discover -s tests -v
```

The `tests/` folder covers database creation/migration, corrupt records, archival, backup snapshots, and configuration. An independent GitHub Actions workflow runs syntax checks and tests. The latest test status and remaining release gates are in [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).

## Documentation

- [Changes and upgrade notes](CHANGELOG.md)
- [Restore and recovery](RECOVERY.md)
- [Security and privacy](SECURITY.md)
- [Release checklist](RELEASE_CHECKLIST.md)
- [Publishing to GitHub](PUBLISHING.md)
- [Home Assistant in-app documentation](pet_bathroom_tracker/DOCS.md)

## License

MIT — see [LICENSE](LICENSE).
