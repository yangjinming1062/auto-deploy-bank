# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

whispercpp is Pybind11 bindings for [whisper.cpp](https://github.com/ggerganov/whisper.cpp), providing a Python interface to OpenAI's Whisper speech recognition model. The project uses Bazel as its build system and requires git submodules to be initialized.

## Common Commands

### Setup
```bash
# Initialize git submodules (whispercpp and pybind11)
git submodule update --init --recursive

# Start development shell with nix (recommended)
nix-shell

# Update Python dependencies from pyproject.toml
./tools/bazel run pypi_update
```

### Building
```bash
# Build C++ extensions and copy .so files to src/whispercpp/
./tools/bazel run extensions

# Build wheel package
./tools/bazel build //:whispercpp_wheel
# Or using pypa/build:
python3 -m build -w

# Install locally built wheel
pip install $(./tools/bazel info bazel-bin)/*.whl
```

### Testing
```bash
# Run all tests
./tools/bazel test tests/... examples/...

# Run CI tests only (excludes slow context tests marked as "enormous")
./tools/bazel test tests:ci examples/...

# Run a single test file
./tools/bazel test tests:export
./tools/bazel test tests:params
./tools/bazel test tests:utils
```

### Formatting and Linting
```bash
# Format all code using treefmt (requires nix)
nix-shell --command treefmt

# Or format individually:
./tools/bazel run //:buildfmt  # Bazel files
black . && isort . && ruff --fix .
clang-format -i --style=file:.clang-format src/**/*.cc src/**/*.h

# Check formatting without applying
black --check . && isort --check . && ruff check src

# Check Bazel file syntax
./tools/bazel test //:buildcheck
```

### Type Checking
```bash
./tools/bazel run //:pyright
# Or with nix:
nix-shell --command pyright
```

## Architecture

### Python Layer (`src/whispercpp/`)
- `__init__.py` - Main `Whisper` class with `from_pretrained()` factory method and `transcribe()` API
- `utils.py` - LazyLoader for extensions, model download utilities (XDG-compliant), audio device listing
- `*.pyi` files - Static type hints for pyright

### C++ Bindings (`src/whispercpp/`)
- `api_cpp2py_export.cc/h` - Wraps `Context` (whisper_context) and `Params` (whisper_full_params) with pybind11
- `audio_cpp2py_export.cc/h` - Wraps audio capture via SDL2 and WAV file loading
- `context.cc/h`, `params.cc/h` - C++ helper classes for sampling strategies, callbacks, and parameter building

The C++ code follows a builder pattern for `Params` (fluent API with `with_*` methods) and wraps whisper.cpp structures directly.

### Build Configuration
- Bazel 6.0.0 is required (see `.bazelversion`)
- `BUILD.bazel` - Main build file defining pybind11 extensions, wheel generation, and build targets
- `WORKSPACE` - External dependency loading (pybind11, whisper.cpp, SDL2, Python toolchain)
- `rules/` - Custom Bazel rules for Python ABI handling and dependency management

### Testing (`tests/`)
- `conftest.py` - Pytest configuration for Bazel runfiles integration
- `context_export_test.py` - Full integration tests (marked as "enormous", excluded from CI)
- `export_test.py`, `params_export_test.py`, `utils_test.py` - Unit tests for API coverage
- `tests:ci` test suite excludes the slow `context` test

### External Dependencies (git submodules)
- `extern/whispercpp/` - whisper.cpp source (C++ inference engine)
- `extern/pybind11/` - Pybind11 source (Python/C++ bindings)

Models are downloaded from HuggingFace to `$XDG_DATA_HOME/whispercpp` or `~/.local/share/whispercpp`.

## Key Patterns

- **Lazy extension loading**: C++ extensions (`api_cpp2py_export`, `audio_cpp2py_export`) are loaded lazily via `utils.LazyLoader` to avoid import errors before building
- **Builder pattern**: `Params` uses fluent builder API (`params.with_language("en").with_n_threads(4).build()`)
- **Factory pattern**: `Whisper.from_pretrained(model_name)` creates instances rather than `__init__`