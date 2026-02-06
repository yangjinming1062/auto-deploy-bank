# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyQuokka is a push-based distributed query engine with lineage-based fault tolerance, optimized for time series workloads. Built completely in Python using:
- **Ray**: Task scheduling and distributed execution
- **Redis**: Lineage tracking and coordination (requires Redis > 6.2)
- **Polars/DuckDB**: Relational algebra kernels
- **Apache Arrow**: I/O and data representation
- **SQLGlot**: SQL parsing

## Common Commands

### Installation
```bash
pip3 install pyquokka
```

### Local Development
Requires Redis server running on port 6800:
```bash
redis-server --port 6800 --protected-mode no
```

### Running Examples
```bash
# TPC-H queries
python3 apps/tpc-h/tpch.py

# Time series backtesting
python3 apps/rottnest/backtester.py

# Other examples in apps/ directory
```

## Architecture

### Entry Point
- **`pyquokka.df.QuokkaContext`**: Main user-facing API (similar to SparkContext). Create with `qc = QuokkaContext()` for local mode or pass a `Cluster` object for distributed execution.

### Core Data Types
- **`DataStream`**: Lazy evaluation API for distributed data processing. Create via `qc.read_csv()`, `qc.read_parquet()`, or `qc.from_polars()`.
- **`OrderedStream`**: For time series data with ordering requirements. Created via `qc.from_ordered_csv()` or `qc.from_ordered_parquet()`.

### Execution Layers (Top to Bottom)

1. **API Layer** (`df.py`, `datastream.py`, `orderedstream.py`)
   - `QuokkaContext`: Creates DataStreams from data sources
   - `DataStream`: Lazy transformations (filter, select, join, groupby)
   - `OrderedStream`: Time-series specific operations

2. **Logical Plan** (`logical.py`)
   - `Node` base class for operators in the DAG
   - Lowering transforms logical plans to runtime task graphs

3. **Runtime** (`quokka_runtime.py`, `core.py`)
   - `TaskGraph`: Builds execution DAG from logical plan
   - `TaskManager` / `ReplayTaskManager`: Executes tasks on each node
   - Push-based execution model with stages and channels

4. **Operators** (`executors/`)
   - Base class: `Executor` with `execute()` and `done()` methods
   - `ts_executors.py`: Time series operators (windows, asof joins)
   - `sql_executors.py`: SQL operators (filter, project, join, aggregate)
   - `cep_executors.py`: Complex event processing (pattern matching)
   - `vector_executors.py`: Vector operations

5. **Data Sources** (`dataset/`)
   - `BaseInputDataset`: Abstract base for data readers
   - `UnorderedReaders`: CSV, Parquet, JSON readers
   - `OrderedReaders`: Time-ordered data readers

6. **Coordination** (`coordinator.py`, `tables.py`, `task.py`)
   - `Coordinator`: Ray actor managing global state via Redis
   - Redis tables for lineage, object locations, task tracking
   - Task types: `InputTask`, `ExecutorTask`, `ReplayTask`

### Key Files
- **`pyquokka/__init__.py`**: Package entry point
- **`pyquokka/core.py`**: TaskManager and core execution logic
- **`pyquokka/quokka_runtime.py`**: TaskGraph and execution orchestration
- **`pyquokka/coordinator.py`**: Central coordinator actor
- **`pyquokka/df.py`**: QuokkaContext and high-level API
- **`pyquokka/utils.py`**: Cluster management (LocalCluster, EC2Cluster)

### Data Flow
1. User creates `QuokkaContext` with optional `Cluster`
2. Read data via `qc.read_csv()` / `qc.read_parquet()` returning `DataStream`
3. Chain transformations (filter, join, etc.) - lazy, builds DAG
4. Call `stream.collect()` or `stream.compute()` to execute
5. Logical plan lowered to TaskGraph
6. Coordinator distributes work to TaskManagers
7. TaskManagers push data through channels via Arrow Flight

## Configuration

```python
qc.set_config("fault_tolerance", True)  # Enable checkpoint-based recovery
qc.set_config("blocking", False)         # Pipeline execution
qc.set_config("checkpoint_interval", 30) # Seconds between checkpoints
```

## Example Usage Pattern

```python
from pyquokka import QuokkaContext
import polars

qc = QuokkaContext()  # Local cluster
lineitem = qc.read_parquet("s3://bucket/lineitem.parquet/*")
orders = qc.read_parquet("s3://bucket/orders.parquet/*")

result = (lineitem
    .filter(lineitem["l_commitdate"] < lineitem["l_receiptdate"])
    .join(orders, left_on="l_orderkey", right_on="o_orderkey", how="semi")
    .filter_sql("o_orderdate >= date '1993-07-01'")
    .select(["o_orderkey", "o_custkey", "o_totalprice"])
    .collect())
```