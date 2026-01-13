# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is this project?

Ray is a unified framework for scaling AI and Python applications from a laptop to a cluster. It consists of:
- **Ray Core**: Distributed runtime with Tasks (stateless functions), Actors (stateful workers), and Objects (distributed shared memory)
- **Ray AI Libraries**: Data, Train, Tune, RLlib, and Serve for ML workloads

## Build System

Ray uses **Bazel** as its primary build system. Bazel version 6.5.0 is required (see .bazelversion).

### Build Configuration Files
- `/WORKSPACE`: External dependencies and toolchain registration
- `BUILD.bazel`: Top-level build targets
- `src/**/BUILD.bazel`: Fine-grained build files (transitioning from monolithic BUILD.bazel)
- `python/**/BUILD.bazel`: Python-specific build targets

### Common Build Commands

```bash
# Build C++ code
bazel build //src/ray/...

# Build Python wheels
python/python/build-wheel-manylinux2014.sh  # Linux
python/python/build-wheel-macos.sh         # macOS
python/python/build-wheel-windows.sh       # Windows

# Generate protobuf files
bazel run //:install_py_proto

# Create ray package
bazel build //:ray_pkg
```

## Testing

Ray uses pytest for Python tests and Bazel test for C++ tests.

### Running Tests

```bash
# Run all Python tests
pytest python/ray/tests/...

# Run specific test file
pytest python/ray/tests/test_foo.py

# Run C++ tests
bazel test //cpp:all

# Run C++ worker example tests
bazel test //cpp:cluster_mode_test --test_arg=--external_cluster=true

# Run with timeout (pytest default: 180s)
pytest --timeout=300 python/ray/tests/test_foo.py

# Test output verbosity
bazel test --test_output=all //src/ray/...

# Run specific Python test with cluster mode
bazel test --config=ci //cpp:test_python_call_cpp
```

### Test Structure

- `python/ray/tests/`: Core Ray tests
- `rllib/`: RLlib library tests
- `python/ray/air/tests/`: Ray AIR tests
- `python/ray/serve/tests/`: Ray Serve tests
- `src/ray/cpp/`: C++ example tests
- `cpp/`: C++ worker integration tests
- `python/ray/data/tests/`: Ray Data tests
- `python/ray/train/tests/`: Ray Train tests
- `python/ray/tune/tests/`: Ray Tune tests

### Test Fixtures and Configuration

Ray uses pytest with extensive fixtures defined in `python/ray/tests/conftest.py`:
- **Cluster fixtures**: `cluster`, `autoscaling_cluster` for multi-node testing
- **Redis fixtures**: Redis instances with optional TLS and authentication
- **Dashboard fixtures**: Web dashboard testing utilities
- **Default timeout**: 180 seconds (configurable with `--timeout`)

```bash
# Run tests with fixtures
pytest python/ray/tests/test_actor.py::test_actor_pool_placement_group

# Run tests with specific timeout
pytest --timeout=300 python/ray/tests/test_gcs_fault_tolerance.py

# Run tests with cluster fixture
pytest python/ray/tests/test_autoscaler.py::test_scale_up_mini_cluster

# Run tests with output
pytest -xvs python/ray/tests/test_basic.py
```

### CI Configuration

Ray uses **Buildkite** for CI with pipeline-based execution:

**Pipeline Files:**
- `.buildkite/*.rayci.yml`: Pipeline definitions for different components
- `.buildkite/cicd.rayci.yml`: General CI/CD pipeline
- `.buildkite/lint.rayci.yml`: Linting and code quality checks
- `.buildkite/core.rayci.yml`: Core Ray tests
- `.buildkite/ml.rayci.yml`: ML library tests (Train, Tune, Data, RLlib)

**Test Selection:**
```bash
# Determine which tests to run based on changed files
python ci/pipeline/determine_tests_to_run.py
```

**CI Scripts:**
- `ci/ci.sh`: Main CI entry point with functions for building and testing
- `ci/ray_ci/tester_container.py`: Container-based testing framework
- `ci/run/bazel_export_options`: Bazel test configuration flags

**CI Test Execution:**
- C++ tests: `bazel test --config=ci //cpp:all`
- Python tests: Containerized with ray_ci
- Platform-specific: Linux, macOS, Windows pipelines
- ARM64 support: Separate pipeline for aarch64 builds

## Code Style and Linting

Ray uses multiple linting tools:

### Python Linting
- **Ruff** for import sorting, formatting, and linting (configured in `pyproject.toml`)
- **Pylint** for additional checks (see `pylintrc`)

```bash
# Run Python linters
ci/lint/lint.sh

# Check import order
ci/lint/check_import_order.py

# Format Python code
ruff format python/ray/...

# Lint with ruff
ruff check python/ray/...
```

### C++ Linting
- **clang-format** for code formatting (`.clang-format`, `.git-blame-ignore-revs`)
- **clang-tidy** for static analysis (`.clang-tidy`)
- **Bazel Buildifier** for BUILD file formatting

