# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ReactPress is a full-stack CMS (Content Management System) built with a monorepo architecture using **pnpm workspaces**. It separates concerns into distinct packages:

- **Client**: A Next.js (Pages Router) React application.
- **Server**: A NestJS backend providing a REST API.
- **Toolkit**: A shared library containing the auto-generated API client SDK used by the Client to talk to the Server.

## Development Commands

All commands should be run from the root directory unless otherwise specified.

### Installation
```bash
pnpm install
```

### Development
Run both Server and Client in watch mode concurrently:
```bash
pnpm dev
```

Run only the Server (Backend):
```bash
pnpm dev:server
```

Run only the Client (Frontend):
```bash
pnpm dev:client
```

Run only the Documentation:
```bash
pnpm dev:docs
```

### Building
Build all packages (Toolkit -> Server -> Client):
```bash
pnpm build
```

Build individual packages:
```bash
pnpm build:toolkit
pnpm build:server
pnpm build:client
```

### Production
Start the production servers (requires prior build):
```bash
pnpm start
```

### Docker Development
Manage the full stack dev environment (MySQL, Nginx, Server, Client) using Docker:
```bash
pnpm docker:dev:start
pnpm docker:dev:stop
pnpm docker:dev:logs
```

### Code Quality
Lint and format code:
```bash
pnpm lint
pnpm format
```

### Testing
```bash
# Server tests
cd server && pnpm test
```

## Architecture & Code Structure

### Monorepo Structure
The project uses `pnpm-workspace.yaml` to manage packages.
- `client/`: Next.js application.
- `server/`: NestJS application.
- `toolkit/`: TypeScript library (SDK) auto-generated or manually written for API consumption.

### Database
- **ORM**: TypeORM
- **Database**: MySQL
- **Configuration**: Managed via `.env` file. Key variables are `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWD`, `DB_DATABASE`.

### API Communication
- The **Server** (`server/src`) exposes REST endpoints.
- The **Client** (`client/src`) uses `@fecommunity/reactpress-toolkit` (found in `toolkit/src/api`) to make HTTP requests to the server.
- Authentication is handled via JWT.

### Styling
- The Client uses **Ant Design** (`antd`).
- Styling is implemented using SCSS modules and CSS-in-JS patterns.

## Key Configuration Files
- `.env`: Environment variables (Database, Ports). Create this file if it doesn't exist.
- `docker-compose.dev.yml`: Defines the local Docker environment.

## Package Scripts
- `pnpm run dev:server` maps to `nest start --watch` inside the `server` directory.
- `pnpm run dev:client` maps to `node server.js` inside the `client` directory (custom server).