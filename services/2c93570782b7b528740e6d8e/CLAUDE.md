# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Skyline is a real-time anomaly detection and time series monitoring system that enables passive monitoring on metrics without requiring per-metric configuration. Once running, new metrics are automatically added for analysis. The system uses multiple algorithms to detect anomalies and allows users to train it on what is anomalous per metric.

**Version:** 4.0.0 (master branch, release tag)

## Commands

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r dev-requirements.txt
```

### Testing
```bash
# Run all tests
pytest tests

# Run with verbose output
pytest -v tests

# Run specific test file
pytest tests/baseline/tsfresh_features_test.py
```

### Code Quality
```bash
# pep8 linting (legacy, may not be installed)
pep8 --exclude=migrations --ignore=E501,E251,E265,E402 ./
```

### Running Skyline
Skyline uses daemon scripts in `bin/` that require a Python virtualenv. Configure via `etc/skyline.conf`:
```bash
PYTHON_VIRTUALENV="true"
USE_PYTHON="/path/to/python"
```

## Architecture

### Components

Skyline consists of multiple daemons that work together:

- **flux/** - Data ingestion from various sources (Graphite, statsd, Telegraf, Kafka)
- **horizon/** - Real-time streaming data processing
- **analyzer/** - Real-time anomaly detection using statistical algorithms
- **analyzer_batch/** - Batch anomaly detection for historical data
- **mirage/** - Forecasting-based anomaly detection
- **boundary/** - Boundary/outlier detection
- **ionosphere/** - ML-based anomaly detection using tsfresh feature extraction
- **luminosity/** - Metric classification and categorization
- **panorama/** - Alert generation and management
- **snab/** - Alert forwarding (Slack, PagerDuty, SMTP, etc.)
- **thunder/** - Batch processing for long-term metrics
- **webapp/** - Flask-based web UI for visualization
- **crucible/** - Data processing utilities

### Key Modules

- **skyline_functions.py** - Core utilities (121KB)
- **ionosphere_functions.py** - Ionosphere ML feature matching (106KB)
- **settings.py** - Configuration (200KB) with environment-based overrides via `SKYLINE_SETTINGS`
- **database.py** - MySQL database operations
- **validate_settings.py** - Settings validation

### Data Storage

- **Redis** - Timeseries cache, metrics queue, real-time data (port 6379)
- **MySQL** - Anomaly metadata, Ionosphere features, historical data (port 3306)
- **Memcached** - Query caching (port 11211)
- **Graphite/statsd** - Metrics storage (ports 80, 2003-2004)

### Algorithms

Core algorithms are in `skyline/functions/algorithms.py` (85KB):
- Seasonal ESD, Gradient, Histogram bins, Mean, Median, MinMax, Percentile, etc.

ML-based feature extraction uses `tsfresh` (custom earthgecko fork) and `stumpy` for matrix profile analysis.

### Entry Points

Daemons are started via `bin/*` scripts (one per component). Each daemon:
1. Reads configuration from `etc/skyline.conf`
2. Validates settings
3. Runs as a daemon process

## Configuration

Primary config: `skyline/settings.py` (200KB)

Override with environment variable:
```bash
SKYLINE_SETTINGS=/path/to/custom_settings.py
```

## Development Notes

- Python 3.8+ required
- Custom tsfresh fork at `git+https://github.com/earthgecko/tsfresh@3d5a320`
- Custom luminol fork at `git+https://github.com/earthgecko/luminol@40791e2`
- Custom adtk fork at `git+https://github.com/earthgecko/adtk@895c517`
- numba >=0.56.4 requires numpy<1.24, so pinned to numpy==1.23.5