# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Landing Zone Accelerator on AWS (LZA) is a configuration-driven CDK application that deploys and manages multi-account AWS environments aligned with AWS best practices and compliance frameworks. It supports AWS GovCloud (US), Secret, and Top Secret regions.

## Build Commands

```bash
# Install dependencies (run from source/ directory)
yarn install

# Build all packages in the monorepo
yarn build

# Clean install: remove node_modules, reinstall, and rebuild
yarn build-clean

# Run unit tests (Vitest)
yarn test:unit

# Run linting (ESLint with fixes)
yarn lint

# Run Prettier formatting
yarn prettier

# Validate user configuration files
yarn validate-config

# Run config replacement tool
yarn config-replacement
```

## Testing

- Unit tests use **Vitest** with coverage reporting
- Integration tests use `@aws-cdk/integ-runner` and `@aws-cdk/integ-tests-alpha`
- Run a single test file with `vitest run <file-path>`

## Monorepo Structure

This is a **Lerna + Yarn Workspaces** monorepo. Key packages are in `source/packages/`:

| Package | Purpose |
|---------|---------|
| `@aws-accelerator/accelerator` | Core CDK app and orchestration engine |
| `@aws-accelerator/config` | Configuration loading and validation |
| `@aws-accelerator/constructs` | Reusable L2/L3 CDK constructs |
| `@aws-accelerator/utils` | Shared utilities and types |
| `@aws-accelerator/installer` | Installer stack CDK app |
| `@aws-cdk-extensions/cdk-extensions` | CDK extensions submitted to upstream |

## Architecture

### Deployment Orchestration
The accelerator uses **stage-based deployment** with ordered stages: Bootstrap → Prepare → Accounts → Network → Finalize. This manages complex inter-account and inter-region dependencies.

### Entry Points
- **CLI entry:** `source/packages/@aws-accelerator/accelerator/cdk.ts`
- **Orchestration engine:** `Accelerator` class in `lib/accelerator.ts`
- **Toolkit wrapper:** `AcceleratorToolkit` class in `lib/toolkit.ts` (wraps CDK CLI for multi-account deployments)

### Configuration
User configurations are YAML files (typically in a separate config repo):
- `global-config.yaml` - Core settings, regions, logging
- `accounts-config.yaml` - OU and account definitions
- `network-config.yaml` - VPCs, Transit Gateways, Firewalls
- `iam-config.yaml` - IAM roles, policies, Identity Center
- `security-config.yaml` - Security Hub, GuardDuty, Macie

## Important Notes

- **Node.js:** Version 18 minimum, 20 default (set in `package.json`)
- **Package manager:** Yarn v1 (`yarn.lock`)
- **TypeScript:** Strict mode enabled
- **Pre-commit hooks:** Husky + lint-staged enforce linting on git commits
- **License headers:** Required on all source files (enforced by ESLint)