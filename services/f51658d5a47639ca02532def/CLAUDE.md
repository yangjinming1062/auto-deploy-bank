# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MEAN Stack Relational is a MySQL/Express/AngularJS/Node.js boilerplate using Sequelize ORM instead of MongoDB. It demonstrates authentication strategies, SQL database patterns, and MEAN stack conventions.

**Note:** This is reference code with no planned updates. Node 4.2.x is outdated.

## Development Commands

```bash
# Development with live reload (runs Grunt)
npm start
# or
grunt

# Run tests (backend Mocha + frontend Karma)
npm test
# or
grunt test

# Lint JavaScript
grunt jshint

# Start fresh with dependencies
npm install
```

Grunt tasks:
- `grunt copy` - Copies bower_components to public/lib/
- `grunt watch` - Watches files and livereloads
- `grunt nodemon` - Runs app.js with file watching
- `grunt concurrent` - Runs nodemon + watch concurrently

## Architecture

### Request Flow
1. `app.js` - Entry point, loads config/express.js and starts server
2. `config/express.js` - Configures middleware, routes, and view engine
3. Routes (`app/routes/*.js`) - Map endpoints to controllers
4. Controllers (`app/controllers/*.js`) - Handle requests using models
5. Models (`app/models/*.js`) - Sequelize definitions and associations

### Configuration System

Uses `nconf` with hierarchical fallback:
1. `config/config.js` - Main loader
2. Environment files: `config/env/development.json5`, `production.json5`, `test.json5`
3. Environment variables and command-line args

**Setup:** Sample files must be copied during install:
```bash
cp config/env/development.json5.sample config/env/development.json5
cp config/env/production.json5.sample config/env/production.json5
```

### Authentication

- `config/passport.js` - Passport strategies (local, Facebook, Twitter, Google)
- Sessions stored via `express-sequelize-session` in database
- User model has authentication methods (`hasPassword`, `authenticate`, etc.)

### Database

- MySQL by default, PostgreSQL via `DATABASE_URL` (Heroku)
- Models auto-loaded from `app/models/`
- Define associations in model files; loader (`config/sequelize.js`) sets up relationships

### Frontend

- AngularJS module `mean` with feature modules: `mean.system`, `mean.articles`, `mean.auth`
- Components in `public/js/`: controllers, services (articles, authenticate, global), directives, filters
- Jade templates for server-side rendering in `app/views/`

### Testing

- **Backend:** Mocha + proxyquire for dependency stubbing
- **Frontend:** Karma + Jasmine with PhantomJS
- Test files: `test/mocha/` (backend), `test/karma/unit/` (frontend)

## Key Files

- `app.js` - Application entry point
- `config/express.js` - Express configuration
- `config/sequelize.js` - Database connection and model loader
- `config/passport.js` - Authentication strategies
- `config/config.js` - Configuration loader (nconf)
- `gruntfile.js` - Build configuration