# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BMF (Babit Multimedia Framework) is a cross-platform, multi-language multimedia processing framework with strong GPU acceleration. It handles video processing, transcoding, AI inference, and supports Python, C++, and Go APIs.

**Key directories:**
- `bmf/engine/c_engine/` - Core C++ execution engine (graph scheduling, task dispatch)
- `bmf/sdk/cpp_sdk/` - C++ SDK headers for module development
- `bmf/c_modules/` - Built-in FFmpeg-based modules (decoder, encoder, filter)
- `bmf/python_sdk/` - Python SDK for module implementation
- `bmf/hmp/` - Heterogeneous Media Processing library (GPU acceleration, data format conversion)
- `bmf_lite/` - Client-side lightweight multimedia framework (Android, iOS, OHOS)

## Build Commands

```bash
# Standard build (x86)
./build.sh

# Debug build
./build.sh debug

# Debug with coverage
./build.sh with_cov

# Build with AddressSanitizer
./build.sh asan

# Build with UBSan
./build.sh ubsan

# Clean build
./build.sh clean

# Multi-Python version build (x86 packaging)
export SCRIPT_EXEC_MODE=x86
./build.sh

# Build for ARM (aarch64)
./build_aarch64.sh

# Build for macOS
./build_osx.sh

# Build for Android
./build_android.sh

# Build WASM
./build_wasm.sh
```

## Testing

```bash
# Run Python tests with pytest
pytest bmf/test/

# Run a specific test
pytest bmf/test/sync_mode/

# Run C++ engine tests (after build)
./test_bmf_engine
```

## Architecture

### Graph Pipeline Model
BMF processes media through a **graph** of **modules**. The framework:
1. Creates a `BmfGraph` with input/output streams
2. Chains modules together via `module()`, `decode()`, `encode()` APIs
3. Executes asynchronously with the C++ engine scheduler

### Module Types
- **Python modules** - Extend `bmf.Module` base class, implement `process()` method
- **C++ modules** - Implement `Module` interface via C API
- **FFmpeg modules** - Built-in decoder/encoder/filter modules (ffmpeg_decoder, ffmpeg_encoder, ffmpeg_filter)
- **Go modules** - Loadable Go modules

### Data Flow
- **Packet** - Basic data unit containing VideoFrame, AudioFrame, or custom data
- **Task** - Contains input/output packets for module processing
- **VideoFrame/AudioFrame** - Frame data holders supporting CPU/GPU

### Multi-Mode Operation
- **Graph Mode** - Async pipeline execution with stream chaining
- **Sync Mode** - Direct module invocation without graph building
- **Server Mode** - Long-running graph with dynamic input
- **Generator Mode** - Generate output without input source
- **PushData Mode** - Push data into running graph

### HMP (Heterogeneous Media Processing)
GPU-accelerated processing library providing:
- CPU/GPU memory management
- Color space conversion (NV12, RGB, etc.)
- Tensor conversion (PyTorch, OpenCV, TensorRT)
- Hardware-accelerated filters

## Code Style

**C++:**
```bash
clang-format -sort-includes=false -style="{BasedOnStyle: llvm, IndentWidth: 4}" -i <file>
```

**Python:**
```bash
yapf --in-place --recursive --style="{indent_width: 4}"
```

## Key APIs

**Python Graph Building:**
```python
import bmf

graph = bmf.graph()
output = graph.module(end_node={'name': 'decoder', ...})
     .ff_filter('scale', {'size': '320x240'})
     .encode('libx264', {'preset': 'fast'})
     .output()
```

**Sync Module Usage:**
```python
from bmf.builder import bmf_sync

decoder = bmf_sync.sync_module('c_ffmpeg_decoder', option, [0], [0, 1])
# Process frames directly without graph
```

## Development Notes

- Built-in modules defined in `BUILTIN_CONFIG.json` (bmf/c_modules/meta/)
- C++ module SDK headers in `bmf/sdk/cpp_sdk/include/bmf/sdk/`
- FFmpeg modules wrap ffmpeg components (libavcodec, libavfilter, etc.)
- PyBind11 used for Python/C++ bindings
- Connector pattern used for C++ engine communication (see bmf/engine/connector/)