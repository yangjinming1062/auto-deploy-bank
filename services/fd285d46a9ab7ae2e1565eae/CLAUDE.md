# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Authlib is a Python library for building OAuth 1.0, OAuth 2.0, and OpenID Connect servers and clients. It provides spec-compliant implementations including JWS, JWK, JWA, and JWT support. Python 3.10+.

**Note**: The `authlib.jose` module is deprecated in favor of `joserfc`. See [Migration Guide](https://jose.authlib.org/en/dev/migrations/authlib/).

## Development Commands

```bash
# Install dependencies
uv sync

# Run all tests (tox with py, flask, django, clients, jose)
uvx --with tox-uv tox -p auto

# Run specific test path
pytest tests/core  # or tests/clients, tests/flask, tests/django, tests/jose

# Run with coverage
uv run coverage run -m pytest
uv run coverage report

# Lint and format
uv run ruff check .
uv run ruff format .

# Build package
python3 -m build

# Build docs
uvx sphinx-build docs build/_html
```

## Code Architecture

```
authlib/
├── jose/              # JSON Object Signing and Encryption (RFC7515-7519)
│   └── drafts/        # Draft implementations (ECDH-1PU, etc.)
├── oauth1/            # OAuth 1.0 (RFC5849)
│   └── rfc5849/
├── oauth2/            # OAuth 2.0 implementations
│   ├── rfc6749/       # Core OAuth2 framework with grants (code, implicit, client_credentials, etc.)
│   ├── rfc7523/       # JWT profile for client auth
│   ├── rfc7636/       # PKCE (Proof Key for Code Exchange)
│   └── [other RFCs]/  # token revocation, introspection, etc.
├── oidc/              # OpenID Connect
│   ├── core/          # Core OIDC with grants
│   ├── discovery/     # OIDC Discovery (/.well-known/openid-configuration)
│   └── registration/  # Dynamic Client Registration
├── integrations/      # Framework integrations
│   ├── base_client/   # BaseOAuth, OAuth1Mixin, OAuth2Mixin, OpenIDMixin
│   ├── flask_oauth1/  # Flask OAuth 1.0 provider
│   ├── flask_oauth2/  # Flask OAuth 2.0 provider
│   ├── flask_client/  # Flask OAuth client
│   ├── django_oauth1/ # Django OAuth 1.0 provider
│   ├── django_oauth2/ # Django OAuth 2.0 provider
│   ├── django_client/ # Django OAuth client
│   ├── starlette_client/
│   ├── httpx_client/  # Async HTTPX OAuth client
│   └── requests_client/
└── common/            # Utilities (security, URLs, etc.)
```

### Key Patterns

- **Mixin-based clients**: `OAuth1Mixin`, `OAuth2Mixin`, `OpenIDMixin` classes provide reusable authentication flows
- **Grant types**: OAuth2 grants extend `BaseGrant` in `authlib.oauth2.rfc6749.grants`
- **Context managers**: OAuth clients use context managers (e.g., `with self._get_oauth_client() as client`)
- **Server metadata**: OAuth2 clients support `server_metadata_url` for OIDC Discovery
- **Error handling**: Custom exceptions in `authlib.integrations.errors` (`OAuthError`, `MissingTokenError`, etc.)

### Test Structure

```
tests/
├── core/              # Core OAuth2/OIDC tests
├── clients/           # Client integration tests (requests, httpx, starlette)
├── flask/             # Flask provider and client tests
├── django/            # Django provider and client tests
└── jose/              # JOSE tests
```