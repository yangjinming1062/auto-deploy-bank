# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyCBC is a gravitational wave detection and analysis toolkit used by LIGO/Virgo collaboration. It implements matched filtering algorithms for detecting coalescing compact binaries and provides Bayesian inference tools for parameter estimation. The package was used in the first direct detection of gravitational waves (GW150914).

## Development Commands

### Installation
```bash
# Install from source (requires LALSuite)
pip install .

# Full dependencies for development
pip install -r requirements.txt
pip install pytest "tox<4.0.0"
```

### Running Tests
```bash
# Run unit tests (primary test type)
tox -e py-unittest

# Test command-line help messages
tox -e py-help

# Run search-related tests (inspiral examples)
tox -e py-search

# Run inference tests
tox -e py-inference

# Build documentation
tox -e py-docs

# Run a single test file
python test/test_fft_base.py

# Run a single pytest
pytest test/test_fft_base.py -v
```

### Documentation
```bash
# Build documentation
python setup.py build_docs
```

## Architecture Overview

### Core Data Types (`pycbc/types/`)
- `TimeSeries` and `FrequencySeries`: Fundamental data containers with GPS time awareness
- `Array`: N-dimensional array wrapper with units support
- All types support HDF5 serialization

### Pipeline Architecture

**1. Signal Processing (`pycbc/filter/`)**
- Matched filtering implementation
- SNR computation (matchedfilter_cpu Cython module)
- Correlation algorithms (simd_correlate_cython)
- Autochisq: Auto-chi-squared signal consistency test

**2. Waveform Generation (`pycbc/waveform/`)**
- SPA (stationary phase approximation) templates (spa_tmplt_cpu Cython)
- Full Taylor expansions and effective-one-body (EOB) models via LALSuite
- Waveform decompressors (decompress_cpu_cython)
- `decompress_cpu_cython`: Optimized waveform interpolation

**3. Trigger Generation (`pycbc/events/`)**
- `pycbc_inspiral`: Main inspiral detection executable
- Trigger finding and thresholding
- Event manager (eventmgr_cython Cython module)
- SIMD threshold calculations (simd_threshold_cython)

**4. Coincidence & Ranking (`pycbc/workflow/coincidence.py`)**
- Timeslide coincidence searches
- Multi-detector coincident trigger ranking
- False alarm rate (FAR) calculation

**5. Bayesian Inference (`pycbc/inference/`)**
- Models: `models/` directory - Likelihood implementations (relative binning, marginalization)
- Samplers: `sampler/` directory - emcee (MCMC), dynesty (nested sampling), Gibbs
- Jump proposals: `jump/` directory - MCMC proposal distributions
- Burn-in: `burn_in.py` - Convergence diagnostics
- IO: `io/` - Posterior sample file handling (HDF5)

**6. Workflow Orchestration (`pycbc/workflow/`)**
- `core.py`: Main workflow orchestration (Pegasus-based)
- `pegasus_workflow.py`: DAG generation for distributed execution
- `jobsetup.py`: Job configuration and submission
- `coincidence.py`: Coincidence workflow setup
- Configuration parsing via `configparser`

### Key Executables (`bin/`)
- `all_sky_search/`: Template bank, coincidence, and ranking executables
- `bank/`: Template bank generation (pycbc_tmpltbank, pycbc_geom_aligned_bank)
- `inference/`: Bayesian inference scripts (pycbc_inference, plotters)
- `hwinj/`: Hardware injection tools
- `workflow/`: Pipeline orchestration scripts

### Hardware Acceleration
- CUDA support via PyCUDA/scikit-cuda (optional, via `extras_require['cuda']`)
- SIMD optimizations via Cython extensions
- MKL backend support (`pycbc.fft.mkl`)
- FFTW3 backend support (`pycbc.fft.fftw_pruned_cython`)
- OpenMP parallelization (disabled on macOS)

### Key Dependencies
- **LALSuite**: C gravitational wave library (required, `lalsuite!=7.2`)
- **lscsoft-glue**: Workflow and coincidence processing
- **igwn-ligolw**: LIGO lightweight XML format
- **igwn-segments**: Segment query and handling
- **gwdatafind**: GWF frame file discovery
- **pegasus-wms**: Workflow management for distributed computing
- **dynesty<3.0**: Nested sampling sampler
- **emcee==2.2.1**: MCMC sampler

### Configuration System
- INI-style config files (ConfigParser)
- Section naming uses `+` as delimiter (`VARARGS_DELIM` in `pycbc/__init__.py`)
- Common options via `add_common_pycbc_options()` in `pycbc/__init__.py`
- Logging via `init_logging()` with ISO-8601 timestamps and SIGUSR1 dynamic verbosity

### CUDA Configuration
- Auto-detected at import via PyCUDA
- `HAVE_CUDA` boolean set in `pycbc/__init__.py`
- CUDA modules listed in `setup.py` `cythonext` for conditional compilation

## Important Paths
- Test files: `test/` directory (not `pycbc/test/`)
- Executable scripts: `bin/` (automatically installed as scripts)
- Workflow templates: `pycbc/workflow/`
- Documentation source: `docs/`