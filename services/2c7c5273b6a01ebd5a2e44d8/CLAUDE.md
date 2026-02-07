# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pyret is a self-hosted programming language focused on education, functional programming, and integrated testing. The compiler is written in Pyret itself, targeting JavaScript as the runtime.

## Build Commands

```bash
npm install                    # Install dependencies and build Phase A deps
make                           # Build Phase A compiler (development snapshot)
make phaseB                    # Build Phase B (fully-bootstrapped compiler)
make phaseC                    # Build Phase C (for verification)
make new-bootstrap             # Build phases B and C, verify they match, update Phase 0
make test-all                  # Run full test suite (alias: npm test)
make pyret-test                # Run Pyret language tests
make pyret-io-test             # Run Node.js IO tests (Jest)
make type-check-test           # Run type checking tests
make parse-test                # Run parser tests
make regression-test           # Run regression tests
make clean                     # Clean build artifacts
make test-clean                # Clean compiled test files
```

## Running Pyret Programs

```bash
# Run with development compiler (Phase A)
./src/scripts/phaseA <program.arr> [args...]

# Compile to standalone and run separately
node build/phaseA/pyret.jarr --build-runnable <program.arr> --outfile <output.jarr>
node <output.jarr>

# Run tests for a specific file (if it has check blocks)
./src/scripts/phaseA <test-file.arr>
```

## Architecture

### Multi-Phase Bootstrapping

Pyret uses a 4-phase build system to handle self-hosting:

1. **Phase 0** (`build/phase0/`): Canonical compiled compiler (committed to git). Used as the starting point for all builds.
2. **Phase A** (`build/phaseA/`): Built with Phase 0. Used for development and most testing.
3. **Phase B** (`build/phaseB/`): Built with Phase A. Fully-bootstrapped compiler reflecting current source.
4. **Phase C** (`build/phaseC/`): Built with Phase B. Must match Phase B to confirm bootstrapping is stable.

Run `diff build/phaseB/pyret.jarr build/phaseC/pyret.jarr` to verify the compiler has reached a fixed point before updating Phase 0.

### Compiler Passes

The compiler pipeline in `src/arr/compiler/compile-lib.arr` follows this sequence:
1. **Parsing**: Surface parse to AST (`parse-pyret`)
2. **Well-formedness checking** (`well-formed.arr`)
3. **Check block desugaring** (`desugar-check.arr`)
4. **Scope resolution** (`resolve-scope.arr`)
5. **Name resolution** (`resolve-scope.arr`)
6. **Desugaring** (`desugar.arr`)
7. **Type checking** (`type-check.arr`) - optional via `--type-check` flag
8. **Post-typecheck desugaring** (`desugar-post-tc.arr`)
9. **ANF conversion** and **JS code generation** (`anf-loop-compiler.arr`)

The `compile-module` function in `compile-lib.arr` is the core entry point.

### Key Source Directories

- `src/arr/compiler/`: Self-hosted compiler written in Pyret (main files: `compile-lib.arr`, `pyret.arr`)
- `src/arr/trove/`: Pyret standard library (built-in types and functions)
- `src/js/base/`: Core runtime (`runtime.js`), tokenizer, grammar, parser components
- `src/js/trove/`: Native JavaScript implementations of standard library modules
- `lib/jglr/`: RNG LR parser generator (`rnglr.js`, `jglr.js`)
- `tests/pyret/tests/`: Feature tests (`.arr` files with `check` blocks)
- `tests/type-check/`: Type checker tests organized by expectation (`good/`, `bad/`, `should/`, `should-not/`)
- `tests/pyret/regression/`: Regression tests
- `tests/io-tests/`: Jest-based Node.js IO tests

### Build Outputs

- `*.jarr`: Bundled Pyret archive files (compiled Pyret + runtime, run with `node file.jarr`)
- `build/phaseX/compiled/`: Intermediate compiled `.js` files for each phase
- `tests/pyret/*.jarr`: Compiled test bundles

### File Types

- `.arr` - Pyret source files
- `.jarr` - Bundled compiled output (executable with Node.js)
- `.bnf` - Parser grammar definition files

### Debugging Tips

- Use `make show-comp` to build a debugging utility for viewing compilation phases
- `./src/scripts/phaseA src/scripts/show-compilation.arr <file.arr>` - Show each compilation phase output