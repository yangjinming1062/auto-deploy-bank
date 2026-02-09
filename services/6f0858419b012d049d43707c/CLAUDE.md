# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
pnpm build              # Build all packages
pnpm run watch          # Build all packages in watch mode
pnpm run typecheck      # Type-check all packages
pnpm run typegen        # Generate types for Framework Mode (writes to .react-router/types/)
pnpm run lint           # Run ESLint
pnpm run format         # Format code with Prettier
pnpm run format:check   # Check Prettier formatting
```

## Test Commands

```bash
pnpm test                                    # All unit tests (Jest)
pnpm test packages/react-router/             # Single package
pnpm test packages/react-router/__tests__/router/fetchers-test.ts  # Single file
pnpm test -- -t "action fetch"               # Tests matching name pattern

pnpm test:integration                        # Build + run all integration tests
pnpm test:integration:run                    # Run integration tests only (skip build)
pnpm test:integration:run --project chromium integration/middleware-test.ts
pnpm test:integration:run --project chromium -g "middleware"
```

**Important**: Always use `--project chromium` for integration tests unless explicitly stated otherwise.

## Project Overview

React Router v7 is a multi-strategy router for React bridging the gap from React 18 to React 19. It can be used maximally as a React framework or minimally as a library.

### Five Architectural Modes

Always identify which mode(s) a feature applies to:

1. **Declarative**: `<BrowserRouter>`, `<Routes>`, `<Route>` components
2. **Data**: `createBrowserRouter()` with `loader`/`action`, `<RouterProvider>`
3. **Framework**: Vite plugin + `routes.ts` + Route Module API (route exports like `loader`, `action`, `default`) + type generation + SSR/SPA
4. **RSC Data** (unstable): RSC runtime APIs, manual bundler setup, runtime route config
5. **RSC Framework** (unstable): Framework Mode with `unstable_reactRouterRSC` Vite plugin

### Monorepo Structure

```
packages/
  react-router/              # Core router (all modes)
  react-router-dom/          # Re-exports react-router (v6→v7 compatibility)
  @react-router/dev/         # Dev tools + Vite plugin
  @react-router/node/        # Node.js server adapter
  @react-router/cloudflare/  # Cloudflare Workers adapter
  @react-router/serve/       # Minimal server for Framework Mode
  @react-router/fs-routes/   # File-system routing utility
  create-react-router/       # CLI for creating new projects

integration/                 # Playwright integration tests
playground/                  # Example projects for testing
decisions/                   # Architecture decision records
```

### Key Implementation Files

| Purpose | Location |
|---------|----------|
| Core router | `packages/react-router/lib/router/router.ts` |
| React components | `packages/react-router/lib/components.tsx`, `lib/hooks.tsx` |
| Vite plugin (Framework) | `packages/react-router-dev/vite/plugin.ts` |
| Vite plugin (RSC) | `packages/react-router-dev/vite/rsc/plugin.ts` |
| Type generation | `packages/react-router-dev/typegen/` |

## Framework Mode Routes

Framework Mode uses `routes.ts` in `app/`. Most tests use `flatRoutes()` for file-system routing:

```ts
// app/routes.ts
import { type RouteConfig } from "@react-router/dev/routes";
import { flatRoutes } from "@react-router/fs-routes";

export default flatRoutes() satisfies RouteConfig;
```

**File-system conventions** (`app/routes/`):
- `_index.tsx` → `/` (index route)
- `about.tsx` → `/about`
- `blog.$slug.tsx` → `/blog/:slug` (URL param)
- `settings.profile.tsx` → `/settings/profile` (`.` creates nesting)
- `_layout.tsx` → pathless layout route

## Testing Guidelines

### Unit Tests (`packages/react-router/__tests__/`)
Use Jest for pure routing logic, router state, and React component behavior. No build required.

### Integration Tests (`integration/`)
Use Playwright for Vite plugin, build pipeline, SSR/hydration, RSC, and type generation.

**Fixture hierarchy**: `createFixture()` → `createAppFixture()` → `PlaywrightFixture`

**RSC testing**:
- RSC Framework: Use `createFixture` with `rsc-vite-framework/` template
- RSC Data: Use `setupRscTest` in `integration/rsc/`

When behavior should work across modes, test multiple templates (e.g., `["vite-5-template", "rsc-vite-framework"]`).

## Changesets

When making user-facing changes, create a changeset at `.changeset/<unique-name>.md`:

```markdown
---
"react-router": patch
"@react-router/dev": minor
---

Brief description of the change
```

If iterating on a change that hasn't shipped yet, update the existing changeset file instead of creating a new one.

## Branching Strategy

- `main`: Latest stable release
- `dev`: Active development (branch from here for code changes)
- `v6`: v6.x maintenance
- `release-next`: Pre-release branch
- `release-v6`: v6 release branch

## Generated Files - Do Not Edit

- `docs/api/*`: Generated from JSDoc via `pnpm docs`
- `.react-router/types/*`: Generated from typegen via `pnpm typegen`
- `packages/*/dist/*`: Build output

## Documentation Standards

- All docs need mode indicators: `[MODES: framework, data, declarative]`
- Unstable features: prefix with `unstable_`, add `unstable: true` to frontmatter, include warning block
- Edit JSDoc in `packages/react-router/lib/` then run `pnpm docs`

## Future Flags

- **Future flags** (`vX_*`): Stable breaking changes prepared for next major
- **Unstable flags** (`unstable_*`): Experimental features that may change

Test both states (on/off) for future flags. Don't break existing behavior without a flag.