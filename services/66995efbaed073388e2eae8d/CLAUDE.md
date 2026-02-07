# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quokka is a **push-based distributed query engine with lineage-based fault tolerance** for time series analytics. It's built on Python with DuckDB, Polars, Ray, Arrow, Redis, and SQLGlot.

**Key difference from Spark**: DataStream partitions can be consumed immediately after produced, enabling pipelined shuffles and I/O for significant performance gains.

## Development Commands

```bash
# Install in development mode
pip install -e .

# Requires Redis > 6.2 to be running
redis-server -v  # verify version
```

## Architecture

### Core Components

- **QuokkaContext** (`pyquokka/df.py`): Main entry point, similar to SparkContext. Creates IO and compute nodes on Ray cluster.
- **DataStream** (`pyquokka/datastream.py`): Lazy stream of Polars DataFrames. User-facing API for transformations.
- **TaskGraph** (`pyquokka/quokka_runtime.py`): Builds and executes the task dependency DAG.
- **TaskManager** (`pyquokka/core.py`): Executes tasks on each node. Handles input reading, execution, and output pushing.

### Operator Implementations

- **Executors** (`pyquokka/executors/`):
  - `sql_executors.py`: Filter, select, join, aggregate operators using DuckDB
  - `ts_executors.py`: Time series operators (windows, asof joins, stateful transforms)
  - `cep_executors.py`: Complex event processing (pattern matching, transactions)
  - `vector_executors.py`: Vector embedding operations

- **Input Readers** (`pyquokka/dataset/`):
  - `ordered_readers.py`: Time-ordered readers (逐 timestamps, crypto, etc.)
  - `unordered_readers.py`: Parquet, CSV, S3 readers

### Redis Tables (in `pyquokka/tables.py`)

Quokka uses Redis for coordination and fault tolerance:
- **FOT** (FunctionObjectTable): Stores operators
- **NTT** (NodeTaskTable): Task queue per node
- **LT** (LineageTable): Lineage of each object (for recovery)
- **CT** (CemetaryTable): Tracks garbage collection eligibility
- **PT** (PresentObjectTable): Object locations
- **NOT** (NodeObjectTable): Objects per node

### Execution Flow

1. User creates QuokkaContext → spawns Ray actors (coordinator, catalog, task managers)
2. User defines DataStream transformations (lazy)
3. `compute()` or `collect()` triggers TaskGraph creation
4. TaskGraph registers operators and partition functions in Redis
5. Coordinator orchestrates execution across nodes
6. TaskManagers pull tasks from NTT, execute, push outputs

### Fault Tolerance

Quokka uses **lineage-based recovery**:
- All objects logged in LT (lineage → how to recreate)
- On node failure: coordinator reads NTT for pending tasks, reconstructs from lineage
- Objects buffered in HBQ (high-bandwidth queue) until confirmed consumed
- See `fault-tolerance.md` for detailed protocol

## Key Files

| File | Purpose |
|------|---------|
| `pyquokka/core.py` | TaskManager implementation, main execution loop |
| `pyquokka/quokka_runtime.py` | TaskGraph, coordinates execution |
| `pyquokka/df.py` | QuokkaContext API |
| `pyquokka/datastream.py` | DataStream API (filter, select, join, etc.) |
| `pyquokka/executors/*.py` | Operator implementations |
| `pyquokka/dataset/*.py` | Input readers |
| `pyquokka/logical.py` | Logical plan nodes |
| `pyquokka/utils.py` | Cluster management (EC2Cluster, LocalCluster) |

## Adding New Operators

1. Create executor class in `pyquokka/executors/` inheriting from `Executor`
2. Implement `execute(self, batches, stream_id, executor_id)` returning output batches
3. Add DataStream method in `pyquokka/datastream.py` wrapping the operator
4. Register in logical plan (`pyquokka/logical.py`) if needed