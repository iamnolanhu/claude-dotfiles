# Claude Code Configuration

## Key File Locations

| File                              | Purpose                                                 |
| --------------------------------- | ------------------------------------------------------- |
| `~/.claude.json`                  | **MCP config** - edit this for MCP servers              |
| `~/.claude/settings.json`         | Hooks, permissions, plugin settings                     |
| `~/.claude/CLAUDE.md`             | This file - Claude instructions                         |
| `~/.claude/.env`                  | **Global API keys** - Claude references across projects |
| `~/.claude/TROUBLESHOOTING.md`    | **Known issues & fixes** - check first when debugging   |
| `~/.claude/.changelog/`           | Weekly session changelogs                               |
| `~/.claude/.backups/CHANGELOG.md` | Log of config changes and fixes applied                 |

## MCP Configuration

**Config File**: `~/.claude.json` (verify with `/mcp` command)

### Core MCP Servers (no API key needed)

- **context7**: Documentation lookup, library patterns
- **serena**: Code assistant
- **morphllm-fast-apply**: Fast code application

### Optional MCP Servers (need API keys - enable with `./setup.sh add <name>`)

- **chrome-devtools**: Browser DevTools integration (desktop only)
- **firecrawl-mcp**: Web scraping (large-scale crawling)
- **github**: GitHub repo/issue/PR management
- **openrouterai**: OpenRouter AI models
- **apify**: Apify web scraping actors
- **digitalocean-mcp**: DigitalOcean App Platform & database management
- **n8n-mcp**: N8N workflow automation
- **crawl4ai**: Self-hosted scraping (SSE)
- **playwright**: Browser automation & testing
- **browser-tools-mcp**: Advanced browser automation
- **magic**: UI component generation (@21st-dev/magic)

### Plugin MCPs (auto-loaded by installed plugins)

- **plugin:claude-mem:mcp-search**: Persistent memory search
- **plugin:context7:context7**: Documentation lookup
- **plugin:serena:serena**: Code assistant

## Superpowers Plugin

**Source**: `obra/superpowers-marketplace`

A complete software development workflow built on composable skills that activate automatically.

### Core Workflow

1. **Brainstorming** - Refines ideas through questions before writing code
2. **Git Worktrees** - Creates isolated workspace on new branch
3. **Plan Writing** - Breaks work into 2-5 minute tasks with exact file paths
4. **Subagent Development** - Dispatches fresh agents per task with two-stage review
5. **TDD** - Enforces RED-GREEN-REFACTOR cycle
6. **Code Review** - Reviews against plan, blocks on critical issues
7. **Branch Finishing** - Presents merge/PR/keep/discard options

### Available Skills

| Category      | Skills                                                                                                                                                                                                                        |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Testing       | `test-driven-development`                                                                                                                                                                                                     |
| Debugging     | `systematic-debugging`, `verification-before-completion`                                                                                                                                                                      |
| Collaboration | `brainstorming`, `writing-plans`, `executing-plans`, `dispatching-parallel-agents`, `requesting-code-review`, `receiving-code-review`, `using-git-worktrees`, `finishing-a-development-branch`, `subagent-driven-development` |
| Meta          | `writing-skills`, `using-superpowers`                                                                                                                                                                                         |

### Commands

- `/superpowers:brainstorm` - Interactive design refinement
- `/superpowers:write-plan` - Create implementation plan
- `/superpowers:execute-plan` - Execute plan in batches

## Package Manager Preference

**Prefer Bun over npm/node** for all JavaScript and TypeScript operations:

| Task             | Use                | Instead of             |
| ---------------- | ------------------ | ---------------------- |
| Run files        | `bun run index.ts` | `node index.js`        |
| Install deps     | `bun install`      | `npm install`          |
| Add package      | `bun add <pkg>`    | `npm install <pkg>`    |
| Dev dependency   | `bun add -d <pkg>` | `npm install -D <pkg>` |
| Run scripts      | `bun run dev`      | `npm run dev`          |
| Execute packages | `bunx <pkg>`       | `npx <pkg>`            |

**Fallback to npm** only when:

