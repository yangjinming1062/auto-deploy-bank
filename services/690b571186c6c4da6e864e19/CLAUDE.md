# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nile is a Postgres platform for building multi-tenant B2B applications. The repository is a pnpm workspace monorepo containing:
- **`www`**: Main marketing website and documentation portal (Next.js 15 with App Router)
- **`examples/`**: Example applications demonstrating Nile SDK usage across languages/frameworks

## Common Commands

```bash
# Install dependencies
pnpm install

# Run all dev servers (turbo orchestrates workspaces)
pnpm run dev

# Run only the www dev server
pnpm run dev:www

# Build www application
pnpm run build:www

# Format all code
pnpm run format
```

## Workspace Structure

Each example in `examples/` is a standalone application. Each has its own setup instructions - check the `README.md` in each example directory. Common patterns:
- Next.js examples: `pnpm run dev` (often on port 6969)
- Python examples: `uvicorn main:app --reload`
- Frontend-only examples: See their individual READMEs

## www Application (Main Site)

Built with:
- Next.js 15 (App Router, React 19)
- TypeScript
- TailwindCSS
- Radix UI components
- MDX for documentation

Key scripts (run from `/www`):
```bash
pnpm run dev      # Development server
pnpm run build    # Production build
pnpm run lint     # Run ESLint
```

## SDK Integration

Examples use Nile SDK packages:
- `@niledatabase/client`, `@niledatabase/server`
- `@niledatabase/nextjs`, `@niledatabase/react`

Environment variables for examples typically include:
- `NILE_USER`, `NILE_PASSWORD` - Database credentials
- `NEXT_PUBLIC_APP_URL` - App URL for client-side context
- `AI_API_KEY`, `AI_BASE_URL`, `AI_MODEL`, `EMBEDDING_MODEL` - For AI features

## Adding Templates

To add a new template to the www site:
1. Create a new object in `/www/app/templates/template.ts`
2. Run `pnpm run build:www` from root
3. Access at `http://localhost:3000/templates`