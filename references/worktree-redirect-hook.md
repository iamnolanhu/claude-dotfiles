# Worktree Redirect Hook — Reusable Pattern

Drop-in for any project where Claude Code's `EnterWorktree(name=...)` auto-creation conflicts with a custom worktree layout.

## When to use

You have a project where:

- Worktrees live somewhere other than `.claude/worktrees/` (e.g., `.worktrees/{area}/{type}/{desc}/`)
- Branch names contain `/` and you want directories to mirror the branch name (not sanitized to `+`)
- You want a long-lived, navigable worktree tree, not ephemeral isolation scratch space

Claude Code 2.1+ adds an "isolate before editing" instruction for background sessions, which calls `EnterWorktree(name=...)`. The tool hardcodes the path to `.claude/worktrees/` and replaces `/` with `+` in the directory name. There's no config to override the path — but a PreToolUse hook can intercept the call and redirect the agent to your project's flow.

## Files to add

### 1. `.claude/scripts/enforce-worktree-convention.sh`

```bash
#!/usr/bin/env bash
# PreToolUse hook: enforce the project's worktree convention.
# Blocks EnterWorktree(name=...) auto-creation; allows EnterWorktree(path=...).
set -euo pipefail

input="$(cat)"

tool_name="$(printf '%s' "$input" | jq -r '.tool_name // ""')"
[ "$tool_name" = "EnterWorktree" ] || exit 0

path="$(printf '%s' "$input" | jq -r '.tool_input.path // ""')"
[ -n "$path" ] && exit 0  # entering existing worktree by path is OK

cat <<'JSON'
{
  "decision": "block",
  "reason": "<PROJECT-SPECIFIC INSTRUCTIONS HERE — see template below>"
}
JSON
exit 0
```

Make executable: `chmod +x .claude/scripts/enforce-worktree-convention.sh`

The `reason` should be a multi-line string telling the agent the exact `git worktree add ...` command and the `EnterWorktree(path=...)` call to make. Example template:

```
"This project uses .worktrees/{area}/{type}/{desc}/ for worktrees (see CLAUDE.md). Claude Code's EnterWorktree(name=...) breaks the layout. Use the project workflow:\n\n  1. git fetch origin dev\n  2. git worktree add .worktrees/{area}/{type}/{desc} -b {area}/{type}/{desc} origin/dev\n  3. EnterWorktree(path='.worktrees/{area}/{type}/{desc}')\n\nValid areas: <list>. Always branch from origin/dev — never main."
```

### 2. `.claude/settings.json` (tracked — propagates to all sessions)

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "EnterWorktree",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/scripts/enforce-worktree-convention.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

If the project already has a `.claude/settings.json`, merge into the existing `hooks.PreToolUse` array. Don't put it in `.claude/settings.local.json` — that's gitignored and won't propagate.

### 3. Project `CLAUDE.md`

Add a short section under the Worktrees heading documenting:

- The hook exists and what it does
- The correct sequence (`git worktree add ...` + `EnterWorktree(path=...)`)
- Why (the location/sanitization conflict)

So when the hook fires, the agent has docs to fall back on.

## Verification

In a Claude Code session, ask the agent to "create a worktree to fix X". With the hook active:

- `EnterWorktree(name=...)` → blocked with your redirect message
- The agent runs `git worktree add .worktrees/{area}/{type}/{desc} -b ... origin/dev`
- Then `EnterWorktree(path=...)` → allowed

If the agent ignores the redirect, the hook keeps blocking; eventually it'll follow the path it's told.

## Why a hook, not just docs

Docs (CLAUDE.md, README) get ignored under context pressure. A PreToolUse hook is enforced by Claude Code itself before the tool runs — agents can't drift, even with summarized context. Spend 10 lines of shell + 12 lines of JSON once; never fight the worktree location again.

## Original context

First implemented in `sigma-synapses-monorepo` (2026-05-13). Project uses `.worktrees/{area}/{type}/{desc}/` with areas `website | dashboard | packages | infra | cross | business` and branches from `origin/dev`. See that repo's `.claude/settings.json`, `.claude/scripts/enforce-worktree-convention.sh`, and `CLAUDE.md` "Claude Code's EnterWorktree" section for a working example.
