#!/bin/bash
set -uo pipefail
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR/Auto" || exit 1
"$APP_DIR/venv/bin/python3" get_trends.py
status=$?
[ "$status" -eq 0 ] && rm -f "$APP_DIR/Logs/crawler.failed"
exit "$status"
