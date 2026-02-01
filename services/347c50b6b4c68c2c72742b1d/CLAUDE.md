# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fedlearner is a collaborative machine learning framework that enables joint modeling of data distributed between institutions (federated learning). It follows a Leader/Follower architecture where participants jointly train models without sharing raw data.

## Commands

### Main Repository (fedlearner core)

```bash
# Run full CI (custom ops, protobuf, lint, unit tests, integration tests)
make ci

# Generate Protocol Buffer Python code
make protobuf

# Build custom TensorFlow ops
make op

# Run linter
make lint

# Run unit tests only
make unit-test

# Run integration tests
make integration-test

# Run all tests
make test
```

### Web Console V2 (Flask API + React UI)

**API (Flask):**
```bash
cd web_console_v2/api
make unit-test              # Run unit tests
make lint                   # Run linter
make protobuf               # Generate proto files
```

**Client (React):**
```bash
cd web_console_v2/client
pnpm install                # Install dependencies
pnpm start                  # Dev server with hot reload
pnpm build                  # Production build
pnpm test                   # Run tests
```

## Architecture

### Core Components (fedlearner/)

- **data_join/** - Data alignment/joining process between Leader and Follower using RSA-based PSI (Private Set Intersection). Handles example ID synchronization and paired data generation.
- **trainer/** - Distributed training implementation with TrainerMaster, TrainerWorker, and ParameterServer. Supports both dense and sparse models.
- **fedavg/** - FedAvg algorithm implementation with cluster management and training service coordination.
- **channel/** - gRPC-based communication between Leader/Follower instances.
- **proxy/** - Network proxy for leader-follower communication.
- **model/** - Model definitions and utilities.
- **common/** - Shared utilities and common functions.

### Protocol Buffers (protocols/)

Located in `protocols/fedlearner/`:
- **common/** - Shared message types for communication protocols
- **channel/** - gRPC service definitions for leader-follower data transmission

### Web Console V2

- **api/** - Flask REST API server with SQLAlchemy ORM, Flask-Migrate for database migrations, and gRPC integration
- **client/** - React 17 frontend with TypeScript, Ant Design, styled-components, and React Query for data fetching

### Deployment (deploy/)

Kubernetes Helm charts for deploying Fedlearner components including Elasticsearch stack, ingress-nginx, and spark-operator.

## Key Concepts

### Leader/Follower Architecture
- Leader initiates training and coordinates the process
- Follower participates and synchronizes with Leader
- Communication via gRPC channels defined in `protocols/fedlearner/channel/`

### Data Join Process
1. Raw data is partitioned and transmitted between parties
2. Example IDs are synchronized using RSA-based PSI
3. Data blocks are paired and stored for training

### Training Flow
1. DataJoinWorker prepares training data
2. TrainerMaster coordinates distributed training
3. TrainerWorker processes data batches
4. ParameterServer handles model parameter synchronization

## Development Notes

### Python Style (web_console_v2/api)
- Follow [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- Use single quotes for string literals: `'hello world'`
- Use f-strings or `str.format()` for string formatting
- RESTful API design with proper HTTP verbs (GET, POST, PATCH, DELETE)

### Database Models (web_console_v2/api)
- Use integers/strings for enum values in DB columns
- Add explicit `Index()` and `UniqueConstraint()` in `__table_args__`
- Use `db.relationship()` with `primaryjoin` for associations (no foreign keys)
- Add `comment=` parameter to each column

### Dependencies
- TensorFlow 1.15.2 (main ML framework)
- Python 3.6 (CI runs on Ubuntu 20.04 with Python 3.6)
- gRPC/grpcio-tools for service definitions
- SQLAlchemy 1.3.20 for web console API

### Proto File Generation
- Main repo: `make protobuf` generates Python from `protocols/fedlearner/` and `fedlearner/fedavg/`
- Web console API: `make protobuf` generates Python/mypy stubs from `web_console_v2/api/protocols/`