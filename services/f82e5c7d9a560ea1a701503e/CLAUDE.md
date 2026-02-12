# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DiskCache is a pure-Python disk and file-backed cache library compatible with Django. It uses SQLite for metadata storage and the filesystem for large values, implementing multiple eviction policies (LRU, LFU).

## Commands

```bash
# Run all tests (uses pytest-xdist for parallel execution)
pytest

# Run single test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::TestCache::test_set_get

# Run all checks (code formatting, linting, type checking)
tox

# Run individual tox environments
tox -e flake8
tox -e mypy
tox -e pylint
tox -e bluecheck

# Build docs
tox -e docs

# Install development dependencies
pip install -r requirements-dev.txt
```

## Architecture

### Core Components (`diskcache/`)

- **core.py** (2455 lines): Core `Cache` class and `Disk` serialization layer
  - `Cache`: Main cache implementation using SQLite + filesystem
  - `Disk`: Handles key/value serialization and file storage
  - Default 1GB size limit, 10 cull limit, WAL journal mode, 64MB mmap

- **fanout.py** (687 lines): `FanoutCache` provides sharding across multiple `Cache` instances for write distribution

- **persistent.py** (1245 lines): `Deque` and `Index` - persistent, disk-backed data structures implementing Sequence and Mapping ABCs

- **djangocache.py** (456 lines): Django cache backend integration (`DjangoCache`)

- **recipes.py** (488 lines): Synchronization primitives
  - `Lock`, `RLock`: Cross-process file locking
  - `barrier`: Sync barrier for multiple processes
  - `throttle`: Rate limiting via cache
  - `memoize_stampede`: Cache-aside with stampede prevention

### Database Schema

The SQLite database stores cache metadata including:
- `key` (text, primary): Serialized key
- `raw` (integer): Whether value is stored raw in DB
- `value` (blob): Serialized value (for small values)
- `filename` (text): Path to file (for large values)
- `expire_time` (real): Optional TTL expiration
- `tag` (text): User-defined tag for grouping
- `size` (integer): Total size of value + metadata
- `access_time`, `store_time`, `access_count`: For eviction policies

### Key Design Patterns

1. **Small values stored in DB, large values in files**: Threshold is `disk_min_file_size` (32KB default)
2. **Eviction policies**: `least-recently-stored`, `least-recently-used`, `least-frequently-used`, `none`
3. **Transaction safety**: Nested transactions with thread-local transaction IDs
4. **WAL mode**: Enables concurrent reads during writes
5. **Sharding**: FanoutCache distributes keys across N Cache instances to reduce lock contention

### Performance Considerations

- Tests require 98%+ coverage
- Uses memory-mapped files (mmap) for efficient I/O
- Checksum-based hash for portable key distribution