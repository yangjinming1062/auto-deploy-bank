# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run build      # Build with Rollup (outputs to build/)
npm test           # Run Jest tests
npm run lint       # Run ESLint
npm run lint:fix   # Run ESLint with auto-fix
npm run coverage   # Run tests with coverage report
```

## Project Overview

ASN1js is a pure JavaScript/TypeScript library implementing ASN.1 (Abstract Syntax Notation One) BER/DER encoding and decoding. ASN.1 is the basis of all X.509 related data structures and numerous web protocols.

## Architecture

### Core Encoding/Decoding Flow

The library uses a three-block structure for all ASN.1 types:

1. **idBlock** (`LocalIdentificationBlock`) - Tag identification (class, tag number, constructed flag)
2. **lenBlock** (`LocalLengthBlock`) - Length encoding
3. **valueBlock** - Actual value content

All ASN.1 types extend `BaseBlock<T>` which provides `fromBER()` for decoding and `toBER()` for encoding.

### Type System

- **TypeStore** (`src/TypeStore.ts`) - Central registry for all ASN.1 types. Uses static blocks to auto-register types on class definition.
- **src/index.ts** exports all public types from the typeStore

### Key Internal Modules

- **LocalBaseBlock** (`src/internals/LocalBaseBlock.ts`) - Base class for all blocks with error/warning handling
- **LocalIdentificationBlock** (`src/internals/LocalIdentificationBlock.ts`) - Parses/encode tag bytes
- **LocalLengthBlock** (`src/internals/LocalLengthBlock.ts`) - Parses/encode length bytes (supports definite and indefinite forms)
- **LocalIntegerValueBlock** (`src/internals/LocalIntegerValueBlock.ts`) - BigInt-based integer handling

### Schema Validation

- **compareSchema()** (`src/schema.ts`) - Validates decoded ASN.1 against a schema
- **verifySchema()** - Combines decoding + schema validation in one step
- Special schema types: `Any`, `Choice`, `Repeated`, `Primitive`, `Constructed`

### Encoding Standards

- **BER** (Basic Encoding Rules) - Primary format, supports indefinite length forms
- **DER** (Distinguished Encoding Rules) - Subset of BER for PKI; use `convertToDER()` method

## Coding Conventions

- Double quotes for strings
- 120 character line length
- ESLint config at `eslint.config.mjs`
- TypeScript strict mode enabled