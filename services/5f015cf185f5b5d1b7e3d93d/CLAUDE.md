# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**gaze-detection** is a JavaScript library that uses TensorFlow.js to detect eye gaze direction (RIGHT, LEFT, STRAIGHT, TOP) for building gaze-controlled interfaces. The demo implements an on-screen keyboard where looking left/right narrows down letter selections.

## Commands

```bash
# Development
npm run watch          # Build main index.html with hot module reloading disabled
npm run watch:demo     # Build demo/keyboard/index.html with HMR disabled

# Production builds
npm run build          # Build index.js as global 'gaze-detection' library
npm run build-demo     # Build demo keyboard with public URL ./ for deployment
```

## Architecture

**Main module** (`index.js`):
- Exports `gaze` object with three methods: `loadModel()`, `setUpCamera()`, `getGazePrediction()`
- Uses TensorFlow.js face landmark detection with MediaPipe Facemesh package
- Tracks left iris position relative to face bounding box
- Detects face rotation to filter out invalid predictions
- Returns gaze direction based on normalized iris coordinates

**Detection logic** (`index.js:62-88`):
- Normalizes iris X position > 0.355 = RIGHT, < 0.315 = LEFT
- Normalized Y position > 0.62 = TOP
- Requires 8+ consecutive STRAIGHT frames to return STRAIGHT (debouncing)

**Demo** (`demo/keyboard/`):
- Implements gaze-controlled keyboard with letter elimination
- Imports main module from `index.js`
- Handles special keys: Delete, space, Enter

## Technology Stack

- **Bundler**: Parcel 1.x
- **ML Model**: `@tensorflow-models/face-landmarks-detection` (mediapipeFacemesh)
- **Backend**: WebGL (`@tensorflow/tfjs-backend-webgl`)
- **Babel**: Preset-env with browser targets > 3% market share