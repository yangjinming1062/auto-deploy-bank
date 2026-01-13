# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Danfo.js** is a JavaScript/TypeScript data analysis toolkit heavily inspired by Python's Pandas library. It provides fast, flexible, and expressive data structures for working with structured/labeled data in both Node.js and browser environments.

This is a **Yarn Workspace monorepo** with three main packages:
- **danfojs-base**: Core shared functionality
- **danfojs-node**: Node.js-specific implementation
- **danfojs-browser**: Browser-optimized build

## Common Commands

### Installation
```bash
yarn install
```

### Building
```bash
yarn build                    # Build all packages
yarn build:browser            # Build only browser version
yarn build:node               # Build only Node.js version
```

### Development Mode (Watch)
```bash
# In individual packages
cd src/danfojs-node && yarn dev
cd src/danfojs-browser && yarn dev
```

### Testing
```bash
yarn test                     # Run all tests (browser + node)
yarn test:node                # Run only Node.js tests
yarn test:browser             # Run only browser tests

# Run single test file (in danfojs-node)
yarn test tests/core/frame.test.js

# Run tests matching pattern
yarn test -g "DataFrame.add"

# Watch mode
yarn test --watch
```

### Linting
```bash
# Lint all packages
yarn lint

# Or in individual packages
cd src/danfojs-node && yarn lint
cd src/danfojs-browser && yarn lint
```

### Coverage
```bash
cd src/danfojs-node && yarn coverage
cd src/danfojs-browser && yarn coveralls
```

## Code Architecture

### Monorepo Structure

```
src/
├── danfojs-base/          # Shared core - add new features here
│   ├── core/              # DataFrame, Series, indexing, math ops
│   ├── transformers/      # Encoders, scalers, merge, concat
│   ├── io/                # Input/output (node & browser)
│   ├── plotting/          # Plotly.js integration
│   ├── shared/            # Shared utilities
│   └── aggregators/       # GroupBy operations
├── danfojs-node/          # Node.js specific
│   ├── src/core/          # Node-specific extensions
│   ├── src/streams/       # Streaming operations
│   ├── test/              # Test suite
│   └── scripts/           # Build scripts
└── danfojs-browser/       # Browser specific
    ├── src/core/          # Browser optimizations
    ├── tests/             # Browser tests
    └── scripts/           # Build scripts
```

### Key Entry Points
- **danfojs-node**: `src/danfojs-node/src/index.ts` → `dist/danfojs-node/src/index.js`
- **danfojs-browser**: `src/danfojs-browser/src/index.ts` → `lib/bundle.esm.js` (ESM) & `lib/bundle.js` (ES5)

### Dependencies
- **Core**: TensorFlow.js, mathjs, papaparse, xlsx, stream-json
- **Browser**: @tensorflow/tfjs, plotly.js-dist-min
- **Node.js**: @tensorflow/tfjs-node (native bindings for performance)

### Testing Framework
- **Node.js**: Mocha + Chai + ts-node + NYC
- **Browser**: Karma + Mocha + Chai + ChromeHeadless
- **Test files**: `.test.ts` extension, organized by module

## Development Guidelines

### Adding New Features
1. **Most features should be added to `danfojs-base`** for code reuse
2. Only add environment-specific code to `danfojs-node` or `danfojs-browser`
3. Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` new features
   - `fix:` bug fixes
   - `docs:` documentation
   - `test:` tests
   - `refactor:` refactoring

### Testing Requirements
- Write tests for all new functionality
- Place Node.js tests in `src/danfojs-node/test/`
- Place browser tests in `src/danfojs-browser/tests/`
- Test files use `.test.ts` extension

### Documentation Standards
- Use JSDoc comments for all public methods
- Include parameter descriptions
- Include return value documentation
- Include usage examples
- Reference: `CONTRIBUTING.md` for full guidelines

### Build Configuration
- **Node.js**: TypeScript → Babel → dist/
- **Browser**: TypeScript → Webpack (ES5) + esbuild (ESM)

## Key Documentation
- **README.md**: Main project overview and examples
- **CONTRIBUTING.md**: Development setup and guidelines
- **Official Docs**: https://danfo.jsdata.org
- **GitHub Discussions**: https://github.com/opensource9ja/danfojs/discussions

## API Reference
The library provides:
- **DataFrame**: 2D labeled data structure (similar to Pandas DataFrame)
- **Series**: 1D labeled array
- **IO Operations**: CSV, JSON, Excel loading
- **Transformers**: OneHotEncoder, LabelEncoder, StandardScaler, MinMaxScaler
- **Plotting**: Plotly.js integration for interactive visualizations
- **GroupBy**: Split-apply-combine operations
- **TensorFlow.js Integration**: Direct conversion to/from tensors

## CI/CD
- **GitHub Actions**: Runs on Node.js 18.x and 20.x
- **Test Suite**: Runs on every push/PR to master/dev
- **Coverage**: NYC + Coveralls integration

## Important Notes
- This project is inspired by Pandas and aims to provide a similar API for JavaScript
- Two distribution formats: ESM and ES5 (via webpack)
- TensorFlow.js integration provides high-performance tensor operations
- Missing data is represented as `NaN` (consistent with JavaScript numeric handling)