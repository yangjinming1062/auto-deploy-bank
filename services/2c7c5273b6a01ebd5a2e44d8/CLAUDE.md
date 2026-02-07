# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pyret is a self-hosted programming language with a compiler written in Pyret itself. The compiler is built using a multi-phase bootstrapping process. Most development work uses Phase A, while Phase B and C are used for verifying compiler correctness.

## Build Commands

```bash
npm install          # Install dependencies (runs make phaseA-deps)
make                 # Build the Pyret compiler (Phase A)
make test            # Run all tests (pyret-test, type-check-test, pyret-io-test)
make test-all        # Alias for make test
make parse-test      # Run parser tests only
make phaseB          # Build Phase B compiler (fully bootstrapped)
make phaseC          # Build Phase C compiler (verification phase)
make new-bootstrap   # Build phaseB/phaseC, verify with diff, update phase0
make clean           # Remove all build artifacts
make test-clean      # Remove compiled test files
```

To run a single test file:
```bash
./src/scripts/phaseA <path-to-pyret-program> [args...]
# Or compile and run standalone:
node build/phaseA/pyret.jarr --build-runnable <file.arr> --outfile <out.jarr>
node <out.jarr>
```

## Architecture

### Multi-Phase Bootstrapping

Pyret uses four distinct phases for building:

- **Phase 0** (`build/phase0/pyret.jarr`): The committed standalone compiler blob. Updated rarely for major features.
- **Phase A** (`build/phaseA/pyret.jarr`): Development snapshot built from Phase 0. Most development/testing uses this.
- **Phase B** (`build/phaseB/pyret.jarr`): Fully bootstrapped compiler built from Phase A.
- **Phase C** (`build/phaseC/pyret.jarr`): Second bootstrap from Phase B for verification. Phase B and C outputs must be identical.

To verify compiler correctness before committing Phase 0 updates:
```bash
make phaseB phaseC
diff build/phaseB/pyret.jarr build/phaseC/pyret.jarr  # Should be empty
make new-bootstrap
```

### Source Directory Structure

- `src/arr/compiler/`: The Pyret compiler (written in Pyret). Key files include:
  - `pyret.arr`: Main compiler entry point
  - `compile-lib.arr`, `compile-structs.arr`: Compiler core
  - `desugar.arr`, `well-formed.arr`: Parsing/desugaring phases
  - `type-check.arr`, `type-structs.arr`, `type-defaults.arr`: Type checker
  - `resolve-scope.arr`: Scope resolution
  - `anf.arr`, `anf-loop-compiler.arr`: ANF transformation
  - `js-of-pyret.arr`, `js-ast.arr`: JavaScript code generation

- `src/arr/trove/`: Built-in Pyret standard library modules

- `src/js/base/`: JavaScript base utilities and parser grammar/tokenizer:
  - `*-grammar.bnf`: Parser grammar files
  - `*-tokenizer.js`: Tokenizer implementations

- `src/js/trove/`: Built-in JavaScript runtime functions

- `lib/jglr/`: JavaScript GLR parser framework

- `tests/`: Test suites:
  - `tests/pyret/`: Pyret language tests
  - `tests/type-check/`: Type checker tests (good/, bad/, should/, should-not/)
  - `tests/parse/`: Parser tests
  - `tests/io-tests/`: I/O tests (Jest-based)
  - `tests/jsnums-test/`: Number library tests

### Compilation Pipeline

Pyret source (.arr) → Parsing → Desugaring → Type Checking → ANF → JavaScript Code Generation → JavaScript (.jarr)

## Running Tests

The test suite runs in three parts:

1. **Pyret tests** (`make pyret-test`): Runs `tests/pyret/main2.jarr`
2. **Type check tests** (`make type-check-test`): Validates type checker with good/bad/should files
3. **IO tests** (`make pyret-io-test`): Jest-based integration tests

All three run with `make test` or `make test-all`.

To test against Phase B or C instead of Phase A:
```bash
make test P=B    # Test with Phase B
make test P=C    # Test with Phase C
```

## Key Configuration Files

- `Makefile`: Build orchestration, test commands
- `package.json`: Node dependencies and npm scripts
- `src/scripts/standalone-config*.json`: Compiler configuration for each phase