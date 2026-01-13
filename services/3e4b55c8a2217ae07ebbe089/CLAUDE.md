# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Amundsen is a data discovery and metadata engine for improving the productivity of data analysts, data scientists, and engineers. It indexes data resources (tables, dashboards, streams) and powers a page-rank style search based on usage patterns. Think of it as "Google search for data."

This is a monorepo containing multiple microservices and libraries, all managed as git submodules.

## Architecture

Amundsen consists of three microservices and two libraries:

1. **Frontend** (`frontend/`): Flask-based web application with React/Redux frontend
   - Entry point: `frontend/amundsen_application/wsgi.py`
   - Configuration: `frontend/amundsen_application/config.py`
   - Frontend assets: `frontend/amundsen_application/static/`

2. **Metadata Service** (`metadata/`): Neo4j-backed metadata API
   - Proxies Neo4j graph database
   - Serves metadata to frontend
   - Models data as a graph

3. **Search Service** (`search/`): Elasticsearch-powered search API
   - Provides RESTful API for search
   - Uses Elasticsearch index for fast search
   - Currently indexes only table resources

4. **Databuilder** (`databuilder/`): Data ingestion library
   - ETL library for building metadata graph
   - Used to ingest data into Neo4j and Elasticsearch
   - Includes Airflow integration and sample scripts
   - Example: `databuilder/example/scripts/sample_data_loader.py`
   - Example DAGs: `databuilder/example/dags/`

5. **Common** (`common/`): Shared utilities library
   - Common code used across all microservices

Additional libraries:
- `amundsenrds/`: ORM models for relational database support
- `amundsengremlin/`: Library for converting models to Gremlin vertices/edges

## Common Development Commands

Each service has its own Makefile with standard targets:

### Run All Tests (across all services)
```bash
make test  # Runs in each service directory
```

### Test Individual Services
```bash
cd common && make test          # Tests common library
cd frontend && make test        # Tests frontend service + React
cd metadata && make test        # Tests metadata service
cd search && make test          # Tests search service
cd databuilder && make test     # Tests databuilder library
```

### Lint and Type Check Individual Services
```bash
make lint    # flake8
make mypy    # type checking
```

### Build Docker Images
```bash
cd frontend && make image         # Build frontend image
cd metadata && make image         # Build metadata image
cd search && make image           # Build search image
```

### Install Dependencies
```bash
cd {service} && make install_deps
```

## Local Development Workflow

### Initial Setup

1. **Clone the repository with submodules**:
   ```bash
   git clone --recursive git@github.com:amundsen-io/amundsen.git
   ```

2. **Update submodules to latest** (when creating new branches):
   ```bash
   git submodule update --remote
   ```

### Running Services with Docker

**Start all services for local development:**
```bash
docker-compose -f docker-amundsen-local.yml up -d
```

**Rebuild and restart after making changes:**
```bash
docker-compose -f docker-amundsen-local.yml build \
  && docker-compose -f docker-amundsen-local.yml up -d
```

**View logs:**
```bash
docker-compose -f docker-amundsen-local.yml logs --tail=3 -f
# Or for a specific service:
docker logs amundsenmetadata --tail 10 -f
```

**Stop all services:**
```bash
docker-compose -f docker-amundsen-local.yml down
```

### Reset Local Databases

Local data is persisted under `.local/`. To reset:

```bash
# Reset Elasticsearch
rm -rf .local/elasticsearch

# Reset Neo4j
rm -rf .local/neo4j
```

### Development Containers

Three docker-compose files are available:
- `docker-amundsen-local.yml`: For local development (uses local code)
- `docker-amundsen.yml`: Production-like setup
- `docker-amundsen-atlas.yml`: Uses Apache Atlas instead of Neo4j

### Service-Specific Development

**Frontend Development:**
- Local frontend setup: `frontend/docs/installation.md`
- For Windows: set `LOCAL_HOST = '127.0.0.1'` in `amundsen_application/config.py`

**Testing Search Service:**
```bash
# Start Elasticsearch
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:6.2.4

# Test API
curl "http://localhost:5001/search?query_term=test&page_index=0"
```

## Testing Strategy

All services use `pytest` for unit tests:
- `python3 -m pytest tests`
- Tests are located in each service's `tests/` directory

Each service's `test` target typically runs:
1. Unit tests (`test_unit`)
2. Linting (`lint` - flake8)
3. Type checking (`mypy`)
4. Import sorting check (`isort_check` in metadata/search)

To run a single test:
```bash
cd {service} && python3 -m pytest tests/path/to/test_file.py::test_function
```

## Key Files and Directories

- **Documentation**: `docs/` - Architecture, installation, troubleshooting
- **Example data**: `example/` - Sample data and scripts
- **Helm charts**: `amundsen-kube-helm/` - Kubernetes deployment
- **Docker configs**: Root directory - `docker-amundsen*.yml`

## Dependencies and Requirements

- **Python**: 3.6 or 3.7
- **Node**: v10 or v12 (v14 may have compatibility issues)
- **npm**: >= 6
- **Databases**: Neo4j 3.5.26, Elasticsearch 7.13.3

Requirements files:
- `requirements.txt` - Common requirements
- `requirements-dev.txt` - Development requirements
- `requirements-common.txt` - Shared across services

## CI/CD

GitHub workflows in `.github/workflows/`:
- Pull request workflows for each service (`*_pull_request.yml`)
- Monthly release workflow (`monthly_release.yml`)
- Documentation deployment (`deploy_docs.yml`)

## Extending Amundsen

### Adding New Connectors (Databuilder)

The databuilder library supports many connectors:
- Database connectors: Athena, Redshift, BigQuery, Snowflake, etc.
- Dashboard connectors: Superset, Tableau, Mode Analytics
- Other: dbt, Delta Lake, PostgreSQL, MySQL, etc.

Most databases with `dbapi` or `sql_alchemy` interface are supported.

### Supported Entities

- Tables (from databases)
- People (from HR systems)
- Dashboards

## Troubleshooting

- **Browser cache issues**: Hard refresh or clear cache when frontend doesn't show changes
- **Windows development**: See `docs/windows_troubleshooting.md`
- **Local Elasticsearch setup**: Use provided Docker commands in developer guide
- **Container issues**: Check logs with `docker logs {container_name}`

## Development Tips

- Always update submodules when pulling latest changes
- Each service can be developed independently
- Use `docker-amundsen-local.yml` for development to mount local code
- Reset `.local/` directories to start with clean databases
- Frontend changes may require hard browser refresh
- Each service has its own `setup.py` for package configuration

## Documentation Links

- Project docs: https://www.amundsen.io/amundsen/
- Developer guide: https://www.amundsen.io/amundsen/developer_guide/
- Architecture: https://www.amundsen.io/amundsen/architecture/
- Installation: https://www.amundsen.io/amundsen/installation/