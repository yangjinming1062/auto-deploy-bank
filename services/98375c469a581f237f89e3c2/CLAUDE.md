# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the TensorFlow.js models repository - a collection of pre-trained ML models ported to TensorFlow.js. Each model is published as an independent NPM package.

**Model categories:**
- **Images**: MobileNet, Hand Pose Detection, Pose Detection, Coco SSD, DeepLab v3, Face Landmark Detection, Face Detection
- **Audio**: Speech Commands
- **Text**: Universal Sentence Encoder, Text Toxicity, GPT-2, Question and Answer
- **Depth Estimation**: Portrait Depth
- **General Utilities**: KNN Classifier

## Common Commands

Run from the root directory or within a specific model package.

```bash
# Build a package (TypeScript compilation + Rollup bundling)
yarn build

# Lint with tslint
yarn lint

# Run tests (Karma for browser tests)
yarn test

# Run Node.js tests only
yarn test-node

# Build and bundle for NPM publication
yarn build-npm

# Build and publish locally via yalc (useful for testing against tfjs)
yarn publish-local

# Run Rollup bundling only (after TypeScript compilation)
yarn bundle

# Run all tests across all packages (root-level)
yarn presubmit
```

## Architecture

### Package Structure

Each model package follows a consistent pattern:
- `src/` - TypeScript source code
- `src/index.ts` - Main entry point exporting public API
- `run_tests.ts` - Test runner configuration
- `rollup.config.mjs` - Bundle configuration (UMD, minified UMD, ESM)
- `tsconfig.json` - TypeScript configuration
- `tsconfig.test.json` - Test-specific TypeScript configuration
- `tslint.json` - Linting rules

### Shared Utilities

The `shared/` directory at the root contains cross-package utilities:
- `shared/calculators/` - Reusable computational components (tensor transformations, pose utilities, rendering)
- `shared/filters/` - Smoothing filters (OneEuroFilter, KeypointsVelocityFilter)
- `shared/test_util.ts` - Shared test helpers (image/video loading, IOU calculation)

### Model Implementation Patterns

Many models support multiple backends (e.g., `pose-detection/src/blazepose_mediapipe/` and `src/blazepose_tfjs/`). When modifying these:
- Configuration types are typically in `types.ts` files
- Model-specific logic is isolated in dedicated subdirectories
- The main `createDetector`/`createEstimator` factory function dispatches to the appropriate backend

### Build Outputs

Each package produces:
- `dist/index.js` - CommonJS entry
- `dist/{package}.esm.js` - ES module bundle
- `dist/{package}.min.js` - Minified UMD bundle (for CDN usage)
- `dist/index.d.ts` - TypeScript declarations

## Dependency Management

TensorFlow.js packages follow strict version rules:
- `peerDependencies` must use `^` version ranges (e.g., `"^4.10.0"`)
- `devDependencies` must satisfy corresponding `peerDependencies`
- The `yarn presubmit` script validates these constraints across all packages

Common peer dependencies:
- `@tensorflow/tfjs-core`
- `@tensorflow/tfjs-converter`
- `@tensorflow/tfjs-backend-webgl`
- `@mediapipe/` packages (for MediaPipe-based models)

## Testing

- Tests use Jasmine framework with `*_test.ts` naming convention
- Browser tests run via Karma configuration (`karma.conf.js`)
- Test data is served from `base/test_data` via Karma server
- Node.js tests use `ts-node` with `NODE_PRESERVE_SYMLINKS=1`