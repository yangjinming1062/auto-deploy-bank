# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SiYuan is a privacy-first personal knowledge management system with fine-grained block-level reference and Markdown WYSIWYG. The project consists of two main components:

- **Kernel** (`/kernel`): Go backend that handles data storage, synchronization, and provides HTTP/WebSocket APIs
- **App** (`/app`): Electron-based desktop/mobile frontend built with TypeScript

## Development Commands

### Kernel (Go)

```bash
cd kernel
# Enable CGO for SQLite
export CGO_ENABLED=1

# Build for desktop
go build --tags "fts5" -o "../app/kernel/SiYuan-Kernel"  # Linux/macOS
go build --tags "fts5" -o "../app/kernel/SiYuan-Kernel.exe"  # Windows

# Run kernel in dev mode
cd ../app/kernel
./SiYuan-Kernel --wd=.. --mode=dev
```

### App (TypeScript/Electron)

```bash
cd app
pnpm install
pnpm run dev        # Development build
pnpm run start      # Start Electron app
pnpm run lint       # Lint with ESLint (auto-fix)
pnpm run build      # Production build
pnpm run dist       # Create distribution packages
```

### China Mainland Development

```bash
# Use npm mirror
pnpm --registry https://registry.npmmirror.com/ i

# Electron mirror for installation
ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/ pnpm install electron@39.3.0 -D
```

## Architecture

### Kernel Structure

- **api/**: HTTP API handlers using Gin framework. Routes follow `/api/*` pattern
- **model/**: Business logic layer (60+ files). Most functionality lives here
- **server/**: Web server setup (Gin, WebSocket, WebDAV, CalDAV/CardDAV)
- **sql/**: SQLite database initialization and queries
- **util/**: Utility functions
- **job/**: Background cron jobs (sync, cleanup, etc.)

### App Structure

- **src/boot/**: Application initialization
- **src/protyle/**: Editor component (the core editing experience)
- **src/layout/**: UI layout management (dock, tab, etc.)
- **src/editor/**: Block-based editor implementation
- **src/menus/**: Context menus
- **src/dialog/**: Modal dialogs
- **src/sync/**: Data synchronization with kernel
- **src/plugin/**: Plugin system

### Communication Pattern

- Frontend connects to kernel via HTTP API on port 6806
- WebSocket connection for real-time updates
- API response format: `{code: 0, msg: "", data: {...}}`
- Authentication: `Authorization: Token <token>` header

## Code Conventions

### Go (Kernel)

- Use `gulu.Ret.NewResult()` pattern for API responses with `defer c.JSON()`
- Request parsing: `util.JsonArg(c, ret)` returns `(arg map[string]any, ok bool)`
- Error handling: Set `ret.Code = -1` and `ret.Msg = err.Error()`
- SQLite with full-text search enabled via build tag `fts5`

### TypeScript (App)

- ESLint config in `eslint.config.mjs`
- No explicit function return types required
- `any` type is allowed without restriction
- Use `fetchPost`/`fetchGet` from `./util/fetch` for API calls
- Conditional compilation with `/// #if BROWSER` / `/// #if MOBILE` directives
- Global `window.siyuan` object provides app state and utilities

## Key Dependencies

- **Lute** (`github.com/88250/lute`): Markdown editor engine
- **Gin**: HTTP web framework
- **Electron 39.3.0**: Desktop app framework
- **SQLite**: Data storage with fts5 full-text search

## API Development

New API endpoints follow this pattern in `kernel/api/*.go`:

```go
func exampleHandler(c *gin.Context) {
    ret := gulu.Ret.NewResult()
    defer c.JSON(http.StatusOK, ret)

    arg, ok := util.JsonArg(c, ret)
    if !ok {
        return
    }

    // Business logic in model package
    result, err := model.ExampleOp(arg["param"])
    if err != nil {
        ret.Code = -1
        ret.Msg = err.Error()
        return
    }
    ret.Data = result
}
```

Register routes in `kernel/server/serve.go` using `POST("/api/path", api.handler)`.