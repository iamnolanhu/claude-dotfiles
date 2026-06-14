#!/usr/bin/env bash
# Throttled Claude Code marketplace auto-update.
# Triggered from the SessionStart hook in ~/.claude/settings.json.
# Runs `claude plugin marketplace update` (refreshes ALL configured marketplaces)
# at most once every THROTTLE_HOURS, fire-and-forget so session start isn't slowed.

set -uo pipefail

MARKER="$HOME/.claude/.marketplace-last-update"
LOG="$HOME/.claude/.marketplace-auto-update.log"
THROTTLE_HOURS=24
THROTTLE_SECONDS=$((THROTTLE_HOURS * 3600))

now=$(date +%s)
last=0
[ -f "$MARKER" ] && last=$(cat "$MARKER" 2>/dev/null || echo 0)
[[ "$last" =~ ^[0-9]+$ ]] || last=0
elapsed=$((now - last))

# Within throttle window — skip silently.
if [ "$elapsed" -lt "$THROTTLE_SECONDS" ]; then
  exit 0
fi

# Detached background job. We touch the marker BEFORE running so concurrent
# session starts within the same minute don't double-trigger; if the run fails
# the next session ≥24h later will retry.
echo "$now" > "$MARKER"

(
  ts() { date '+%Y-%m-%d %H:%M:%S'; }
  echo "[$(ts)] Starting marketplace update..." >> "$LOG"
  # `claude plugin marketplace update` (no name) refreshes every configured marketplace
  if claude plugin marketplace update >> "$LOG" 2>&1; then
    echo "[$(ts)] Marketplace update complete." >> "$LOG"
  else
    rc=$?
    echo "[$(ts)] Marketplace update FAILED (exit $rc) — will retry next eligible session." >> "$LOG"
    # Roll back marker so the next session retries instead of waiting 24h.
    rm -f "$MARKER"
  fi
) </dev/null >/dev/null 2>&1 &
disown 2>/dev/null || true

exit 0
