# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

ConsoleMe is a Python/Tornado web service that makes AWS IAM permissions and credential management easier for end-users and cloud administrators. It provides:
- AWS Console login (multiple methods)
- IAM Self-Service Wizard for permission requests
- Weep CLI for serving AWS credentials locally
- Cross-account role and policy management
- Support for ALB Authentication, OIDC/OAuth2, and SAML

## Common Commands

### Setup and Installation
```bash
# Install all dependencies, build UI, and bootstrap local services
make install

# Just install Python dependencies
make env_install

# Build the React UI
make build_ui

# Setup DynamoDB and Redis (for local development)
make bootstrap
```

### Development Server
```bash
# Run ConsoleMe backend
python consoleme/__main__.py
# Access at http://localhost:8081

# Run UI in development mode (for local UI development)
cd ui && yarn start
# Access at http://localhost:3000
```

### Testing
```bash
# Run all tests with coverage
make test

# Run tests with HTML coverage report
make testhtml

# Run security linting
make bandit

# Run code style checks
make lint

# Run both tests and lint
make test-lint

# Run a specific test file
pytest tests/test_filename.py -v

# Run tests with specific marker
pytest -m "marker_name"

# Run tox for multiple Python versions
tox
```

### Code Quality
```bash
# Install pre-commit hooks (required before committing)
pre-commit install

# Run pre-commit on all files
pre-commit run -a

# Manual linting
flake8 consoleme setup.py test
```

### Dependencies
```bash
# Update Python requirements
make up-reqs

# Sync dependencies
make deps
```

### Documentation
```bash
# Build documentation
make docs

# Build and open documentation
make docsopen
```

### Cleaning
```bash
# Remove build artifacts
make clean
```

## Local Development Setup

ConsoleMe requires **Python 3.8+**. For local development:

1. **Start dependencies**:
   ```bash
   docker-compose -f docker-compose-dependencies.yaml up -d
   ```

2. **Install and setup**:
   ```bash
   python3 -m venv env
   . env/bin/activate
   make install
   ```

3. **Run the application**:
   ```bash
   python consoleme/__main__.py
   ```

For unauthenticated local development, ConsoleMe uses `example_config/example_config_development.yaml` which bypasses authentication.

## Architecture

ConsoleMe is built as a **Python Tornado web application** with the following stack:

- **Backend**: Python 3.8+ with Tornado web framework
- **Frontend**: React (located in `ui/`)
- **Database**: DynamoDB for persistent storage
- **Cache**: Redis for quick data retrieval and Celery task management
- **Optional**: S3 for data storage outside Redis
- **Async Tasks**: Celery Beat scheduler for scheduled tasks

### Key Directory Structure

```
consoleme/
├── __main__.py              # Application entry point
├── routes.py                # API route definitions
├── models.py                # Domain models
├── config/                  # Configuration handling
├── handlers/                # HTTP request handlers
│   ├── v1/                  # API v1 handlers
│   ├── v2/                  # API v2 handlers
│   ├── auth.py              # Authentication handler
│   └── base.py              # Base handler class
├── lib/                     # Business logic (bulk of backend)
│   ├── aws.py               # AWS integration
│   ├── auth.py              # Authentication logic
│   ├── cache.py             # Redis cache management
│   └── [other modules]      # Various business logic modules
└── default_plugins/         # Example plugins for extension

ui/                          # React frontend

tests/                       # Python tests

docs/gitbook/                # Documentation (GitBook format)
```

### Application Flow

1. **Entry Point**: `consoleme/__main__.py:init()` starts the Tornado HTTP server
2. **Routing**: `consoleme/routes.py` defines URL routes mapped to handlers
3. **Handlers**: HTTP handlers in `consoleme/handlers/` process requests
4. **Business Logic**: Core logic in `consoleme/lib/` modules
5. **Data Layer**:
   - **DynamoDB Tables**: `consoleme_iamroles_global`, `consoleme_config_global`, `consoleme_policy_requests`, `consoleme_resource_cache`, `consoleme_cloudtrail`
   - **Redis Keys**: `ALL_POLICIES`, `CREDENTIAL_AUTHORIZATION_MAPPING_V1`, `AWSCONFIG_RESOURCE_CACHE`, etc.

### Plugin System

ConsoleMe uses a plugin system for extensibility. Default plugins are registered in `setup.py`:
- `default_config` - Configuration management
- `default_auth` - Authentication
- `default_aws` - AWS integration
- `default_celery_tasks` - Celery task scheduling
- `default_metrics` - Metrics collection
- `default_policies` - Policy management
- `default_group_mapping` - Group mapping
- `default_internal_routes` - Internal routes

Plugins can be loaded with `get_plugin_by_name()` from `consoleme.lib.plugins`.

## Configuration

Configuration is YAML-based and loaded via:
- `CONFIG_LOCATION` environment variable (path to YAML file)
- Or default locations checked by the application

Example configurations in `example_config/`:
- `example_config_development.yaml` - Local development with auth bypass
- `example_config_test.yaml` - Testing configuration
- Various auth configurations (OIDC, SAML, ALB, etc.)

## Testing and Code Quality

### Testing Stack
- **pytest** - Test framework
- **coverage.py** - Coverage reporting
- **bandit** - Security linting
- **flake8** - Code style enforcement
- **isort** - Import sorting
- **black** - Code formatting
- **pre-commit** - Git hooks for quality checks

### Test Configuration
- **Test files**: Located in `tests/`
- **Coverage config**: `.coveragerc`
- **Test timeout**: Configured via `--async-test-timeout` and `--timeout`
- **Test database**: Uses local DynamoDB instance

Pre-commit hooks automatically run:
- pytest
- bandit security checks
- flake8
- isort
- black formatting
- prettier (for frontend)
- helm lint (for Kubernetes configs)

### Running Specific Tests
```bash
# Run tests matching a pattern
pytest -k "test_name_pattern"

# Run with verbose output
pytest -v

# Run without cache
pytest --tb=short

# Run async tests with custom timeout
pytest --async-test-timeout=60
```

## Docker and Deployment

### Development with Docker
```bash
# Start all services (ConsoleMe + dependencies)
docker-compose up

# Start only dependencies (DynamoDB, Redis)
docker-compose -f docker-compose-dependencies.yaml up -d

# Test deployment
docker-compose -f docker-compose-test.yaml up
```

### Deployment Options
- **Terraform**: Configuration in `terraform/`
- **Packer/AMI**: Configuration in `packer/` and `create_ami` make target
- **ECS/CDK**: Configuration in `cdk/`
- **Kubernetes**: Helm charts in `helm/`

## Key Development Notes

1. **Python Version**: Requires Python 3.8 or higher
2. **Pre-commit**: Required for all contributions - run `pre-commit install`
3. **Configuration**: Set `CONFIG_LOCATION` env var to your YAML config
4. **Local Dependencies**: DynamoDB and Redis run via Docker Compose
5. **Testing**: All tests must pass before PR submission
6. **Documentation**: Update docs in `docs/gitbook/` for user-facing changes
7. **Breaking Changes**: Update `swagger.yaml` API specification
8. **Plugin Development**: Extend ConsoleMe via the plugin system in `consoleme/default_plugins/`

## Resources

- [Documentation](https://hawkins.gitbook.io/consoleme/)
- [Quick Start](https://hawkins.gitbook.io/consoleme/quick-start)
- [Configuration Guide](https://hawkins.gitbook.io/consoleme/configuration/)
- [Weep CLI](https://github.com/Netflix/weep)
- [Discord Community](https://discord.gg/nQVpNGGkYu)