# HyperFrames

**Repo:** <https://github.com/heygen-com/hyperframes>
**License:** Apache 2.0
**Author:** HeyGen
**Stars:** 12k+ (created 2026-03)
**Tagline:** "Write HTML. Render video. Built for agents."

## What

HTML-based video rendering framework. Compositions are plain HTML files with `data-*` attributes — Puppeteer drives headless Chrome through frames, FFmpeg encodes to MP4. Deterministic. No React, no build step.

Direct alternative to **Remotion**. The decisive difference: Remotion is source-available with paid tiers above thresholds. HyperFrames is fully Apache 2.0 — no per-render fees, no seat caps, OSI-compliant.

## When to use

- Programmatic video generation (marketing, social posts, demos)
- Client deliverables (case studies, pitch reels) where existing HTML templates can be reused
- Agent-driven content pipelines (LLM output → animated video)
- Personalized videos at scale (welcome reels, comparison content)

## Requirements

- Node ≥22
- FFmpeg installed locally

## Install (per project)

```bash
npx hyperframes init my-video    # scaffold
npx hyperframes preview          # live-reload browser preview
npx hyperframes render           # render to MP4
```

## Skills (Claude Code / Cursor / Codex / Gemini CLI)

Install upstream skills globally:

```bash
bunx skills add heygen-com/hyperframes -y -g
```

Installs to `~/.agents/skills/` and symlinks into `~/.claude/skills/`. Skills:

| Skill | What it teaches |
| --- | --- |
| `hyperframes` | HTML composition authoring (captions, TTS, audio-reactive, transitions) |
| `hyperframes-cli` | CLI commands: init, lint, preview, render, transcribe, tts, doctor |
| `hyperframes-registry` | Installing prebuilt blocks via `hyperframes add <name>` |
| `gsap` | GSAP animations, timelines, easing, plugins |
| `website-to-hyperframes` | Capture a URL → turn it into a video |
| `remotion-to-hyperframes` | Migration helper for existing Remotion projects |

## Catalog

50+ prebuilt blocks: shader transitions, social overlays (Instagram-style), animated charts, captions, lower-thirds. Browse: <https://hyperframes.heygen.com/catalog/blocks/data-chart>

```bash
npx hyperframes add flash-through-white   # shader transition
npx hyperframes add instagram-follow      # social overlay
npx hyperframes add data-chart            # animated chart
```

## Packages

- `hyperframes` — CLI
- `@hyperframes/core` — types, parsers, linter, runtime, frame adapters
- `@hyperframes/engine` — page-to-video capture (Puppeteer + FFmpeg)
- `@hyperframes/producer` — full pipeline (capture + encode + audio mix)
- `@hyperframes/studio` — browser-based composition editor
- `@hyperframes/player` — `<hyperframes-player>` web component for embedding
- `@hyperframes/shader-transitions` — WebGL transitions

## vs Remotion

| | HyperFrames | Remotion |
| --- | --- | --- |
| License | Apache 2.0 | Source-available, paid tiers |
| Authoring | HTML + CSS + GSAP | React (TSX) |
| Build step | None | Required |
| GSAP-style library clocks | Frame-accurate seekable | Plays at wall-clock during render |
| Distributed rendering | Single-machine today | Lambda |
| AI agent fit | First-class (ships skills) | Decent |

If you need distributed rendering at scale today and your team is already deep in React, Remotion is more mature. For everything else — especially when working with AI agents and existing HTML templates — HyperFrames wins.

## Gotchas

- **Git LFS** required to clone full repo for contributions (`brew install git-lfs`). For source-only: `GIT_LFS_SKIP_SMUDGE=1 git clone ...`
- **Skills location** is `~/.agents/skills/` (not `~/.claude/skills/`); they're symlinked in
- **Single-machine** rendering today — heavy batch jobs need careful CPU planning (FFmpeg-bound, not GPU)

## Docs

- Quickstart: <https://hyperframes.heygen.com/quickstart>
- Guides: <https://hyperframes.heygen.com/guides/gsap-animation>
- API: <https://hyperframes.heygen.com/packages/core>
- Comparison: <https://hyperframes.heygen.com/guides/hyperframes-vs-remotion>

## Project usage

| Project | Usage doc | Plan |
| --- | --- | --- |
| sigma-synapses-monorepo | `docs/engineering/VIDEO_RENDERING.md` | `.claude/plans/to-implement/hyperframes-integration.md` |