- A tool explicitly requires Node.js/npm
- Bun compatibility issues arise
- The project explicitly uses npm (check for `package-lock.json` vs `bun.lockb`)

**Prefer uv over pip/venv/pipx** for all Python operations:

| Task                   | Use                            | Instead of                        |
| ---------------------- | ------------------------------ | --------------------------------- |
| Install package        | `uv add <pkg>`                 | `pip install <pkg>`               |
| Create venv            | `uv venv`                      | `python -m venv .venv`            |
| Run script             | `uv run script.py`             | `python script.py`                |
| Run tool               | `uvx <tool>`                   | `pipx run <tool>`                 |
| Install tool globally  | `uv tool install <tool>`       | `pipx install <tool>`             |
| Sync from requirements | `uv pip sync requirements.txt` | `pip install -r requirements.txt` |
| Pin Python version     | `uv python pin 3.12`           | (manual pyenv/asdf)               |

**Fallback to pip/venv** only when:

- A tool explicitly requires pip
- uv compatibility issues arise
- The project uses a different environment manager (poetry, conda, etc.)

## Global API Keys (.env)

**Location**: `~/.claude/.env` (600 permissions, never commit)

Claude can reference API keys from this file across all projects. When working with APIs:

1. **Check if key exists**: `grep <SERVICE> ~/.claude/.env`
2. **Reference in code**: Use environment variable name (e.g., `process.env.KAGGLE_KEY`)
3. **Add new keys**: Edit `~/.claude/.env` and document the variable name

**When using these keys in projects**:

- Never hardcode values
- Use `.env.example` with placeholder values for documentation
- Load from environment: `process.env.KAGGLE_KEY` (Node), `os.getenv("KAGGLE_KEY")` (Python)

**Security reminder**: Keys shared in conversation should be regenerated after setup.

## GitHub Access Priority

**Always use `gh` CLI (authenticated)** for all GitHub operations:

| Task             | Use                                           | Instead of              |
| ---------------- | --------------------------------------------- | ----------------------- |
| View repo        | `gh repo view`                                | WebFetch github.com     |
| List issues      | `gh issue list`                               | Scraping issues page    |
| View PR          | `gh pr view`                                  | WebFetch PR URL         |
| Get file content | `gh api repos/{owner}/{repo}/contents/{path}` | Raw GitHub URLs         |
| Search code      | `gh search code`                              | WebFetch search results |
| View release     | `gh release view`                             | WebFetch releases page  |

**Why authenticated access first**:

- Avoids GitHub's strict rate limits for unauthenticated requests
- Uses your existing `gh` authentication
- More reliable and structured data output
- Full access to private repos you have permissions for

**Fallback to WebFetch** only when:

- The `gh` CLI doesn't support the specific operation
- You need to access non-GitHub URLs that redirect from GitHub

## Documentation Lookup Priority

**Use context7 MCP** for library/framework documentation before web search:

| Task               | Use                         | Instead of                   |
| ------------------ | --------------------------- | ---------------------------- |
| Library API docs   | `context7:get-library-docs` | WebSearch "react hooks docs" |
| Framework patterns | `context7:get-library-docs` | WebFetch random blog posts   |
| Package usage      | `context7:get-library-docs` | Stack Overflow answers       |

**Why context7 first**:

- Authoritative, up-to-date library documentation
- Avoids outdated blog posts and deprecated examples
- Structured output optimized for code generation

**Fallback to WebSearch** when:

- Researching general programming concepts
- Bleeding-edge features not yet in context7
- Comparing multiple libraries or approaches

## Web Scraping Tool Priority

**Use crawl4ai REST API** (PRIMARY) for all web scraping tasks. Self-hosted, no rate limits, saves money vs firecrawl.

**Base URL**: Set `CRAWL4AI_URL` in `~/.claude/.env`
**Auth**: Set `CRAWL4AI_TOKEN` in `~/.claude/.env`

### Quick Reference

