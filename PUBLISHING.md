# Publishing and maintaining Pet Bathroom Tracker

## Repository

Public repository: https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant

The repository root contains `repository.yaml` and the app directory `pet_bathroom_tracker/` with its `config.yaml`. Home Assistant OS can add the repository from **Settings → Apps → Install app → ⋮ → Repositories** or via the [one-click Add repository link](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FMonsoonSaloon%2Fpet-bathroom-tracker-home-assistant).

## Tested so far (October 23, 2026)

- The GitHub `main` branch was pushed and the **Source checks** workflow completed successfully.
- The public repository was added to a clean Home Assistant OS VM on AMD64.
- The app installed, started, displayed a zero-pet welcome screen, accepted a pet and a combined pee/poop trip, and retained those records after an app restart.
- An earlier encrypted Home Assistant app backup was restored to a disposable second HA OS VM, preserving existing pets, icons, and history; an edit persisted through restart.

## Still required before a stable release

1. Build and test on real `aarch64` Home Assistant OS hardware (not just manifest syntax).
2. Review Python dependency vulnerability advisories and update pins as needed.
3. Consider pre-built, signed multi-platform container images to avoid on-device builds.
4. Capture **sanitized** example screenshots without private information.
5. Test in-place upgrade **v0.5.1 → v0.5.2** on an existing GitHub-installed app; verify data and view the changelog.
6. Repeat access, edit/delete, error-path, and watchdog checks in the publicly installed app.
7. Keep `stage: experimental` until the remaining checks and security review are complete.

## Making changes

1. Modify source in your local clone (outside cloud-sync folders).
2. Increment `version` in `pet_bathroom_tracker/config.yaml`, and keep the dashboard version label and tests consistent.
3. Add the new version at the top of **both** `CHANGELOG.md` and `pet_bathroom_tracker/CHANGELOG.md`. Keep the full version history for Home Assistant's update dialog.
4. Update the app's `README.md` and `DOCS.md` if installation/user-facing behavior changed.
5. Run local automated tests, commit, and push from GitHub Desktop.
6. Check **GitHub → Actions → Source checks** for a green run.
7. On the disposable HA OS instance, use **Check for updates**, update in place, and confirm previous pet/trip records survive.

For upgrades, do not uninstall. Maintain an independent encrypted Home Assistant backup and encryption emergency kit.

## Security hygiene

Review every changed file for keys, personal IPs, user-specific settings, and SQLite databases before pushing. The `.gitignore` covers common file patterns, but is not a security audit. Do not include data snapshots or Home Assistant backup archives in the public repository.

Home Assistant repository documentation: https://contributors.home-assistant.io/apps/guides/repository/
