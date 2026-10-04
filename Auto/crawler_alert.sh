#!/bin/bash
# Invoked by systemd OnFailure=; records the failure where the health checks and the user can see it.
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MESSAGE="ytd-trends crawler failed at $(date -Is); see 'journalctl --user -u ytd-trends.service' and $APP_DIR/Logs/Extractio.log"
logger -t ytd-trends -p user.crit "$MESSAGE"
echo "$MESSAGE" > "$APP_DIR/Logs/crawler.failed"
command -v notify-send >/dev/null && notify-send -u critical "Extractio crawler failed" "$MESSAGE" || true
