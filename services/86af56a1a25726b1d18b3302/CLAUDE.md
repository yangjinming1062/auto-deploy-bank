# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Axios is a promise-based HTTP client for the browser and Node.js. It provides interceptors, automatic JSON transformation, request cancellation, and multi-environment support (XHR, HTTP, Fetch adapters).

## Build Commands

```bash
npm run build          # Clear dist, build with rollup (ESM, UMD, CJS for browser/node)
npm run test           # Run all tests (node + browser + package tests)
npm run test:node      # Run mocha unit tests (test/unit/**/*.js)
npm run test:mocha     # Run mocha tests with 30s timeout
npm run test:browser   # Run karma browser tests
npm run test:karma     # Run karma tests (Chrome/Firefox)
npm run test:exports   # Test module exports (CJS + ESM)
npm run test:eslint    # Run eslint on lib/**/*.js
npm run test:dtslint   # Run TypeScript definition linting
npm run test:karma:firefox  # Run karma with Firefox instead of Chrome
npm run fix            # Auto-fix eslint issues
npm run build:version  # Check build version consistency
npm start              # Start sandbox server at localhost:3000
npm run examples       # Start examples server
```

To run a single test file: `node bin/ssl_hotfix.js mocha test/unit/specific.spec.js --timeout 30000 --exit`

## Architecture

### Directory Structure

- **lib/core/**: Core classes (Axios.js, AxiosError.js, AxiosHeaders.js, InterceptorManager.js, dispatchRequest.js, mergeConfig.js, settle.js)
- **lib/adapters/**: HTTP adapter implementations (xhr.js for browser, http.js for Node.js, fetch.js)
- **lib/helpers/**: Utility functions (buildURL.js, bind.js, formDataToJSON.js, isAxiosError.js, etc.)
- **lib/defaults/**: Default configuration
- **lib/platform/**: Platform-specific code (browser vs Node.js)
- **lib/utils.js**: Shared utilities (type checking, object manipulation)
- **lib/env/**: Environment data (version, etc.)

### Request Flow

1. `axios(config)` or `axios.get(url, config)` creates request config
2. `Axios.request(config)` merges config with defaults
3. Request interceptors execute in **reverse order** (LIFO)
4. `dispatchRequest` selects and calls appropriate adapter
5. Adapter performs actual HTTP request
6. `settle` resolves/rejects based on status code
7. Response interceptors execute in **forward order** (FIFO)
8. Promise resolves with response or rejects with AxiosError

### Adapter Pattern

Adapters are selected based on environment capabilities (tried in order: xhr → http → fetch):
- **xhr.js**: XMLHttpRequest for browsers
- **http.js**: Node.js HTTP/HTTPS with streams and redirects
- **fetch.js**: Fetch API with progress events

Use `adapter: 'fetch'` or `adapter: 'http'` in config to force specific adapter.

### Key Classes

- **Axios**: Main class managing interceptor chains and request dispatch
- **AxiosHeaders**: Case-insensitive header management with normalization
- **InterceptorManager**: Handles request/response interceptors with sync/async support
- **AxiosError**: Custom error with standardized codes (ERR_NETWORK, ETIMEDOUT, etc.)

### Config Merging

Config precedence: library defaults → instance defaults → request config. Uses deep merge for nested objects with header normalization.

## Coding Conventions

- Use `'use strict';` at the top of every file
- Use JSDoc comments with `@param` and `@returns` for all public functions
- Use named imports with `.js` extension: `import utils from '../utils.js';`
- Always use `AxiosError` for library errors with appropriate error codes
- Use explicit null/undefined checks instead of truthy/falsy
- Prefix internal helper functions with underscore (e.g., `_request`)
- Classes: PascalCase; functions: camelCase; constants: UPPER_SNAKE_CASE
- Private internals use Symbol (e.g., `$internals`)

### Error Codes

```javascript
AxiosError.ERR_BAD_REQUEST;
AxiosError.ERR_BAD_RESPONSE;
AxiosError.ERR_NETWORK;
AxiosError.ETIMEDOUT;
AxiosError.ECONNABORTED;
AxiosError.ERR_CANCELED;
```

## Important Notes

- **Do not mutate config objects** - always return new objects
- **Do not use global variables or singletons**
- **Do not throw generic Error** - always use AxiosError
- **Do not add dependencies** without team discussion
- **Avoid unnecessary object allocations** in hot paths
- Platform detection uses capability checks, not environment names

## Testing

- Unit tests in `test/unit/**/*.js`
- Integration tests in `test/specs/**/*.js`
- Module tests in `test/module/` (ESM, CJS, TypeScript)
- Browser tests use Karma + Jasmine
- Mock adapters for isolated unit tests