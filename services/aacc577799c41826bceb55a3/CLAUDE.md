# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **DefinitelyTyped** repository - a pnpm monorepo containing high-quality TypeScript type definitions for JavaScript libraries. All type definitions are published to npm under the `@types` scope.

## Architecture

- **Monorepo Structure**: pnpm workspace containing:
  - `types/` - All type definition packages (thousands of them)
  - `scripts/` - Repository management scripts
  - Root level configuration files

- **Package Structure**: Each type definition package contains:
  - `index.d.ts` - Type declarations for the package
  - `*-tests.ts` - Test files that validate the API (type-checked but not executed)
  - `tsconfig.json` - TypeScript configuration (must have strict settings)
  - `package.json` - Package metadata and dependencies
  - `.npmignore` - Controls which files are published (usually just declaration files)
  - `.eslintrc.json` - Rarely needed, only to disable specific lint rules

- **Scoped Packages**: Types for `@foo/bar` are in `types/foo__bar` (double underscore)

- **Versioned Packages**: For major version breaks, use subdirectories like `types/foo/v2/`

## Common Commands

### Testing and Linting
```bash
# Test a specific package
pnpm test <package-name>

# Test all packages (takes hours)
pnpm test-all

# Lint all types
pnpm lint

# Format code
pnpm format
```

### Package Management
```bash
# Install all dependencies (entire monorepo)
pnpm install

# Install only specific package and its dependencies
pnpm install -w --filter "{./types/foo}..."

# Clean node_modules (useful on Windows)
pnpm run clean-node-modules

# Remove packages that are no longer needed (when upstream bundles types)
pnpm run not-needed <typings-package-name> <as-of-version> [<library-name>]
```

### CI and Validation
- CI uses `dtslint-runner` to validate all packages
- Uses `dtslint` for type checking and linting
- Uses `@arethetypeswrong/cli` (attw) to check module format compatibility
- Failing `attw` checks are in `attw.json` (remove packages when fixed)

## Important Guidelines

### TypeScript Configuration
- **Never** use `esModuleInterop` or `allowSyntheticDefaultImports` in `tsconfig.json`
- Must have: `noImplicitAny`, `noImplicitThis`, `strictNullChecks`, `strictFunctionTypes` all set to `true`
- For async functions, add `"target": "es6"` to `tsconfig.json`

### Export Guidelines
- CJS exports (`module.exports = ...`) should use `export =`, not `export default`
- ESM exports (`export default ...`) should use `export default`
- Match the actual runtime behavior of the JavaScript package

### Test Files
- Must have `<package-name>-tests.ts` file
- Use `$ExpectType` to assert types
- Use `@ts-expect-error` to assert compile errors
- Test both global and module usage patterns when applicable

### Package.json Requirements
- Version format: `<major>.<minor>.9999` (e.g., `4.3.9999`)
- Add non-`@types` dependencies to allowed list (see DEFINITIONS-PARSER allowlist)
- Set `"type": "module"` if the implementation package uses it
- Include all dependencies including other `@types` packages

### Module Format Checking (attw)
- The `package.json` must have matching `type` and `exports` fields to the implementation
- Each `.js` file needs a corresponding `.d.ts` declaration file
- `.d.ts` files type `.js`, not `.mjs` or `.cjs` files
- Export formats must match: `export =` for CJS, `export default` for ESM default

## Repository Scripts

Located in `scripts/`:
- `not-needed.js` - Remove packages that are no longer needed
- `update-codeowners.js` - Sync package owners to CODEOWNERS file
- `clean-node-modules.js` - Clean node_modules on Windows
- `get-ci-matrix.js` - Generate CI test matrix

## Resources

- **README.md** - Comprehensive contribution guide
- **docs/admin.md** - On-call procedures for DT maintainers
- **dtslint** - https://github.com/microsoft/DefinitelyTyped-tools/tree/master/packages/dtslint
- **dts-gen** - Tool to generate new packages: `npx dts-gen --dt --name <pkg> --template module`

## CI/CD

- Azure Pipelines handles automated testing and publishing
- `dtslint-runner` validates all type packages
- Successful PRs are automatically published to npm as `@types/*` packages
- See README.md for current build status badges

## Support

- **Discord**: TypeScript Community Discord (channel: #definitely-typed)
- **Projects Board**: https://github.com/orgs/DefinitelyTyped/projects/1
- **Issues**: Use for bug reports and package requests