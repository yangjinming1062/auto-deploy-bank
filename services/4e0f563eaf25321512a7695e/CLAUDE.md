# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Setup

-   **Install dependencies:** `pip install -e mapproxy/`
-   **Install dev dependencies:** `pip install -r mapproxy/requirements-tests.txt`
-   **Create a new application:** `mapproxy-util create -t base-config apps/base`

### Running Tests

-   Run all tests: `pytest mapproxy` (run from the `mapproxy/` directory)
-   Run a single test: `pytest mapproxy/test/unit/test_grid.py -v` (run from the `mapproxy/` directory)

### Running the Development Server

-   Start a dev server in debug mode: `mapproxy-util serve-develop apps/base/mapproxy.yaml --debug`

## Code Architecture

MapProxy is an open source proxy for geospatial data. It caches, accelerates and transforms data from existing map services.

-   **Request Handling**: The application determines which handler (e.g., WMS, WMTS) to use based on the request URL. Incoming HTTP requests are converted into internal request objects (e.g., `WMSRequest`).
-   **Tiling**: The `TileManager` class decides whether to serve tiles from the cache or a source.
-   **Caching**: All caches implement the `TileCacheBase` interface. The application is stateless except for the cache, which uses file system locks.
-   **Configuration**: The code in the `config/` directory builds MapProxy from a configuration file. `config/spec.py` is used for configuration validation.
-   **Data Sources**: The `source/` directory contains code for fetching data, which uses low-level functions from the `client/` directory.
-   **Layers**: The `layer.py` file is responsible for merging, clipping, and transforming tiles.
