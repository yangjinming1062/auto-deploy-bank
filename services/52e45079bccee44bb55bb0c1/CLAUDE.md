# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Online-edit-web is an online code editor with real-time collaboration features. It uses WebContainer API to run Node.js directly in the browser, Monaco Editor for code editing, and Yjs for collaborative editing via WebSocket.

## Commands

```bash
pnpm install           # Install dependencies
pnpm dev               # Start development server
pnpm build             # Build for production
pnpm start             # Start production server
pnpm lint              # Lint with ESLint (autofixes)
pnpm format            # Format with Prettier
pnpm test              # Run tests with Vitest
pnpm test run          # Run tests once (no watch mode)
pnpm commit            # Create commit with cz-git interactive prompt
pnpm storybook         # Run Storybook on port 6006
pnpm build-storybook   # Build Storybook static site
```

## Architecture

### App Router Structure (`src/app/`)
- `(main)/(router)/dashboard` - User dashboard
- `(main)/(router)/login` - Authentication page
- `edit/[projectId]` - Code editor page with sub-routes (ai, settings, plugins, search, file)
- `cooperation/[room]` - Real-time collaborative editing page
- `community` - Community page

### State Management (`src/store/`)
Zustand stores manage application state:
- `editorStore.tsx` - Monaco editor instances and models
- `webContainerStore.tsx` - WebContainer instance for browser Node.js environment
- `fileSearchStore.tsx` - File search functionality
- `cooperationPersonStore.tsx` - Collaboration users state
- `authStore.tsx` - Authentication state

### API Layer (`src/services/`)
Custom `Request` class wrapping fetch with:
- Request/response interceptors
- Caching configuration
- Authentication token support
- Base URL from `NEXT_PUBLIC_API_URL`

### Component Organization (`src/components/`)
Components are grouped by feature:
- `ui/` - Base UI components (shadcn-like, using Radix UI)
- `editor/` - Monaco editor integration
- `webContainerProvider/` - WebContainer context provider
- `file/` - File tree and file management
- `terminal/` - xterm.js terminal integration
- `cooperation/` - Yjs collaborative editing components
- `fileSearch/` - File search functionality
- `common/` - Shared components

### Key Technologies

- **Monaco Editor** - VS Code's editor with `@monaco-editor/react` wrapper
- **WebContainer API** - In-browser Node.js runtime via `@webcontainer/api`
- **Yjs + y-monaco** - CRDT-based real-time collaboration
- **y-websocket** - WebSocket provider for Yjs sync
- **Zustand** - Lightweight state management
- **Tailwind CSS** - Styling with custom animations and scrollbar plugin
- **Radix UI** - Accessible UI primitives

### Environment Variables

Required in `.env.development`:
- `NEXT_PUBLIC_SERVER_URL` - Backend API server
- `NEXT_PUBLIC_WS_URL` - WebSocket server for collaboration
- `MODEL_API_BASE_URL` - AI model API base URL
- `QWEN_APP_ID`, `QWEN_AUTH` - AI authentication (optional)

### Next.js Configuration (`next.config.mjs`)

Key settings:
- `reactStrictMode: false` - Disabled for WebContainer compatibility
- COOP/COEP headers required for WebContainer (`require-corp`, `same-origin`)
- `/cooperation/` route uses `unsafe-none` for collaboration features
- Image domains allowed from all protocols

### Import Alias
`@` maps to `/src` directory.

## Code Style

- ESLint with TypeScript rules, import ordering, padding between statements
- Prettier formatting
- Commit messages via cz-git with conventional commits format (type: scope: description)
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`, `wip`, `workflow`, `types`, `release`