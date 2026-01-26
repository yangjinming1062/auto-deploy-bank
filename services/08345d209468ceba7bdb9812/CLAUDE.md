# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Busy is an open-source social network built on the Steem blockchain. It features server-side rendering (SSR), a React/Redux frontend, and integrates with Steem blockchain APIs for social features and digital payments.

## Common Commands

```bash
# Development
yarn dev                  # Start development server (accessible at localhost:3000)
yarn build                # Production build
yarn start                # Run production server (after build)

# Testing
yarn test                 # Run all tests
yarn test:watch           # Run tests in watch mode
yarn test -u              # Update snapshot tests

# Code Quality
yarn lint                 # Run ESLint on all source files
yarn linc                 # Run linter without fixes
yarn prettier-check-all   # Check code formatting
yarn prettier             # Format code automatically
```

## Architecture

### Directory Structure

- `src/client/` - React frontend application
- `src/server/` - Express server for SSR
- `src/common/` - Shared code between client and server
- `webpack/` - Webpack configuration files
- `scripts/` - Build and development scripts
- `templates/` - Handlebars templates for SSR

### Server-Side Rendering Flow

1. `src/server/index.js` - Express server entry point
2. `src/server/app.js` - Route configuration (handles callbacks, AMP, redirects)
3. `src/server/handlers/createSsrHandler.js` - SSR renderer that:
   - Initializes sc2-sdk for SteemConnect authentication
   - Calls `fetchData()` on matched route components
   - Renders React to string via `StaticRouter`
   - Injects preloaded state into HTML

### Client-Side Architecture

**Entry Point**: `src/client/index.js`
- Hydrates SSR output, initializes Redux store with `__PRELOADED_STATE__`
- Sets up SteemConnect authentication from cookies

**Routing**: `src/common/routes.js`
- Centralized route definitions using `react-router-config`
- Nested routes for user profiles (e.g., `/@username`, `/@username/comments`)
- Components implement `static async fetchData({ store, match, req, res })` for SSR data loading

**State Management**: `src/client/store.js`
- Redux store with middleware: error handling, promise middleware, thunk with extra arguments (steemAPI, steemConnectAPI, busyAPI), routing
- `src/client/reducers.js` - Combined reducer with selectors for all sub-reducers

**Main Layout**: `src/client/Wrapper.js`
- Root layout component with navigation, modals, and route rendering
- Handles authentication state, notifications, and global features like nightmode

### Redux State Shape

Key reducers: `app`, `auth`, `comments`, `editor`, `feed`, `posts`, `user`, `users`, `notifications`, `bookmarks`, `favorites`, `reblog`, `wallet`, `settings`, `search`

### API Integration

- **Steem Blockchain**: `src/server/steemAPI.js` uses `lightrpc` to connect to Steem nodes
- **SteemConnect**: `sc2-sdk` for OAuth authentication
- Extra arguments passed to thunk actions include: `steemAPI`, `steemConnectAPI`, `busyAPI`

### Internationalization

- Translations in `src/client/locales/` (default.json is source)
- Use `FormattedMessage` component or `intl.formatMessage()` for user-facing text
- Add new strings to `default.json` with consistent `id` and `defaultMessage`

## Key Patterns

- **Decorators**: Use `@withRouter` and `@connect` decorators from react-router-redux and react-redux
- **PropTypes**: All components define `propTypes` and `defaultProps`
- **Fetch Data**: Components that need server data implement `fetchData` static method for SSR
- **Testing**: Jest + Enzyme; snapshots in `__tests__/` directories alongside components
- **CSS**: LESS styles with Ant Design components (`antd`)

## Tech Stack

- React 16.2, Redux 3.x, React Router 4.x
- Webpack 4, Babel 6, Jest 21
- ESLint (airbnb config), Prettier
- Ant Design 3.x for UI components
- Steem blockchain integration via lightrpc + sc2-sdk