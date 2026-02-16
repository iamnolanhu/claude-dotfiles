## Headless Environment

This machine has **no display server or browser**. Do not attempt to use:

- agent-browser, chrome-devtools, playwright, or browser-tools MCP servers
- Any tool that launches a GUI window or browser process

### Web Scraping on VPS

Use crawl4ai REST API or firecrawl-mcp for web scraping. Both work headless.

For simple pages, WebFetch is sufficient.