```bash
# Format C++ code
ci/lint/git-clang-format HEAD~1

# Check clang-tidy
ci/lint/check-git-clang-tidy-output.sh

# Format BUILD files
bazel run --config=ci //:refresh_compile_commands
```

### Documentation Style

Documentation in `/doc` follows comprehensive style guidelines (see `doc/.cursor/rules/ray-docs-style.mdc`):

**Key Rules:**
- **Voice**: Always use active voice ("The system retries failed tasks", not "Failed tasks are retried")
- **Contractions**: Use contractions throughout ("don't", "can't", "it's") except in warnings
- **Headings**: Use sentence case ("## Why asynchronous inference?", not "## Why Asynchronous Inference?")
- **Format**: Use Sphinx/reStructuredText directives (`:::{note}`, `:doc:`, `:ref:`) not Markdown
- **Component names**: Always capitalize ("Ray Serve", "Ray Data", "Ray Core")
- **Code examples**: Use complete descriptive lead-ins ("The following example shows...", not "Example:")
- **Word choice**: Use "such as" not "like" for examples, "ID" not "id"

```bash
# Check documentation style
ci/lint/check-documentation-style.sh
```

## Project Architecture

### Directory Structure

```
/src/ray/                 # C++ core components
  ├── common/            # Common utilities and data structures
  ├── core_worker/       # Core worker process (task execution)
  ├── gcs/              # Global Control Service (GCS) server
  ├── object_manager/   # Distributed object store
  ├── raylet/           # Node manager (scheduling, resource management)
  ├── rpc/              # RPC client/server implementations
  └── protobuf/         # Protocol buffer definitions

/python/ray/             # Python bindings and libraries
  ├── _private/         # Internal implementation details
  ├── air/              # Ray AI Runtime (AIR) libraries
  ├── autoscaler/       # Cluster autoscaler
  ├── data/             # Ray Data library
  ├── serve/            # Ray Serve library
  ├── train/            # Ray Train library
  ├── tune/             # Ray Tune library
  ├── workflow/         # Ray Workflow library
  └── dashboard/        # Web dashboard

/cpp/                    # C++ example applications and tests

/bazel/                  # Bazel-specific build rules and macros
```

### Key Components

1. **Core Worker** (`src/ray/core_worker/`): Executes tasks and actors, manages object references
2. **Raylet** (`src/ray/raylet/`): Node-level scheduling and resource management
3. **GCS** (`src/ray/gcs/`): Global metadata store for cluster state
4. **Object Manager** (`src/ray/object_manager/`): Distributed object store with plasma
5. **Dashboard** (`python/ray/dashboard/`): Web UI for monitoring and debugging

### Build Artifacts

Key build targets:
- `//:ray_pkg`: Complete Ray package with C++ components
- `//:ray_pkg_zip`: Zipped binary distribution
- `//:ray_py_proto_zip`: Generated Python protobuf files
- `//cpp:all`: C++ examples and tests

## Development Workflow

### Setting Up Environment

```bash
# Install dependencies (see python/requirements.txt)
pip install -e python  # Install Ray in editable mode

# Build C++ components
bazel build //:ray_pkg

# Set up pre-commit hooks (optional)
cat .pre-commit-config.yaml
```

### Making Changes

1. **C++ changes**: Update corresponding BUILD.bazel files in `src/**/`
2. **Protobuf changes**: Modify `.proto` files, regenerate with `bazel run //:install_py_proto`
3. **Python changes**: Follow import order (see `ci/lint/check_import_order.py`)

### Common Development Tasks

```bash
# Build specific component
bazel build //src/ray/core_worker:core_worker_lib
bazel build //src/ray/raylet:raylet_lib
bazel build //src/ray/gcs:gcs_server

# Test specific component
bazel test //src/ray/core_worker:core_worker_lib_test
pytest python/ray/tests/test_actor.py
pytest python/ray/serve/tests/test_replica.py

# Run tests in a specific module
pytest python/ray/data/tests/
pytest python/ray/train/tests/
pytest python/ray/tune/tests/

# Generate compile commands for IDE
bazel run //:refresh_compile_commands

# Compile C++ in debug mode
bazel build //:ray_pkg --config=dbg

# Check for banned words
ci/lint/check-banned-words.sh

# Run documentation style checks
ci/lint/check-documentation-style.sh

# Format imports and code
ruff check --fix python/ray/serve/
ruff format python/ray/data/

# Check import order
python ci/lint/check_import_order.py

# Build dashboard frontend
NO_DASHBOARD=1 ci/ci.sh build_dashboard_front_end  # Skip if not needed

# Compile Python protobuf files
bazel run //:install_py_proto

# Clean build artifacts
bazel clean --expunge
```

## Important Development Notes

### Protocol Buffer Standards

When modifying `.proto` files, follow RPC fault-tolerance standards:
- Review: https://github.com/ray-project/ray/tree/master/doc/source/ray-core/internals/rpc-fault-tolerance.rst
- Bugbot will automatically flag `.proto` changes in PRs

### Build Configuration

- Bazel config options in `.bazelrc`
- CI configuration: `--config=ci` in `BUILD.bazel`
- Platform-specific builds use `select()` in BUILD files
- Default test timeout: 180 seconds (pytest.ini)

