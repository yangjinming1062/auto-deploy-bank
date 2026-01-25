# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TensorFlow.js is a hardware-accelerated JavaScript library for training and deploying machine learning models in browsers and Node.js. This is a monorepo containing multiple NPM packages.

## Commands

```bash
# Lint the entire codebase
yarn lint

# Run all tests (Bazel)
yarn test

# Run CPU tests only
yarn test-cpu

# Run GPU tests only
yarn test-gpu

# Build all packages
yarn build

# Build a specific package (e.g., tfjs-core)
cd tfjs-core && yarn build

# Package a specific package for NPM
cd <package> && yarn build-npm
```

### Package-Level Testing

```bash
# Run all tests for a package
cd <package> && yarn test

# Development mode with auto-rebuild (ibazel)
cd <package> && yarn test-dev

# Debug mode (keeps Karma server running)
cd <package> && yarn test-debug

# Run subset of tests with grep filter
yarn test --//:grep=multinomial

# Run tests with visible browser window
yarn test --//:headless=false
```

### Release Commands

```bash
yarn release              # Create a new release
yarn publish-npm          # Publish to NPM
yarn publish-pypi         # Publish Python bindings
yarn release-notes        # Generate release notes
```

## Architecture

This is a monorepo with modular package structure:

### Core API Packages
- **tfjs-core**: Low-level API for tensors, operations, engine, gradients
- **tfjs-layers**: High-level Keras-like API for model building
- **tfjs-data**: Data pipeline API (analogous to tf.data)
- **tfjs-converter**: Import TensorFlow SavedModel and Keras models
- **tfjs-vis**: In-browser visualization library
- **tfjs-automl**: AutoML Edge model support

### Backend/Platform Packages
- **tfjs-backend-cpu**: Pure JavaScript CPU backend
- **tfjs-backend-webgl**: WebGL-accelerated backend
- **tfjs-backend-wasm**: WebAssembly backend with XNNPACK
- **tfjs-backend-webgpu**: WebGPU backend (modern browsers)
- **tfjs-node**: Node.js with TensorFlow C++ bindings
- **tfjs-react-native**: React Native platform

### Backend Abstraction Pattern

Each backend follows this structure:
```
src/kernels/              # Operation implementations
src/register_all_kernels.ts  # Kernel registration
src/backend_*.ts          # Backend-specific implementation
src/index.ts              # Public API exports
```

Kernels are registered via a backend registry system, allowing runtime backend switching.

## Build System

- **Bazel**: Primary build system (bazelisk, rules_typescript, rules_cc)
- **TypeScript**: Compiles to JavaScript (5.0.4)
- **Karma**: Browser testing with headless Chrome
- **Jasmine**: Test framework
- **Rollup**: Final bundling for browser distribution

## Commit Style Guide

When merging commits, use tags for automatic release notes:

- `FEATURE` - New functionality/API
- `BREAKING` - API breakage
- `BUG` - Bug fixes
- `PERF` - Performance improvements
- `DEV` - Development flow changes
- `DOC` - Documentation changes
- `SECURITY` - Security changes

Example commit:
```
FEATURE

Add tf.toPixels - inverse of tf.fromPixels
```

## Development Notes

### Windows Development
- Requires WSL2 (Debian recommended)
- Chrome must be installed on Windows host
- Set `CHROME_BIN` environment variable to chrome.exe path
- Use `.bazelrc.user` for WSL-specific configuration

### Editor Configuration
- VSCode recommended
- Install TSLint VSCode extension
- Install clang-format 1.2.2+ with Clang-Format VSCode extension

### TypeScript Path Aliases
The root tsconfig.json defines path aliases for cross-package imports (e.g., `@tensorflow/tfjs-core`).