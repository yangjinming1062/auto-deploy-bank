# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PostBot 3000 is an AI agent that generates social media content (Twitter/X and LinkedIn posts) from user input. It consists of two services:

- **agent-service** (port 8000): Python/FastAPI backend with LangGraph agent workflow
- **agent-ui** (port 3000): Next.js frontend with Vercel AI SDK for streaming

## Development Commands

### Agent Service (Python)
```bash
cd agent-service
poetry install              # Install dependencies
poetry run uvicorn app.main:app --reload  # Start dev server (port 8000)
# Or with Docker:
docker compose up           # Start in container
```

### Agent UI (Next.js)
```bash
cd agent-ui
pnpm install               # Install dependencies (uses pnpm)
pnpm run dev              # Start dev server
pnpm run build            # Build for production
pnpm run type-check       # TypeScript type checking
pnpm run format:write     # Format code with Prettier
```

## Architecture

### Agent Service (`agent-service/app/`)

The backend uses **LangGraph** to orchestrate a multi-step agent workflow. The agent uses `gpt-4o-mini` (temperature=0) via ChatOpenAI:

```
                    ┌──────────────────────────────────────────┐
START ─────► editor ─────► tweet_writer ──────┐
                    │                         │
                    └────► linkedin_writer ──┼──► supervisor ──► END
                                              │          │
                                              │          ▼
                                              │    (if n_drafts not reached)
                                              │          │
                                              ▼          ▼
                                        tweet_critique ◄─┤
                                              │          │
                                              ▼          │
                                        linkedin_critique
                                              │
                                              ▼
                                        tweet_writer ◄──┤
                                        linkedin_writer ─┘
```

**Key files:**
- `agent.py`: Defines the LangGraph workflow with 6 nodes and conditional edges based on `n_drafts`
- `prompts.py`: Contains system prompts for each agent node
- `configuration.py`: Configuration dataclass with thread_id for conversation persistence
- `main.py`: FastAPI app using langserve to expose the graph via `/`

The agent state (`OverallState`) contains:
- `user_text`: Original user input
- `edit_text`: Enhanced/edited content
- `tweet`/`linkedin_post`: Post objects with drafts and feedback
- `target_audience`: Audience specification
- `n_drafts`: Number of draft iterations

### Agent UI (`agent-ui/`)

Uses **Vercel AI SDK** with RSC (React Server Components) for streaming agent state:

**Key files:**
- `app/(chat)/actions.tsx`: Defines `sendMessage` action that streams LangGraph events. Uses `RemoteRunnable` to connect to agent-service and processes `on_chain_end` events to update UI incrementally
- `app/actions.ts`: Server actions for CRUD operations on chats and posts (persisted to Redis)
- `lib/types.ts`: TypeScript interfaces for AgentState, Chat, Message, Artifact, ContentPost
- `components/ui/`: Shadcn/ui component library

**Key components:**
- `components/socialmedia-post.tsx`: Renders tweet and LinkedIn drafts with feedback
- `components/post-generator-form.tsx`: Form for post details, audience, and draft count

**Data flow:**
1. User submits post details via `PostGeneratorForm`
2. `sendMessage` invokes `RemoteRunnable.streamEvents()` against agent-service
3. Each `on_chain_end` event updates `streamData` and re-renders the UI
4. On `supervisor` completion, chat state is saved to Redis via `saveChat()`

### Data Persistence

- **Upstash Redis** (via `@upstash/redis`): Stores chats, messages, and generated posts with key patterns:
  - `chat:{id}`: Chat document with messages
  - `user:chat:{userId}`: Sorted set of chat keys by timestamp
  - `user:posts:{userId}`: Sorted set of post keys by timestamp
- **LangGraph Checkpoint**: Thread-based conversation state via `thread_id` (configurable in `Configuration`)

### Authentication

**Clerk** (`@clerk/nextjs`) handles user auth with:
- Protected routes via middleware
- Server-side auth checks in actions (`auth()` from `@clerk/nextjs/server`)

## Environment Configuration

**agent-service/.env:**
- `OPENAI_API_KEY`: Required for GPT-4o-mini LLM calls
- `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2`, `LANGCHAIN_PROJECT`: Optional LangSmith tracing

**agent-ui/.env:**
- `AGENT_URL`: URL of agent-service (e.g., `http://localhost:8000`)
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`: Clerk auth credentials
- `NEXT_PUBLIC_CLERK_SIGN_IN_URL`, `NEXT_PUBLIC_CLERK_SIGN_UP_URL`: Auth redirect paths
- `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`: Redis connection

## Key Dependencies

- **Backend**: FastAPI, LangGraph, LangChain, Pydantic, Uvicorn, langserve
- **Frontend**: Next.js 14, Vercel AI SDK, Radix UI primitives, TailwindCSS, Framer Motion, shadcn/ui