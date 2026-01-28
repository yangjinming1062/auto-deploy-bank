# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PoseNet is a TensorFlow.js model for real-time pose estimation in the browser. It detects human poses (17 keypoints per person) from images/video using a MobileNet v1 architecture.

## Commands

```bash
# Build the library (compiles both ES5 and ES6, runs rollup, minifies)
npm run build

# Run tests (Karma + Jasmine + Chrome)
npm test

# Run linting
npm run lint

# Watch mode + run demos
npm run dev

# Build and publish to npm
npm run publish-npm
```

## Architecture

The library has two main detection approaches:

**Single-Person Detection** (`src/singlePose/`):
- `decodeSinglePose.ts` - Decodes heatmap/offsets into a single pose
- `argmax2d.ts` - Finds max values in 2D arrays
- Faster but conflates multiple people into one pose

**Multi-Person Detection** (`src/multiPose/`):
- `decodeMultiplePoses.ts` - Main multi-pose decoding with fast greedy algorithm
- `decodePose.ts` - Individual pose decoding
- `buildPartWithScoreQueue.ts` - Priority queue for part detection
- `maxHeap.ts` - Heap implementation for scoring
- Slower but correctly separates multiple people

**Core Pipeline** (`src/posenet.ts`):
- `PoseNet` class wraps MobileNet and exposes `estimateSinglePose()` and `estimateMultiplePoses()`
- `load()` function loads checkpoints and returns a PoseNet instance
- `predictForSinglePose()` / `predictForMultiPose()` run the model and return heatmaps/offsets
- Uses `tf.tidy()` for automatic tensor memory management

**Model Loading** (`src/checkpoint_loader.ts`):
- Loads pre-trained MobileNet weights from TensorFlow checkpoints
- `checkpoints.ts` maps multiplier values (0.5, 0.75, 1.0, 1.01) to architecture URLs
- Multiplier controls accuracy vs speed tradeoff (1.01 = best accuracy, 0.50 = fastest)

**Key Types** (`src/types.ts`):
- `Pose` - Array of `Keypoint`s with a `score`
- `Keypoint` - `{position: Vector2D, score, part}`
- `Vector2D` - `{x, y}` coordinates

## Keypoints

Parts are indexed 0-16: nose(0), leftEye(1), rightEye(2), leftEar(3), rightEar(4), leftShoulder(5), rightShoulder(6), leftElbow(7), rightElbow(8), leftWrist(9), rightWrist(10), leftHip(11), rightHip(12), leftKnee(13), rightKnee(14), leftAnkle(15), rightAnkle(16).

## Build Outputs

- `dist/` - ES5 CommonJS with minified bundle (`posenet.min.js`)
- `dist-es6/` - ES2015 modules
- `dist/index.d.ts` - TypeScript declarations