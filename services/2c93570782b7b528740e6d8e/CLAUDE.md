# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Skyline is a real-time anomaly detection, time series analysis, and performance monitoring system. It's designed for passive monitoring of metrics without requiring per-metric configuration. Once running, new metrics are automatically added for analysis, and algorithms attempt to detect what is anomalous for each metric.

**Version:** 4.0.0 | **Python:** 3.8 | **Stack:** Flask, SQLAlchemy, Redis, MySQL, tsfresh, stumpy

## Development Commands

### Install Dependencies
```bash
pip install -r requirements.txt
# Note: numpy, scipy, patsy, and pandas must be installed first in that order
# For Docker, see Dockerfile for the layer-by-layer build pattern
```

### Run Tests
```bash
# Run all tests with pytest
pytest -v

# Run specific test file
pytest tests/algorithms_test.py -v

# Run with nosetests (legacy)
nosetests -v --nocapture
```

### Code Style
```bash
pep8 --exclude=migrations --ignore=E501,E251,E265,E402 ./
```

### Running Individual Daemons
```bash
# Each daemon is started via its bin/*.d script
# These require Redis, MySQL, and Memcached to be running first
./bin/analyzer.d
./bin/mirage.d
./bin/ionosphere.d
./bin/webapp.d
# etc.
```

### Docker Development
```bash
# Start full stack with Redis, MySQL, Memcached, Graphite
docker-compose up -d

# Build documentation
cd docs && make html
```

## Architecture

### Core Services (Daemon Applications)

Skyline is composed of multiple daemon processes that run independently:

1. **analyzer** (`skyline/analyzer/`) - Primary anomaly detection service. Uses multiple statistical algorithms to analyze incoming metrics and detect anomalies. Processes metrics from Redis.

2. **mirage** (`skyline/mirage/`) - Handles lower-frequency metrics and batch processing. Runs algorithmic analysis on metrics that don't need real-time processing.

3. **ionosphere** (`skyline/ionosphere/`) - Machine learning layer for reducing false positives. Learns patterns from historical data and performs pattern matching using tsfresh feature extraction and matrix profile algorithms.

4. **boundary** (`skyline/boundary/`) - Threshold-based alerting service for metrics with known expected ranges.

5. **horizon** (`skyline/horizon/`) - Real-time data ingestion service that receives and stores metrics at high throughput using UDP.

6. **flux** (`skyline/flux/`) - Data ingestion service supporting multiple protocols (Graphite, Prometheus, StatsD, Kafka, HTTP). Also includes an HTTP API for metric submission.

7. **webapp** (`skyline/webapp/`) - Flask-based web application providing the UI, API endpoints, and anomaly management interfaces.

8. **thunder** (`skyline/thunder/`) - Background tasks for periodic operations like metric maintenance and Ionosphere training.

9. **crucible** (`skyline/crucible/`) - Development tool for testing and debugging algorithms with your own data.

10. **panorama** (`skyline/panorama/`) - Handles anomaly event storage and management via MySQL.

11. **snab** (`skyline/snab/`) - SNAB (Skyline Noise Abatement) for alert management and noise reduction.

12. **luminosity** (`skyline/luminosity/`) - Metric classification and cloudburst analysis using ADTK and luminol.

13. **vista** (`skyline/vista/`) - Visualization and graph generation utilities using matplotlib.

14. **analyzer_dev** (`skyline/analyzer_dev/`) - Development version of analyzer with additional debugging capabilities.

### Key Shared Modules

- **skyline/settings.py** - Central configuration file (not user-defined settings; user config is in etc/skyline.conf)
- **skyline/functions/** - Shared utility functions organized by domain (database, redis, metrics, ionosphere, etc.)
- **skyline/custom_algorithms/** - User-defined custom anomaly detection algorithms
- **skyline/algorithm_exceptions.py** - Custom exceptions for algorithm errors
- **skyline/database.py** - SQLAlchemy-based database operations
- **skyline/skyline_functions.py** - Core Skyline utility functions
- **skyline/ionosphere_functions.py** - Ionosphere ML layer functions

### Configuration Approach

User configuration lives in `etc/skyline.conf` - defines Redis socket path, database credentials, namespaces, and algorithm settings. The `skyline/settings.py` file reads from `etc/skyline.conf` and sets Python module-level variables. The `skyline/docker.settings.py.default` provides a template for Docker deployments.

### Data Flow

```
Metrics -> Horizon/Flux (ingest to Redis)
              |
              v
    Analyzer/Mirage (read from Redis)
              |
              v
    Algorithm detection -> Ionosphere (ML layer for FP reduction)
              |                        |
              v                        v
    Panorama (store anomaly events in MySQL)
              |
              v
    Alerters (send notifications via Redis/SMTP/Slack/PagerDuty/etc.)

Ionosphere uses:
- tsfresh for feature extraction
- stumpy matrix profile for pattern matching
- Mass-Ts for similarity search
- SQLAlchemy + MySQL for pattern storage
```

### Alerting Pipeline

Anomalies trigger alerts via the alerters module which supports:
- SMTP email
- Slack
- PagerDuty
- HipChat
- Custom endpoints via HTTP POST to Redis

### External Dependencies

- **Redis** - Primary cache and metrics storage (socket: /tmp/redis.sock)
- **MySQL** - Persistent storage for anomalies, Ionosphere features profiles and configurations (see `skyline/skyline.sql` for schema)
- **Memcached** - Caching layer for Ionosphere feature profiles
- **Graphite/StatsD** - Optional external metric sources
- **Apache2** - Served by webapp for static assets

### Ionosphere Features

Ionosphere reduces false positives by:
1. Extracting 1300+ features using tsfresh
2. Computing matrix profiles using stumpy
3. Performing similarity search with Mass-Ts
4. Learning normal patterns from historical data
5. Training via the thunder daemon

Feature profiles are stored in MySQL with base64-encoded matplotlib visualizations.

### Configuration

- **etc/skyline.conf** - Main daemon configuration (PYTHON_VIRTUALENV, USE_PYTHON paths)
- **skyline/settings.py** - Application settings (Redis socket, namespaces, algorithm settings)
- **docker-compose.yml** - Full stack with Redis, MySQL, Memcached, Graphite

## Adding Custom Algorithms

Place custom algorithms in `skyline/custom_algorithms/`. Each algorithm should:
- Accept `timeseries` (tuple of timestamps, values) and `series` (pandas Series) parameters
- Return `True` if anomalous, `False` otherwise
- Handle edge cases gracefully to avoid killing the analyzer process
- Be wrapped in timeout-decorator to prevent hung algorithms
- Return results via `anomalyScore` attribute for scoring algorithms

Example algorithms in `skyline/custom_algorithms/`:
- `abs_stddev_from_median.py` - Statistical deviation
- `dbscan.py` - Density-based clustering
- `isolation_forest.py` - Tree-based anomaly detection
- `median_absolute_deviation.py` - MAD algorithm
- `pca.py` - Principal component analysis
- `spectral_residual.py` - FFT-based approach
- `adtk_*.py` - ADTK library wrappers
- `m66.py`, `mstl.py`, `prophet.py` - Time series specific

The `skyline/custom_algorithms/` directory contains both implementations and their source templates in `custom_algorithm_sources/`.