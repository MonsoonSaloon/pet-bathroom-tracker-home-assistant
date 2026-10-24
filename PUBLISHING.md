# Publishing and maintaining Pet Bathroom Tracker

## Repository

Public repository: https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant

The repository root contains `repository.yaml` and the app directory `pet_bathroom_tracker/` with its `config.yaml`. Home Assistant OS can add the repository from **Settings → Apps → Install app → ⋮ → Repositories** or via the [one-click Add repository link](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FMonsoonSaloon%2Fpet-bathroom-tracker-home-assistant).

The app remains an **experimental preview**, not a stable v1.0 release. At the time of this document update (October 24, 2026), **v0.5.5 is the latest published version**. v0.5.6 has passed the release-candidate checks described below, but the official pull request to `main` and GitHub release are still pending.

## Tested so far (October 24, 2026)

### Earlier preview and v0.5.5 verification

- The GitHub `main` branch was pushed, and the **Source checks** workflow completed successfully.
- The public repository was added to a clean Home Assistant OS VM on AMD64.
- The app installed, started, displayed a zero-pet welcome screen, accepted a pet and a combined pee/poop trip, and retained those records after an app restart.
- An earlier encrypted Home Assistant app backup was restored to a disposable second Home Assistant OS VM, preserving pets, icons, and history; an edit persisted through restart.
- The v0.5.5 app on isolated VM 103 passed pet management, non-admin shared access, and intentional Supervisor Watchdog recovery tests.
- Native AMD64 and ARM64 container builds, entry operations, permissions, and restart-persistence checks passed in GitHub Actions.
- v0.5.5 was published on October 24, 2026, as an experimental preview.

### v0.5.6 security and automated verification

