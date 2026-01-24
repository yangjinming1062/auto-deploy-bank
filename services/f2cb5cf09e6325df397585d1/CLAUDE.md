# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HyperLPR3 is a high-performance Chinese license plate recognition framework with implementations in both C++ (core) and Python (wrapper). It supports real-time plate recognition across multiple platforms: Linux (x86, ARM), MacOS, Android, and iOS.

## Build Commands

### Python Package
```bash
# Install dependencies
pip install -r Prj-Python/requirements.txt

# Install package in development mode
pip install -e Prj-Python/

# Run quick test
lpr3 sample -src images/test_img.jpg -det high

# Start WebAPI service
lpr3 rest --port 8715 --host 0.0.0.0
```

### C++ Shared Library (Linux/Mac)
```bash
# Build shared library
sh command/build_release_linux_share.sh

# Output: build/linux/install/hyperlpr3/{include,lib,resource}
```

### C++ Demo
```bash
cd Prj-Linux
sh build.sh
./build/PlateRecDemo ../hyperlpr3/resource/models/r2_mobile ../hyperlpr3/resource/images/test_img.jpg
```

### Android
```bash
# Requires ANDROID_NDK environment variable
sh command/build_release_android_share.sh
# Output: build/release_android/{arm64-v8a,armeabi-v7a}
```

### Docker
```bash
docker build -t hyperlpr_build .
docker-compose up build_linux_x86_shared_lib
```

### CMake Options
- `-DLINUX_FETCH_MNN=ON` (default): Download MNN from git during build
- `-DLINUX_USE_3RDPARTY_OPENCV=ON`: Use pre-compiled OpenCV from 3rdparty
- `-DBUILD_SAMPLES=ON`: Build sample executables
- `-DBUILD_TEST=ON`: Build unit tests

## Architecture

### C++ Core Structure (cpp/src/)
- **buffer_module/**: Image data stream handling, format conversion (RGB/BGR/YUV)
- **context_module/**: Core recognition context, configuration, plate detection pipeline
- **nn_module/**: Neural network interface abstractions
- **nn_implementation_module/**: Model loading and inference implementations
- **inference_helper_module/**: MNN inference helper (required, not RKNN)

### C++ API (cpp/c_api/hyper_lpr_sdk.h)
- C-style API for cross-platform use
- Key types: `HLPR_Context`, `HLPR_DataBuffer`, `HLPR_PlateResult`
- Key functions: `HLPR_CreateContext()`, `HLPR_ContextUpdateStream()`, `HLPR_ReleaseContext()`

### Python Package (Prj-Python/hyperlpr3/)
- **hyperlpr3.py**: Main Python interface wrapping C++ library
- **inference/**: ONNX runtime inference fallback
- **command/**: CLI tools (`lpr3 sample`, `lpr3 rest`)

### Platform Projects
- **Prj-Linux/**: Linux demo application
- **Prj-Android/**: Android project structure
- **Prj-iOS/**: iOS project structure

## Dependencies

### C++ Build
- OpenCV 4.0+
- MNN 2.0+ (fetched automatically or from 3rdparty_hyper_inspire_op)
- CMake 3.14+

### Python Runtime
- opencv-python, onnxruntime, fastapi, uvicorn, loguru, python-multipart, tqdm, requests

## Key Configuration Files

- **CMakeLists.txt**: Main build configuration with platform detection
- **command/build_release_linux_share.sh**: Linux shared library build script
- **Prj-Python/setup.py**: Python package configuration with CLI entry points