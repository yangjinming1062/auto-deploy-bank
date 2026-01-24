# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the [Teachable Machine Community](https://github.com/googlecreativelab/teachablemachine-community) repository by Google Creative Lab. It contains two main components:

1. **Libraries** (`/libraries`) - TensorFlow.js-based TypeScript libraries for using Teachable Machine models
2. **Snippets** (`/snippets`) - Markdown code snippets displayed in the Teachable Machine export panel

## Architecture

### Libraries Structure

Each library (image, pose) follows a common pattern:
- `src/` - TypeScript source code
- `test/` - Karma/Mocha tests
- `dist/` - Compiled output (gitignored)
- `scripts/` - Build utilities like `make-version.js`
- Built with TypeScript + Webpack, peer dependency on `@tensorflow/tfjs`

**Library exports:**
- **image** (`@teachablemachine/image`): Wraps MobileNet for custom image classification
- **pose** (`@teachablemachine/pose`): Wraps PoseNet for body pose classification
- **audio**: Direct usage of `@tensorflow-models/speech-commands` (no custom library)

### Snippets Structure

Markdown files organized by model type and export format:
- `markdown/` - Final markdown files served to frontend
- `converter/` - Source files converted to `markdown/`
- `markdown/index.json` - Master index mapping UI options to markdown files
- New snippets require adding entries to `index.json`

## Common Commands

### Libraries (image/pose)

```bash
cd libraries/image  # or libraries/pose
npm install                    # Install dependencies (Node > 12 required)
npm run build                  # Compile TypeScript + webpack bundle
npm run build-clean            # Clean + full rebuild
npm run test                   # Run Karma tests (headless Chrome via Puppeteer)
npm run test-watch             # Watch mode for tests
npm run lint                   # Run TSLint
npm run dev                    # Concurrent watch mode + test runner
npm run publish-local          # Build + publish to local yalc
```

### Snippets

```bash
cd snippets
npm install
npm run lint                   # Run markdownlint on markdown/ and converter/
npm run start                  # Serve snippets via http-server
```

## Key Dependencies

- **@tensorflow/tfjs** (peer dep, version 1.3.1): Core ML runtime
- **@tensorflow-models/mobilenet** / **@tensorflow-models/posenet** / **@tensorflow-models/speech-commands**: Pre-trained backbones
- **TypeScript 3.x** with experimentalDecorators enabled
- **Webpack 4.x** for bundling
- **Karma** + **Mocha** + **Puppeteer** for testing

## Development Notes

- Libraries use legacy TSLint (not ESLint)
- Pose and image libraries have nearly identical structure and tooling
- Audio models use TensorFlow.js Speech Commands directly without a custom wrapper library
- Snippets use `{{URL}}` placeholder that gets replaced at export time with model URL