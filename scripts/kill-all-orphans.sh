#!/bin/bash
# Kill all orphaned Claude and MCP processes - verbose version

echo "Scanning for orphans..."

# Count before
mcp_count=$(ps aux | grep -E "context7|serena|chrome-devtools|firecrawl|morphllm" | grep -v grep | wc -l | tr -d ' ')
claude_orphans=$(ps aux | grep "claude$" | grep "??" | wc -l | tr -d ' ')
worker_count=$(ps aux | grep -E "worker-service|mcp-server.cjs" | grep -v grep | wc -l | tr -d ' ')

echo "Found: $mcp_count MCP servers, $claude_orphans orphan Claude, $worker_count plugin workers"

if [ "$mcp_count" -gt 0 ]; then
    pkill -9 -f "context7|serena|chrome-devtools|firecrawl|morphllm" 2>/dev/null
    echo "Killed $mcp_count MCP servers"
fi

if [ "$claude_orphans" -gt 0 ]; then
    ps aux | grep "claude$" | grep "??" | awk '{print $2}' | xargs kill -9 2>/dev/null
    echo "Killed $claude_orphans orphan Claude processes"
fi

if [ "$worker_count" -gt 0 ]; then
    pkill -9 -f "worker-service.cjs|mcp-server.cjs" 2>/dev/null
    echo "Killed $worker_count plugin workers"
fi

total=$((mcp_count + claude_orphans + worker_count))
if [ "$total" -eq 0 ]; then
    echo "No orphans found - all clean!"
else
    echo "Cleaned up $total total processes"
fi
