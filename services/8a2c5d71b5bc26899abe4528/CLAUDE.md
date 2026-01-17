# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Wipi is a personal, open-source CMS system supporting article publishing, page creation, and knowledge management. It's a monorepo using pnpm workspaces with four packages:

- **packages/server** - NestJS backend API (port 3003)
- **packages/client** - Next.js public frontend (port 3001)
- **packages/admin** - Next.js admin dashboard (port 3002)
- **packages/config** - Shared configuration and environment variables

Tech stack: MySQL, NestJS, Next.js, TypeORM, Ant Design, Aliyun OSS.

## Development Commands

### Core Commands
```bash
# Install dependencies
pnpm install

# Start all services in development
pnpm run dev

# Start individual packages
pnpm run dev:server  # NestJS API (port 3003)
pnpm run dev:client  # Next.js client (port 3001)
pnpm run dev:admin   # Next.js admin (port 3002)

# Build all packages
pnpm run build

# Build individual packages
pnpm run build:server
pnpm run build:client
pnpm run build:admin
pnpm run build:config

# Lint all packages
pnpm run lint

# Lint individual packages
pnpm run lint:server
pnpm run lint:client
pnpm run lint:admin

# Format code
pnpm run format

# Clean dependencies
pnpm run clean
```

### Testing Commands
```bash
# Server package only (uses Jest)
cd packages/server
npm test              # Run unit tests
npm run test:watch    # Watch mode
npm run test:cov      # Coverage report
npm run test:e2e      # End-to-end tests
npm run test:debug    # Debug mode
```

### Production
```bash
# Start production servers
pnpm run start

# Deploy with PM2
pnpm run pm2          # Starts all three packages
pnpm run pm2:server
pnpm run pm2:client
pnpm run pm2:admin
```

## Architecture

### Backend (packages/server)
NestJS application following standard module architecture:
- **Entry**: `src/main.ts` - Creates Nest app with middleware (helmet, compression, rate limiting, CORS)
- **App Module**: `src/app.module.ts` - Root module
- **Database**: Uses TypeORM with MySQL
- **Modules** (in `src/modules/`):
  - `article/` - Article management (entity, service, controller)
  - `category/` - Category management
  - `comment/` - Comment system
  - `user/` - User management
  - `auth/` - Authentication
  - `file/` - File upload/management
  - `knowledge/` - Knowledge base
  - `page/` - Static pages
  - `search/` - Search functionality
  - `setting/` - System settings
  - `smtp/` - Email configuration
  - `tag/` - Tag management
  - `view/` - View tracking
- **Utils**: `src/utils/` - OSS client, markdown, IP/location, user-agent
- **Filters/Interceptors**: Global error handling and response transformation
- **API Docs**: Swagger available at `/api` endpoint

### Frontend (packages/client)
Next.js public-facing website (SSR):
- **Layouts**: `src/layout/` - AppLayout, DoubleColumnLayout
- **Components**: `src/components/` - ArticleList, Header, Footer, Search, Tags, Theme
- **Hooks**: `src/hooks/` - Custom React hooks
- **Providers**: `src/providers/` - Context providers
- **Styling**: Uses Less with theme support

### Admin (packages/admin)
Next.js admin dashboard:
- **Layout**: `src/layout/AdminLayout/` - Admin sidebar navigation
- **Components**: `src/components/` - Editor (Monaco), Settings, Pagination
- **Providers**: API providers for backend services
- **Hooks**: Custom hooks for data fetching

### Config (packages/config)
Shared configuration package:
- **Source**: `src/index.ts`, `env.ts`, `i18n.ts`
- **Build**: TypeScript compilation to `lib/`
- **Consumed by**: All three apps for environment variables and i18n

## Environment Configuration

Default environment in `.env`:
- **Client**: Port 3001, site URL, asset prefix
- **Admin**: Port 3002, asset prefix
- **Server**: Port 3003, API URL and prefix (/api)
- **Database**: MySQL connection (host, port, user, password, database)
- **Auth**: Default admin credentials (admin/admin)
- **GitHub OAuth**: Optional client ID and secret

Production loads `.env.prod` if it exists.

## Database Setup

MySQL 5.7 required:
```bash
docker image pull mysql:5.7
docker run -d --restart=always --name wipi -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql:5.7

# Create database
mysql -u root -p
CREATE DATABASE `wipi` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Git Hooks

Pre-commit hook configured via Husky (`.husky/pre-commit`):
- Runs `pnpm run precommit`
- Lint-staged configured for `.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.scss`
- Auto-formats with Prettier and fixes ESLint issues

## Key Files to Know

- `/` - Root workspace config
- `.env` - Environment variables
- `.husky/pre-commit` - Pre-commit hooks
- `packages/server/src/main.ts` - Server entry point
- `packages/server/src/app.module.ts` - Server root module
- `packages/server/jest.config.js` - Server test configuration
- `packages/config/src/index.ts` - Shared config exports