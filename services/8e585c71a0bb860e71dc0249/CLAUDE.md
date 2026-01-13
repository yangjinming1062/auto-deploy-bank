# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is MindSpore

MindSpore is an open-source deep learning training/inference framework supporting mobile, edge, and cloud scenarios. It provides native support for Ascend AI processors and features:

- **Automatic Differentiation** using Source Transformation (ST), enabling both dynamic usability and static optimization
- **Automatic Parallel** training with data/model/hybrid parallelism
- **Multi-platform support**: Ascend (910/910b), GPU (CUDA 10.1/11.1), CPU

## Common Development Commands

### Building MindSpore

**Prerequisites:**
- Initialize submodules: `git submodule update --init --recursive`
- CMake ≥ 3.14.0
- Python ≥ 3.7.5

**Basic build:**
```bash
# CPU backend
bash build.sh -e cpu -j8

# GPU backend
bash build.sh -e gpu -V 10.1 -j8

# Ascend backend
bash build.sh -e ascend -V 910 -j8

# Debug build
bash build.sh -e cpu -d -j8

# Build options
bash build.sh -e cpu -r          # Release mode (default)
bash build.sh -e cpu -i          # Incremental build
bash build.sh -e cpu -k          # Clean build artifacts
bash build.sh -e cpu -v          # Show build commands
```

See `scripts/build/usage.sh` for complete build options.

### Running Tests

**Python unit tests:**
```bash
# Run all Python UT
bash tests/ut/python/runtest.sh

# Run by stages
bash tests/ut/python/runtest.sh stage1  # dataset
bash tests/ut/python/runtest.sh stage2  # parallel
bash tests/ut/python/runtest.sh stage3  # ops, pynative_mode, pipeline, train
bash tests/ut/python/runtest.sh stage4  # nn and other tests

# Run single test
pytest tests/ut/python/ops/test_xxx.py -v
pytest tests/ut/python/nn/test_xxx.py -v
```

**C++ unit tests:**
```bash
bash tests/ut/cpp/runtest.sh
```

**System tests:**
```bash
bash tests/st/runtest.sh
```

### Code Quality Checks

**Linters (automatically run in CI):**
- Python: PyLint, PEP 8
- C++: CppLint, CppCheck
- Markdown: MarkdownLint
- Shell: ShellCheck
- CMake: CMakeLint

**Install and run locally:**
```bash
pip install pylint cppcheck shellcheck cmakelint
pylint mindspore/python/mindspore/...
cppcheck mindspore/ccsrc/...
```

### Code Formatting

**C++ formatting:**
```bash
# Format C++ code with clang-format
find mindspore/ccsrc -name "*.cc" -o -name "*.h" | xargs clang-format -i
```

**Python formatting:**
```bash
# Using autopep8 or black (configure in your IDE)
autopep8 --in-place --aggressive --aggressive mindspore/python/mindspore/...
```

## High-Level Architecture

### Core Components

```
mindspore/
├── mindspore/ccsrc/          # C++ core runtime
│   ├── backend/              # Backend execution (graph compilation, optimization)
│   ├── frontend/             # Frontend compilation (IR generation)
│   ├── runtime/              # Runtime execution engine
│   ├── kernel/               # Computation kernels
│   ├── pipeline/             # Execution pipeline (pynative, graph)
│   ├── plugin/device/        # Device backends (ascend, gpu, cpu)
│   └── minddata/             # Dataset processing
│
├── mindspore/lite/           # Lightweight inference runtime
│   ├── src/                  # C++ source
│   ├── schema/               # Model schema definitions
│   └── tools/                # Conversion/optimization tools
│
└── mindspore/python/mindspore/  # Python API
    ├── nn/                   # Neural network layers
    ├── ops/                  # Operations
    ├── dataset/              # Data pipeline
    ├── parallel/             # Distributed training
    ├── pynative_mode/        # Dynamic graph mode
    ├── pipeline/             # Graph compilation pipeline
    └── train/                # Training utilities
```

### Execution Modes

1. **Graph Mode** (`context.GRAPH_MODE`): Static graph with optimizations, better performance
2. **PyNative Mode** (`context.PYNATIVE_MODE`): Dynamic graph, easier debugging

### Critical Submodules

MindSpore depends on several submodules that must be initialized:
- **`graphengine`**: Graph execution engine
- **`akg`**: Array Generation Kernel (for computation kernel generation)
- **`tests/models`**: Test models repository

## Key Development Workflows

### Contributing Changes

1. **Sign CLA**: Required before first contribution (see [ICLA](https://www.mindspore.cn/icla))
2. **Fork and clone**: Fork repo, add upstream remote
3. **Create branch**: `git checkout -b feature_name`
4. **Develop**: Make changes following code style guidelines
5. **Test**: Run relevant unit tests (ut) and system tests (st)
6. **Submit PR**: PRs require 2+ LGTM from approvers

**PR Guidelines:**
- Avoid irrelevant changes
- Keep commit history ordered
- Link related issues
- Update tests as needed
- Maintain bilingual documentation (EN/CN) for user-facing changes

### Testing Requirements

- **Python tests**: pytest framework (see `tests/ut/python/`)
- **C++ tests**: GoogleTest framework (see `tests/ut/cpp/`)
- **System tests**: Integration tests (see `tests/st/`)
- Test design intent should be clear from name/comment (CONTRIBUTING.md:39-41)

### Build Variants

| Target | Command | Use Case |
|--------|---------|----------|
| CPU | `build.sh -e cpu` | General development, CI |
| GPU | `build.sh -e gpu -V 10.1` | GPU-specific features |
| Ascend | `build.sh -e ascend -V 910` | Ascend-specific features |
| Lite | `build.sh -e cpu -n lite` | Mobile/edge deployment |

## Platform Support

MindSpore runs on:
- **Ascend**: 910, 910b (EulerOS, Ubuntu, CentOS)
- **GPU**: CUDA 10.1, 11.1 (Ubuntu)
- **CPU**: x86_64, ARM64 (Ubuntu, Windows, macOS)
- **Lite**: ARM32, ARM64, x86_64 (for edge devices)

See [README.md:72-141](README.md#installation) for detailed installation options.

## Performance Optimization

- **Source Transformation**: Automatic differentiation at compilation time enables static optimization
- **Automatic Parallel**: Splits operators across devices for distributed training
- **Kernel Fusion**: Combines operations to reduce memory overhead
- **Graph Optimization**: Dead code elimination, constant folding, kernel selection

## Documentation

- **README.md**: Main project documentation and architecture overview
- **CONTRIBUTING.md**: Contribution guidelines and development workflow
- **/docs/**: Detailed architecture diagrams and API documentation
- **Bilingual**: English and Chinese versions available for major docs

## Additional Resources

- [Architecture Guide](https://www.mindspore.cn/tutorials/en/master/beginner/introduction.html)
- [User Documentation](https://gitee.com/mindspore/docs)
- [MindSpore Slack](https://join.slack.com/t/mindspore/shared_invite/zt-dgk65rli-3ex4xvS4wHX7UDmsQmfu8w)

## Important Notes

- **Submodules**: Always `git submodule update --init` after clone
- **CI**: Jenkins CI automatically builds and tests PRs
- **Code Style**: Google C++ style, Python PEP 8 (enforced by linters)
- **Performance**: MindSpore IR is functional; supports composable transformations
- **Devices**: Plugin architecture allows adding new hardware backends
- **Lite Runtime**: Separate lightweight runtime for production inference