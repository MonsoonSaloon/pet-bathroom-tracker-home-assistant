#!/bin/sh
set -eu

# Files created by the bootstrap process and the application are private.
umask 077

# Supervisor keeps options and the persistent database under /data.
mkdir -p /data
chown dogtracker:dogtracker /data
chmod 700 /data

# Protect existing/restored SQLite files before root performs a migration.
# Leave Supervisor-owned options.json untouched.
find /data -maxdepth 1 -type f -name 'tracker.db*' -exec chmod 600 {} \;

export DOG_TRACKER_DATABASE=/data/tracker.db
export DOG_TRACKER_INGRESS_ONLY=1
export DOG_TRACKER_TIMEZONE="$(python3 -c 'import json;from pathlib import Path;p=Path("/data/options.json");print(json.loads(p.read_text()).get("timezone", "America/New_York") if p.exists() else "America/New_York")')"

# Supervisor's options.json may be root-owned and private. Bootstrap as root;
# then hand only SQLite files to the unprivileged application account.
python3 /app/bootstrap.py
find /data -maxdepth 1 -type f -name 'tracker.db*' -exec chown dogtracker:dogtracker {} \;
find /data -maxdepth 1 -type f -name 'tracker.db*' -exec chmod 600 {} \;

echo 'Starting Pet Bathroom Tracker ingress service on port 8099'
exec su-exec dogtracker:dogtracker gunicorn --bind 0.0.0.0:8099 --workers 1 --threads 4 --timeout 30 --access-logfile - --error-logfile - app:app
