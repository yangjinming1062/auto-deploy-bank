# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Arco Design Pro is an enterprise-level Vue 3 application template built with [Arco Design Vue](https://arco.design/) component library. The main application lives in the `arco-design-pro-vite/` directory.

## Common Commands

All commands should be run from `arco-design-pro-vite/` directory:

```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Type check
pnpm type:check

# Build for production
pnpm build

# Preview production build
pnpm preview

# Generate bundle report
pnpm report
```

## Path Aliases

- `@` → `src` (e.g., `@/components`, `@/store`, `@/router`)
- `assets` → `src/assets`

## Architecture

### State Management (Pinia)

Three main stores in `src/store/modules/`:
- `app.ts` - Application settings (theme, layout, navbar, menu)
- `user.ts` - User authentication and profile
- `tab-bar.ts` - Multi-tab navigation state

### Routing (Vue Router)

Routes are auto-loaded from `src/router/routes/modules/*.ts`. Each module file exports a route or array of routes. External routes live in `externalModules/`.

Route guards are defined in `src/router/guard/`:
- `permission.ts` - Route permission checks
- `userLoginInfo.ts` - User login state handling

### API Layer

- API interceptor with JWT auth: `src/api/interceptor.ts`
- API responses use `HttpResponse<T>` interface
- Mock endpoints: `src/mock/index.ts` imports individual page mocks
- API files in `src/api/` categorize by feature (dashboard, user, visualization, etc.)

### Internationalization

Locale files in `src/locale/`:
- `en-US.ts` - English translations
- `zh-CN.ts` - Chinese translations
- Settings UI labels in `en-US/settings.ts` and `zh-CN/settings.ts`

### Component Patterns

- Global components auto-registered from `src/components/`
- Chart wrapper component: `src/components/chart/index.vue`
- Layout components: `src/layout/` (default-layout, page-layout)

### Configuration

- App settings: `src/config/settings.json`
- LESS global styles: `src/assets/style/global.less`
- Vite config split across `config/vite.config.base.ts`, `dev.ts`, and `prod.ts`

## TypeScript Notes

- `vue-tsc` is used for type checking (not TSC directly)
- `@typescript-eslint/no-explicit-any` is disabled (rule level 0)
- Component props don't require default values (vue/require-default-prop disabled)

## Commit Guidelines

Follow conventional commits. Husky runs `commitlint` on commit messages.