# Pet Bathroom Tracker — Home Assistant app documentation

## Getting started

Install on Home Assistant OS, choose an IANA timezone in the Configuration tab (for example `America/New_York`), then start the app. Click **Open Web UI** and choose **Add your first pet**. Pet icons and names can be edited later under **Manage pets**.

Enable **Show in sidebar** so other non-admin members of the household can open the tracker through Home Assistant, without a second login.

## Recording trips

Select Pee, Poop, or both; adjust the timestamp if necessary; add optional notes; and save. New-entry timestamps refresh automatically until changed manually. The day selector, totals, and hourly tiles show history. Tap a tile or listed entry to edit or delete it. On narrow screens, use the pet selector above the timeline; on wide screens multiple pet columns are visible.

Manage pets allows adding, renaming, changing icons, archiving, and restoring pets. Archiving hides the pet from active forms and timeline columns **without deleting trips**. Every Home Assistant user who can open the tracker sees and can change the same data.

## Upgrading between preview releases

1. In **Settings → System → Backups**, make a manual backup that includes this preview app. Keep your backup encryption recovery key secure.
2. Start Samba temporarily and copy the updated **app folder contents** into the existing `local_apps` preview folder without creating a nested directory or uninstalling.
3. In **Settings → Apps → Install app**, select **Check for updates**, then update to the new version.
4. Verify the logs say `Pet Bathroom Tracker database ready` and Gunicorn is listening on port 8099.
5. Open the app and verify saved pet names, icons, archives, and trips. Optionally enable **Watchdog** from the app Info page; its `/health` endpoint checks whether the database tables are readable.

### Why database backups are cold

The app manifest specifies `backup: cold`: Supervisor stops the app while copying `/data` and starts it afterward. This was already present in v0.4.0. Individual-app backups include the private SQLite data; keep an accessible copy of the local-app source ZIP or published repository as well.

An encrypted Home Assistant backup is **not** a standalone SQLite file. Don't upload it to a public issue tracker or attempt to apply the offline recovery tool directly to the encrypted archive. See [RECOVERY.md](../RECOVERY.md).

## Troubleshooting

- **Not visible in Local apps:** Ensure the local folder contains `config.yaml` and use Check for updates.
- **Cannot start:** Inspect the app logs for SQLite integrity errors, unsupported timezone names, or package build issues.
- **Watchdog restarts app:** Check logs for health check failures. Disable Watchdog while intentionally stopping or troubleshooting the app.
- **403 Forbidden:** Open the sidebar/Ingress URL, not a direct container address. Only the Supervisor's Ingress IP `172.30.32.2` is accepted.
- **Wrong times:** Set timezone to your local IANA name and restart; stored timestamps use local wall-clock values and require cross-timezone caution.
- **Missing pets after update:** Stop and inspect backup contents before attempting a restore. Do not uninstall or overwrite `/data/tracker.db`.

## Privacy

All data stays in `/data/tracker.db` under Home Assistant. There is no cloud account, telemetry, public web port, or Home Assistant API permission. This is a **shared household application**, not per-user/private pet tracking.

## Preview limitations

This version has local unit tests and a disposable SQLite snapshot/restore rehearsal. An encrypted app backup was successfully restored to an isolated Home Assistant OS VM on `amd64` on October 23, 2026; `aarch64` runtime behavior and clean installation from a public repository still need testing. The current app remains a developer preview, not a stable public release.
