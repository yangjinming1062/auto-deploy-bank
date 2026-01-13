# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Victory is an ecosystem of composable React components for building interactive data visualizations. This is a **monorepo** containing 32+ packages managed with pnpm workspaces and built with Wireit for fast, cacheable builds.

**Owner**: Formidable (NearForm Commerce)
**Repository**: https://github.com/FormidableLabs/victory
**Documentation**: https://commerce.nearform.com/open-source/victory

## Development Requirements

- **Node.js**: >= 18.0.0
- **Package Manager**: pnpm (v9.13.0) - use `corepack enable` and `pnpm install`
- **Must use pnpm, not npm or yarn** for all operations in this monorepo

## Common Commands

### Setup
```bash
pnpm install
```

### Development Workflow
```bash
# Run all checks (format, lint, jest, types) - your main workflow command
pnpm run check
pnpm run check --watch  # watch mode for faster iteration

# Build all packages
pnpm run build
pnpm run build --watch  # watch mode

# Only run tests
pnpm run jest
pnpm run jest --watch

# Format and linting
pnpm run format
pnpm run format:fix  # auto-fix formatting
pnpm run lint
pnpm run lint:fix  # auto-fix lint issues

# Type checking
pnpm run types:check
```

### Development Servers
```bash
# Storybook (component development) - recommended
pnpm storybook:dev

# Start storybook standalone
pnpm storybook:start

# Documentation website (local development)
pnpm start:docs
```

### Cache Management
```bash
# Clean all caches (wireit, eslint, modules)
pnpm run clean:cache

# Clean only specific caches
pnpm run clean:cache:lint      # eslint cache
pnpm run clean:cache:wireit    # wireit cache
pnpm run clean:cache:modules   # node_modules cache
```

### Working on Individual Packages
You can run commands from the root or from within a package directory:
```bash
cd packages/victory-core
pnpm run check --watch  # only checks victory-core
```

### Releases & Changesets
```bash
# Add a changeset (creates version change file in .changesets/)
pnpm run changeset

# Build before publishing
pnpm run build
```

## Architecture

### Monorepo Structure
```
/                      # Root workspace
├── packages/          # 32+ npm packages
│   ├── victory            # Main package
│   ├── victory-core       # Base components (most important)
│   ├── victory-vendor     # D3 dependencies
│   ├── victory-native     # React Native support
│   ├── victory-chart      # Chart container
│   ├── victory-*          # Individual chart types
│   └── victory-*container # Interaction containers
├── stories/           # Storybook stories
├── demo/              # Demo apps (deprecated)
├── website/           # Docusaurus documentation site
└── test/              # Test configuration
```

### Key Packages
- **victory-core** (`packages/victory-core/`): The foundation - contains base components, utilities, and types. Most changes start here.
- **victory** (`packages/victory/`): Main package that re-exports components
- **victory-vendor** (`packages/victory-vendor/`): Wraps d3 and other dependencies
- **victory-native** (`packages/victory-native/`): React Native implementation

Each package builds to:
- `lib/` - CommonJS
- `es/` - ES modules
- `dist/` - UMD

### Package Build System
This project uses **Wireit** (not plain npm scripts) for:
- Task caching and dependency graph management
- Parallel execution with `WIREIT_PARALLEL=<NUM>`
- Smart rebuilds based on file changes

Wireit scripts are defined in `package.json` under the `"wireit"` key. See CONTRIBUTING.md for detailed Wireit usage patterns.

### Testing Stack
- **Jest** for unit tests (jsdom environment)
- **@testing-library/react** for component testing
- **Storybook** + **Chromatic** for visual regression testing
- Tests use pattern: `**/src/**/*.test.{js,ts,tsx}`

### Code Quality
- **TypeScript** v5.7.2 (strict mode)
- **ESLint** v9 (flat config in `eslint.config.mjs`)
- **Prettier** v3 for formatting
- All quality checks run via `pnpm run check`

## Development Tips

### Performance Optimization
- Use `WIREIT_PARALLEL=4 pnpm run check` to limit CPU usage during heavy builds
- Use `--watch` flags for faster iteration: `pnpm run check --watch`
- For package-specific work, cd into that package directory

### Cache Issues
If experiencing strange errors:
1. Try `pnpm run clean:cache:lint` for ESLint cache issues
2. Use `pnpm run clean:cache` for complete cache wipe
3. Restart TypeScript Language Server in your IDE

### Storybook Development
```bash
# Watch mode with auto-rebuild
pnpm storybook:dev

# Storybook runs on http://localhost:6006
```

### Working with Dependencies
Since this is a monorepo with pnpm workspaces:
- All `victory-*` packages are automatically linked after `pnpm install`
- Run `pnpm run sync` to sync package.json scripts across packages
- Never use `npm` or `yarn` - only `pnpm`

## Important Notes

1. **Wireit caching**: Tasks are cached based on input files. Successful tasks won't re-run unless inputs change
2. **IDE TypeScript issues**: When built types change (e.g., victory-core), restart TypeScript service instead of IDE
3. **Demo app deprecated**: Use Storybook for development, not the demo app
4. **Visual tests**: New features should include stories in the `stories/` directory
5. **Build order matters**: victory-core → victory-vendor → other packages (Wireit handles this)

## Additional Resources

- **Contributing Guide**: `/CONTRIBUTING.md` - Contains detailed development workflow
- **Main README**: `/README.md` - Project overview and getting started
- **Full Documentation**: https://commerce.nearform.com/open-source/victory
- **Storybook**: Run `pnpm storybook:dev` and visit http://localhost:6006
- **Wireit**: https://github.com/google/wireit - Build tool documentation
- **Changesets**: https://github.com/changesets/changesets - Version management