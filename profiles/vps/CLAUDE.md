## Headless Environment

This machine has **no display server or browser**. Do not attempt to use:

- agent-browser, chrome-devtools, playwright, or browser-tools MCP servers
- Any tool that launches a GUI window or browser process

### Web Scraping on VPS

Use crawl4ai REST API or firecrawl-mcp for web scraping. Both work headless.

For simple pages, WebFetch is sufficient.

### Resource Awareness

VPS environments have limited RAM and CPU. Be conservative with subagents:

- Limit concurrent subagents to 2 (each uses ~500MB with MCP processes)
- Prefer sequential task execution over parallel when possible
- Kill orphaned processes promptly: `~/.claude/scripts/cleanup-subagents.sh 2 5`
