# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AutoGPT-Next-Web is a web-based UI for AutoGPT, allowing users to deploy and interact with autonomous AI agents. It's built on Next.js 13 with TypeScript, providing a modern web interface for creating and managing AI agents.

## Tech Stack

- **Framework**: Next.js 13 (Pages Router)
- **Language**: TypeScript
- **Database**: Prisma ORM with MySQL/SQLite
- **Authentication**: NextAuth
- **API Layer**: tRPC for type-safe APIs
- **State Management**: Zustand
- **Styling**: Tailwind CSS with Radix UI components
- **Testing**: Jest with React Testing Library
- **Internationalization**: next-i18next (English, Chinese, Japanese)
- **Payments**: Stripe integration
- **Deployment**: Docker, Vercel

## Key Architecture

### Directory Structure

- `src/pages/`: Next.js pages and API routes
  - `src/pages/api/`: API endpoints including:
    - `/api/auth/`: NextAuth authentication
    - `/api/agent/`: Agent management (create, start, execute)
    - `/api/trpc/`: tRPC endpoint
    - `/api/webhooks/stripe/`: Stripe webhooks

- `src/server/`: tRPC server implementation
  - `src/server/api/root.ts`: Main router combining all tRPC routers
  - `src/server/api/routers/`: Individual API routers (agent, account, example)
  - `src/server/db.ts`: Prisma client instance
  - `src/server/auth.ts`: NextAuth configuration

- `src/services/agent-service.ts`: Core agent execution logic using LangChain
  - `startGoalAgent()`: Initial goal processing
  - `analyzeTaskAgent()`: Task analysis and action planning
  - `executeTaskAgent()`: Task execution with web search capability

- `src/components/`: React components
  - `src/components/stores/`: Zustand stores (agentStore, messageStore)
  - Individual UI components for chat, tasks, settings, etc.

- `src/hooks/`: Custom React hooks (useAuth, useAgent, useSettings, etc.)

- `src/utils/`: Utilities for API calls, parsers, prompts, helpers

- `prisma/schema.prisma`: Database schema
  - User, Account, Session models (NextAuth)
  - Agent and AgentTask models for agent management

## Common Development Commands

### Development
```bash
# Start development server
npm run dev

# Run with Docker (development)
docker-compose -f docker-compose.dev.yml up -d --remove-orphans

# Interactive setup (installs deps, configures env, initializes DB)
./setup.sh
```

### Building & Deployment
```bash
# Build for production
npm run build

# Start production server
npm start

# Build with Docker (production)
docker-compose -f docker-compose.prod.yml up -d --remove-orphans
```

### Code Quality
```bash
# Run ESLint
npm run lint

# Run tests
npm test

# Run single test file
npm test -- extract-array.test.ts
```

### Database
```bash
# Push schema changes to database
npx prisma db push

# Switch to SQLite (for local development)
./prisma/useSqlite.sh

# Generate Prisma client
npx prisma generate
```

## Environment Setup

Required environment variables (see `.env.example`):

```bash
# Core
OPENAI_API_KEY=sk-...           # Required: OpenAI API key
NEXTAUTH_SECRET=...             # Required: Generated with `openssl rand -base64 32`
NEXTAUTH_URL=http://localhost:3000
DATABASE_URL=...                # MySQL or file:./db.sqlite

# Guest Mode (optional)
NEXT_PUBLIC_GUEST_KEY=...       # Comma-separated keys for guest access

# Web Search (optional)
NEXT_PUBLIC_WEB_SEARCH_ENABLED=true/false
SERP_API_KEY=...                # From https://serper.dev/

# Auth Providers (optional, for production)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
DISCORD_CLIENT_ID=...
DISCORD_CLIENT_SECRET=...
```

## Key Implementation Details

### Agent Execution Flow

1. **Goal Creation**: User sets a goal in the UI
2. **Task Generation**: `startGoalAgent()` uses LLMChain to break goal into tasks
3. **Task Analysis**: `analyzeTaskAgent()` determines action (reason or search)
4. **Task Execution**: `executeTaskAgent()` runs the task via:
   - LangChain LLM for reasoning tasks
   - Serper service for web search tasks
5. **Result Storage**: Tasks and messages stored in database via tRPC

### tRPC Integration

- Client: `src/utils/api.ts` creates type-safe hooks via `api.withTRPC()`
- Server: Routers defined in `src/server/api/routers/` combined in `root.ts`
- Endpoint: `/api/trpc/[trpc].ts` handles all tRPC requests

### State Management

- **Agent State**: `src/components/stores/agentStore.ts` - agent mode, status, settings
- **Message State**: `src/components/stores/messageStore.ts` - chat messages and tasks
- Accessed via `useMessageStore.use` and `useAgentStore.use` hooks

### Authentication

- NextAuth configured in `src/server/auth.ts`
- Supports Google, GitHub, Discord (configurable via env)
- Guest mode available with access keys
- Prisma Adapter for database sessions

## Testing

Tests are located in `__tests__/` directory using Jest:

```bash
# All tests
npm test

# Specific test
npm test whitespace.test.ts
```

## Internationalization

- Config: `next-i18next.config.js`
- Translation files: `public/locales/{locale}/{namespace}.json`
- Supported locales: English (en), Chinese (zh), Japanese (ja)
- Usage: `useTranslation()` hook or `t()` function

## Development Notes

1. **Type Safety**: tRPC provides end-to-end type safety between client and server
2. **API Routes**: Legacy Next.js API routes coexist with tRPC (mainly for agent execution)
3. **Edge Runtime**: Some API routes run on Edge runtime for better performance
4. **Database**: Prisma schema uses MySQL by default, SQLite available for local dev
5. **Payment**: Stripe integration for potential monetization features
6. **Build**: Skips lint during build with `next build --no-lint`

## Useful Utilities

- `src/utils/env-helper.ts`: Environment variable utilities
- `src/utils/helpers.ts`: Core helper functions (task parsing, extraction)
- `src/utils/prompts.ts`: LLM prompts for agent operations
- `src/utils/constants.ts`: Application constants

## Getting Started for Development

1. Run `./setup.sh` for automated setup
2. Or manually:
   ```bash
   npm install
   # Configure .env with required variables
   npx prisma db push
   npm run dev
   ```

## Important Files

- `package.json`: Dependencies and scripts
- `prisma/schema.prisma`: Database schema
- `src/server/api/root.ts`: Main API router
- `src/pages/index.tsx`: Main application page
- `src/services/agent-service.ts`: Core agent logic
- `.env.example`: Environment variable template