# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

matplotlib/basemap is a library for plotting data on map projections with matplotlib. It provides the `Basemap` class for mapping geographic data onto various map projections and helper functions for interpolation, masking oceans, and grid manipulation.

## Build Commands

```bash
# Install in development mode with all extras
pip install -e ".[lint,test,doc]"

# Run all tests
python -m pytest test/

# Run a single test
python -m pytest test/mpl_toolkits/basemap/test_Basemap.py::TestMplToolkitsBasemapBasemap::test_init_with_ortho_c_resolution

# Run linters (flake8 and pylint)
flake8 src/mpl_toolkits/basemap/
pylint src/mpl_toolkits/basemap/

# Build source distribution
python -m build --sdist

# Build documentation
python -m sphinx -j auto doc/source public
```

## Architecture

The project is structured as a matplotlib toolkit with these key components:

### Core Modules (`src/mpl_toolkits/basemap/`)

- **`__init__.py`** (5420 lines): Main module containing the `Basemap` class. Handles map projection setup, coastline/river/lake drawing, meridian/parallel lines, and coordinate transformations. Contains utility functions: `interp`, `maskoceans`, `shiftgrid`, `addcyclic`.

- **`proj.py`**: `Proj` class wrapping pyproj for cartographic transformations (lat/lon to x/y projection coordinates and back).

- **`cm.py`**: Colormap utilities for matplotlib with geographic colormaps.

- **`solar.py`**: Solar position and terminator calculations.

- **`diagnostic.py`**: Diagnostic functions for the library.

### C Extension (`src/_geoslib.pyx`)

Cython extension wrapping the GEOS (Geometry Engine - Open Source) library. Provides efficient geometry operations for polygon clipping and geometric manipulations. Must call `initGEOS()` before use and `finishGEOS()` when done.

### Data Packages

Geographic data (coastlines, rivers, political boundaries) is distributed separately via `basemap-data` and optionally `basemap-data-hires` packages. The library expects data in `mpl_toolkits.basemap_data` package.

### Dependencies

Key runtime dependencies:
- `numpy` - Array operations
- `matplotlib` - Plotting framework
- `pyproj` - PROJ library bindings for map projections
- `pyshp` - Shapefile handling
- `geos_c` - Geometry engine (C library, not a Python package)

### Test Structure (`test/mpl_toolkits/basemap/`)

- `test_Basemap.py`: Main tests for Basemap class initialization and drawing methods
- `test_proj.py`: Tests for Proj class coordinate transformations
- `test_cm.py`: Tests for colormap utilities
- `test_diagnostic.py`: Tests for diagnostic functions

## Development Notes

- Python 3.9-3.13 supported (see `setup.py` for exact bounds)
- GEOS library (version 3.6.5 in CI) must be available when building from source
- Use `GEOS_DIR` environment variable if GEOS is not in standard locations
- NumPy include paths determined at build time via `numpy.get_include()` or `NUMPY_INCLUDE_PATH` env var