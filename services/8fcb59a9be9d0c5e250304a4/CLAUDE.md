# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CKibana is a ClickHouse adapter for Kibana that allows using native Kibana to query and analyze ClickHouse data. It acts as a proxy that translates Elasticsearch/Kibana API requests into ClickHouse SQL queries.

**Key Features:**
- ES/Kibana 6.x, 7.x compatibility (Kibana 7.1.1 and below)
- Elasticsearch query syntax to ClickHouse SQL translation
- Sampling for large result sets to improve performance
- Result caching via Elasticsearch
- Time rounding for cache optimization
- SQL blacklist to prevent expensive queries
- Query circuit breaker with max time range configuration

## Build Commands

```bash
# Compile the project
mvn compile

# Run tests
mvn test

# Run a single test
mvn test -Dtest=PathTrieTest

# Build JAR package
mvn package

# Run the application (builds first)
make run

# Checkstyle verification (runs during mvn verify)
mvn checkstyle:check

# Format license headers in source files
mvn license:format

# Docker build
make image-build

# Docker run
make image-run

# Docker push
make image-push
```

## Architecture

### Request Flow
```
HTTP Request → BaseHandler → SearchParser → MsearchParamParser
    → AggResultParser → CkService → ClickHouse
    → ResultParser → Response
```

### Key Layers

**Handlers** (`src/main/java/com/ly/ckibana/handlers/`)
- `BaseHandler`: Abstract base class implementing CORS and request routing; catches `FallbackToEsException` to proxy unhandled requests to ES
- `SearchHandler`: Handles `/_search` and `/{index}/_search` endpoints
- `MSearchHandler`: Handles multi-search requests
- `MappingHandler`, `IndicesHandler`, `FieldCapsHandler`: Metadata endpoints
- `HealthHandler`, `CheckHandler`: Health check endpoints

**Parsers** (`src/main/java/com/ly/ckibana/parser/`)
- `ParamParser`: Parses request parameters and builds IndexPattern
- `SearchParser`: Orchestrates search request parsing and execution
- `AggResultParser`: Builds aggregation results from CK responses
- `ResultParser`: Formats final response for Kibana
- `MsearchParamParser`: Parses multi-search request body

**Services** (`src/main/java/com/ly/ckibana/service/`)
- `CkService`: Executes SQL queries against ClickHouse; handles connection pooling, caching, and SQL monitoring
- `EsClientUtil`: Proxies requests to Elasticsearch when falling back or for metadata
- `CkResultCacheService`: Caches query results in ES
- `BlackSqlService`: SQL blacklist checking
- `SqlMonitorService`: Query template monitoring

**Strategies** (`src/main/java/com/ly/ckibana/strategy/`)
- `aggs/`: Aggregation type implementations (Terms, DateHistogram, Range, etc.)
- `clause/`: Query clause translation strategies (Bool, QueryString, Range, Term, etc.)
- Each aggregation/clause has a strategy class implementing `Aggregation` or `ClauseStrategy`

**Routing** (`src/main/java/com/ly/ckibana/configure/web/`)
- `RoutesConfigurer`: Bean that registers all `BaseHandler.routes()` into a `PathTrie`
- `PathTrie`: Custom trie structure for URL path matching with parameter extraction
- `HttpRoute`: Defines path patterns and allowed HTTP methods

### Data Flow: ES Query → CK SQL

1. Request body deserialized from JSON
2. `SearchParser.parseAggregations()` extracts aggregations
3. `MsearchParamParser.parseRequestBySearchQuery()` translates query clauses:
   - QueryString → ClickHouse WHERE clause (via `QueryStringClauseStrategy`)
   - Bool queries → Combined WHERE clauses
   - Range/term queries → Filter conditions
4. `AggResultParser` builds aggregation SQL:
   - Bucket aggregations → GROUP BY + aggregate functions
   - Metric aggregations → SUM, AVG, MIN, MAX, etc.
5. `CkService` executes SQL and returns results
6. `ResultParser` converts CK result format to ES response format

### Key Models

- `RequestContext`: Request metadata, proxy config, index info
- `CkRequestContext`: Extends RequestContext with CK-specific context (columns, sampling params, time limits)
- `IndexPattern`: Maps ES index pattern to CK table/database with column metadata
- `Aggregation`: Abstract syntax tree for aggregations

## Code Conventions

- **Java 17** minimum, Spring Boot 2.5.5
- All Java files must include Apache License 2.0 header (managed by license-maven-plugin)
- Checkstyle enforced at `style/checkstyle.xml` (max line length 200, nested if depth max 2)
- Use `@Resource` for dependency injection (Spring), not `@Autowired`
- Logging via `lombok.extern.slf4j.Slf4j` (`log` variable)
- Custom exceptions in `model/exception/` for different error scenarios

## Configuration

Primary config: `src/main/resources/application.yaml`

Key settings:
- `server.port`: Default 8080
- `metadata-config.hosts`: ES cluster for metadata (index patterns, cache)
- `metadata-config.headers`: ES request headers
- `logging.config`: logback-spring.xml

## Unsupported Features

- Kibana Query Language (KQL) - use Lucene syntax instead
- ip_range and date_range queries (querystring syntax only)