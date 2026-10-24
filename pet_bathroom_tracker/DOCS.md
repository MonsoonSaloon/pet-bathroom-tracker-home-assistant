# Pet Bathroom Tracker — Documentation

This is a free community **Home Assistant OS app**. It uses Home Assistant Ingress to provide access without a separate username/password or exposed LAN port.

## Install from GitHub (recommended)

1. Open **Settings → Apps → Install app → ⋮ → Repositories** in Home Assistant.
2. Add **https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant**.
3. Install **Pet Bathroom Tracker (Preview)** from the new repository section.
4. Under **Configuration**, select your IANA time zone (for example `America/New_York`).
5. Start the app. Click **Open Web UI** and then **Add your first pet**.
6. Turn on **Show in sidebar** to give all permitted Home Assistant users convenient access. A non-admin user can open the sidebar app but cannot administer its installation.
7. After confirming it works, turn on **Start on boot**; optionally enable **Watchdog** for availability monitoring.

This is an **app**, not a HACS integration. The GitHub version will build a container on Home Assistant during installation; a ready-made multi-architecture image is not yet provided. Native AMD64 and ARM64 container builds and smoke tests have passed in GitHub Actions, but a full Home Assistant OS installation on ARM64 has not yet been tested.

## Record and review bathroom trips

Select **Pee**, **Poop**, or both; leave the current time or set another time; add optional notes; and save. Daily totals and the color-coded hourly timeline update. Tap a trip tile to edit or delete it. Use the date selector to browse previous days.

Use **Manage pets** to add more pets, rename them, pick icons, or archive and restore them. Archiving hides a pet's active form and timeline column **without deleting history**. On phones, select one pet for the hourly timeline; on desktops, multiple pet columns appear.

All authenticated Home Assistant users who can open the app share the **same pets and history**. They can all edit/delete entries; there is no per-user or pet-level permission model.

## Update the GitHub-installed app

1. Create a manual backup via **Settings → System → Backups**, selecting **Pet Bathroom Tracker (Preview)** in the backup contents. Keep the backup encryption emergency kit secure.
2. In **Settings → Apps → Install app**, select **⋮ → Check for updates** if Home Assistant hasn't recognized the new version.
3. Open the app's update dialog, read the changelog, and choose **Update**. **Do not uninstall** the existing app.
4. Confirm the app starts and the previous pets, icons, and bathroom history remain. The Logs tab should include `Pet Bathroom Tracker database ready`.
5. If you enable Watchdog, it will check the `/health` endpoint. It will not replace regular backups.

### Older Local-app previews

Local-app previews installed from `/local_apps` have a different Home Assistant app identity than this GitHub repository app. **Installing the GitHub version does not automatically migrate records from a Local app.** Keep the old app and its backup until you have explicitly tested a migration; don't assume the two apps share `/data`.

## Backups and recovery

The app stores records in private SQLite storage at `/data/tracker.db`. Starting with v0.5.4, startup automatically restricts `/data` to mode `700` and SQLite files to mode `600`, including restored databases. The configuration declares `backup: cold`, which stops the app briefly during a Home Assistant app-data backup to reduce SQLite write-consistency risk.

The project successfully restored an encrypted app backup to a separate Home Assistant OS VM on October 23, 2026 and confirmed edits survived restart. This does not guarantee every hardware version or backup environment will behave identically.

A Home Assistant encrypted backup `.tar` file is **not** a raw SQLite database. Do not share backup files or your encryption recovery key publicly. Detailed restoration instructions: https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/blob/main/RECOVERY.md

## Troubleshooting

- **App is not listed:** Confirm the correct repository URL, refresh the app store, and verify the GitHub repository is reachable.
- **Install fails:** Read the installation/build logs. This source-built preview needs network access to obtain dependencies.
- **App won't start:** Inspect the app's **Log** tab for database integrity errors or runtime failures.
- **Dashboard is forbidden/unreachable:** Use **Open Web UI** or its Home Assistant sidebar entry, not an internal container URL.
- **Times look wrong:** Check the configured time zone. Timestamps use local wall-clock values; take extra care with historical trips around daylight saving time.
- **Update available but no graphical Update button:** Check **Settings → Devices & services → Entities** for the **Pet Bathroom Tracker (Preview) → Update** entity under the Home Assistant Supervisor integration. If its status is disabled, enable it. Home Assistant may take time to discover the entity after first installation. If the entity is missing, restarting Home Assistant Core is an optional troubleshooting step; it is not normally required for installation. Do not uninstall the app to update it.
- **Records missing after update:** Don't uninstall or delete app data. Check your saved app backup before attempting recovery.

## Security and privacy

No remote accounts, advertising, analytics, or telemetry are built into this app. Home Assistant Ingress authenticates access. Pet records stay in your local Home Assistant storage unless your backups sync them elsewhere. This application has not been independently security-audited. Please report vulnerabilities privately to the repository owner.

More information: https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/blob/main/SECURITY.md
