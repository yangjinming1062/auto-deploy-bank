# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pnpm install                # Install dependencies
pnpm run dev                # Start dev server at localhost:4321
pnpm run build              # Build production site to ./dist/
pnpm run preview            # Preview build locally
pnpm run deploy             # Build and deploy to Cloudflare Workers
pnpm run lint               # Format with Prettier and fix ESLint issues
pnpm run lint:ci            # Run ESLint without auto-fix (CI)
pnpm run check              # Run Astro type checking
pnpm run check-all          # Run lint, check, and build
pnpm run validate-episode   # Validate episode markdown format
pnpm run get-missed-episode # Get missed episodes from YouTube
```

## Architecture

This is an Astro-based website for the GeeksBlabla Community (largest tech community in Morocco). The site uses:

- **Astro 5.x** with **Cloudflare Workers** adapter for static deployments
- **React** for interactive components (chatbot, episode creation forms)
- **Tailwind CSS** for styling with custom design system (`tailwind.config.mjs` defines the color palette and typography)
- **Content Collections** for managing episodes, articles, authors, team, testimonials, and gallery

### Content Structure

| Collection | Source | Type |
|------------|--------|------|
| `podcast` | `episodes/*.md` | Markdown files with frontmatter |
| `blog` | `articles/*.md` | Markdown articles |
| `authors` | `authors/*.json` | Author profiles |
| `gallery` | `gallery-mock-data.json` or Cloudinary | Community gallery images |
| `team` | `team/team-members.json` | Team members |
| `testimonials` | `testimonials/data.json` | Community testimonials |

### AI Chatbot (RAG System)

The podcast chatbot uses Retrieval-Augmented Generation:
- **Embeddings**: OpenAI `text-embedding-3-small`
- **Vector Store**: ChromaDB
- **Chat Model**: OpenAI GPT-4 Turbo (configurable)
- **Collection**: `podcast_episodes` (configurable)

API endpoints: `src/pages/api/chat.ts` and `src/pages/api/episode-analysis.ts`

Mock data is used in development without API keys. Requires ChromaDB server running and OpenAI API key for full functionality.

### Key Directories

- `src/actions/` - Astro server actions for Notion API integration (episode submission, suggestion forms)
- `src/components/` - Reusable components (`.astro` for static, `.tsx` for React)
- `src/content/` - Content collection configurations and schemas
- `src/lib/` - Utility functions
- `src/pages/` - Astro file-based routing
- `public/` - Static assets

### Environment Variables

The project uses Astro's `envField` for server-side secrets. For development, mock data is used so the site runs without API keys. Required for full functionality:

```
NOTION_API_KEY, GEEKSBLABLA_NOTION_DATABASE_ID (episode planning)
YOUTUBE_API_KEY (gallery)
CLOUDINARY_* (image hosting)
OPENAI_API_KEY, CHROMA_* (podcast chatbot)
```

## Episode Format

Episodes are markdown files in `episodes/` with required frontmatter:

```yaml
---
date: 2020-02-16
duration: "01:40:00"
title: "Episode Title"
tags: ["dev", "indie", "career"]
category: "dev"  # enum: dev, mss, ai, career, ama
youtube: https://www.youtube.com/watch?v=...
published: true
---
```

Required sections: `## Guests`, `## Notes`, `## Links`, `## Prepared and Presented by`.

Note timestamps format: `HH:MM:SS - Description`

Valid episode format is enforced by `pnpm run validate-episode` which runs as a pre-commit hook via husky/lint-staged.

## Development Patterns

- Use `.astro` components for static content, `.tsx` for interactive React components
- Follow Astro's file-based routing in `src/pages/`
- Name all files in `kebab-case`
- Path aliases: `@/*` maps to `./src/*`
- TypeScript is strict; extends `astro/tsconfigs/strict`
- Components use Tailwind CSS; use the configured colors/fonts from `tailwind.config.mjs`
- Follow `.cursorrules` for coding conventions: use `.astro` for static components, `.tsx` for React, file-based routing, and kebab-case naming