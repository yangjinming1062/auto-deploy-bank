# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Talisman is a JavaScript library for fuzzy matching, information retrieval, and natural language processing. It provides modular algorithms and functions for string metrics, clustering, phonetics, stemming, tokenization, and more.

## Common Commands

```bash
npm install          # Install dependencies
npm test             # Run all unit tests
npm run lint         # Lint source and test files
npm run dist         # Build distribution (transpiles src/ to root with Babel)
npm run check        # Run tests and lint together
npm run bib          # Regenerate BIBLIOGRAPHY.md from citation data
```

To run a single test file, use mocha directly:
```bash
./node_modules/.bin/mocha --require babel-core/register -R spec ./test/endpoint.js --grep "levenshtein"
```

## Architecture

### Module Structure

The library uses **ES6 modules** transpiled to **CommonJS** via Babel for Node.js compatibility. Each module in `src/` is designed to be independently loadable.

**Export patterns:**
- `export default` - The main function/class for the module
- `export function` - Named utility functions exported on the default object

**Custom Babel plugin (`babel-plugin.js`):** Transforms ES6 exports into a `module.exports.default` pattern that enables both `require('talisman/metrics/levenshtein')()` and `import levenshtein from 'talisman/metrics/levenshtein'` to work correctly.

### Source Organization

- `src/metrics/` - Distance/similarity functions (levenshtein, jaccard, cosine, etc.)
- `src/clustering/` - Clustering algorithms (naive, canopy, k-means variants, etc.)
- `src/phonetics/` - Phonetic encoding (soundex, metaphone, double-metaphone, etc.)
- `src/stemmers/` - Word stemmers (porter, lancaster, language-specific)
- `src/tokenizers/` - Text tokenization (words, sentences, ngrams, etc.)
- `src/helpers/` - Utility functions used across modules
- `src/keyers/` - String key generation for indexing
- `src/hash/` - Hashing functions (minhash, crc32)
- `src/parsers/` - Data format parsers (CoNLL, Brown)

### Code Conventions

- Source files use **ES6 syntax** (arrow functions, destructuring, spread operator)
- **Functional style** preferred; classes used only where state is essential (clustering algorithms)
- Each source file includes JSDoc with `[Reference]`, `[Article]`, and `[Tags]` headers documenting the algorithm's origin
- Tests mirror the `src/` directory structure in `test/`
- Constants are typically declared at the top of files (e.g., `const VECTOR = []`)

### Clustering

Clustering modules extend the abstract `RecordLinkageClusterer` class from `src/clustering/abstract.js` and use helper functions from `src/clustering/helpers.js` for distance/similarity polymorphism handling.

### Test Resources

Test fixtures are stored in `test/_resources/` and loaded via `test/helpers.js` utilities `loadResource()` and `loadCSV()`.