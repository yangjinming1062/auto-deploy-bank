# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal knowledge base and blog (Wener's Notes) built with Docusaurus. It contains technical notes, documentation, and personal stories across DevOps, programming languages, databases, and more.

## Commands

```bash
# Install dependencies
pnpm install

# Development
cd site && pnpm start          # Start Docusaurus dev server with hot reload
cd site && pnpm run build      # Build for production
pnpm run scan-links            # Scan notes for broken links

# Git
just status                     # Show git status with staged changes
just pull                       # Rebase current branch from origin

# Utility
pnpm svgo ./path/to/*.svg       # Optimize SVG files
```

## Architecture

- **Content**: Markdown files in `notes/` (docs) and `story/` (blog posts)
- **Site**: Docusaurus 3.9.1 in `site/` workspace package
  - Docs configured at `site/docusaurus.config.js` with plugins: KaTeX, Mermaid, remark-math
  - Sidebar structure defined in `site/notes.yaml` and `site/notes.ts`
  - Custom plugins in `site/src/plugins/`
- **Workspace**: pnpm workspace with `site` as the only package
- **CLI**: `scripts/cli.ts` provides utilities like link scanning

## Content Conventions

- Markdown files use Chinese comments and Chinese headings
- File naming: lowercase with hyphens (e.g., `alpine-setup.md`)
- Special suffixes: `-faq.md`, `-awesome.md`, `-glossary.md`, `-cookbook.md`
- Math support: `$...$` for inline, `$$...$$` for block LaTeX (KaTeX)
- Diagrams: Mermaid syntax supported

## Editor Settings

- Prettier configured with 120 print width, single quotes, trailing commas
- Additional languages: SQL (4-space indent), HTML/CSS (double quotes)