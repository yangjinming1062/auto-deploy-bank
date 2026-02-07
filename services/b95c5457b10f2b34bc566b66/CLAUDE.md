# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **MongoDB River Plugin for ElasticSearch** - an ElasticSearch plugin that uses MongoDB (or TokuMX) as a datasource to continuously sync data into ElasticSearch. It tails MongoDB's oplog to capture changes in real-time and supports filtering, transformation, and GridFS attachments.

**Technology Stack:**
- Java 7, Groovy (for build and tests)
- ElasticSearch 1.7.3
- MongoDB Java Driver 3.0.4
- Maven for build
- TestNG for testing
- Groovy scripts for transformations

## Build Commands

```bash
# Build the plugin (skips tests)
mvn -Dmaven.test.skip=true package

# Build and install to local ElasticSearch
./install-local.sh

# Run tests (default profile excludes 'slow' tests)
mvn test

# Run all tests including slow ones (use the 'default' profile which excludes 'slow')
mvn test -P-default

# Run a single test class
mvn test -Dtest=MyTestClass

# Run a single test method
mvn test -Dtest=MyTestClass#myTestMethod

# Compile only
mvn compile

# Full clean build
mvn clean package
```

## Architecture

### Core Components

**River Lifecycle** (`MongoDBRiver.java`):
- Main entry point implementing ElasticSearch's `River` interface
- Manages startup/shutdown via `start()`, `close()`, and internal thread management
- Coordinates between oplog tailing, initial import, and indexing

**Configuration** (`MongoDBRiverDefinition.java`):
- Builder pattern for constructing river configuration
- Parses river settings from ElasticSearch river definition JSON
- Handles MongoDB connection options, credentials, bulk settings, filters, and scripts

**Data Flow Pipeline:**
1. **OplogSlurper** - Tails MongoDB's oplog.rs collection for real-time changes (inserts, updates, deletes)
2. **CollectionSlurper** - Handles initial bulk import of existing collection data
3. **Indexer** - Processes operations from queue and batches them into ElasticSearch bulk requests
4. **MongoDBRiverBulkProcessor** - Manages ElasticSearch bulk indexing with flush intervals

**Supporting Services:**
- **MongoClientService** - Manages MongoDB client connections (cluster vs shard clients)
- **MongoConfigProvider** - Retrieves MongoDB sharding configuration
- **StatusChecker** - Monitors river status and handles start/stop transitions
- **MongoDBHelper/MongoDBRiverHelper** - Utility classes for version info and status management

**Key Data Structures:**
- **QueueEntry** - Packages oplog operations with metadata (data, operation type, timestamp, collection)
- **SharedContext** - Holds the blocking queue and current river status (STOPPED, RUNNING, STARTING, etc.)
- **Timestamp** - Represents oplog timestamps (BSON or GTID format for TokuMX compatibility)
- **Operation** - Enum for operation types: INSERT, UPDATE, DELETE, DROP_COLLECTION, DROP_DATABASE, COMMAND, UNKNOWN
- **Status** - River lifecycle states: STOPPED, RUNNING, START_PENDING, STARTING, STOP_PENDING, IMPORT_FAILED, START_FAILED, RIVER_STALE

### Key Concepts

**Oplog Operations:** The river watches MongoDB's oplog for CRUD operations (`i`=insert, `u`=update, `d`=delete, `c`=command) and transforms them into ElasticSearch index operations.

**Bulk Processing:** Operations are queued and processed in batches with configurable bulk actions, concurrent requests, and flush intervals. Throttling can be configured via `throttle_size`.

**Initial Import:** On first run, the river can either:
- Import existing collection data via `CollectionSlurper`
- Skip import and start from a specific timestamp
- Skip entirely and only process new oplog entries

**Transformation Scripts:** Supports Groovy scripts for advanced document transformation, including parent-child relationships. Scripts can modify documents, set routing/parent, change index/type, or ignore/delete documents.

**GridFS Support:** Can index binary files stored in MongoDB GridFS as ElasticSearch attachments. The plugin sets up attachment mapping automatically.

**Retry Mechanism:** On `MongoSocketException` or `MongoTimeoutException`, the river waits 10 seconds (MONGODB_RETRY_ERROR_DELAY_MS) before retrying to handle temporary network issues.

**Timestamp Tracking:** The last processed oplog timestamp is stored in `_river/{riverName}/{db.collection}` to support river restarts and prevent data loss.

### Threading Model

The river uses multiple daemon threads:
- `mongodb_river_status:*` - Status checker monitoring start/stop requests
- `mongodb_river_indexer:*` - Processes queued operations into ES bulk requests
- `mongodb_river_slurper_*:*` - One thread per MongoDB shard tailing the oplog
- `mongodb_river_startup:*` - Handles river initialization (runs in separate thread to avoid blocking ES startup)

**Sharded Collection Support:**
- Detects if connected to `mongos` vs direct replica set
- One `OplogSlurper` per shard replica set
- Uses latest oplog timestamp across all shards for initial import coordination
- Skips `fromMigrate` entries (chunk migrations)
- Uses `OPLOG_REPLAY` flag for efficient oplog queries

## Testing

Tests use **TestNG** with **embedded MongoDB** (flapdoodle embed-mongo). Test classes extend `RiverMongoDBTestAbstract` which sets up:
- Embedded MongoDB instance
- ElasticSearch node with the plugin
- MongoDB client connections

**Test Organization:**
- `simple/` - Basic river functionality tests
- `gridfs/` - GridFS attachment indexing tests
- `script/` - Groovy transformation script tests
- `advanced/` - Advanced features like parent-child relationships
- `tokumx/` - TokuMX-specific tests

Tests are in `src/test/java` with resources in `src/test/resources` and test scripts in `src/test/scripts`.

## River Configuration Example

```json
{
  "type": "mongodb",
  "mongodb": {
    "db": "mydb",
    "collection": "mycollection",
    "gridfs": true,
    "filter": "{ \"op\": \"i\" }"
  },
  "index": {
    "name": "myindex",
    "type": "mytype",
    "bulk": {
      "actions": 1000,
      "flush_interval": "5s"
    }
  }
}
```