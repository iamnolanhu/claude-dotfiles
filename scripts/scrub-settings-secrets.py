#!/usr/bin/env python3
"""
Scrub inline secrets from Claude Code settings permission allowlists.

Claude Code persists approved Bash commands into `permissions.allow`. If a command
contained an inline secret (e.g. `TOKEN='dop_v1_...' curl ...`), that secret gets
written into settings.json. This removes such entries.

Safety:
  - Dry-run by DEFAULT (prints what it would remove). Use --apply to write.
  - Before writing, backs up to ~/.claude/.backups/settings/<name>.<timestamp>
    and logs to ~/.claude/.backups/CHANGELOG.md.
  - Only removes permission entries that match a known secret pattern; never
    touches anything else.

Usage:
  python3 ~/.claude/scripts/scrub-settings-secrets.py            # dry-run, default targets
  python3 ~/.claude/scripts/scrub-settings-secrets.py --apply    # back up + scrub
  python3 ~/.claude/scripts/scrub-settings-secrets.py --apply --quiet
  python3 ~/.claude/scripts/scrub-settings-secrets.py path/to/settings.json --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
BACKUP_DIR = HOME / ".claude" / ".backups" / "settings"
CHANGELOG = HOME / ".claude" / ".backups" / "CHANGELOG.md"

DEFAULT_TARGETS = [
    HOME / ".claude" / "settings.json",
    HOME / ".claude" / "settings.local.json",
]

# Known secret prefixes + assignments of a long value to a sensitive-looking var.
SECRET_PATTERNS = [
    r"dop_v1_[a-f0-9]{16,}",                         # DigitalOcean
    r"sk-or-v1-[A-Za-z0-9]{16,}",                    # OpenRouter
    r"sk-ant-[A-Za-z0-9_\-]{16,}",                   # Anthropic
    r"sk-[A-Za-z0-9]{32,}",                          # OpenAI-style
    r"ghp_[A-Za-z0-9]{20,}",                         # GitHub PAT (classic)
    r"github_pat_[A-Za-z0-9_]{20,}",                 # GitHub PAT (fine-grained)
    r"sbp_[a-f0-9]{20,}",                            # Supabase
    r"pmx_[a-f0-9]{20,}",                            # parse.bot
    r"xox[baprs]-[A-Za-z0-9-]{10,}",                 # Slack
    r"AKIA[0-9A-Z]{16}",                             # AWS access key id
    r"glpat-[A-Za-z0-9_\-]{20,}",                    # GitLab PAT
    # generic: SENSITIVE_VAR = 'long-high-entropy-value'
    r"(TOKEN|API[_-]?KEY|SECRET|PASSWORD|PASSWD|PAT|ACCESS[_-]?KEY)\s*=\s*['\"]?[A-Za-z0-9_\-]{16,}",
]
SECRET_RE = re.compile("|".join(SECRET_PATTERNS), re.IGNORECASE)

PERMISSION_BUCKETS = ("allow", "deny", "ask")


def redact(s: str) -> str:
    """Show enough to identify the rule, hide the secret value."""
    return SECRET_RE.sub(lambda m: m.group(0)[:8] + "…<redacted>", s)[:160]


def scrub_file(path: Path, apply: bool, quiet: bool) -> int:
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        print(f"!! {path}: cannot parse ({e}); skipping", file=sys.stderr)
        return 0

    perms = data.get("permissions")
    if not isinstance(perms, dict):
        return 0

    removed: list[str] = []
    for bucket in PERMISSION_BUCKETS:
        lst = perms.get(bucket)
        if not isinstance(lst, list):
            continue
        kept = []
        for entry in lst:
            if isinstance(entry, str) and SECRET_RE.search(entry):
                removed.append(f"{bucket}: {redact(entry)}")
            else:
                kept.append(entry)
        perms[bucket] = kept

    if not removed:
        if not quiet:
            print(f"   {path}: clean (0 secret entries)")
        return 0

    print(f"{'SCRUB' if apply else 'DRY-RUN'} {path}: {len(removed)} secret-bearing entr"
          f"{'y' if len(removed) == 1 else 'ies'}")
    if not quiet:
        for r in removed:
            print(f"     - {r}")

    if apply:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = BACKUP_DIR / f"{path.name}.{ts}"
        backup.write_text(path.read_text())
        path.write_text(json.dumps(data, indent=2) + "\n")
        with CHANGELOG.open("a") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M} | {path} | "
                    f"scrubbed {len(removed)} inline-secret permission entries "
                    f"(backup: {backup})\n")
        print(f"     ↳ backed up to {backup}")

    return len(removed)


def main() -> int:
    ap = argparse.ArgumentParser(description="Scrub inline secrets from CC settings permissions")
    ap.add_argument("targets", nargs="*", help="settings.json paths (default: ~/.claude/settings*.json)")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    ap.add_argument("--quiet", action="store_true", help="less output (for hooks)")
    args = ap.parse_args()

    targets = [Path(t) for t in args.targets] or DEFAULT_TARGETS
    total = sum(scrub_file(p, args.apply, args.quiet) for p in targets)

    if total and not args.apply:
        print("\nRun again with --apply to back up + remove these.")
    elif total and args.apply:
        print(f"\nDone. Removed {total} entr{'y' if total == 1 else 'ies'}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
