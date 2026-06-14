# Claude Squad (`cs`) — Cheatsheet

Run a fleet of Claude Code agents in parallel, each isolated in its own git
worktree/branch, watched from one TUI. A friendlier face over tmux — **you never
type raw tmux commands.** Installed via `brew install claude-squad` (binary
`claude-squad`, aliased to `cs`).

## Launch

```bash
cd <a git repo>     # cs operates on the repo you launch it from
cs                  # opens the TUI
```

The TUI = **sidebar of agent sessions (left)** + **live preview of the
highlighted one (right)**. The keymap is always printed at the bottom — nothing
to memorize.

## The whole vocabulary

| Key | Does |
| --- | --- |
| `n` | new session (you type the task; it spins up a fresh worktree + branch) |
| `N` | new session **with a custom prompt** |
| `↑` / `↓` | move the highlight between sessions in the sidebar |
| `↵` Enter | **attach** — drop into that agent's live terminal to interact/answer |
| `Ctrl-q` *(or `Esc`)* | detach — pop back out to the list (the agent keeps running) |
| `s` | **submit** — commit that session's changes to its branch |
| `c` | checkout / open that session's worktree |
| `p` | push the branch / open a PR flow |
| `D` | kill + delete the session (and its worktree) |
| `q` | quit the TUI (sessions you didn't kill keep running in the background) |
| `?` | in-app help with the full current keymap |

> If a key here ever disagrees with what's printed at the bottom of the TUI,
> trust the TUI — it reflects your installed version (1.0.18 as of 2026-06-05).

## How it works under the hood

- Each session = its own **git worktree + branch** (isolation, like the monorepo
  worktree discipline) + its own `claude` process inside a tmux session.
- `cs` manages the tmux part for you; you drive it with the keys above.
- Config: `~/.claude-squad/config.json`
  - `default_program` → the claude binary it launches
    (currently `…/node/v24.11.1/bin/claude` — **re-point this when node updates**)
  - `branch_prefix` → `nolanhu/` (branches are named `nolanhu/<slug>`)
  - `auto_yes` → `false` (agents pause for your approval; flip to `true` for
    hands-off runs — riskier)

## ⚠️ Caveats for THIS machine / monorepo

- **Kernel-panic watch:** each session is a full `claude` process (~0.5–1GB RAM).
  On the 2018 Intel Mac under the open T2-watchdog investigation, **keep
  concurrency low (2–3 sessions)** and glance at `swap_used` while running.
  Memory pressure + process accumulation are two live panic hypotheses.
- **sigma-synapses-monorepo branch flow:** cs creates `nolanhu/<slug>` branches
  in its own worktrees — that does **not** match the repo's strict
  `{area}/{type}/{desc}` convention or the `{area}/dev → dev → main` merge flow,
  and there's a PreToolUse hook enforcing worktree naming. Use cs for
  **exploratory / parallel investigation** there (or in other repos) first;
  don't wire its auto-branches into the real area-branch promotion flow without
  deciding how they reconcile.

## When to reach for it vs. alternatives

- **`cs`** — several independent tasks at once, want to watch + attach to each,
  no tmux memorization. Closest to cmux (which needs macOS 14+; this Mac is
  Ventura 13.7.6, so cmux is out).
- **`claude agents`** (native, stable) — simpler list view, peek (`Space`) /
  attach (`Enter`); no worktree auto-management.
- **Agent Teams** (`claude --teammate-mode in-process`, experimental) — when you
  want the agents to **coordinate with each other** (shared task list + inter-agent
  messaging), not just run in parallel.

_Set up 2026-06-05. Source: https://github.com/smtg-ai/claude-squad_