| Task         | Endpoint      | Method | Notes                                       |
| ------------ | ------------- | ------ | ------------------------------------------- |
| Crawl URL(s) | `/crawl`      | POST   | **Primary** - returns markdown, HTML, links |
| Screenshot   | `/screenshot` | POST   | Returns base64 image                        |
| Generate PDF | `/pdf`        | POST   | Returns base64 PDF                          |
| Execute JS   | `/execute_js` | POST   | Run JS on page                              |
| Get markdown | `/md`         | POST   | Requires server LLM config                  |
| Query docs   | `/ask`        | POST   | Requires server LLM config                  |

### Usage Examples

**Crawl a URL** (PRIMARY - returns markdown directly):

```bash
curl -s -X POST "$CRAWL4AI_URL/crawl" \
  -H "Authorization: Bearer $CRAWL4AI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://example.com"]}' | jq '.results[0].markdown'
```

Response includes:

- `raw_markdown` - Full page markdown
- `markdown_with_citations` - Markdown with reference numbers
- `references_markdown` - Link references section

### Note on /md endpoint

The `/md` endpoint requires server-side LLM configuration (returns `{"detail":"'llm'"}` error without it).
**Use `/crawl` instead** - it returns markdown directly in the response without LLM dependency.

### Why crawl4ai first

- **Free**: Self-hosted, no API costs
- **No rate limits**: Your own server
- **Full browser**: Playwright-based, handles JS-rendered pages
- **Smart extraction**: fit/bm25 filters for clean content

### Fallback to firecrawl-mcp when

- crawl4ai server is down (check `/health` first)
- Need sitemap-based crawling of entire sites
- Need structured data extraction schemas

### Fallback to WebFetch when

- Simple static page (no JS rendering needed)
- Quick content where quality isn't critical

## Agent & Subagent Timeout Rules

**Subagents MUST follow these rules to prevent hour-long hangs:**

| Rule                     | Requirement                                                |
| ------------------------ | ---------------------------------------------------------- |
| **Use fastest tools**    | `gh` > WebFetch for GitHub, context7 > WebSearch for docs  |
| **Progress updates**     | Report findings every 30 seconds, never go silent          |
| **Operation timeout**    | Abandon any single operation after 2 minutes of waiting    |
| **Fallback on failure**  | If primary approach fails, immediately try alternative     |
| **Never block silently** | Always communicate status, even if just "still waiting..." |

**If stuck on a slow operation:**

1. Stop waiting after 2 minutes
2. Report what you've learned so far
3. Try alternative approach (different tool, different query)
4. If all approaches fail, return partial results and explain blockers

**Red flags that indicate wrong approach:**

- WebFetch on GitHub URLs -> Use `gh` CLI instead
- WebSearch for library docs -> Use context7 MCP instead
- Waiting on rate-limited API -> Switch to authenticated tool
- No response after 30 seconds -> Report status, consider alternatives

**Parent agent responsibilities:**

- Use `run_in_background: true` for potentially slow operations
- Check agent output periodically with Read tool
- Kill stuck agents with TaskStop if no progress after 5 minutes

## Secret & API Key Handling

**NEVER expose secrets in any form:**

- Don't commit `.env`, `.env.*`, or any file containing secrets
- Don't log API keys, tokens, or credentials (even partially)
- Don't include secrets in error messages or stack traces
- Don't hardcode secrets in source code - use environment variables

**When working with secrets:**

- Reference by variable name only (e.g., `process.env.API_KEY`)
- Use `.env.example` with placeholder values for documentation
- Verify `.gitignore` includes all secret-containing files before any git operation

## Git Commit Policy

{{GIT_COMMIT_POLICY}}

## Claude Code Auto-Update Fix

If auto-update fails, remove temp dirs then update:

```bash
rm -rf ~/.nvm/versions/node/$(node -v)/lib/node_modules/@anthropic-ai/.claude-code-* && npm update -g @anthropic-ai/claude-code
```

## Engineering Excellence Standards

**Code to 10x staff engineer quality. Apply these principles to ALL projects:**

