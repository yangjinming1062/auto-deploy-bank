# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**kafka-node** is a Node.js client library for Apache Kafka (versions 0.9.x, 0.10.x, 0.11.x, 1.0, 1.1, and 2.0+). It provides both high-level and low-level APIs for producers, consumers, consumer groups, and administrative operations.

**Main Entry Point:** `kafka.js` - exports all public APIs

## Common Commands

### Testing
```bash
# Run full test suite (includes linting, TypeScript checks, and integration tests)
npm test

# Run only TypeScript type checking and linting
npm run test:ts

# Run tests against specific Kafka version
KAFKA_VERSION=0.9 npm test
KAFKA_VERSION=0.10 npm test
KAFKA_VERSION=0.11 npm test
KAFKA_VERSION=1.0 npm test
KAFKA_VERSION=1.1 npm test
KAFKA_VERSION=2.0 npm test
```

### Docker Management
```bash
# Start Kafka in Docker for testing
npm run startDocker

# Stop Kafka Docker containers
npm run stopDocker
```

### Development Utilities
```bash
# Update README table of contents
npm run updateToc
```

## Architecture Overview

### Core Components

**Client Layer:**
- `lib/kafkaClient.js` - Direct connection to Kafka brokers, handles metadata, correlations, and broker discovery
- `lib/baseClient.js` - Base client functionality shared between components

**Producer Layer:**
- `lib/producer.js` - Basic producer with manual partition assignment
- `lib/highLevelProducer.js` - High-level producer with automatic round-robin partitioning
- `lib/producerStream.js` - Stream-based producer (Kafka 0.9+)
- `lib/baseProducer.js` - Common producer functionality
- `lib/batch/` - Batch message handling for producers

**Consumer Layer:**
- `lib/consumer.js` - Basic consumer with manual offset management
- `lib/consumerStream.js` - Stream-based consumer
- `lib/consumerGroup.js` - Consumer group implementation with coordinator-based rebalancing (Kafka 0.9+)
- `lib/consumerGroupStream.js` - Stream-based consumer group (Kafka 0.9+)
- `lib/assignment/` - Partition assignment strategies
- `lib/consumerGroupRecovery.js` - Consumer group recovery mechanisms

**Admin & Metadata:**
- `lib/admin.js` - Administrative APIs (list/describe groups, create topics, list topics, describe configs)
- `lib/offset.js` - Topic offset management and fetching

**Protocol Layer:**
- `lib/protocol/` - Low-level Kafka protocol implementation (request/response structures, encoding/decoding)
- `lib/protocol/index.js` - Protocol message definitions and helpers
- `lib/protocol/protocolVersions.js` - Protocol version handling

**Utilities:**
- `lib/partitioner.js` - Message partitioning strategies (Default, Cyclic, Random, Keyed, Custom)
- `lib/errors/` - Error classes for various failure scenarios
- `lib/codec/` - Message compression codecs (gzip, snappy)
- `lib/utils.js` - Common utility functions
- `lib/logging.js` - Logging configuration

### Key Data Flow

1. **Producer Flow:** Application → Producer → KafkaClient → Broker
2. **Consumer Flow:** Broker → KafkaClient → Consumer/ConsumerGroup → Application
3. **Consumer Group Flow:** Coordinator → Rebalance → Partition Assignment → Consumer

### Important Implementation Details

- **Connection Management:** `kafkaClient.js:1` manages all broker connections, metadata fetching, and correlation handling
- **Consumer Groups:** `consumerGroup.js:1` implements Kafka's group coordinator protocol for consumer group management
- **Protocol Versioning:** The library supports multiple Kafka protocol versions (checked via `protocolVersions.js`)
- **Compression:** Supported codecs are in `lib/codec/` (gzip and snappy)
- **Error Handling:** Custom error classes in `lib/errors/` for specific failure modes

## Testing Infrastructure

- **Test Framework:** Mocha with custom test runner script `run-tests.sh`
- **Coverage:** Istanbul (`./node_modules/.bin/istanbul cover _mocha`)
- **Integration Tests:** Require Kafka running in Docker (started via `start-docker.sh`)
- **Test Structure:** Individual test files in `/test` directory named `test.*.js`
- **Mock System:** `/test/mocks/` contains mock implementations for isolated unit tests
- **Test Timeout:** Default mocha timeout is 20000ms (20 seconds)

## Configuration & Environment

- **Node.js Version:** Requires Node.js >= 8.5.1
- **Linting:** ESLint with `semistandard` configuration (`.eslintrc.json`)
- **Type Definitions:** TypeScript definitions in `/types` directory
- **Docker Compose:** Main config in `docker-compose.yml`, version-specific configs in `docker/docker-compose.*.yml`

## Project Structure

```
/
├── kafka.js              # Main entry point (public API exports)
├── logging.js            # Logging configuration
├── package.json          # Dependencies and scripts
├── README.md             # Full documentation
├── CONTRIBUTING.md       # Contribution guidelines
├── CHANGELOG.md          # Version history
├── docker/               # Docker compose files for different Kafka versions
├── example/              # Usage examples
├── lib/                  # Core implementation
│   ├── admin.js
│   ├── baseClient.js
│   ├── baseProducer.js
│   ├── consumer*.js      # Consumer implementations
│   ├── kafkaClient.js
│   ├── offset.js
│   ├── producer*.js      # Producer implementations
│   ├── partitioner.js
│   ├── protocol/         # Low-level protocol
│   ├── errors/           # Error classes
│   ├── codec/            # Compression
│   └── assignment/       # Partition assignment
├── test/                 # Test suite
│   ├── test.*.js         # Individual test files
│   ├── helpers/
│   └── mocks/
└── types/                # TypeScript definitions
```

## Debugging

Enable debug logging using the `debug` module:
```bash
export DEBUG=kafka-node:*
```

## Development Notes

- **Contribution Workflow:** See `CONTRIBUTING.md` for contribution guidelines
- **Rebasing:** Prefer rebasing over merging for clean commit history
- **Code Review:** At least two collaborators should LGTM for new features or big changes
- **Logging:** Uses `debug` module; custom logger providers can be set before requiring kafka-node (see README.md section on logging)