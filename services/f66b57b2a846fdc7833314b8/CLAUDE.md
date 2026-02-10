# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Test Commands

```bash
# Install dependencies
make deps

# Run linting (isort, flake8, mypy, lint scripts)
make lint isort flake8 mypy

# Run tests with local thread executor (fastest, smallest test set)
make local_thread_test

# Run full local test suite with monitoring, HTEX, etc.
make config_local_test  # Requires: pip install ".[monitoring,visualization,proxystore,kubernetes]"

# Run all tests (full suite)
make test

# Run a single test
pytest parsl/tests/test_python_apps/test_basic.py::test_simple

# Clean environment
make clean
```

## Code Architecture

Parsl is a parallel scripting library that enables workflow execution across multiple compute resources. Key components:

### Core Components

1. **DataFlowKernel (`parsl/dataflow/dflow.py`)** - Central orchestrator managing task dependencies and execution. Creates AppFutures for apps, submits tasks to executors, and handles retries/memoization.

2. **Apps (`parsl/app/app.py`)** - Decorators (`@python_app`, `@bash_app`, `@join_app`) that convert functions into asynchronous apps returning AppFutures.

3. **Executors (`parsl/executors/`)** - abstractions for different compute resources:
   - `ThreadPoolExecutor` - Local multi-threaded execution
   - `HighThroughputExecutor` - MPI-based distributed execution with worker pools
   - `WorkQueueExecutor` - Cooperative scheduling via Work Queue
   - `TaskVineExecutor` - Cooperative scheduling via TaskVine
   - `RadicalPilotExecutor`, `FluxExecutor`, `GlobusComputeExecutor` - External scheduler integration

4. **Providers (`parsl/providers/`)** - Resource managers for batch systems and clouds:
   - Slurm, PBS, LSF, GridEngine, Condor - HPC schedulers
   - AWS, Azure, GoogleCloud - Cloud providers
   - Kubernetes - Container orchestration
   - Local - Direct execution

5. **Monitoring (`parsl/monitoring/`)** - Database logging of workflow execution via `MonitoringHub`

### Key Patterns

- **AppFutures** (`parsl/dataflow/futures.py`) - Wraps executor futures, enables `.result()` blocking and dependency chaining via `__getitem__`
- **Config** (`parsl/config.py`) - Defines executors, strategy, retries, monitoring, etc. Loaded via `parsl.load(config)`
- **Type checking** - Uses `typeguard` for runtime type validation on public APIs
- **Serialization** - Uses `dill` for task/closure serialization; `tblib` for exception traceback pickling

### Data Flow

```
User Code → @python_app decorator → AppFuture
AppFuture → DataFlowKernel.submit() → Executor.submit() → Worker Process/Thread
Result → AppFuture.result()
```

### Directory Structure

- `parsl/app/` - App decorators and futures
- `parsl/dataflow/` - DFK, memoization, dependency resolution
- `parsl/executors/` - Executor implementations and base class
- `parsl/providers/` - Resource provisioning for various schedulers/clouds
- `parsl/data_provider/` - File staging (local, HTTP, Globus, etc.)
- `parsl/jobs/` - Job status polling and status handling
- `parsl/launchers/` - Parallel job launchers (mpi_exec, aprun, srun, etc.)
- `parsl/monitoring/` - Monitoring hub and database schema
- `parsl/tests/` - Test suite organized by feature area

## Development Notes

- **Python version**: 3.10+
- **Style**: PEP-8 enforced via flake8; import sorting via isort; type hints checked with mypy
- **Testing**: Use pytest with `--config` flag for executor-specific tests. Tests requiring no DFK use `@pytest.mark.local`
- **Versioning**: Calendar versioning (YYYY.MM.DD) - updates in `parsl/version.py`
- **Documentation**: NumPy/SciPy style docstrings; built with Sphinx on ReadTheDocs