# Security notes — Pet Bathroom Tracker (Preview)

- Uses Home Assistant **Ingress** for authentication; no separate application password or publicly mapped port.
- Allows web requests only from the Supervisor's documented Ingress address (`172.30.32.2`). Do not forward or expose port 8099 externally.
- Database lives in the app's private `/data`. Gunicorn runs as non-root `dogtracker`; a small startup script initializes and grants ownership of only the database files.
- `backup: cold` prevents a live copy during Supervisor-managed app backup.
- Health checks can be used with Home Assistant Watchdog, but are not a substitute for alerting or a restore drill.
- Limits write-request payloads and validates pet names/icons and timestamps. Doesn't grant privileged access, bind host networking, or request the Home Assistant API.
- **Shared data:** Any authenticated Home Assistant user with access to the app can read, add, edit and delete all trips and pets. Pet-level permissions and audit history do not exist. Treat the app as shared household data.
- Do not upload `/data/tracker.db`, Home Assistant backups, auth tokens, IP addresses, or encryption keys to public bug reports.
- The preview has not undergone a third-party security audit. Python dependencies are pinned in `requirements.txt`; check upstream advisories and update versions before a stable public release.

Report security concerns privately to the eventual repository maintainer rather than posting active exploitation details in public issues.
