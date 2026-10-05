#!/bin/sh
set -eu
swarm_project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$swarm_project_dir"
for swarm_python in python3.13 python3.12 python3.11 python3.10 python3.9 python3 python; do
  if command -v "$swarm_python" >/dev/null 2>&1 && "$swarm_python" -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)' 2>/dev/null; then
    exec "$swarm_python" production/render_all.py "$@"
  fi
done
printf '%s\n' 'Python 3.9 or newer is required. Install it, then run this command again.' >&2
exit 2
