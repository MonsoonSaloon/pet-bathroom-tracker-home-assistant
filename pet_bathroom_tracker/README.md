# Pet Bathroom Tracker (Preview)

A private-to-your-home shared pet bathroom log for Home Assistant OS.
Track pee, poop, or both, review an hourly timeline, and keep persistent
history for multiple pets.

**Published experimental pre-release: v0.5.6** · Status: Experimental ·
Runs inside Home Assistant using Ingress

## Get started

1.  In Home Assistant, open **Settings → Apps → Install app**.
2.  From the upper-right ⋮ menu, choose **Repositories**.
3.  Add this repository:
    https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant.
4.  Install **Pet Bathroom Tracker (Preview)**, then open its
    **Configuration** tab to choose your time zone (for example,
    `America/New_York`).
5.  Start the app and select **Open Web UI**. Select **Add your first
    pet**.
6.  Enable **Show in sidebar** for convenient access by your household,
    including non-admin Home Assistant accounts.

Already installed? Use Home Assistant's **Update** button to upgrade in
place. Make a manual Home Assistant backup containing this app before
updating, and keep its encryption recovery key securely stored. Do not
uninstall the app if you want to keep your saved trips.

An isolated AMD64 Home Assistant OS test confirmed that an in-place
v0.5.5 → v0.5.6 update preserved both test pets, four bathroom entries,
icons, timestamps, and notes.

## Features

-   Any number of pets, custom names, and emoji icons
-   Add, edit, or delete bathroom trips with times and optional notes
-   Daily pee/poop counts and a color-coded hourly timeline
-   Mobile pet selector; multi-pet timeline on larger screens
-   Archive and restore pets without deleting trip history
-   Local SQLite records backed up through Home Assistant
    (`backup: cold`)
-   Shared across authenticated Home Assistant users with access to the
    app; no separate pet-tracker account

## v0.5.6 fixes and verification

-   **Stricter input validation:** Reject invalid, fractional, boolean,
    and oversized pet IDs; reject invalid pet/entry IDs in route paths
    with controlled error responses.
-   **Daylight-saving-time display correction:** Show saved local
    bathroom timestamps without unintended browser time normalization.
-   **Regression coverage:** Add Flask API input-validation and security
    tests, plus JavaScript tests for timestamp formatting and HTML
    escaping.
-   **Database compatibility:** No database migration is required;
    v0.5.6 does not change the SQLite schema.

Validation completed October 24, 2026. GitHub pull requests passed
source checks, CodeQL scanning, and native AMD64/ARM64 container tests.
On an isolated AMD64 Home Assistant OS VM 103, the v0.5.6 branch
installed, launched through Ingress, and passed functional, restart, and
log checks. A separate rehearsal branch was upgraded in place from
v0.5.5 to v0.5.6 using Home Assistant's **Update** button. Both test
pets, four entries across two dates, and saved notes remained visible.

Exact before-and-after SQLite record comparisons and database integrity
checks passed. This does not establish full ARM64 Home Assistant OS
compatibility or constitute an independent security audit.

## Important notes

-   This is an experimental community app, not an official Home
    Assistant integration or HACS plugin.
-   Home Assistant OS is required for this app installation method.
    AMD64 has been tested; AMD64 and ARM64 containers passed native
    automated tests; a full Home Assistant OS installation on ARM64
    remains unverified.
-   Pet data is shared: anyone with access to this app can view and edit
    all pets and trips. There are no per-user permissions.
-   The app does not require router port forwarding, a separate cloud
    service, or an access token.
-   Upgrades should preserve data, but make backups and retain your Home
    Assistant backup encryption recovery key securely.

## Documentation & support

-   Documentation tab in this app: detailed use, upgrades, and
    troubleshooting.
-   Full setup and recovery guides:
    https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant#readme
-   Release notes:
    https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/blob/main/CHANGELOG.md
-   Report an issue:
    https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/issues

**Release status:** v0.5.6 was published on GitHub on October 24, 2026
as an experimental pre-release. Validation included automated checks,
isolated AMD64 Home Assistant OS testing, and an in-place v0.5.5 →
v0.5.6 upgrade rehearsal. Full Home Assistant OS ARM64 testing and an
independent external security review remain outstanding.
