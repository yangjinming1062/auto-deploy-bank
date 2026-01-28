# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Node.js/Express shopping cart application using Handlebars (`.hbs`) as the templating engine. This is a tutorial project from a YouTube series.

## Commands

```bash
# Install dependencies
npm install

# Start development server (runs on port 3000 by default)
npm start
```

## Architecture

```
bin/www          → Server entry point (creates HTTP server, listens on port 3000)
app.js           → Express app configuration (middlewares, view engine, routes)
routes/index.js  → Main router (home page renders shop/index.hbs)
views/           → Handlebars templates
  ├── shop/index.hbs
  ├── partials/header.hbs
  ├── layouts/layout.hbs
  └── error.hbs
public/          → Static assets (stylesheets, images)
```

**Key middleware setup in app.js:**
- Body parser (JSON and URL-encoded)
- Cookie parser
- Morgan for logging
- Static file serving from `/public`
- Handlebars view engine with default layout

**View engine:** `.hbs` files use `express-handlebars` with layouts in `views/layouts/` and partials in `views/partials/`.

## Technology Stack

- Express 4.x
- Handlebars (express-handlebars 3.x)
- Node.js built-ins (http, path, etc.)