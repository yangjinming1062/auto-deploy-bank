# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DoraCMS is a Node.js + Express + MongoDB content management system. It features role-based admin permissions, user registration, document/content management, and template-based theming.

## Development Commands

```bash
npm install              # Install dependencies
npm start                # Start server (runs on port 81)
```

**Prerequisites:**
- MongoDB must be running on `127.0.0.1:27017`
- Redis must be running on `127.0.0.1:6379` (for session storage)

## Architecture

### Entry Points
- **app.js** - Express app configuration and middleware setup
- **bin/www** - HTTP server creation and startup

### Route Structure (`routes/`)
- **index.js** - Frontend routes: home, document details, category listings, sitemap
- **admin.js** - Admin panel CRUD operations for all modules
- **adminCtrl.js** - Admin permission filtering layer (checks auth and power before allowing CRUD)
- **content.js** - Frontend content interactions (comments, likes)
- **users.js** - User registration, login, and user center
- **system.js** - System operations: file uploads, email, backups

### Data Layer (`models/`)
- **Mongoose schemas** (`Content.js`, `User.js`, `AdminUser.js`, `ContentCategory.js`, etc.)
- **Dbopt.js** - Generic database operations helper
- **db/siteFunc.js** - Site-wide template rendering and notification utilities
- **db/adminFunc.js** - Admin permission checking logic

### Key Middleware (`util/`)
- **filter.js** - User authentication (session + cookie-based auth token)

### Configuration (`models/db/settings.js`)
- Site metadata, MongoDB/Redis connection strings, email settings
- Permission module keys (e.g., `adminUsersList`, `contentList`) map to admin permission strings
- Theme paths: `SYSTEMTEMPFORDER` points to installed templates (`views/web/temp/{themeAlias}/`)

## Authentication & Permissions

**Admin auth:** Session-based with Redis storage. Permissions checked in `adminCtrl.js` before routing to `admin.js` handlers. Each module has permission strings like `sysTemManage_user_view`, `sysTemManage_user_add`, etc.

**User auth:** Cookie-signed token with fallback to session. `filter.js` handles user authentication.

## Important Patterns

- `siteFunc.renderToTargetPageByType()` - Unified rendering for different page types (index, detail, contentList, error)
- `shortid` - Used for readable URLs (e.g., `/details/VymuSlpGg.html`)
- `express-promise` - Wraps routes to handle async/await
- Template system uses EJS with `express-partials` for layout composition
- Socket.io is attached to the HTTP server for real-time features (instant messaging, notifications)

## Key Utilities

- `util/cache.js` - Redis wrapper for caching (sitemap, template data, content counts)
- `util/redis.js` - Redis connection module used by session store and cache