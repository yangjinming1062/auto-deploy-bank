# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AppShark is a static taint analysis platform for scanning security vulnerabilities in Android apps. It uses Soot for Java bytecode analysis and transforms APK bytecode to Jimple (3-address code) for interprocedural analysis.

## Build Commands

```bash
# Build the project (skip tests)
./gradlew build -x test

# Build produces: build/libs/AppShark-0.1.2-all.jar (shadow JAR with all dependencies)

# Run tests
./gradlew test

# Run a single test class
./gradlew test --tests "net.bytedance.security.app.rules.RulesTest"

# Run a specific test method
./gradlew test --tests "net.bytedance.security.app.util.ProfilerTest.testFormatTime"
```

## Running AppShark

```bash
java -jar build/libs/AppShark-0.1.2-all.jar config/config.json5
```

Configuration example (`config/config.json5`):
```json
{
  "apkPath": "/path/to/app.apk",
  "out": "out",
  "rules": "unZipSlip.json",
  "rulePath": "config/rules",
  "logLevel": 0
}
```

## Architecture

### Core Analysis Pipeline (`src/main/kotlin/net/bytedance/security/app/`)

1. **StaticAnalyzeMain.kt** - Entry point that orchestrates the full analysis workflow:
   - `initSoot()` - Initializes Soot framework, loads APK and Android SDK
   - `parseApk()` - Decompiles APK using jadx
   - `loadRules()` - Loads vulnerability detection rules
   - `createContext()` - Builds call graph and preprocesses code
   - `solve()` - Runs taint flow analysis

2. **AnalyzeStepByStep.kt** - Step-by-step analysis coordinator

3. **PreAnalyzeContext.kt** - Holds preprocessed code, call graph, and analysis state

### Taint Analysis (`taintflow/`)

- **TwoStagePointerAnalyze.kt** - Two-stage pointer analysis: 1) Compute pointer information, 2) Find taint paths
- **TaintAnalyzer.kt** - Represents a rule's source/sink pair with context
- **StmtTransfer.kt** - Statement-level taint propagation rules

### Pointer Analysis (`pointer/`)

- **PLPointer.kt** - Base class for pointer representations
- **PLLocalPointer.kt** - Points to local variables
- **PLObject.kt** - Points to object fields
- **PointerFactory.kt** - Creates pointer instances

### Rule System (`rules/`)

Rules define vulnerability detection patterns with four analysis modes:
- **DirectMode** - Fixed entry point, traces forward N layers
- **SliceMode** - Dynamic entry from source/sink intersection (default)
- **ConstStringMode** - Constant string as source entry
- **ConstNumberMode** - Constant number as source entry

Rule structure: source → [sanitizers] → sink

### Preprocessing (`preprocess/`)

- **AnalyzePreProcessor.kt** - Main preprocessing coordinator
- **CallGraph.kt** - Builds heirarchical call graph
- **MethodSSAVisitor.kt** - Converts to SSA form
- **ClassVisitor.kt** - Extracts class hierarchy

### Result Output (`result/`)

- **OutputSecResults.kt** - Generates `results.json` and HTML reports

### Android-Specific (`android/`)

- **AndroidUtils.kt** - APK parsing, lifecycle extraction, component discovery
- **LifecycleConst.kt** - Android lifecycle method constants

### Key Utilities (`util/`)

- **TaskQueue.kt** - Parallel task execution with thread pool
- **Profiler.kt** - Performance timing and memory profiling
- **JavaAST.kt** - Java statement patterns

## UI Components (`ui/`)

- **client/** - Vue.js 2.x frontend (Element UI, ECharts)
- **server/** - Node.js backend serving results

## Rule Configuration

Rules are JSON files in `config/rules/`. Example structure:
```json
{
  "ruleName": {
    "SliceMode": true,
    "traceDepth": 8,
    "source": {
      "Return": ["<java.util.zip.ZipEntry: java.lang.String getName()>"]
    },
    "sanitizer": {
      "ruleName": {
        "<java.io.File: java.lang.String getCanonicalPath()>": {
          "TaintCheck": ["@this"]
        }
      }
    },
    "sink": {
      "<java.io.FileOutputStream: * <init>(*)>": {
        "TaintCheck": ["p*"]
      }
    }
  }
}
```

## Code Conventions

- Follow [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Branch naming: `optimize/feature/bugfix/doc/ci/test/refactor` prefix required
- Stable code in `master`, development in `develop`

## Dependencies

- **JDK 11** - Required (does not work with JDK 8 or 16)
- Kotlin 1.6.21
- Soot-infoflow-android 2.10.4
- kotlinx-coroutines for async processing