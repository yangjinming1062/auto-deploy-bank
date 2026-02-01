# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MemoryLeakDetector (codename "Raphael") is a native memory leak monitoring tool for Android developed by ByteDance. It monitors malloc/calloc/realloc/memalign/mmap/munmap allocations and captures stack traces to detect memory leaks. It uses PLT/GOT hooking and inline hooking to intercept memory allocation functions.

## Build Commands

```bash
# Build the entire project (library and demo)
./gradlew assembleDebug

# Build only the library module
./gradlew :library:assembleRelease

# Build the demo app
./gradlew :demo:assembleDebug

# Run a specific task
./gradlew <task-name>
```

## Architecture

### Module Structure
- **library/**: Android library module containing the core leak detection logic
  - `src/main/java/com/bytedance/raphael/`: Java API layer
  - `src/main/cpp/`: C++ core logic (Raphael.cpp, HookProxy.h, MemoryCache.cpp, MapData.cpp)
  - `src/main/xHook/`: xHook library for PLT/GOT hooking
  - `src/main/xDL/`: xDL library for dynamic library loading
  - `src/main/inline32/` and `inline64/`: Inline hooking implementations for ARM/ARM64
  - `src/main/unwind32/` and `unwind64/`: Stack unwinding implementations
  - `src/main/python/`: Analysis scripts (raphael.py, mmap.py)
- **demo/**: Demo application showing how to use the library

### Core Components

**HookProxy.h**: Contains the hook implementation that intercepts memory allocation functions:
- `malloc_proxy`, `calloc_proxy`, `realloc_proxy`, `memalign_proxy`
- `mmap_proxy`, `mmap64_proxy`, `munmap_proxy`
- Uses pthread guard key to prevent recursive calls
- Two registration modes: inline hooking (current process) and PLT/GOT hooking (specific SO files)

**Raphael.java**: Main Java API with three control modes:
- `start(configs, space, regex)`: Start monitoring
- `print()`: Output leak report
- `stop()`: Stop monitoring

**Raphael.cpp**: Native entry point handling JNI calls and system state dumping

### Data Flow
1. `Raphael.start()` → registers hooks (inline or PLT/GOT) → MemoryCache tracks allocations
2. Allocations → proxy functions capture address, size, and stack trace → store in cache
3. `Raphael.print()` → cleans cache files → outputs report + /proc/self/maps
4. `raphael.py` analysis script → parses report → groups by SO → symbolication via addr2line

### Monitoring Modes
- **ALLOC_MODE (0x00400000)**: Monitor heap allocations (malloc/calloc/realloc/memalign)
- **MAP64_MODE (0x00800000)**: Monitor mmap allocations
- Config depth: `(configs & DEPTH_MASK) >> 16` for stack depth (max 31)
- Config limit: `configs & LIMIT_MASK` for minimum allocation size to track

## Analysis Workflow

```bash
# 1. Run the app and trigger monitoring
adb shell am broadcast -a com.bytedance.raphael.ACTION_START -f 0x01000000 --es configs 0xCF0400

# 2. Reproduce the leak scenario, then print results
adb shell am broadcast -a com.bytedance.raphael.ACTION_PRINT -f 0x01000000

# 3. Pull the report
adb pull /sdcard/Android/data/com.bytedance.demo/files/raphael/ ./report/

# 4. Analyze with Python script
python3 library/src/main/python/raphael.py -r report -o leak-doubts.txt -s ./symbol/
```

## Key Files
- `library/CMakeLists.txt`: CMake build configuration for native code
- `library/src/main/cpp/HookProxy.h`: Hook registration and proxy implementations
- `library/src/main/cpp/Raphael.h/cpp`: Core orchestration logic
- `library/src/main/cpp/MemoryCache.cpp`: Allocation tracking
- `library/src/main/python/raphael.py`: Report analysis and symbolication