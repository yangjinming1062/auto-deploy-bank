# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Install dependencies
npm install

# Start development server (runs on port 8787)
npm run dev

# Run type checking
npm run typecheck
npm run typecheck:watch  # watch mode

# Run linter and formatter checks
npm run lint

# Format code (prettier)
npm run prettier

# Run unit tests
npm run test           # watch mode
npm run test:ci        # CI mode (no watch)

# Run e2e tests (Playwright, requires dev server)
npm run test:e2e

# Full check (lint + typecheck + tests)
npm run check

# Build for production
npm run build

# Build E2EE worker (Rust)
npm run build:e2ee-worker
```

## Database Commands

```bash
# Generate migrations
npm run db:generate

# Apply migrations locally
npm run db:migrate:local

# Apply migrations to remote environments
npm run db:migrate:development
npm run db:migrate:staging
npm run db:migrate:production

# Open Drizzle Studio
npm run db:studio:local
npm run db:studio:development
```

## Deployment

```bash
# Deploy to production (runs CI tests, builds, removes sourcemaps, publishes)
npm run deploy

# Set required secrets before first deploy
echo $SECRET | wrangler secret put CALLS_APP_SECRET
echo $SECRET | wrangler secret put TURN_SERVICE_TOKEN  # optional
echo $SECRET | wrangler secret put OPENAI_API_TOKEN    # optional
```

## Architecture Overview

Orange Meets is a video conferencing demo application built on **Cloudflare Workers** with **Remix**, using **Cloudflare Calls** for WebRTC media transport.

### Core Stack
- **Runtime**: Cloudflare Workers (ES modules)
- **Framework**: Remix 2.11 with React 18
- **Styling**: Tailwind CSS with `@apply` usage pattern
- **Database**: D1 (SQLite) with Drizzle ORM
- **Real-time**: PartyKit (WebSockets via partyserver)
- **Media**: Cloudflare Calls SFU
- **State**: Durable Objects for room coordination

### Key Architecture Patterns

**1. Durable Object Room Coordination (`app/durableObjects/ChatRoom.server.ts`)**
- Each meeting room is a Durable Object (`ChatRoom`)
- Extends `Server` from `partyserver` for WebSocket handling
- Stores user session state in Durable Object storage
- Coordinates signaling via WebSocket broadcasts
- Integrates with Cloudflare Calls for media negotiation
- Supports optional AI participant via OpenAI Realtime API

**2. WebRTC Signaling Flow**
```
Client → PartyKit WebSocket → ChatRoom DO → Broadcast to participants → SDP exchange via Calls API
```

**3. Remix Route Structure (`app/routes/`)**
- `_index.tsx` - Landing page to create/join rooms
- `_room.$roomName._index.tsx` - Pre-room settings (permissions, username)
- `_room.$roomName.room.tsx` - Main video room UI
- `_room.tsx` - Lobby/enforcement logic
- `parties.rooms.$roomName.$` - PartyKit WebSocket endpoint
- API routes for bug reports, analytics, debug info

**4. Client State Management**
- `useRoom()` hook - manages WebSocket connection and room state
- `useRoomContext()` - provides combined room/userMedia/e2ee context
- `useStageManager()` - handles participant video grid layout (speakers prioritized)
- `useUserMedia()` - manages local media tracks (camera, mic, screenshare)

**5. E2EE Layer (`app/utils/e2ee.ts` + `rust-mls-worker/`)**
- Rust WebAssembly worker for MLS-based end-to-end encryption
- Intercepts and encrypts media tracks before WebRTC push
- Safety numbers displayed on join to verify encryption keys

### Important Patterns & Conventions

- **Path aliases**: `~` maps to `/app`
- **Server-only code**: Files ending in `.server.ts` or `server.ts` don't bundle to client
- **Client imports**: `app/utils/*.server.ts` are tree-shaken from client bundles
- **Message types**: `ClientMessage` and `ServerMessage` in `~/types/Messages.ts` define WS protocol
- **Environment types**: `Env` interface in `~/types/Env.ts` declares all bindings

### Environment Configuration

Required in `.dev.vars`:
```
CALLS_APP_ID=<your-calls-app-id>
CALLS_APP_SECRET=<your-calls-secret>
```

Optional variables:
- `MAX_WEBCAM_BITRATE` - default 1200000
- `MAX_WEBCAM_FRAMERATE` - default 24
- `MAX_WEBCAM_QUALITY_LEVEL` - default 1080 (smallest dimension)
- `OPENAI_API_TOKEN` + `OPENAI_MODEL_ENDPOINT` - for AI participant feature
- `TURN_SERVICE_ID` + `TURN_SERVICE_TOKEN` - for Cloudflare TURN service

### Testing Strategy

- **Unit tests**: Vitest in `app/**/*.test.ts` files
- **E2E tests**: Playwright in `e2e-tests/` directory, requires camera/mic permissions
- Tests run against local dev server (`npm run dev`)

### Key Files

- `server.ts` - Worker entry point, asset handling, exports ChatRoom DO
- `schema.ts` - Drizzle schema for analytics (Meetings, AnalyticsSimpleCallFeedback)
- `remix.config.js` - Remix configuration with workerd server target
- `wrangler.toml` - Worker configuration, DO bindings, migrations
- `vitest.config.mts` - Vitest configuration with path aliases