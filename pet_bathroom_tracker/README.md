# Pet Bathroom Tracker (Preview)

A private-to-your-home **shared pet bathroom log** for Home Assistant OS. Track pee, poop, or both, review an hourly timeline, and keep persistent history for multiple pets.

**Preview version: 0.5.2** · **Status: Experimental** · **Runs inside Home Assistant using Ingress**

## Get started

1. In Home Assistant, open **Settings → Apps → Install app**.
2. From the upper-right **⋮** menu, choose **Repositories**.
3. Add this repository: **https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant**.
4. Install **Pet Bathroom Tracker (Preview)**, then open its **Configuration** tab to choose your time zone (for example, `America/New_York`).
5. **Start** the app and select **Open Web UI**. Select **Add your first pet**.
6. Enable **Show in sidebar** for convenient access by your household, including non-admin Home Assistant accounts.

**Already installed?** Use Home Assistant's **Update** button to upgrade in place. Make a manual Home Assistant backup containing this app before updating. **Do not uninstall** if you want to keep your saved trips.

## Features

- Any number of pets, custom names and emoji icons
- Add, edit, or delete bathroom trips with times and optional notes
- Daily pee/poop counts and color-coded hourly timeline
- Mobile pet selector; multi-pet timeline on larger screens
- Archive and restore pets without deleting trip history
- Local SQLite records backed up through Home Assistant (`backup: cold`)
- Shared across authenticated Home Assistant users with access to the app; **no separate pet-tracker account**

## Important notes

- This is an **experimental community app**, not an official Home Assistant integration or HACS plugin.
- Home Assistant OS is required for this app installation method. AMD64 has been tested; ARM64 remains unverified.
- Pet data is shared: anyone with access to this app can view and edit all pets and trips. There are no per-user permissions.
- The app does not require any router port forwarding, separate cloud service, or access token.
- Upgrades should preserve data, but make backups and retain your Home Assistant backup encryption recovery key securely.

## Documentation & support

- **Documentation tab** in this app: detailed use, upgrades, and troubleshooting.
- **Full setup and recovery guides:** https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant#readme
- **Release notes:** https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/blob/main/CHANGELOG.md
- **Report an issue:** https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/issues

**Changes in v0.5.2:** replaced outdated store text with setup instructions, added the one-click repository link to the main README, and refreshed release/testing documentation. Tracking behavior and database schema are unchanged.
