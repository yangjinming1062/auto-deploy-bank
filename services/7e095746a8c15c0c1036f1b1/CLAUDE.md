# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **TechEmpower Framework Benchmarks** repository - a comprehensive performance testing suite that measures web framework performance across multiple programming languages. The project benchmarks frameworks like Express, Spring, Django, Rails, and many others across different test scenarios.

## Architecture Overview

### Directory Structure

- **frameworks/**: Contains all framework implementations organized by language (JavaScript/, Java/, Python/, Go/, Rust/, etc.). Each framework has its own directory with:
  - `benchmark_config.json`: Test configuration defining URLs, database settings, and metadata
  - Framework-specific source code
  - `*.dockerfile`: Docker build files for different database combinations
  - `config.toml` or similar: Framework-specific configuration

- **toolset/**: Python-based testing infrastructure:
  - `run-tests.py`: Main entry point for running benchmarks
  - `benchmark/`: Core benchmark orchestration (`benchmarker.py`, `framework_test.py`)
  - `test_types/`: Test type definitions:
    - `json/`: JSON serialization tests
    - `db/`: Single database query
    - `query/`: Multiple database queries
    - `cached-query/`: Cached database queries
    - `fortune/`: Template rendering (Fortune page)
    - `update/`: Database updates
    - `plaintext/`: Plain text response
  - `databases/`: Database implementations (MongoDB, MySQL, PostgreSQL)
  - `utils/`: Helper utilities (metadata, results, docker_helper, audit)

- **scripts/**: Utility scripts (fail detector, etc.)

- **tfb**: Main shell script that wraps Docker container execution

### How It Works

The testing infrastructure uses Docker containers for isolation:
1. **Toolset container** (Python-based) orchestrates the entire test run
2. **Framework containers** run each web framework implementation
3. **Database containers** provide MongoDB, MySQL, PostgreSQL
4. **wrk container** generates load for benchmarking

Each framework's `benchmark_config.json` defines which test types it supports and their endpoints. Test types in `toolset/test_types/` implement the verification and benchmarking logic for each scenario.

## Common Commands

### Running Tests

```bash
# Run a specific test in verify mode (quick validation)
./tfb --mode verify --test express

# Run all tests for a framework
./tfb --mode verify --test-dir express

# Run all tests for a language
./tfb --mode verify --test-lang JavaScript

# Run benchmarks (full performance test, takes hours)
./tfb --mode benchmark --test express

# Run only specific test types
./tfb --mode verify --test express --type json,plaintext

# List all available tests
./tfb --list-tests

# Run with custom duration (seconds per test)
./tfb --mode benchmark --duration 15 --test express

# Run quietly (logs to file instead of stdout)
./tfb --mode verify --quiet --test express

# Exclude specific tests
./tfb --test-dir express --exclude postgres,mongodb
```

### Adding New Tests

```bash
# Interactive wizard to create a new framework test
./tfb --new
```

This walks you through creating a new framework implementation with proper structure and configuration.

### Development Commands

```bash
# Build toolset image (after Dockerfile changes)
docker build -t techempower/tfb .

# Run audit to check framework configurations
./tfb --audit

# Parse existing results
./tfb --parse <results_timestamp>

# Run tests in reverse order
./tfb --mode verify --test express --reverse-order
```

## Key Configuration Files

### benchmark_config.json (per framework)

Each framework has a `benchmark_config.json` with:
- Framework metadata (language, platform, classification)
- Test type configurations with URLs for each endpoint
- Database configurations (MongoDB, MySQL, PostgreSQL, postgres.js)
- ORM classification (Full, Minimal, Raw)

Example structure:
```json
{
  "framework": "express",
  "tests": [{
    "default": {
      "json_url": "/json",
      "plaintext_url": "/plaintext",
      "port": 8080
    },
    "postgres": {
      "db_url": "/db",
      "query_url": "/queries?queries=",
      "database": "Postgres",
      "orm": "Full"
    }
  }]
}
```

## Test Types Reference

- **json**: Tests JSON serialization with `{message: "Hello, World!"}`
- **plaintext**: Tests plain text response with "Hello, World!"
- **db**: Single database query returning random World object
- **query**: Multiple database queries (1-20 queries based on parameter)
- **cached-query**: Same as query but with query caching
- **fortune**: Template rendering displaying fortunes from database
- **update**: Updates random records in database

## Databases

Supported databases:
- **PostgreSQL**: Most common, with multiple driver options (sequelize, postgres.js)
- **MySQL**: With Sequelize ORM
- **MongoDB**: With Mongoose ODM

Each framework can support multiple database configurations simultaneously.

## Development Tips

1. **Framework structure**: Each framework directory should contain Dockerfiles for each database combination it supports (e.g., `express-mongodb.dockerfile`, `express-postgres.dockerfile`)

2. **Test endpoints**: Each test type needs a corresponding URL endpoint in `benchmark_config.json`

3. **Verification**: Use `--mode verify` for quick iteration during development. This runs basic endpoint validation without full performance benchmarking

4. **Logs**: When running with `--quiet`, check `results/<timestamp>/benchmark.log` for detailed logs

5. **Results**: Benchmark results are saved to `results/<timestamp>/` with `results.json` containing the data

6. **Multiple implementations**: A framework can have multiple implementations (e.g., `express` vs `express-mongo`) in separate directories

## Important Notes

- All tests run in Docker containers with isolated networking
- The `tfb` script automatically creates the `tfb` Docker network
- Full benchmark runs can take several hours
- Use `--cpuset-cpus` to pin containers to specific CPU cores for consistent results
- Results are automatically uploaded to https://tfb-status.techempower.com/ during continuous benchmarking
- The `results.json` can be visualized at https://tfb-status.techempower.com/share