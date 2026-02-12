# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

authentik is an open-source Identity Provider (IdP) for modern SSO. It supports SAML, OAuth2/OIDC, LDAP, RADIUS, and SCIM. The project consists of three main components:

- **Python/Django server** (`authentik/`): Main application handling API, flows, policies, providers
- **Go proxy/outposts** (`cmd/`, `internal/`): Embedded proxy server and outpost implementations (LDAP, proxy, RAC, RADIUS)
- **TypeScript/Lit web UI** (`web/`): Admin interface, user portal, and flow executor

## Development Commands

### Python/Django Development

```bash
# Install all dependencies
make install

# Run the main server (handles API and web UI)
make run-server

# Run the worker (handles background tasks via Dramatiq)
make run-worker

# Reset development database (drop, create, migrate)
make dev-reset

# Run database migrations only
make migrate

# Generate a local development config
make gen-dev-config
```

### Go Development

```bash
# Test Go components
make go-test

# Lint Go code
golangci-lint run -v
```

### Web UI Development

```bash
# Install Node dependencies
make node-install

# Build and watch for changes (use this for frontend development)
npm run --prefix web watch

# Run web tests
npm run --prefix web test

# Run web linting
npm run --prefix web lint
npm run --prefix web lit-analyse

# Type-check the web UI
npm run --prefix web tsc
```

### Testing

```bash
# Run Python unit tests (requires PostgreSQL)
make test

# Run a specific test module
uv run manage.py test authentik.core

# Run integration tests
uv run manage.py test tests/integration

# Run e2e tests (requires Chrome and docker compose)
docker compose -f tests/e2e/compose.yml up -d
uv run manage.py test tests/e2e

# Run OpenID conformance tests
docker compose -f tests/openid_conformance/compose.yml up -d
uv run manage.py test tests/openid_conformance
```

### Linting & Code Generation

```bash
# Lint everything (Python + Go)
make lint

# Python linting (black + ruff)
make lint-fix

# Generate API clients from OpenAPI schema
make gen

# Build the web UI
make web-build
```

## Architecture

### Python/Django Structure

- **`authentik/core/`**: Core models (User, Group, Token, Sessions) and authentication
- **`authentik/api/`**: REST API powered by DRF with OpenAPI schema generation
- **`authentik/flows/`**: Flow engine for multi-step authentication flows
- **`authentik/policies/`**: Policy engine for access control decisions
- **`authentik/providers/`**: External SP integrations (OAuth2, SAML, LDAP, Proxy, SCIM, RAC, RADIUS)
- **`authentik/sources/`**: External IdP sources (OAuth, SAML, LDAP, SCIM)
- **`authentik/stages/`**: Flow stages (password, identification, TOTP, WebAuthn, email, etc.)
- **`authentik/events/`**: Audit logging and notification system
- **`authentik/tenants/`**: Multi-tenant configuration using django-tenants

### Go Outpost Structure

The Go components are built with Cobra and GORM:

- **`cmd/server/`**: Main server entry point combining Django ASGI + Go proxy
- **`cmd/ldap/`**: LDAP outpost for directory services
- **`cmd/proxy/`**: Reverse proxy outpost for application integration
- **`cmd/rac/`**: Remote access console outpost (RDP/VNC gateway)
- **`cmd/radius/`**: RADIUS outpost for network authentication
- **`internal/outpost/`**: Shared outpost utilities and core logic

### Web UI Structure

- **`web/src/admin/`**: Admin interface components
- **`web/src/user/`**: User portal components
- **`web/src/flow/`**: Flow executor components
- **`web/src/elements/`**: Reusable UI components using Lit web components
- **`web/src/components/`**: PatternFly-based React components

### Configuration

Configuration is loaded from (in order):
1. `authentik/lib/default.yml` (defaults)
2. `/etc/authentik/config.yml` (system config)
3. `/etc/authentik/config.d/*.yml` (drop-in configs)
4. Environment variables prefixed with `AUTHENTIK_`

Use `make gen-dev-config` to create a local development configuration.

### Database

PostgreSQL is required with the following setup:
- Database name: `authentik` (configurable)
- Schema: Uses `django-tenants` for multi-tenancy
- Cache: PostgreSQL-based cache backend
- Message queue: PostgreSQL-backed Dramatiq broker

### API Schema

The OpenAPI schema is auto-generated from Django REST Framework:
- Schema file: `schema.yml`
- Generated API clients: `gen-ts-api/`, `gen-py-api/`, `gen-go-api/`
- Regenerate with: `make gen`

## Code Style

### Python

- Formatter: Black (line-length 100)
- Linter: Ruff with flake8-bugbear, django, pylint rules
- Type checking: mypy with django-stubs and drf-stubs
- Imports: sorted automatically by Ruff

### TypeScript/Web

- Framework: Lit web components + React for complex components
- Formatter: Prettier
- Linter: ESLint with TypeScript support
- Type checker: TypeScript (strict mode)
- Analysis: lit-analyzer for web components

### Go

- Formatter: gofmt (default)
- Linter: golangci-lint
- Version: Go 1.25+

## Testing Notes

- Python tests use pytest-django with coverage
- Go tests use standard `go test` with race detector
- Web tests use Vitest for unit tests, Playwright for e2e
- Tests require a running PostgreSQL instance
- Set `AUTHENTIK_POSTGRESQL__NAME` for test database override