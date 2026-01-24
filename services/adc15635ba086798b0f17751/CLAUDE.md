# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UpscalerJS is an image super-resolution library that enhances images using TensorFlow.js. It supports browser, Node.js (CPU/GPU), and Web Worker environments through a unified API. The project is a pnpm monorepo with multiple packages for the core library, models, and internal tooling.

## Common Commands

```bash
# Install dependencies (requires pnpm)
pnpm install

# Build the core package
pnpm --filter upscaler build

# Build all models
pnpm build:models

# Build everything
pnpm build

# Lint all packages
pnpm lint

# Run unit tests (browser + node)
pnpm --filter upscaler test

# Run specific test suites
pnpm test:unit:browser:playwright     # Playwright browser tests
pnpm test:unit:browser:vite           # Vite browser tests
pnpm test:unit:node                   # Node.js tests
pnpm test:integration:clientside      # Browser integration tests (requires build first)
pnpm test:integration:serverside      # Node.js integration tests (requires build first)
pnpm test:integration:memory-leaks    # Memory leak tests

# Start development servers
pnpm dev:browser                      # Browser development
pnpm dev:node                         # Node.js development

# Update TensorFlow.js dependencies
pnpm update:tfjs

# Update all npm dependencies
pnpm update:npm:dependencies

# Build documentation
pnpm docs:build
pnpm docs:start                       # Live reload docs dev server
```

## Architecture

### Monorepo Structure

- **packages/upscaler** - Main library with platform-specific entry points (`./node`, `./node-gpu`, `.`)
- **packages/shared** - Shared utilities and model definitions (ESRGAN, MAXIM implementations)
- **packages/upscalerjs-models** - Model package utilities
- **packages/upscalerjs-wrapper** - Wrapper utilities
- **models/** - Individual model packages (ESRGAN variants, MAXIM variants, pixel-upsampler)
- **internals/** - Build tools, test runners, bundlers, and scripts
- **test/** - Integration tests with vitest configuration
- **examples/** - 22 runnable example applications demonstrating various use cases

### Core Library Design

The main `Upscaler` class is created via a factory function `getUpscaler()` defined in `packages/upscalerjs/src/shared/upscaler.ts`. This factory is called with platform-specific implementations from:

- `packages/upscalerjs/src/browser/index.ts` - Browser entry point (uses `@tensorflow/tfjs`)
- `packages/upscalerjs/src/node/index.ts` - Node.js CPU entry point (uses `@tensorflow/tfjs-node`)
- `packages/upscalerjs/src/node-gpu/index.ts` - Node.js GPU entry point (uses `@tensorflow/tfjs-node-gpu`)

### Model Architecture

Models follow the `ModelDefinition` interface (defined in `packages/shared/src/types.ts`) with:
- `path` - Path to model.json file
- `scale` - Upscaling factor (2x, 3x, 4x, 8x)
- `modelType` - 'graph' or 'layers' (TensorFlow.js model type)
- `preprocess/postprocess` - Optional pixel range transformations
- `inputRange`/`outputRange` - Normalization ranges (defaults to [0, 255])
- `setup`/`teardown` - Lifecycle hooks for custom layer registration
- `meta` - Model metadata (architecture, patchSize, size, etc.)

Pre-built models include:
- ESRGAN variants (slim, medium, thick, legacy)
- MAXIM variants (denoising, deblurring, dehazing, deraining, enhancement, retouching)
- Pixel-upsampler (for simple bilinear upscaling)

### Build Outputs

The library produces multiple bundle formats:
- **Browser ESM**: For modern bundlers (Vite, Webpack 5+)
- **Browser UMD**: For direct browser `<script>` inclusion
- **Node.js CJS**: For Node.js environments (CPU and GPU variants)
- **Bundled examples**: esbuild, webpack outputs for compatibility testing

### Testing Strategy

Tests use multiple frameworks for different environments:
- **Playwright**: For real browser testing in headless mode
- **Vitest**: For fast unit and integration tests
- **Jest**: For legacy unit tests with custom matchers (e.g., `toMatchImage`)

Integration tests verify:
- Different bundler outputs (UMD, Webpack, esbuild)
- Server-side vs client-side execution
- Model-specific functionality
- Memory leak detection

## Key Files

- Root `package.json` - Wireit configuration for monorepo-wide builds
- `packages/upscalerjs/package.json` - Core library wireit build configuration
- `packages/shared/src/types.ts` - Model definition TypeScript interfaces
- `packages/shared/src/esrgan/esrgan.ts` - ESRGAN model factory
- `packages/shared/src/maxim/maxim.ts` - MAXIM model factory