| Principle                     | Rule                                            | Violation Example                           |
| ----------------------------- | ----------------------------------------------- | ------------------------------------------- |
| **DRY**                       | If you repeat a pattern in >1 file, abstract it | Copy-pasting className strings across files |
| **KISS**                      | Simple > clever; readable > concise             | One-liner regex when a loop is clearer      |
| **YAGNI**                     | Don't build until needed                        | Adding config options "just in case"        |
| **Single Source of Truth**    | One canonical location per data/config          | Duplicating types across packages           |
| **Composition > Inheritance** | Build from small, focused pieces                | Deeply nested component hierarchies         |
| **Separation of Concerns**    | UI != logic; data fetch != display              | API calls inside UI components              |
| **Fail Fast**                 | Validate at boundaries, throw early             | Silently returning null on errors           |

**Before committing any code:**

- [ ] No duplicated patterns (DRY)
- [ ] Solution is as simple as possible (KISS)
- [ ] No speculative features (YAGNI)
- [ ] Data has single source of truth
- [ ] TypeScript strict mode passing (no `any`, no `@ts-ignore`)

**When you see copy-paste, STOP and create an abstraction first.**

## Config Backup Strategy

**Before editing any config file**, backup to `~/.claude/.backups/`:

```bash
# Backup command pattern
cp <file> ~/.claude/.backups/<folder>/<filename>.$(date +%Y%m%d_%H%M%S)

# Examples
cp ~/.claude/CLAUDE.md ~/.claude/.backups/claude-md/CLAUDE.md.$(date +%Y%m%d_%H%M%S)
cp ~/.claude/.mcp.json ~/.claude/.backups/mcp-json/.mcp.json.$(date +%Y%m%d_%H%M%S)
```

**Update changelog** after backup:

```bash
echo "$(date '+%Y-%m-%d %H:%M') | <file> | <reason>" >> ~/.claude/.backups/CHANGELOG.md
```

## Documentation Organization Pattern

**When creating project documentation, use this battle-tested structure:**

```
<project>/
+-- README.md              # Main entry point
+-- inventory/             # Current state (what exists)
|   +-- *.md              # Facts: servers, users, APIs, databases, etc.
+-- guides/                # How to use (instructions)
    +-- INDEX.md          # Navigation guide
    +-- <topic>/          # Organized by topic (ssh, deployment, etc.)
```

### Pattern Rules

**inventory/** - Document WHAT you have:

- Servers, IPs, domains
- User accounts, permissions
- API keys, credentials (where they're stored, not the values)
- Current configuration snapshots
- Resource inventories

**guides/** - Document HOW to use:

- Connection instructions
- Deployment guides
- Troubleshooting steps
- Templates and snippets
- Best practices

**Why this works:**

1. **Clear mental model** - "What do I have?" vs "How do I use it?"
2. **Scales infinitely** - Add new docs without clutter
3. **AI-friendly** - Clear categories help me navigate faster
4. **Separation of concerns** - Facts vs instructions
5. **Easy maintenance** - Update inventory without touching guides

## Things Claude Should NOT Do

- Don't edit config files without backing up first to `~/.claude/.backups/`
- Don't try to use crawl4ai MCP - it's broken (SSE bug #1594). Use REST API via curl instead
- Don't use `any` type in TypeScript without explicit approval
- Don't skip error handling or swallow errors silently
- Don't commit without running tests first
- Don't make breaking API changes without discussion
- Don't add unnecessary dependencies when stdlib suffices
- Don't over-engineer simple solutions
- Don't guess at file paths or URLs - verify they exist first
- Don't assume package manager - check for lockfiles first
- Don't scrape GitHub URLs when `gh` CLI can retrieve the same data
- Don't commit or log secrets, API keys, or `.env` file contents
- Don't let subagents run silently for >2 minutes without progress updates
- Don't use slow tools (WebFetch) when fast authenticated tools exist (gh, context7)
- Don't let subagent processes accumulate - kill with: `ps aux | grep "disallowedTools" | grep -v grep | awk '{print $2}' | xargs kill -9`
- Don't enable SSE-type MCP servers without testing - they can cause Claude Code to hang on startup
- Don't invent or guess email addresses - ask the user which email to use

---

_Update this file when Claude makes mistakes. Every error is a learning opportunity._
