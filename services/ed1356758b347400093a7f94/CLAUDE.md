# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`unist-util-visit` is a unified/syntax-tree utility for walking abstract syntax trees (AST). It provides depth-first tree traversal (preorder NLR, or reverse preorder NRL) with filtering capabilities. Part of the unist ecosystem used by remark, rehype, and other processor tools.

## Commands

```bash
# Full build, format, and test with coverage
npm test

# Build only (TypeScript + tsd + type coverage)
npm run build

# Run tests without coverage
npm run test-api

# Format code (remark, prettier, xo with --fix)
npm run format

# Type coverage check
npx type-coverage --detail
```

## Architecture

- **`index.js`** - Public API re-exports from `lib/`
- **`lib/index.js`** - Main implementation. The `visit()` function wraps `unist-util-visit-parents` and provides:
  - Visitor function overloads (with/without test filter)
  - Complex TypeScript type inference for visitor callbacks based on tree and test types
  - Traversal control via `CONTINUE`, `EXIT`, `SKIP` return values

### Core Concepts

- **Tree**: The AST node to traverse (must have `children` array for non-leaf nodes)
- **Test**: Optional filter (string type, array of types, or `unist-util-is` compatible function) to only visit matching nodes
- **Visitor**: Callback receiving `(node, index, parent)` - returns control flow directive
- **Reverse**: Optional boolean to traverse in reverse preorder (NRL)

### Key Exports

`CONTINUE` (`true`) - Continue traversal normally
`EXIT` (`false`) - Stop traversal immediately
`SKIP` (`'skip'`) - Skip node's children, continue with siblings

## Type System

The package uses extensive TypeScript generics to infer:
- Node types matching the test filter
- Parent types based on the child node type
- Visitor callback parameters are strongly typed based on tree structure

Type tests in `index.test-d.ts` verify type correctness using `tsd`.

## Testing

Uses Node.js native `node:test` runner. Test file uses `assert` for assertions and `mdast-util-from-markdown` to generate test trees.