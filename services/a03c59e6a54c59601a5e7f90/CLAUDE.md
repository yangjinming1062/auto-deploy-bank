# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

BigDL 2.0 is a Big Data AI platform that seamlessly scales data analytics & AI applications from laptop to cloud. It provides multiple libraries:

- **Orca** (`python/orca/`, `scala/orca/`): Distributed Big Data & AI (TF & PyTorch) Pipeline on Spark and Ray
- **Nano** (`python/nano/`): Transparent Acceleration of TensorFlow & PyTorch Programs on Intel CPU/GPU
- **DLlib** (`python/dllib/`, `scala/dllib/`): "Equivalent of Spark MLlib" for Deep Learning
- **Chronos** (`python/chronos/`): Scalable Time Series Analysis using AutoML
- **Friesian** (`python/friesian/`, `scala/friesian/`): End-to-End Recommendation Systems
- **PPML** (`python/ppml/`, `scala/ppml/`): Secure Big Data and AI (with SGX/TDX Hardware Security)
- **LLM** (deprecated, `python/llm/`): Now moved to [IPEX-LLM](https://github.com/intel-analytics/ipex-llm) - use that instead
- **Serving** (`python/serving/`, `scala/serving/`): Model serving infrastructure

## Building and Installation

### Python Packages

Each module can be installed individually:

```bash
# Install specific modules
pip install bigdl-orca==${VERSION}
pip install bigdl-nano==${VERSION}
pip install bigdl-chronos==${VERSION}
pip install bigdl-friesian==${VERSION}
pip install bigdl-serving==${VERSION}
pip install bigdl-ppml==${VERSION}

# Or install all at once
pip install bigdl

# Install nightly build
pip install --pre --upgrade bigdl
```

Build and install a module from source:

```bash
# For Python modules
cd python/[module]
bash dev/build_and_install.sh linux default false [pytorch|tensorflow]

# Example for Nano
cd python/nano
bash dev/build_and_install.sh linux default false pytorch
```

### Scala Modules

Build Scala modules using Maven:

```bash
# Build all Scala modules
cd scala
mvn clean install -DskipTests

# Build specific module
cd scala/[module]
mvn clean install -DskipTests

# Run tests
mvn test
```

Create distribution package:

```bash
cd scala
bash make-dist.sh
```

## Testing

### Python Tests

Each module has its own test directory structure. Run tests using pytest:

```bash
# Run all tests for a module
cd python/[module]
pytest test/ -v

# Run specific test file
pytest test/bigdl/[module]/[submodule]/test_[name].py -v

# Run with coverage
pytest --cov=src/bigdl/[module] test/

# Run tests in parallel
pytest -n auto test/
```

Module-specific test commands:

```bash
# Orca tests
cd python/orca
bash dev/test/run-pytests.sh

# Chronos tests
cd python/chronos
bash dev/test/run-pytests.sh

# Nano tests
cd python/nano
bash test/run-nano-howto-tests.sh

# PPML tests
cd python/ppml
pytest test/ -v

# Friesian tests
cd python/friesian
pytest test/ -v
```

Run single test:
```bash
pytest python/[module]/test/bigdl/[module]/[submodule]/test_[specific_test].py::test_function_name -v
```

### Scala Tests

```bash
# Run all tests for a module
cd scala/[module]
mvn test

# Run specific test class
mvn test -Dtest=TestClassName

# Run tests in parallel
mvn test -DtestsThreadCount=4
```

### Style Checking

Run linting and style checks:

```bash
# Check Python style for all modules
bash python/dev/check-license
bash python/dllib/dev/lint-python
bash python/orca/dev/test/lint-python
bash python/nano/dev/lint-python
bash python/chronos/dev/test/lint-python
bash python/friesian/dev/test/lint-python
bash python/ppml/dev/lint-python
bash python/serving/dev/lint-python
bash python/llm/dev/test/lint-python

# Check Scala style
bash scala/dev/scalastyle
```

## Code Architecture

### Project Structure

```
/
├── apps/                    # Example applications
├── python/                  # Python modules
│   ├── orca/               # Orca library
│   ├── nano/               # Nano acceleration library
│   ├── dllib/              # DLlib deep learning library
│   ├── chronos/            # Chronos time series analysis
│   ├── friesian/           # Friesian recommendation systems
│   ├── ppml/               # PPML privacy-preserving ML
│   ├── llm/                # LLM library (deprecated, use IPEX-LLM)
│   ├── serving/            # Model serving
│   ├── dev/                # Development utilities
│   └── requirements/       # Python requirements
├── scala/                   # Scala modules
│   ├── orca/               # Orca Scala components
│   ├── dllib/              # DLlib Scala components
│   ├── friesian/           # Friesian Scala components
│   ├── ppml/               # PPML Scala components
│   ├── serving/            # Serving Scala components
│   ├── common/             # Common Spark versions
│   └── assembly/           # Assembly configurations
├── ppml/                    # PPML documentation and examples
├── docker/                  # Docker configurations
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

### Key Components

**Orca** (`python/orca/`, `scala/orca/`):
- Integrates TensorFlow and PyTorch with Spark and Ray
- Provides distributed training and inference capabilities
- Supports `RayOnSpark` for running Ray programs on Spark clusters
- Entry point: `from bigdl.orca import init_orca_context`

**Nano** (`python/nano/`):
- Provides transparent acceleration for TensorFlow and PyTorch
- Automatically applies CPU optimizations (SIMD, multiprocessing, low precision)
- Entry point: `from bigdl.nano.pytorch import TorchNano, InferenceOptimizer`

**DLlib** (`python/dllib/`, `scala/dllib/`):
- Keras-style API for deep learning on Spark
- Integrates with Spark ML Pipeline
- Entry point: `from bigdl.dllib.keras import Model` (Python) or `com.intel.analytics.bigdl.dllib.keras.Model` (Scala)

**Chronos** (`python/chronos/`):
- Time series forecasting with AutoML
- Entry point: `from bigdl.chronos.forecaster import TCNForecaster`

**Friesian** (`python/friesian/`, `scala/friesian/`):
- End-to-end recommendation systems
- Entry point: `from bigdl.friesian import feature`

**PPML** (`python/ppml/`, `scala/ppml/`):
- Privacy-preserving machine learning using SGX/TDX
- Entry point: `from bigdl.ppml.fl import *

## Migration from BigDL/Analytics Zoo

This is BigDL 2.0. Code needs to be migrated from legacy BigDL or Analytics Zoo:

### Import Path Changes

**BigDL Python migration**:
- `from bigdl.XYZ import *` → `from bigdl.dllib.XYZ import *`
- `from bigdl.dataset.XYZ import *` → `from bigdl.dllib.feature.dataset.XYZ import *`
- `from bigdl.transform.XYZ import *` → `from bigdl.dllib.feature.transform.XYZ import *`

**BigDL Scala migration**:
- `import com.intel.analytics.bigdl.XYZ` → `import com.intel.analytics.bigdl.dllib.XYZ`
- `com.intel.analytics.bigdl.dataset.XYZ` → `com.intel.analytics.bigdl.dllib.feature.dataset.XYZ`

**Analytics Zoo Python migration**:
- `from zoo.XYZ import *` → `from bigdl.dllib.XYZ import *` (for feature/nnframes)
- `from zoo.pipeline.api.keras import *` → `from bigdl.dllib.keras import *`
- `from zoo.XYZ import *` → `from bigdl.orca.XYZ import *` (for tfpark modules)

**Analytics Zoo Scala migration**:
- `import com.intel.analytics.zoo.XYZ` → `import com.intel.analytics.bigdl.dllib.XYZ` (for feature/nnframes)
- `import com.intel.analytics.zoo.pipeline.api.keras.XYZ` → `import com.intel.analytics.bigdl.dllib.keras.XYZ`
- `import com.intel.analytics.zoo.XYZ` → `import com.intel.analytics.bigdl.orca.XYZ` (for tfpark)

See `MappingGuidance.md` and `MigrationGuidance.md` for complete mapping details.

## Common Development Tasks

### Adding Type Hints (Friesian)

Use the automated type hinting tool:

```bash
cd python/dev
bash add_type_hint.sh [module_name] [submodule_name]
```

### Running Examples

Most modules have example directories:

```bash
# Run Orca examples
cd python/orca/example
python [example_file].py

# Run Chronos examples
cd python/chronos/example
python [example_file].py

# Run Nano tutorials
cd python/nano/tutorial
jupyter notebook
```

### Environment Variables

Common environment variables:

```bash
export BIGDL_HOME=/path/to/BigDL
export ANALYTICS_ZOO_ROOT=/path/to/BigDL
export PYSPARK_PYTHON=python
export PYSPARK_DRIVER_PYTHON=python
```

### Docker Usage

```bash
# Build Docker image
docker build -t bigdl/[module]:latest -f docker/[module]/Dockerfile .

# Run container
docker run -it --rm -e notebook bigdl/[module]:latest
```

## Important Notes

1. **LLM Deprecation**: `bigdl-llm` has been deprecated. Use [IPEX-LLM](https://github.com/intel-analytics/ipex-llm) for LLM features instead.

2. **Migration Required**: This is BigDL 2.0. Legacy BigDL/Analytics Zoo code requires import path updates (see Migration section above).

3. **Multi-Language Project**: Both Python and Scala modules are developed. When making changes, ensure both are updated if applicable.

4. **Version Consistency**: All Python modules should use the same version number (see `python/version.txt`).

5. **Testing Strategy**: Each module has comprehensive test suites. Run relevant tests before submitting changes. Style checks are enforced via CI.

6. **Documentation**: Python modules use Sphinx for documentation. Build docs with `bash python/dev/docs_build.sh` in respective modules.

7. **Spark Compatibility**: Scala modules support multiple Spark versions (2.0, 2.4, 3.0+). Check `scala/common/spark-version/` for version-specific code.