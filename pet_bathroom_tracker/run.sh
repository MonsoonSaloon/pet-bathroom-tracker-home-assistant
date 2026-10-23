#!/bin/sh
set -eu
# HA stores options and the persistent database under /data.
mkdir -p /data
chown dogtracker:dogtracker /data
export DOG_TRACKER_DATABASE=/data/tracker.db
export DOG_TRACKER_INGRESS_ONLY=1
export DOG_TRACKER_TIMEZONE="$(python3 -c 'import json;from pathlib import Path;p=Path("/data/options.json");print(json.loads(p.read_text()).get("timezone", "America/New_York") if p.exists() else "America/New_York")')"
python3 /app/bootstrap.py
# Supervisor may create options.json owned by root; initialize while privileged,
# then hand only database files to the unprivileged application process.
find /data -maxdepth 1 -type f -name "tracker.db*" -exec chown dogtracker:dogtracker {} \;
echo 'Starting Pet Bathroom Tracker ingress service on port 8099'
exec su-exec dogtracker:dogtracker gunicorn --bind 0.0.0.0:8099 --workers 1 --threads 4 --timeout 30 --access-logfile - --error-logfile - app:app
