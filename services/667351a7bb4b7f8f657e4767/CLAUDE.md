# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a monorepo containing web worker modules for client-side image processing using TensorFlow.js and MediaPipe. Each worker module provides a specific ML/cv capability (body segmentation, face detection, etc.) that runs in a web worker to avoid blocking the UI thread.

## Repository Structure

- **`{NNN}_name-worker-js`** - Worker library packages (e.g., `001_bodypix-worker-js`, `019_mediapipe-mix2-worker-js`)
- **`{NNN}demo_name-worker-js-demo`** - React demo applications for each worker
- **`tfl{NNN}_name/`** - TFLite WebAssembly implementations (alternative to TFJS workers)
- **`lib{NNN}_name-js/`** - Shared library modules
- **`exp{NNN}_*/`** - Experimental implementations
- **`000_DemoBase`** - Shared React components and hooks for demos (VideoInputSelector, CommonSlider, etc.)
- **`000_WorkerBase`** - Base classes (`WorkerManagerBase`, `ImageProcessor`, `BlockingQueue`) used by all workers

## Common Commands

### Worker Library Development
```bash
cd <worker-dir>              # e.g., 001_bodypix-worker-js
npm run build                # Clean + webpack build
npm run webpack              # Just webpack build
```

### Demo Application Development
```bash
cd <demo-dir>                # e.g., 001demo_bodypix-worker-js-demo
npm install
npm run build                # Full production build
npm run watch                # Watch mode for development
npm run start                # Dev server with hot reload
npm run lint                 # Check code quality
npm run lint:fix             # Auto-fix linting issues
```

### TFLite WASM Projects
```bash
cd tfl001_google-meet-segmentation
npm run build                # Copy common/*.ts and run react-scripts build
npm run start                # Start dev server (react-scripts start)
npm run build_wasm           # Build TFLite WASM via Docker (requires bazel)
npm run build_wasm_simd      # Build with SIMD support
npm run build_wasm_all       # Build both standard and SIMD versions
```

### Publishing a Worker
```bash
cd 001_bodypix-worker-js
npm version patch|minor|major   # Update version
npm publish --access=public     # Publish to npm (@dannadori scope)
```

## Architecture

### Worker Pattern (all workers follow this)

Each worker module implements:
1. **`WorkerManager` class** - Extends `WorkerManagerBase`, handles worker thread communication, canvas resizing, and transferables
2. **`LocalWorker` class** - Implements `ImageProcessor`, runs ML inference on main thread (fallback for Safari)
3. **Worker entry point** - Loads model and processes messages via `WorkerDispatcher`

```typescript
// Typical worker structure
class LocalWorker implements ImageProcessor<Config, Params> {
  init(config: Config) { /* load model */ }
  predict(config: Config, params: Params, data: any) { /* run inference */ }
}

class XxxWorkerManager extends WorkerManagerBase<Config, Params> {
  init(config?: Config) { /* creates worker or uses local fallback */ }
  predict(params: Params, target: HTMLCanvasElement) { /* returns prediction */ }
}
```

### Key Base Classes (`000_WorkerBase`)

- **`WorkerManagerBase`** - Abstract base with worker communication, BlockingQueue for serialization, canvas manipulation
- **`ImageProcessor`** - Interface for model implementations
- **`WorkerDispatcher`** - Message dispatcher for worker thread

### Configuration Interface Pattern

All workers define consistent config/params interfaces:

```typescript
// In src/const.ts
export const WorkerCommand = { INITIALIZE: "initialize", PREDICT: "predict" } as const;
export type WorkerCommand = typeof WorkerCommand[keyof typeof WorkerCommand];

export const WorkerResponse = { INITIALIZED: "initialized", PREDICTED: "predicted" } as const;
export type WorkerResponse = typeof WorkerResponse[keyof typeof WorkerResponse];

export interface XxxConfig {
    browserType: BrowserTypes;
    model: ModelConfig;
    processOnLocal: boolean;
    useTFWasmBackend?: boolean;
}

export interface XxxOperationParams {
    type: XxxFunctionType;
    processWidth: number;
    processHeight: number;
    // ... operation-specific parameters
}
```

### Demo Pattern

React apps use:
- `@dannadori/demo-base` - Shared UI (CommonSlider, VideoInputSelector, Credit)
- `@dannadori/xxx-worker-js` - The worker library
- Worker managers are instantiated in components, initialized on mount, and predict() is called on video frames

## Dependencies

- **TensorFlow.js** (`@tensorflow/tfjs` + backend packages) - Core ML runtime
- **MediaPipe packages** (`@tensorflow-models/face-landmarks-detection`, `hand-pose-detection`, `pose-detection`) - Modern MediaPipe-based models
- **@tensorflow-models/{model}** - Legacy TFJS models (body-pix, handpose, posenet, facemesh)
- **React 18** - Demo UI only
- **Webpack 5** - Module bundler with worker-loader
- **TypeScript 4.6** - Type safety

## Model Types

1. **TensorFlow.js Legacy Models** - `@tensorflow-models/*` packages (body-pix, posenet, handpose, facemesh)
2. **MediaPipe Models** - `@tensorflow-models/face-landmarks-detection`, `hand-pose-detection`, `pose-detection`
3. **TFLite Models** - Custom TFLite models loaded via WASM (tfl001-009 projects), built with Bazel

## Webpack Configuration

- **Worker libraries** - Output as UMD module, use `worker-loader` for inline workers
- **Demo apps** - Output to `dist/`, include HTML plugin for dev server, use Babel for TS/JSX

## Browser Support

Workers support configurable execution:
- `processOnLocal: true` - Run on main thread (slower but works everywhere)
- `useWorkerForSafari: false` - Safari has web worker restrictions
- Default is worker mode on supported browsers