### Documentation

- Use reStructuredText (`.rst`) for documentation
- Sphinx for documentation generation
- Follow style guide in `doc/.cursor/rules/ray-docs-style.mdc`

### Platform Support

- **Linux**: x86_64, arm64 (aarch64)
- **macOS**: x86_64 (Intel), arm64 (Apple Silicon/M1/M2/M3)
- **Windows**: x86_64
- **Python versions**: 3.9, 3.10, 3.11, 3.12, 3.13
- **Bazel**: 6.5.0 required (enforced in WORKSPACE)

**Platform-specific notes:**
- macOS cluster mode: Enabled via `RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER=1`
- Windows: Uses MSVC compiler, special Bazel config (`build:msvc-cl`)
- ARM64: Some dependency resolution limitations in CI
- Test environment: Requires `LC_ALL` and `LANG` set for C++ worker tests

## Bug Reports and Contributing

### Communication Channels
- **Discourse Forum**: https://discuss.ray.io/ - Development discussions and usage questions
- **GitHub Issues**: Bug reports and feature requests
- **StackOverflow**: General usage questions (tag: ray)
- **Slack**: https://www.ray.io/join-slack - Community collaboration

### PR Review Process
For ray-project members:
1. Add reviewer to assignee section when creating PR
2. Address reviewer comments and remove `@author-action-required` label
3. Add `test-ok` label after build passes
4. Committers will merge once build is passing

For external contributors:
1. PRs will be assigned reviewers
2. Actively ping assignees after addressing comments

### Code Review Settings
Ray has automated code review configured (see `.gemini/config.yaml`):
- Comment severity threshold: MEDIUM
- Automatic code review on PR opened
- Pull request summaries enabled

## Additional Development Notes

### Import Organization

Ray uses a specific import order enforced by `ci/lint/check_import_order.py`:
```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import os
import sys

# 3. Third-party
import numpy as np
import pandas as pd

# 4. First-party (ray modules)
import ray
from ray import serve
from ray.data import Dataset

# 5. Local folder
from .module import Class
```

Configuration in `pyproject.toml` under `[tool.ruff.lint.isort]`:
- `section-order`: future, standard-library, third-party, first-party, local-folder, afterray
- `known-local-folder`: ray, ray_release
- `combine-as-imports`: true for cleaner imports

### Buildifier and BUILD File Standards

Ray is migrating from monolithic BUILD.bazel to distributed BUILD files:
- **Old**: Single large `BUILD.bazel` in root
- **New**: Fine-grained `BUILD.bazel` files in each subdirectory
- **Migration**: Use `git mv` to preserve file history
- **Format**: Use `bazel run --config=ci //:refresh_compile_commands`

Key BUILD targets:
- `ray_cc_library`: C++ library compilation
- `py_binary`, `py_library`: Python targets
- `cc_proto_library`: Protocol buffer compilation

### Key Internal Modules

**Critical Python Modules** (`python/ray/_private/`):
- `worker.py`: Core worker implementation (74KB+)
- `services.py`: Ray cluster services (74KB+)
- `node.py`: Node management and lifecycle (74KB+)
- `utils.py`: Utility functions and helpers (58KB+)
- `ray_constants.py`: System-wide constants
- `function_manager.py`: Function registration and execution

**Core C++ Components** (`src/ray/raylet/`):
- Node-level scheduling and resource management
- Task dispatch and execution coordination
- Object store integration

### Pre-commit Hooks

Ray uses pre-commit for automated formatting (`.pre-commit-config.yaml`):
- **Ruff**: Python formatting and linting
- **Buildifier**: BUILD file formatting
- **clang-format**: C++ code formatting
- **cpplint**: C++ static analysis
- **pydoclint**: Documentation linting

Install and run:
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### Protocol Buffer Standards

When modifying `.proto` files:
1. Follow RPC fault-tolerance standards (see `doc/source/ray-core/internals/rpc-fault-tolerance.rst`)
2. Regenerate Python bindings: `bazel run //:install_py_proto`
3. Changes automatically flagged by Bugbot in PRs
4. Review process includes cross-language compatibility checks

## References

### Documentation
- **Main docs**: https://docs.ray.io/
- **Ray Core walkthrough**: https://docs.ray.io/en/latest/ray-core/walkthrough.html
- **Ray AI Libraries**: https://docs.ray.io/en/latest/ray-air/getting-started.html

### Core Concepts
- **Tasks**: https://docs.ray.io/en/latest/ray-core/tasks.html
- **Actors**: https://docs.ray.io/en/latest/ray-core/actors.html
- **Objects**: https://docs.ray.io/en/latest/ray-core/objects.html

### Architecture Papers
- **Current architecture**: https://docs.google.com/document/d/1tBw9A4j62ruI5omIJbMxly-la5w4q_TjyJgJL_jN2fI/preview
- **Ownership paper**: https://www.usenix.org/system/files/nsdi21-wang.pdf
- **Exoshuffle paper**: https://arxiv.org/abs/2203.05072