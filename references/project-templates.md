# Project Templates Reference

Referenced from ~/.claude/CLAUDE.md.

## Turborepo Monorepo Template

**Repo**: `iamnolanhu/template` (private)
**Stack**: Next.js 16, Tailwind v4, Bun, Node 24, TypeScript strict, Turborepo

Dual-deployment monorepo (same codebase, switch via env vars):

| Mode            | Infra                                   | Auth        | Email           | DB                |
| --------------- | --------------------------------------- | ----------- | --------------- | ----------------- |
| **Self-hosted** | Docker Compose + Traefik on your server | Better Auth | Nodemailer/SMTP | Postgres (own)    |
| **Managed**     | Vercel + Supabase                       | Better Auth | Resend          | Supabase Postgres |

**Packages** (scope `@my-project`, replaced by `scripts/setup.sh`):

| Package             | Purpose                                                 |
| ------------------- | ------------------------------------------------------- |
| `@my-project/auth`  | Better Auth + Drizzle adapter (server + client exports) |
| `@my-project/db`    | Drizzle ORM + optional Supabase client                  |
| `@my-project/ui`    | Shared React components with `cn()` utility             |
| `@my-project/trpc`  | tRPC v11 with public/protected procedures (optional)    |
| `@my-project/email` | React Email with auto-detect Resend vs SMTP (optional)  |
| `@my-project/jobs`  | BullMQ background jobs via Redis (optional)             |
| `@my-project/types` | Shared TypeScript types                                 |
| `@my-project/utils` | Shared utility functions                                |

**Key commands** (Bun, not pnpm):

```bash
bun run dev               # All apps (web:3000, dashboard:3001)
bun run build             # Build all
bun run typecheck         # Type check all
bun run lint              # ESLint all (v9, flat config)
bun run docker:dev        # Start local Postgres + Redis
bun run docker:prod       # Full stack with Traefik
./scripts/setup.sh <name> # Clone & rename for new project
```

**Key patterns**:

- Packages export raw `.ts` — apps transpile via `transpilePackages` in `next.config.ts`
- Auth: `@my-project/auth` (server), `@my-project/auth/client` (React hooks)
- DB: Supabase isolated behind `@my-project/db/supabase` (throws if env vars missing in self-hosted mode)
- Docker: Multi-stage Bun builds with `output: "standalone"`
- Config packages at `packages/config/` (eslint, tsconfig, tailwind)
