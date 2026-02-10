# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Parsl (Parallel Scripting Library) extends Python parallelism beyond a single computer. It enables workflow execution across multiple cores and nodes using a dataflow model where tasks are chained together and executed as resources become available.

## Development Commands

```bash
# Setup
make virtualenv              # Create virtual environment
source .venv/bin/activate    # Activate the virtual environment
make deps                    # Install dependencies from requirements.txt and test-requirements.txt
pip install ".[monitoring]"  # Install with extras (monitoring, visualization, workqueue, etc.)

# Linting and Type Checking
make isort                   # Check isort formatting
make flake8                  # Run flake8 linter
make lint                    # Verify all directories have __init__.py files
make mypy                    # Run mypy type checking

# Testing
pytest parsl/tests/test_python_apps/test_basic.py::test_simple  # Run single test
pytest parsl/tests/ -k "test_name" --config parsl/tests/configs/local_threads.py  # Run test by name
make local_thread_test       # Run tests with local_thread config
make htex_local_test         # Run tests with htex_local config (requires `pip install .`)
make config_local_test       # Run tests with local config (installs monitoring, viz, proxystore, kubernetes)
make test                    # Run all tests (isort, lint, flake8, mypy, all test configs)
pytest parsl/tests/ -k "not cleannet" --config local  # Run tests excluding network-dependent tests

# Cleanup
make clean                   # Remove .venv, dist, eggs, mypy cache, coverage, pytest cache
```

## Architecture

### Core Components

**DataFlowKernel (DFK)** (`parsl/dataflow/dflow.py`)
- Central orchestrator managing task futures and dependencies
- Handles task state transitions (pending -> runnable -> executing -> done)
- Integrates with monitoring, memoization, and data staging

**App Decorators** (`parsl/app/app.py`)
- `@python_app`: Decorate functions to run as parallel tasks
- `@bash_app`: Decorate shell command functions
- `@join_app`: Decorate functions that collect results from dependent apps (internal executor)

**Config** (`parsl/config.py`)
- Central configuration class specifying executors, providers, and monitoring
- Must be loaded via `parsl.load(config=config)` before executing apps
- Test configs in `parsl/tests/configs/` use `fresh_config()` pattern returning new Config instances

### Executors (`parsl/executors/`)

All executors inherit from `parsl/executors/base.py::ParslExecutor`.

- **ThreadPoolExecutor** (`parsl/executors/threads.py`): Simple thread-pool for single-node parallelism
- **HighThroughputExecutor** (`parsl/executors/high_throughput/`): Process-based executor using ZMQ interchange
- **WorkQueueExecutor** (`parsl/executors/workqueue/`): For WorkQueue/Condor batch systems
- **TaskVineExecutor** (`parsl/executors/taskvine/`): For TaskVine distributed scheduler
- **GlobusComputeExecutor** (`parsl/executors/globus_compute.py`): Remote execution via Globus Compute
- **RadicalPilotExecutor** (`parsl/executors/radical/`): For Radical Pilot on HPC resources
- **FluxExecutor** (`parsl/executors/flux/`): For Flux scheduler

### Providers (`parsl/providers/`)

Resource providers manage job submission and lifecycle on specific schedulers/systems:
- **LocalProvider**: Single machine execution
- **SlurmProvider**: SLURM cluster scheduling
- **CondorProvider**: HTCondor batch system
- **KubernetesProvider**: K8s cluster
- **AWSProvider, GoogleCloudProvider, AzureProvider**: Cloud providers
- Others: PBSPro, Torque, LSF, GridEngine

### Data Management (`parsl/data_provider/`)

- **File**: Represents input/output files with automatic staging
- **DataManager**: Handles file staging between tasks and storage systems
- Staging providers for FTP, HTTP, Globus, rsync transfers

### Monitoring (`parsl/monitoring/`)

- **MonitoringHub**: Central service receiving task/resource monitoring messages
- Records to SQL database (requires `.[monitoring]` extra)
- Visualization via `parsl-visualize` CLI

### Jobs Layer (`parsl/jobs/`)

Low-level job management:
- **JobStatusPoller**: Tracks job state across resource providers
- **Strategy**: Scaling logic for elastic resources

## Key Patterns

### Configuration and Execution
```python
import parsl
from parsl import python_app
from parsl.config import Config
from parsl.executors.threads import ThreadPoolExecutor

config = Config(executors=[ThreadPoolExecutor()])
parsl.load(config)

@python_app
def my_task(x):
    return x * 2

future = my_task(10)
result = future.result()  # Blocks until complete
```

### Chained Workflows
```python
a1 = app1(inputs=[data])
a2 = app2(inputs=[a1])
a3 = app3(inputs=[a1])
combined = app4(inputs=[a2, a3])  # Executes when both deps complete
```

### App Parameters
Apps support `stdout`, `stderr`, `walltime`, `inputs`, `outputs`, and `parsl_resource_specification` parameters.

## Code Conventions

- **Style**: PEP-8, enforced by flake8 in CI
- **Naming**: `ClassName`, `ExceptionName`, `GLOBAL_CONSTANT`, `lowercase_with_underscores`
- **Documentation**: NumPy/SciPy docstring style
- **Versioning**: CalVer (YYYY.MM.DD)
- **Tests**: Located in `parsl/tests/`, use pytest with `--config` pointing to config file
- **Type hints**: Runtime checking enabled via `typeguard.typechecked` decorator
- **Test markers**: `@pytest.mark.local` for tests needing custom config, `-k "not cleannet"` to exclude network tests