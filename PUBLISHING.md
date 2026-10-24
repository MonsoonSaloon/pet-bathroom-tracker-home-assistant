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

Pet Bathroom Tracker v0.5.5 was published on October 24, 2026, as an experimental preview.

### Completed verification
- [x] Public GitHub repository installation tested on AMD64 Home Assistant OS.
- [x] First-run pet creation and bathroom entry tested.
- [x] Encrypted Home Assistant app backup restored successfully to a separate Home Assistant OS VM.
- [x] Existing pets, icons, and bathroom history recovered successfully.
- [x] In-place upgrade from v0.5.4 to v0.5.5 tested on AMD64 Home Assistant OS.
- [x] Existing data preserved through the v0.5.5 update and subsequent restart.
- [x] Adding, editing, and deleting bathroom entries verified after updating.
- [x] GitHub Actions source checks and AMD64/ARM64 container tests passed.
- [x] All seven previously reported CodeQL findings resolved.
- [x] GitHub v0.5.5 release published.

### Outstanding before stable v1.0
- [ ] Test installation and runtime on physical ARM64/Raspberry Pi Home Assistant OS hardware.
- [ ] Complete a broader independent security review.
- [ ] Establish an ongoing dependency update and vulnerability review process.
- [ ] Recheck the complete pet-management workflow on the public release.
- [ ] Reverify non-admin household access on the current public release.
- [ ] Test intentional Watchdog fault recovery in an isolated installation.

Optional future improvements:
- Publish pre-built AMD64/ARM64 container images.
- Expand automated testing to cover additional operating environments.

Keep the release designated as experimental until the outstanding checks have been evaluated.

## Making changes

1. Modify source in your local clone (outside cloud-sync folders).
2. Increment `version` in `pet_bathroom_tracker/config.yaml`, and keep the dashboard version label and tests consistent.
3. Add the new version at the top of **both** `CHANGELOG.md` and `pet_bathroom_tracker/CHANGELOG.md`. Keep the full version history for Home Assistant's update dialog.
4. Update the app's `README.md` and `DOCS.md` if installation/user-facing behavior changed.
5. Run local automated tests, commit, and push from GitHub Desktop.
6. Check **GitHub → Actions → Source checks** for a green run.
7. On the disposable HA OS instance, use **Check for updates**, update in place, and confirm previous pet/trip records survive.

For upgrades, do not uninstall. Maintain an independent encrypted Home Assistant backup and encryption emergency kit.


## Dependency maintenance

Pet Bathroom Tracker uses GitHub Dependabot to monitor dependencies and propose updates.

### Automated monitoring

Dependabot is configured in `.github/dependabot.yml` to check the following ecosystems weekly:

- Python packages in `pet_bathroom_tracker/requirements.txt`
- GitHub Actions used by repository workflows
- Docker base images in `pet_bathroom_tracker/Dockerfile`

Dependabot opens pull requests for available updates. Updates are reviewed and merged manually; automatic merging is not enabled.

GitHub Dependabot alerts, CodeQL, and secret scanning provide additional security monitoring.

### Weekly maintenance procedure

1. Open the repository's Pull Requests page and review open Dependabot pull requests.
2. Check Security and quality for newly reported vulnerabilities or exposed secrets.
3. Review each dependency update's release notes, breaking changes, and compatibility requirements.
4. Inspect the proposed file changes.
5. Confirm GitHub Actions tests and CodeQL checks pass.
6. Merge compatible updates individually.
7. Verify automated checks pass again on the main branch.
8. Document significant dependency changes in the project changelog when appropriate.

### Testing requirements

GitHub Actions-only updates:
- Confirm source checks and relevant container tests pass.
- Verify the updated workflows succeed after merging.
- No Home Assistant app version increase is required if application files are unchanged.

Python or Docker dependency updates:
- Review compatibility with the supported Home Assistant OS environment.
- Confirm automated source and container tests pass.
- Test application startup and normal tracking functionality on an isolated Home Assistant installation when appropriate.
- Verify existing pet records remain intact.
- Create a backup before installing an application update.
- Increment the application version when publishing a new application build.

### Security considerations

- Never automatically merge dependency updates without review.
- Prioritize security fixes based on severity and actual exposure.
- Do not publish credentials, tokens, databases, or private user information in issues or logs.
- Use GitHub's private vulnerability reporting feature for security issues.
- Continue periodic manual reviews; automated scanning does not replace security testing.

### Initial maintenance verification — October 24, 2026

- [x] Dependabot configured for Python, GitHub Actions, and Docker.
- [x] Weekly dependency update checks activated.
- [x] Dependabot successfully created update pull requests.
- [x] actions/setup-node updated from v4 to v7.
- [x] actions/checkout updated from v4 to v7.
- [x] actions/setup-python updated from v5 to v7.
- [x] Automated checks passed after each merge.
- [x] No open dependency update pull requests remained after the initial review.

Pet Bathroom Tracker remains an experimental preview. Dependency updates should continue to be reviewed and tested before release.

## Security hygiene

Review every changed file for keys, personal IPs, user-specific settings, and SQLite databases before pushing. The `.gitignore` covers common file patterns, but is not a security audit. Do not include data snapshots or Home Assistant backup archives in the public repository.

Home Assistant repository documentation: https://contributors.home-assistant.io/apps/guides/repository/
