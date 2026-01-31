# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VChart is a cross-platform charting library that wraps [VGrammar](https://github.com/VisActor/VGrammar) for charting logic and [VRender](https://github.com/VisActor/VRender) for rendering. It's a Rush.js monorepo with multiple packages for different frameworks (React, Taro, Lark, WeChat mini-program, OpenInula).

## Development Commands

### Rush Commands (Monorepo Level)
```bash
# Install dependencies
rush update

# Build all packages
rush build

# Run all tests
rush test

# Run eslint on all packages
rush eslint

# Run prettier on all packages
rush prettier

# Rebuild everything from scratch
rush rebuild

# Start vchart dev server
rush start

# Start react-vchart dev server
rush react

# Start openinula-vchart dev server
rush openinula

# Start documentation site
rush docs

# Generate changelog
rush change-all -t patch -m "fix: description"
```

### Package-Specific Commands (in packages/vchart)
```bash
npm run build          # Full build with schema and types
npm run test           # Run Jest tests
npm run test-watch     # Watch mode for tests
npm run start          # Vite dev server for browser testing
npm run lint           # Run eslint
npm run prettier       # Format code with Prettier
npm run compile        # Type-check without emitting
```

## Architecture

### Core Package Structure (packages/vchart/src/)
```
src/
├── chart/          # Chart type definitions (bar, line, pie, etc.)
│   ├── base/       # BaseChart class
│   ├── cartesian/  # Cartesian coordinate charts
│   └── polar/      # Polar coordinate charts
├── series/         # Data series implementations (line, bar, pie, etc.)
├── component/      # UI components
│   ├── axis/       # X/Y axes (cartesian & polar)
│   ├── legend/     # Discrete & continuous legends
│   ├── tooltip/    # Tooltip handler
│   ├── label/      # Data labels
│   └── marker/     # MarkLine, MarkArea, MarkPoint
├── compile/        # Spec compilation logic
├── mark/           # Graphic mark definitions
├── data/           # Data processing & transforms
├── event/          # Event system
├── theme/          # Theme definitions
├── interaction/    # User interaction handlers
├── layout/         # Layout algorithms
├── plugin/         # Chart plugins
├── region/         # Region management for multi-region charts
├── scale/          # Scale definitions
├── typings/        # TypeScript type definitions
└── util/           # Utility functions
```

### Key Entry Points
- `src/index.ts` - Main export (re-exports from vchart-all)
- `src/vchart-all.ts` - Full VChart with all chart types registered
- `src/vchart-simple.ts` - Subset with common charts only
- `src/vchart-pie.ts` - Pie chart only
- `src/core/vchart.ts` - Main VChart class

### Chart Registration Pattern
Charts use a registration pattern where each chart type has:
1. A chart class extending `BaseChart`
2. A `registerChartXxx()` function
3. Type definitions for the spec

All charts must be registered via `VChart.useRegisters([...])` before use.

## Code Style

- **TypeScript**: 4.9.5
- **Single quotes**: Yes
- **Trailing commas**: None
- **Print width**: 120
- **Prettier/ESLint**: Enforced via lint-staged on commit

## Git Workflow

- **Branch naming**: `feat/xxx`, `fix/xxx`, `docs/xxx`
- **Base branch**: `develop`
- **Commit format**: [Conventional Commits](https://www.conventionalcommits.org/) - `<type>(scope): <description>`
  - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
  - Examples: `feat(bar): add bar label support`, `fix(tooltip): resolve tooltip positioning issue`

## Testing

- **Test runner**: Jest with jest-electron (headless browser)
- **Test location**: `__tests__/` directories
- **Test pattern**: `*.test.(ts|js)` files
- **Coverage**: Reports in `json-summary`, `lcov`, `text` formats

## Key Dependencies

- `@visactor/vrender-core` - Rendering engine
- `@visactor/vrender-components` - UI components
- `@visactor/vrender-kits` - Canvas/SVG adapters
- `@visactor/vutils` - Utilities
- `@visactor/vdataset` - Data processing
- `@visactor/vscale` - Scale functions
- `@visactor/vlayouts` - Layout algorithms

## Related Packages

- `@visactor/react-vchart` - React wrapper
- `@visactor/taro-vchart` - Taro framework wrapper
- `@visactor/openinula-vchart` - OpenInula wrapper
- `@visactor/lark-vchart` - Lark mini-app wrapper
- `@visactor/wx-vchart` - WeChat mini-program wrapper
- `@visactor/vchart-schema` - JSON schema for specs
- `@visactor/vchart-types` - TypeScript type definitions

## Additional Resources

- [Contributing Guide](./CONTRIBUTING.md)
- [README](./README.md)
- [Documentation](https://www.visactor.io/vchart)