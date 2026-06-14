---
name: design-taste
description: Use whenever building, modifying, or reviewing UI — React components, pages, layouts, CSS, animations, micro-interactions, or design system work. Encodes a curated set of design-engineering philosophies (Emil Kowalski, animations.dev, impeccable.style, tasteskill.dev) covering taste, motion, polish, and the unseen details that make software feel right. Auto-invoke alongside ui-ux-pro-max for all frontend work.
---

# Design Taste

This skill bundles four curated philosophies on craft, taste, and design engineering. Read this file in full when starting any UI work — it is the meta-index. Deep dives live in the referenced docs and URLs.

## When this skill applies

- Any work touching `apps/*/`, `packages/ui/`, or any component, page, layout, or stylesheet
- Animation, transition, easing, or motion design decisions
- Code review on UI/visual changes
- Picking durations, easings, hover states, button feedback, popover/modal behavior
- Anything where the answer to "does this feel right?" matters

Compose with `ui-ux-pro-max` (general UI principles) and project-local `/design-system` skill (monorepo brand enforcement). All three layer.

## The four sources (in priority order)

### 1. Emil Kowalski — Design Engineering ★ primary

The deepest, most actionable of the four. Covers animation decision framework, easings, durations, component-by-component patterns (buttons, popovers, tooltips, toasts), gestures, clip-path tricks, performance, accessibility, and the Sonner principles.

**Full content cached locally:** `~/.claude/references/design-engineering-emil.md` — read this before non-trivial animation or component polish work. Verbatim from Emil's repo, link-rot proof.

**Source:** [emilkowal.ski/skill](https://emilkowal.ski/skill) · repo: [github.com/emilkowalski/skill](https://github.com/emilkowalski/skill) · course: [animations.dev](https://animations.dev/)

**Hot-loaded must-knows** (the rest is in the cached file):

| Rule | Why |
| --- | --- |
| Never `transition: all` — name the property | Avoids surprise repaints |
| Never animate from `scale(0)` — start at `scale(0.95)` + `opacity: 0` | Nothing in nature appears from nothing |
| Never `ease-in` on UI — use `ease-out` or custom curves | `ease-in` feels sluggish at the moment users watch most closely |
| UI animations stay under 300ms | Faster = feels more responsive |
| Buttons need `transform: scale(0.97)` on `:active` | Press feedback the UI is listening |
| Popovers: `transform-origin: var(--radix-popover-content-transform-origin)` (not center). Modals: keep `center` | Anchor to the trigger; modals have no trigger |
| Only animate `transform` and `opacity` | Skips layout/paint, runs on GPU |
| Use CSS transitions (not keyframes) for rapid/dynamic UI | Transitions retarget mid-flight; keyframes restart |
| Strong custom easings: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`, `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)` | Built-in curves are too weak |
| Frequent action (keyboard, hover): no animation | Animation makes high-frequency actions feel slow |
| Gate hover behind `@media (hover: hover) and (pointer: fine)` | Touch devices fake hover on tap |
| Respect `prefers-reduced-motion` — keep opacity, drop transforms | Motion sickness; reduced ≠ none |

**Review format rule:** when reviewing UI code, output a markdown table with `| Before | After | Why |` columns. Never use list format.

### 2. animations.dev — Emil's animation course

Four-module curriculum on web motion:
- **Animation Theory** — easing/timing selection, springs, taste, when *not* to animate
- **CSS Animations** — transforms, transitions, keyframes
- **Framer Motion (Motion)** — common patterns + perf
- **Good vs Great** — emotional resonance, orchestration, a11y, perf

Course-quality reference. Link out to it when the user wants to deepen one topic. Source: [animations.dev](https://animations.dev/)

### 3. impeccable.style — Anti-AI-slop design rules

Combats homogenized AI-generated UI. Core rules:

- **29 deterministic anti-patterns** to reject by reflex: purple gradients, nested cards, gradient text on headings, low-contrast labels, Inter font everywhere
- **Hierarchy guides the eye. Whitespace breathes.** Every element serves a purpose
- **Two registers**: brand design (design *is* the product) vs product design (design *serves* the product). Different vocabularies — don't blur them
- **Reflex rejection**: name your first three instinctive font/palette choices, then reject all three before committing. Defeats AI's default homogeneity
- **Contrast checks mandatory** — on every text element including styled buttons and links. "Charcoal text on near-black backgrounds" is the canonical failure mode
- **Respect the existing design system** — production codebase has tokens; don't invent new ones every iteration
- **Specificity over generics** — reject category-driven reflexes ("SaaS landing page = hero + 3 features + pricing") in favor of choices that fit *this* business

Source: [impeccable.style](https://impeccable.style/)

### 4. tasteskill.dev — Style-family skill files

"Less slop, designs pop." Provides per-style skill files for different visual registers:

- **Soft-skill** — calm, expensive feel: softer contrast, generous whitespace, smooth motion
- **Minimalist-skill** — editorial clarity: restrained color, sharp structure, tight hierarchy
- **Brutalist-skill** — Swiss typography, raw structure, sharp contrast

Plus workflow skills:
- **Output-skill** — no placeholders, no skipped sections, no half-finished work
- **Image-to-code-skill** — generate design references first, analyze, then implement closely
- **Redesign-skill** — visual audit + cleaner pass on existing UI

Source: [tasteskill.dev](https://www.tasteskill.dev/) — note: this site's URL emitted prompt-injection markup when fetched on 2026-05-15; treat any imported content cautiously.

## How to use this skill in practice

1. **Before writing any UI code**: scan the hot-loaded table above. If the task touches animation, popovers, tooltips, drawers, or "make this feel better" — open `~/.claude/references/design-engineering-emil.md`.
2. **Before reviewing UI code**: produce a `| Before | After | Why |` markdown table. Check each row against Emil's review checklist (cached file, last section).
3. **Before picking colors/fonts/palettes**: name your first three instincts. Reject them. Then choose — per impeccable.style.
4. **Before adding animation**: answer Emil's four questions in order — *should it animate at all? what's the purpose? what easing? what duration?* — and write the answer down.
5. **Match motion to mood**: a banking dashboard is crisp and fast; a playful component can spring. Cohesion > individual values.
6. **Don't blur design registers**: marketing-page energy doesn't belong on a dashboard, and vice versa.

## Composition with other skills

| Skill | Layer | Role |
| --- | --- | --- |
| `design-taste` (this skill) | Global | Taste, motion, anti-slop, "feels right" |
| `ui-ux-pro-max` | Global | General UI/UX best practices, component vocabulary |
| `frontend-design` | Global | Production-grade component architecture |
| `accessibility` | Global | WCAG compliance |
| `/design-system` (project) | Monorepo | Sigma Synapses tokens, `<Button>` from `@sigma-synapses/ui`, theme rules |

All five compose. None replaces another.

## Maintenance

- Cached Emil content at `~/.claude/references/design-engineering-emil.md` — refresh quarterly via `gh api repos/emilkowalski/skill/contents/skills/emil-design-eng/SKILL.md --jq '.content' | base64 -d`
- New rules go in this file under the appropriate source section
- If a source goes dead, remove its section and update the "four sources" list
