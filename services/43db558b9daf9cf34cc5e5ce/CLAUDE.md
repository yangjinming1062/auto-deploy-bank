# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **generator-rest**, a Yeoman generator that scaffolds RESTful API projects using Node.js, Express, and MongoDB/Mongoose. It generates production-ready API projects with optional authentication, validation, testing, and documentation.

## Generators

This repository contains two generators:

1. **App Generator** (`generators/app/`) - Creates new REST API projects
   - Run with: `yo rest`
   - Generates Express server, MongoDB models, authentication, and project structure

2. **API Generator** (`generators/api/`) - Creates new API endpoints within generated projects
   - Run with: `yo rest:api`
   - Generates CRUD endpoints, Mongoose schemas, and tests

## Development Commands

Common commands for working on the generator itself:

```bash
# Run all tests and linting (recommended before commits)
npm test
# or
gulp

# Run only linting
gulp lint

# Watch for changes and run tests automatically
gulp watch

# Run tests with coverage
npm run coverage
```

The generator uses:
- **Gulp** for build automation (see `gulpfile.js`)
- **ESLint** for linting
- **Mocha** for generator tests
- **Istanbul** for code coverage
- **Travis CI** for continuous integration

## Generator Architecture

### Generator Structure

Each generator has:
- `index.js` - Main generator logic (extends `yeoman.Base`)
- `templates/` - EJS templates that get copied to generated projects

Key files:
- `generators/app/index.js` - Main app generator (557 lines)
- `generators/api/index.js` - API endpoint generator (8522 lines)
- `generators/app/templates/` - Templates for generated REST API projects
- `generators/api/templates/` - Templates for generated API endpoints

### Generated Project Structure

When users run `yo rest`, it creates a project with this structure (from README.md):

```
src/
├─ api/
│  ├─ user/
│  │  ├─ controller.js
│  │  ├─ index.js
│  │  ├─ index.test.js
│  │  ├─ model.js
│  │  └─ model.test.js
│  └─ index.js
├─ services/
│  ├─ express/
│  ├─ facebook/
│  ├─ mongoose/
│  ├─ passport/
│  ├─ sendgrid/
│  └─ your-service/
├─ app.js
├─ config.js
└─ index.js
```

Each API endpoint has:
- **model.js** - Mongoose schema and model
- **controller.js** - Business logic and middleware
- **index.js** - Route definitions
- **index.test.js** - Unit tests
- **model.test.js** - Model tests

### Testing Approach

The generator uses integration testing:
- Uses `yeoman-test` to run generators in temporary directories
- Tests various API generation scenarios (different endpoints, methods, reserved words, etc.)
- After generating projects, runs the generated code's linting and tests
- See `test/index.js` for test scenarios

## Key Technologies in Generated Projects

- **Express.js** - Web framework
- **MongoDB + Mongoose** - Database and ODM
- **Jest** - Testing framework
- **Babel** - ES6+ transpilation
- **querymen** - Query string handling (pagination, filtering)
- **bodymen** - Request body validation
- **Passport** - Authentication (optional: password, Facebook, Google, GitHub)
- **JWT** - Token-based authentication
- **SendGrid** - Password reset emails (optional)
- **apidoc** - API documentation generation

## Common Development Workflows

### Testing the Generator

1. Make changes to generator code
2. Run `gulp watch` to automatically test changes
3. Integration tests in `test/index.js` will:
   - Create temp directory
   - Run `yo rest` with various prompts
   - Run `yo rest:api` multiple times with different options
   - Execute generated project's linting and tests
4. Tests require environment variables:
   - `SENDGRID_KEY` - SendGrid API key
   - `MASTER_KEY` - Master key for user creation
   - `JWT_SECRET` - Secret for JWT tokens

### Adding New Features

When adding features to the generator:

1. Update generator logic in `generators/app/index.js` or `generators/api/index.js`
2. Add/modify templates in `generators/*/templates/`
3. Add new test scenarios in `test/index.js`
4. Ensure `gulp lint` passes
5. Run full test suite: `npm test`

The generator uses EJS templating with Yeoman's template helpers. Review existing templates to understand the coding patterns.

## CI/CD

- **Travis CI** configuration in `.travis.yml`
- Tests on Node.js v10, v11, v12
- Compiler: g++-4.8 (CXX=g++-4.8)
- Environment variables required for CI:
  - `SENDGRID_KEY=sendgridKey`
  - `MASTER_KEY=masterKey`
  - `JWT_SECRET=jwtSecret`

## Publishing

Version bumps and publishing:
```bash
# Patch release (0.x.x -> 0.x+1.0)
npm run patch

# Minor release (0.x.0 -> 0.x+1.0)
npm run minor
```

These commands automatically bump version, publish to npm, and push to git with tags.

## Important Notes

- This is a **generator**, not a REST API itself
- The `package.json` "main" field points to `generators/index.js`, but this file doesn't exist (Yeoman generators register sub-generators differently)
- The two generators are registered automatically via their directory names (`app` and `api`)
- Generated projects are meant to be deployed to Heroku or similar platforms
- See README.md for detailed usage examples and project documentation