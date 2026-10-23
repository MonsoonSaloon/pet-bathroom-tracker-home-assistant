# Publishing the Pet Bathroom Tracker preview on GitHub

The source package is ready to upload as a **preview**. It is not a verified stable 1.0 release.

## 1. Create your GitHub repository

1. Log in to GitHub and create a new public repository (suggested name: `pet-bathroom-tracker-home-assistant`).
2. Give it a description such as "Local-first multi-pet bathroom tracker for Home Assistant OS".
3. When uploading this package, use the **contents** of the extracted folder as the repository root. In particular, `repository.yaml` must be at the top level and `pet_bathroom_tracker/config.yaml` one directory below.
4. Confirm that no personal SQLite files, backups, passwords, IP addresses, or local keys are being uploaded. `.gitignore` excludes common SQLite and environment files but is not a substitute for inspecting files.
5. Add the repository URL and an appropriate maintainer/contact to `repository.yaml` after you know the real URL. No URL has been prefilled because your GitHub username and repository URL are not known.
6. Commit the files. GitHub will run the CI workflow; check its result under **Actions**. Automated tests alone do not prove every Home Assistant OS architecture works.

## 2. Test as a repository installation

In an isolated Home Assistant OS installation, open **Settings → Apps → Install app → ⋮ → Repositories**, add the GitHub URL, find **Pet Bathroom Tracker (Preview)**, and install it. The Dockerfile will be built **on the user's device** because `image:` is intentionally absent for the preview. Check logs, first-pet onboarding, create/edit/delete, persistence and non-admin Ingress access.

**Local-to-GitHub migration note:** A GitHub repo app and a Local app get different Supervisor IDs. Installing the repo app is a new app, not a seamless update of `local_pet_bathroom_tracker`. Don't remove the Local app or its backups until a separate migration/backup-restore plan is tested.

## 3. Make installation easier

Once the repository URL is known, add a Home Assistant "My" link to the README. The official [repository documentation](https://contributors.home-assistant.io/apps/guides/repository/) explains the `supervisor_add_addon_repository` link, which opens a pre-filled repository installer.

## 4. Before a stable release

- Prove an `aarch64` build and a clean GitHub repository installation.
- Publish **pre-built** container images with the official builder actions instead of building Python from source on every user's device.
- Review dependency security advisories and update pinned versions where needed.
- Finish user screenshots, proper logos, versioned release notes, and documentation of upgrades from Local apps.
- Keep the app in `stage: experimental` until those checks pass.

Sources: [Home Assistant repository documentation](https://contributors.home-assistant.io/apps/guides/repository/) and [publishing guidance](https://contributors.home-assistant.io/apps/guides/publishing/).
