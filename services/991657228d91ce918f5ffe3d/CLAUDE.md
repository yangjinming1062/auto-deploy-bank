# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ontop is a Virtual Knowledge Graph (VKG) system that exposes relational databases as knowledge graphs through SPARQL queries. It translates SPARQL queries into SQL queries executed against relational data sources using R2RML mappings and lightweight ontologies. The system is implemented in Java using Maven as the build system.

## Architecture

Ontop follows a modular architecture with clear separation of concerns:

### Core Modules

- **core/optimization** - Query optimization components, including query planners and transformers
- **core/reformulation** - SPARQL to SQL translation logic and query reformulation
- **core/system** - Core system components and configuration

- **engine/reformulation/** - Query reformulation engine
  - `core/` - Core reformulation logic
  - `sql/` - SQL-specific reformulation generation
- **engine/kg-query/** - Knowledge graph query processing
- **engine/model/** - Internal data models
- **engine/obda/** - OBDA ( Ontology-Based Data Access) components
- **engine/optimization/** - Engine-level optimizations

- **mapping/sql/** - SQL mapping layer
  - `core/` - Core SQL mapping abstractions
  - `r2rml/` - R2RML mapping parser and serializer
  - `native/` - Native Ontop mapping syntax
  - `all/` - Combined SQL mapping configurations

- **ontology/** - OWL ontology handling and processing

- **client/** - User-facing components
  - `cli/` - Command-line interface (main entry point)
  - `endpoint/` - SPARQL endpoint implementation
  - `docker/` - Docker distribution

- **db/** - Database-specific adapters and connectors

- **test/** - Comprehensive test suite
  - `lightweight-tests/` - Fast integration tests with various databases (PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, DB2, Spark, Trino, Dremio, DuckDB, etc.)
  - `docker-tests/` - Full integration tests using Docker
  - `sparql-compliance/` - SPARQL 1.1 compliance tests
  - `rdb2rdf-compliance/` - RDB2RDF specification compliance tests

- **binding/** - RDF framework bindings (RDF4J, Sesame, etc.)

- **protege/** - Protégé plugin components

- **build/** - Build and distribution artifacts

## Development Requirements

- **Java**: 11 or 17 (see `.sdkmanrc` for exact version: `java=11.0.28-amzn`)
- **Maven**: 3.6+ (project uses Maven wrapper: `./mvnw`)
- **Docker**: Required for docker-tests module
- **Database Drivers**: JDBC drivers must be manually downloaded for CLI usage (place in `jdbc/` directory)

## Common Commands

### Building the Project

```bash
# Full compilation and test execution
./mvnw clean install

# Build without running tests
./mvnw clean install -DskipTests

# Build release distribution (skips tests)
./mvnw clean package -DskipTests -Prelease
./build-release.sh  # alternative

# CI build (fail at end for better error reporting)
./mvnw install --fail-at-end

# Install dependencies to local Maven cache
./mvnw dependency:go-offline
```

### Running Tests

```bash
# Run all tests
./mvnw test

# Run tests for a specific module
./mvnw test -pl core/optimization

# Run tests in specific test module with group filters
./mvnw test -pl test/lightweight-tests -Dgroups="pgsqllighttests"
./mvnw test -pl test/lightweight-tests -Dgroups="mysqllighttests"
./mvnw test -pl test/lightweight-tests -Dgroups="dremiolighttests"
./mvnw test -pl test/lightweight-tests -Dgroups="trinolighttests"

# Run with Maven surefire (unit test framework)
./mvnw surefire:test

# Run docker integration tests
cd test/docker-tests && ../../mvnw install -Ddocker.url=tom.inf.unibz.it -DskipTests=false
```

Available lightweight test groups (see `test/lightweight-tests/pom.xml`):
- `pgsqllighttests` - PostgreSQL
- `mysqllighttests` - MySQL
- `mariadblighttests` - MariaDB
- `oraclelighttests` - Oracle
- `mssqllighttests` - SQL Server
- `db2lighttests` - DB2
- `sparksqllighttests` - Spark SQL
- `trinolighttests` - Trino
- `prestolighttests` - Presto
- `dremiolighttests` - Dremio
- `duckdblighttests` - DuckDB
- `tdenginelighttests` - TDengine
- `snowflakelighttests` - Snowflake (requires credentials)
- `athenalighttests` - AWS Athena (requires credentials)

### Using the CLI

After building, the CLI can be found in `client/cli/target/ontop-cli-<version>/`:

```bash
# Basic usage
./ontop --version
./ontop help
./ontop help <command>

# Common commands
./ontop query              # Query the RDF graph
./ontop materialize        # Materialize the RDF graph
./ontop endpoint           # Start SPARQL endpoint
./ontop validate           # Validate ontology and mappings
./ontop bootstrap          # Bootstrap ontology and mapping from database
./ontop mapping            # Manipulate mapping files
./ontop extract-db-metadata # Extract DB metadata to JSON
```

See `client/cli/src/main/resources/README.md` for detailed CLI documentation.

### Database-Specific Builds

Some modules require specific database profiles or dependencies. The build system automatically handles most dependencies, but JDBC drivers for CLI usage must be manually placed in the `jdbc/` directory as noted in the CLI README.

## Key Configuration Files

- **pom.xml** - Main Maven configuration with all dependencies and build profiles
- **.sdkmanrc** - Java version specification (Java 11)
- **.github/workflows/main.yml** - GitHub Actions CI/CD configuration
- **.gitlab-ci.yml** - GitLab CI configuration
- **build-release.sh** - Release build script
- **test/lightweight-tests/lightweight-db-test-images/** - Docker images for database testing

## Development Tips

1. **Memory Configuration**: Set `MAVEN_OPTS="-Xms6000m -Xmx8000m"` for large builds (used in CI)
2. **Incremental Development**: Build specific modules with `-pl <module-path>` to speed up iteration
3. **Test Selection**: Use Maven groups (`-Dgroups="..."`) to run specific test suites
4. **IDE Integration**: The project is标准的 Maven project and works well with IntelliJ IDEA and Eclipse
5. **JDBC Drivers**: For CLI usage, manually download database JDBC drivers and place them in the `jdbc/` directory

## Testing Strategy

The project uses a multi-layered testing approach:

- **Unit Tests** - Fast tests within each module using JUnit and Mockito
- **Lightweight Integration Tests** - Database-specific tests using test containers or embedded databases
- **Docker Integration Tests** - Full integration tests with real database instances
- **Compliance Tests** - SPARQL 1.1 and RDB2RDF specification compliance verification

For development, focus on:
1. Unit tests for new features/fixes
2. Relevant lightweight tests for database connectivity
3. Compliance tests for SPARQL/RDB2RML functionality

## Additional Resources

- Official Documentation: https://ontop-vkg.org
- GitHub Repository: https://github.com/ontop/ontop
- Issue Tracker: https://github.com/ontop/ontop/issues
- CLI Guide: https://ontop-vkg.org/guide/cli
- Contributing Guidelines: https://ontop-vkg.org/community/contributing/