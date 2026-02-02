# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **GPT Researcher MCP Server** - a Python MCP (Model Context Protocol) server that exposes GPT Researcher's web research capabilities as MCP tools for AI assistants like Claude. It enables deep web research with source validation and report generation.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run MCP server (STDIO for local, SSE for Docker)
python server.py

# Run integration tests (requires server running with SSE transport)
python tests/test_mcp_server.py

# Docker
docker-compose up -d          # Build and run
docker-compose logs -f        # View logs
docker-compose down           # Stop
```

## Architecture

### Core Components

- **server.py**: FastMCP server entry point. Auto-detects transport (stdio for local, sse for Docker), registers tools/resources/prompts.
- **utils.py**: Response formatting, error handling, and session management utilities.

### MCP Interface

**Tools** (`@mcp.tool()`):
- `deep_research(query)` - Deep web research; returns research_id, context, sources
- `quick_search(query)` - Fast search; returns results with snippets
- `write_report(research_id, custom_prompt?)` - Generates report from prior research
- `get_research_sources(research_id)` - Lists sources used
- `get_research_context(research_id)` - Retrieves raw context

**Resources** (`@mcp.resource()`):
- `research://{topic}` - Direct cached access to research for a topic

**Prompts** (`@mcp.prompt()`):
- `research_query(topic, goal, report_format)` - Creates research prompts

### Transport Modes

The server auto-detects the environment:
- **STDIO** (default): Local development, Claude Desktop integration
- **SSE** (auto in Docker): Server-Sent Events for web/Docker/n8n integration
- **Streamable HTTP**: Modern web deployments

Override with `MCP_TRANSPORT` environment variable.

### Key Integration Points

- Uses `GPTResearcher` from `gpt_researcher` library for all research operations
- Stores active researchers by session: `mcp.researchers[research_id]`
- Caches completed research by topic: `research_store[topic]`
- Responses wrapped via `create_success_response()` → `{"status": "success", ...data}`

### Dependencies

- `gpt-researcher>=0.14.0` - Core research library
- `fastmcp>=2.8.0` - MCP server framework
- `fastapi` + `uvicorn` - HTTP/SSE transports
- `loguru` - Logging

## Environment Variables

Required:
- `OPENAI_API_KEY` - OpenAI API key
- `TAVILY_API_KEY` - Tavily API key for web search

Optional:
- `MCP_TRANSPORT` - Transport mode: `stdio` (default), `sse`, `streamable-http`
- `DOCKER_CONTAINER` - Set to `true` to force Docker/SSE mode