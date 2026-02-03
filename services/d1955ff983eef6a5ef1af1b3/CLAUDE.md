# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Coze Loop is an AI Agent development platform with full lifecycle management capabilities (Prompt development, Evaluation, Observability). The project consists of:
- **Backend**: Go-based service using CloudWeGo (Hertz HTTP server, Kitex RPC)
- **Frontend**: TypeScript React application in a Rush.js monorepo
- **IDL**: Thrift-based interface definitions for backend-frontend communication

## Commands

### Frontend (Rush Monorepo)

```bash
cd frontend

# Install dependencies (run after git clone)
rush update

# Run development server (port 8090)
cd apps/cozeloop && rushx dev

# Build for production
cd apps/cozeloop && rushx build

# Run linting
cd apps/cozeloop && rushx lint

# Run tests
cd apps/cozeloop && rushx test

# Run single test file
cd apps/cozeloop && rushx test -- <test-file>.test.ts

# Update TypeScript API schema from Thrift IDL
rush update-api
```

### Backend (Go)

```bash
cd backend

# Run all tests
go test -gcflags="all=-N -l" ./...

# Build binary
go build -o coze-loop ./cmd
```

### Docker Deployment

```bash
# Development mode with file watching
make compose-up-dev

# Production mode
make compose-up

# Stop services
make compose-down
```

### Helm Deployment

```bash
# Deploy to Kubernetes
make helm-up

# View logs
make helm-logf-app  # app service logs
```

## Architecture

### Backend Structure

```
backend/
├── api/              # HTTP API handlers (Hertz-generated)
├── cmd/              # Entry points (main.go)
├── infra/            # Infrastructure layer (DB, Redis, MQ, fileserver, etc.)
├── kitex_gen/        # Kitex RPC generated code
├── loop_gen/         # Thrift-generated code for loop services
├── modules/          # Domain modules by feature
│   ├── data/         # Datasets, tags, file management
│   ├── evaluation/   # Evaluators, experiments, evaluation sets
│   ├── foundation/   # Auth, user, space, file services
│   ├── llm/          # LLM runtime and management
│   ├── observability/ # Traces, metrics, tasks
│   └── prompt/       # Prompt management and execution
└── pkg/              # Shared utilities (conf, logs, encoding, etc.)
```

### Frontend Monorepo Structure

Packages are organized by dependency layer (levels indicate build order):

```
frontend/
├── apps/
│   └── cozeloop/     # Main React app (level-6)
├── config/           # Shared configs: eslint, ts, tailwind, vitest (level-1)
├── infra/            # Build tools, plugins, IDL generators (level-1)
└── packages/
    ├── loop-base/    # Base services and utilities (level-2, level-3)
    ├── loop-components/  # UI components by domain (level-3)
    ├── loop-pages/   # Page-level components (level-5)
    ├── loop-modules/ # Feature modules (level-4)
    └── loop-config/  # Build configurations (level-2)
```

### API Communication (Thrift IDL)

```
idl/thrift/coze/loop/
├── apis/             # API definitions
├── data/             # Dataset and tag services
├── evaluation/       # Evaluation services
├── foundation/       # Auth, file, user, space
├── llm/              # LLM runtime and management
├── observability/    # Traces, metrics
└── prompt/           # Prompt management and execution
```

Thrift IDL files generate:
- **Backend Go code**: `backend/loop_gen/` (Hertz handlers, service interfaces)
- **Frontend TypeScript**: `frontend/packages/loop-base/api-schema/src/`

Regenerate frontend API schema with `rush update-api`.

## Key Technologies

| Layer | Technology |
|-------|------------|
| HTTP Server | CloudWeGo Hertz |
| RPC Framework | CloudWeGo Kitex |
| LLM Integration | CloudWeGo Eino |
| Frontend Build | Rsbuild |
| State Management | Zustand |
| Testing | Vitest (Frontend), Go testing (Backend) |
| Database | MySQL + GORM, ClickHouse |
| Cache | Redis |
| Message Queue | RocketMQ |
| Object Storage | S3-compatible |

## Code Conventions

### Go
- Format with `gofmt` or `goimports`
- Follow Effective Go and Go Code Review Comments
- Package names: short, all lowercase
- Error handling uses `errorn` package
- Dependency injection via `wire` package
- Test files: `*_test.go` in same directory

### TypeScript
- Use Rush workspace dependencies (`workspace:*`)
- Linting via `@coze-arch/eslint-config`
- Format with Prettier
- Tests with Vitest

## Common Development Tasks

### Adding a New API Endpoint

1. Define Thrift IDL in `idl/thrift/coze/loop/<module>/`
2. Run `rush update-api` to regenerate TypeScript types
3. Implement handler in `backend/api/handler/coze/loop/apis/`
4. Update frontend API calls using generated schema types

### Adding a Frontend Package

1. Create package in appropriate layer under `frontend/packages/`
2. Add to `rush.json` with appropriate level tag
3. Run `rush update` to update dependencies