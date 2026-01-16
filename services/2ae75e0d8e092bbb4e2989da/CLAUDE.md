# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HyperChat is an open-source Chat client supporting MCP (Model Context Protocol) with LLM integrations (OpenAI, Claude, Qwen, Deepseek, GLM, Ollama). Cross-platform desktop app (Windows, macOS, Linux) with web interface access.

## Development Commands

```bash
# Install dependencies
cd electron && npm install
cd web && npm install

# Start development (runs web dev server + webpack watch + electron)
cd /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da && npm run dev

# Build production (web + electron installer)
npm run build

# Test build
npm run test

# Run web only
cd web && npm start

# Run electron only (with hot reload)
cd electron && npm run dev

# Build node-only version (no electron, web access via browser)
npm run prod_node
```

## Architecture

### Monorepo Structure
- **`web/`** - React 18 frontend with TypeScript, Ant Design, Webpack
- **`electron/`** - Electron main process with MCP implementation
- **`common/`** - Shared TypeScript types and utilities

### Web Frontend (`web/src/`)
- **Router**: `router.tsx` defines routes (Chat, MCP Market, Knowledge Base, Tasks, Settings)
- **Pages**: `pages/chat/`, `pages/hyperAgent/`, `pages/knowledgeBase/`, `pages/setting/`
- **State**: `common/data.ts` - Shared Data<T> classes for persistence (ChatHistory, Agents, GPT_MODELS, MCP_CONFIG, etc.)
- **API**: `common/call.ts` - IPC calls to electron main process
- **AI**: `common/openai.ts` - LLM API abstraction layer

### Electron Backend (`electron/ts/`)
- **Entry**: `main.mts` - Electron main process, creates BrowserWindow, handles IPC
- **MCP Servers**: `mcp/servers/` - Custom MCP server implementations:
  - `hyper_tools/` - Browser automation, web scraping, file operations
  - `KnowledgeBase/` - RAG-based knowledge base with vector storage
  - `Task/` - Scheduled task execution with agents
  - `terminal/` - Shell command execution
  - `settings/` - Application settings management
- **Communication**: `websocket.mts` - HTTP/WebSocket server for web frontend communication
- **Polyfills**: `polyfills/` - Electron vs Node.js abstraction layer

### Data Persistence
- Uses `Data<T>` class pattern in `common/data.ts` for typed data with optional WebDAV sync
- Key data stores: `ChatHistory`, `Agents`, `GPT_MODELS`, `MCP_CONFIG`, `KNOWLEDGE_BASE`, `TaskList`, `VarList`
- Electron process reads/writes files directly; web frontend accesses via IPC

## Key Technologies

- **UI**: React 18, Ant Design 5, Tailwind CSS, Monaco Editor, xterm.js
- **AI/LLM**: OpenAI SDK, LangChain, @modelcontextprotocol/sdk
- **Build**: Webpack 5, TypeScript, zx (for task scripts)
- **RAG**: hnswlib-node, @llm-tools/embedjs for vector storage

## Important Files

- `/home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/task.mts` - Root build orchestration script
- `/home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/electron/task.mts` - Electron build script
- `/home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/web/task.mts` - Web build script
- `/home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/electron/ts/mcp/servers/index.mts` - MCP server registry
- `/home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/electron/ts/common/data.mts` - Data persistence implementation