#!/usr/bin/env bash
# Print the STABLE Vercel git-branch preview URL for a branch.
#
# Vercel auto-maintains a per-branch alias of the form
#   <project>-git-<truncated-slug>-<hash>-<team>.vercel.app
# that ALWAYS points at the latest deployment of that branch (stable across
# pushes). The <hash> is derived from the full branch name (not predictable),
# so we resolve it: find the branch's latest deployment, then look up its alias.
#
# Use this instead of the per-deployment URL (…-<random>-…vercel.app) when
# sharing a preview link — it survives re-pushes.
#
# Usage: vercel-branch-url.sh <vercel-project> [git-branch] [path]
#   vercel-branch-url.sh monorepo-dashboard                  # current branch, /
#   vercel-branch-url.sh monorepo-dashboard cross/feat/x /admin
set -euo pipefail

proj="${1:?usage: vercel-branch-url.sh <vercel-project> [git-branch] [path]}"
branch="${2:-$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)}"
path="${3:-/}"
[ -n "$branch" ] || { echo "No branch given and not in a git repo." >&2; exit 1; }

# Latest deployment hostname for this exact branch.
# `grep -m1` (not `| head -1`) avoids a SIGPIPE that trips `pipefail`.
# `|| true` keeps a no-match/rate-limited pipeline from silently aborting the
# script via `set -e` (a plain `var=$(pipeline)` propagates the pipeline's exit).
dep="$(vercel ls "$proj" --meta githubCommitRef="$branch" 2>/dev/null \
  | grep -m1 -oE 'https://[a-z0-9.-]+\.vercel\.app' | sed 's|https://||' || true)"
[ -n "$dep" ] || { echo "No deployment found for $proj @ $branch (pushed yet?)." >&2; exit 1; }

# The deployment's own alias list (robust — no pagination). Prefer the stable
# git-branch alias (`…-git-<slug>-<hash>-…`); fall back to whatever alias exists.
alias="$(vercel inspect "$dep" --json 2>/dev/null | python3 -c "
import sys, json
try: a = json.load(sys.stdin).get('aliases') or []
except Exception: a = []
g = [x for x in a if '-git-' in x]
print((g or a)[0] if (g or a) else '')
" || true)"
[ -n "$alias" ] || { echo "No alias yet for $dep (deploy still building?)." >&2; exit 1; }

echo "https://${alias}${path}"