- The `security-v056` branch introduced stricter pet-ID validation and dashboard daylight-saving-time corrections, together with Flask API and JavaScript regression tests.
- Pull Request [#4](https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/pull/4) passed all nine reported checks, including source checks, CodeQL, and native AMD64/ARM64 container jobs.
- CodeQL reported no newly introduced findings on the reviewed pull request. This is not a substitute for an independent security assessment.

### v0.5.6 Home Assistant OS verification (AMD64)

- A fresh v0.5.6 installation from `security-v056` started successfully on isolated Home Assistant OS VM 103 and worked through Home Assistant Ingress.
- Pet creation, management, renaming, icon changes, entry editing, archiving/restoring, date navigation, and historical display were exercised on the test installation.
- Restart persistence and application logs were checked; no Python exceptions, database errors, or failed HTTP requests were observed in the reviewed logs.
- A separate database compatibility test initialized a temporary copy of a verified v0.5.5 database twice, confirming integrity, foreign-key consistency, and preservation of its records.
- A genuine **in-place v0.5.5 → v0.5.6 Home Assistant update** was rehearsed on a third independent installation, as documented below.
- An exact SQLite before/after comparison confirmed that all fields in the two pet records and four bathroom entries—including names, icons, dates, timestamps, activity flags, and notes—were unchanged.
- The upgraded app remained accessible through Ingress and recovered successfully after a further restart; its logs showed normal startup and successful health/API requests.

These results support an **experimental AMD64 release candidate**. They do not establish compatibility with every environment or complete an independent security audit.

## Release readiness and outstanding work

### v0.5.6 validation completed

- [x] Source, Flask API, and dashboard JavaScript tests passed.
- [x] CodeQL reported no new findings in the v0.5.6 pull request.
- [x] Native AMD64 and ARM64 container architecture tests passed.
- [x] Fresh Home Assistant OS AMD64 installation, Ingress, and user-interface checks passed.
- [x] SQLite database compatibility and repeat initialization tests passed.
- [x] Isolated, real Home Assistant OS v0.5.5 → v0.5.6 in-place update passed.
- [x] Pre-upgrade database backup and separate encrypted Home Assistant backup created and verified as part of the rehearsal.
- [x] Exact before/after pet and bathroom records comparison passed.
- [x] Post-upgrade restart and application-log review passed.

### Remaining steps before publishing v0.5.6

- [ ] Finish updating both READMEs, both changelogs, `RELEASE_CHECKLIST.md`, and this publishing guide on `security-v056`.
- [ ] Verify the final checks on [Pull Request #4](https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/pull/4) after the documentation commits.
- [ ] Merge Pull Request #4 **into `main`**, without deleting branches that are still needed.
- [ ] Verify `main` contains `version: "0.5.6"` in `pet_bathroom_tracker/config.yaml` and that the post-merge Actions checks pass.
- [ ] Confirm the normal, main-branch Home Assistant repository detects the v0.5.6 update. Verify existing data is preserved if upgrading a disposable main-branch installation.
- [ ] Create and publish the official GitHub v0.5.6 release, including the experimental-preview status, changes, upgrade advice, validation performed, and remaining limitations.
- [ ] Review public README and changelog wording after publication so that the published version is described accurately.

**Important:** Merging the version change into `main` can make v0.5.6 available through Home Assistant's repository update mechanism **before** a GitHub Release is published. Complete the rehearsal and final checks *before* merging. A GitHub Release is a separate publication step, not the switch that controls Supervisor update availability.

### Outstanding before a stable v1.0 release

- [ ] Full Home Assistant OS ARM64 installation, Ingress, and runtime testing on ARM64 hardware (for example, a Raspberry Pi).
- [ ] Broader independent security review.
- [ ] Broader real-world compatibility and recovery testing beyond the current development environment.

Optional future improvements:

- Publish pre-built AMD64/ARM64 container images.
- Expand automated testing to cover additional operating environments.
- Consider pinning reviewed Docker base-image digests and further reducing privileged startup operations, with separate regression testing.

Continue to designate releases as **experimental previews** until the outstanding stable-release requirements have been evaluated.

## Testing a branch safely

Home Assistant Supervisor supports Git-branch repository URLs such as:

`https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant#security-v056`

The `#branch` suffix gives the branch a **different repository identity and app data** from the normal GitHub repository. A fresh branch-based installation therefore tests installation and runtime, but **does not itself test an upgrade of the existing app or transfer stored records**.

### Proven v0.5.5 → v0.5.6 rehearsal procedure (October 24, 2026)

The isolated rehearsal used **Home Assistant OS VM 103**, leaving production VM 100 untouched:

1. Created `upgrade-rehearsal-v056` from the v0.5.5 `main` branch.
2. Added `https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant#upgrade-rehearsal-v056` as another repository and installed its v0.5.5 app as a separate instance.
3. Created two demonstration pets and four trips on October 23–24, 2026, including activity combinations and notes.
4. Captured a SQLite baseline via the SQLite backup API, copied it outside the container, and verified its SHA-256 hash and integrity. A separate encrypted Home Assistant backup was also downloaded to a PC.
5. Created temporary Pull Request [#5](https://github.com/MonsoonSaloon/pet-bathroom-tracker-home-assistant/pull/5) with base `upgrade-rehearsal-v056` and compare `security-v056`.
6. After all nine automated checks passed, merged **only into the temporary rehearsal branch**, making that branch report v0.5.6 without changing `main`.
7. Used Home Assistant's **Check for updates** and regular **Update** button on the existing rehearsal installation. The app updated in place from v0.5.5 to v0.5.6 while keeping its app identity.
8. Verified the Ingress dashboard and both days' entries, then compared all pet and entry rows with the saved v0.5.5 database. All records matched, and both SQLite integrity and foreign-key checks passed.
9. Restarted the upgraded app and reviewed its logs, confirming successful startup, API access, and health checks with no observed errors.

For future releases, repeat this pattern on an isolated test VM if an upgrade needs to be verified **before a change reaches `main`**. Do not merge a rehearsal-only pull request into `main`, and do not uninstall a working app to simulate an upgrade.

## Making changes and publishing a preview

1. Modify source in the local clone (outside cloud-sync folders), using a dedicated development branch for review.
2. Increment `version` in `pet_bathroom_tracker/config.yaml` and keep the dashboard version label and version-sensitive tests consistent.
3. Add the new version at the top of **both** `CHANGELOG.md` and `pet_bathroom_tracker/CHANGELOG.md`. Keep the full version history for Home Assistant's update dialog.
4. Update root and app READMEs, `DOCS.md`, and release/checklist documentation as applicable. Distinguish **candidate** from **published** status.
5. Run local automated tests, commit, and push; open a pull request against the intended branch.
6. Confirm GitHub Actions source checks, CodeQL, and relevant AMD64/ARM64 container tests pass.
7. Test fresh installation and an in-place upgrade with saved data on a **disposable Home Assistant OS installation**. Make independent, verified backups before the test.
8. Review the pull request's exact target, changed files, test evidence, and any remaining limitations.
9. Merge to `main` only once the candidate is ready for Home Assistant users to discover; check automated tests again after merge.
10. Verify the version manifest and actual Home Assistant update availability, then publish a GitHub Release with matching tag and release notes. Keep experimental-preview labeling where applicable.
11. Recheck published documentation and links, and monitor new issues or error reports.

For upgrades, **do not uninstall**. Maintain an independent encrypted Home Assistant backup and safely stored encryption emergency kit. Preserve the app's `/data/tracker.db` records through updates and verify important history afterward. A backup/restore test does not prove all environments are covered.

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

**GitHub Actions-only updates:**

- Confirm source checks and relevant container tests pass.
- Verify the updated workflows succeed after merging.
- No Home Assistant app version increase is required if application files are unchanged.

**Python or Docker dependency updates:**

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
- [x] `actions/setup-node` updated from v4 to v7.
- [x] `actions/checkout` updated from v4 to v7.
- [x] `actions/setup-python` updated from v5 to v7.
- [x] Automated checks passed after each merge.
- [x] No open dependency update pull requests remained after the initial review.

Pet Bathroom Tracker remains an experimental preview. Dependency updates should continue to be reviewed and tested before release.

## Security hygiene

Review every changed file for keys, personal IPs, user-specific settings, and SQLite databases before pushing. The `.gitignore` covers common file patterns, but is not a security audit. Do not include data snapshots or Home Assistant backup archives in the public repository.

Home Assistant repository documentation: https://contributors.home-assistant.io/apps/guides/repository/
