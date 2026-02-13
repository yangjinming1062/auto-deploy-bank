# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cloudflare Agents SDK — a monorepo for building stateful AI agents on Cloudflare Workers. Each agent is a persistent, stateful execution environment powered by Durable Objects, with support for real-time communication, scheduling, AI model calls, MCP, workflows, and more.

## Commands

```bash
# Setup
npm install              # installs all workspaces; postinstall runs patch-package + playwright
npx changeset            # create a changeset (required for package changes)

# Build & typecheck
npm run build            # builds all packages (agents, hono-agents, ai-chat, codemode)
npm run typecheck        # TypeScript checking across repo
npm run check:exports    # verify package.json exports match build output

# Lint & format
npm run format           # oxfmt format all files
npm run check:exports    # check exports match build output
npm run lint             # oxlint examples/ packages/ guides/ openai-sdk/ site/
npm run check            # sherif + exports + oxfmt + oxlint + typecheck

# Testing
npm run test             # agents + ai-chat tests (vitest + vitest-pool-workers)
npm run test:react       # Playwright-based React hook tests (agents package)
CI=true npm test         # run tests in CI mode

# Run an example
cd examples/playground   # or any example
npm run dev              # starts Vite dev server + Workers runtime
```

## Architecture

### Packages (published to npm)

| Package | Purpose |
|---------|---------|
| `packages/agents` | Core SDK — Agent class, routing, state, scheduling, MCP, email, workflows |
| `packages/ai-chat` | Higher-level AI chat — persistent messages, resumable streaming, tool execution |
| `packages/hono-agents` | Hono middleware for agents |
| `packages/codemode` | Experimental — LLMs write executable TypeScript to orchestrate tools |
| `packages/agents-ui` | Shared UI components for examples |

### Key directories

- `examples/` — Self-contained demo apps (all full-stack, use Vite + Cloudflare plugin)
- `guides/` — In-depth pattern tutorials (anthropic-patterns, human-in-the-loop)
- `docs/` — Markdown docs synced to developers.cloudflare.com
- `openai-sdk/` — Examples using @openai/agents SDK
- `scripts/` — Repo-wide tooling (typecheck, export checks)

### Core Agent architecture (`packages/agents`)

- **Agent extends partyserver's `Server`** — Durable Object lifecycle, WebSocket hibernation, and connection management come from `partyserver`
- **State sync is bidirectional** — `this.setState()` on server broadcasts to all clients; client-side `agent.setState()` sends to server
- **RPC is reflection-based** — public methods on Agent subclasses are callable via `agent.call("methodName", ...args)`
- **Scheduling uses cron-schedule** — `this.schedule()` accepts delays, Dates, or cron strings
- **MCP has two sides** — `McpAgent` builds MCP servers; `MCPClientManager` connects to external MCP servers

### Example conventions

- All examples are full-stack (frontend + backend)
- Use `wrangler.jsonc` (not `.toml`) with `compatibility_date: "2026-01-28"`
- Use Kumo UI (`@cloudflare/kumo`) for components and `@cloudflare/agents-ui` for shared UI
- Include required components: `ConnectionIndicator`, `ModeToggle`, `PoweredByAgents`

## Code Standards

- **TypeScript**: Strict mode, ES2022 modules, `verbatimModuleSyntax` (use explicit `import type`)
- **Linting**: oxlint configured in `.oxlintrc.json` — `no-explicit-any: error`, `no-unused-vars: error`
- **Formatting**: oxfmt configured in `.oxfmtrc.json` (`trailingComma: "none"`, `printWidth: 80`)
- **Workers**: ES modules only, no native/FFI dependencies, always use `wrangler.jsonc`

## Testing

Tests use vitest with `@cloudflare/vitest-pool-workers` for Workers runtime tests:

- `packages/agents/src/tests/` — Workers runtime tests
- `packages/agents/src/react-tests/` — Playwright tests for React hooks
- `packages/ai-chat/src/tests/` — AI chat tests
- `packages/agents/src/tests-d/` — Type-level tests (`.test-d.ts`)

## Changesets

Changes to `packages/` affecting the public API need a changeset:

```bash
npx changeset  # interactive prompt — select packages, semver bump, description
```

This creates a markdown file in `.changeset/` consumed during release. Examples, guides, and sites don't need changesets.

## Related Documentation

- User-facing docs: `/docs/AGENTS.md`
- Design decisions: `/design/AGENTS.md`
- Example conventions: `/examples/AGENTS.md`
- Agent SDK internals: `/packages/agents/AGENTS.md`