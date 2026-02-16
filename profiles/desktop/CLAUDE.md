## Browser Automation Tool Priority

**Prefer agent-browser CLI** for all browser automation tasks:

| Task            | Use                        | Instead of                      |
| --------------- | -------------------------- | ------------------------------- |
| Screenshots     | `agent-browser screenshot` | chrome-devtools, Playwright MCP |
| Navigation      | `agent-browser navigate`   | chrome-devtools, Playwright MCP |
| Click/Fill      | `agent-browser click/fill` | chrome-devtools, Playwright MCP |
| Page content    | `agent-browser snapshot`   | chrome-devtools, firecrawl      |
| Form automation | `agent-browser fill-form`  | chrome-devtools                 |

**Fallback to other tools** when:

- **chrome-devtools MCP**: Need DevTools-specific features (network interception, performance traces, console access)
- **Playwright MCP**: Need cross-browser testing (Firefox, WebKit) or complex test scenarios
- **firecrawl-mcp**: Need large-scale web scraping or crawling multiple pages
- **browser-tools-mcp**: Need performance monitoring or cross-browser compatibility testing

**Why agent-browser first**:

- Fast Rust CLI with minimal overhead
- Simple command interface for common tasks
- Integrated Claude Code plugin with skills
- Headless by default, efficient for AI agent workflows
