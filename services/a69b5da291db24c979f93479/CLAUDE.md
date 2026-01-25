# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

letterboxd-list-radarr is a web service that scrapes Letterboxd movie lists and transforms them into a format consumable by Radarr (movie collection manager). It's hosted on Render at `https://letterboxd-list-radarr.onrender.com`.

## Development Commands

```bash
# Install dependencies
npm install

# Build TypeScript to dist/
npm run build

# Run with debug logging (requires Redis)
LOG_LEVEL=debug node --inspect=5858 -r ts-node/register/transpile-only index.ts

# Auto-restart on file changes (uses nodemon)
npm run watch

# Run production build
npm start
```

## Environment Variables

- `REDIS_URL` - Redis connection string (required for caching)
- `PORT` - HTTP server port (default: 5000)
- `LOG_LEVEL` - Logging level (debug, info; default: info)
- `USER_AGENT` - Custom User-Agent string for HTTP requests

## Architecture

**Entry Point (`index.ts`):** Express server that handles all HTTP requests. Routes matching `/(.*)` delegate to `fetchPostersFromSlug()` which dispatches to the appropriate Letterboxd scraper.

**Request Flow:**
1. Route matches `/(.*)` and extracts the Letterboxd path slug
2. `fetchPostersFromSlug()` determines list type and scrapes Letterboxd
3. Results cached in Redis (30min TTL for lists, 7 days for movie details)
4. Movie slugs passed to `getMoviesDetailCached()` which fetches details via kanpai-scraper
5. Each movie transformed via `transformLetterboxdMovieToRadarr()` and streamed to client

**Module Structure:**
- `lib/letterboxd/` - Scrapers for different Letterboxd list types (list, collection, films-popular, tagged-lists)
- `lib/radarr/` - Transforms Letterboxd data to Radarr's expected JSON format
- `lib/cache/` - Redis wrapper for caching responses
- `lib/express/` - `sendChunkedJson()` streams responses as they're processed
- `lib/axios/` - HTTP client with `robots-guard.ts` enforcing Letterboxd's robots.txt
- `lib/logger/` - Winston logger with module-based child loggers

**Key Interfaces:**
- `LetterboxdPoster` - { slug, title } from list scraping
- `LetterboxdMovieDetails` - Full movie data from kanpai-scraper

## Code Conventions

- Prettier: 4-space tabs, no tabs for indentation
- TypeScript with strict mode enabled
- Child loggers used per module: `logger.child({ module: "ModuleName" })`