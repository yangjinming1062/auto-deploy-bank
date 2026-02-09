# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AR Face Doodle** - A web-based AR application that allows users to draw directly on their face using the webcam. Real-time face tracking via TensorFlow.js FaceMesh drives Three.js rendering where drawing occurs on invisible planes aligned to face surfaces.

## Commands

```bash
npm install              # Install dependencies
npm start                # Start dev server (Parcel, accessible on 0.0.0.0:1234)
npm run deploy           # Build and deploy to GitHub Pages
```

## Architecture

### Module Structure

| File | Purpose |
|------|---------|
| `src/main.js` | Application controller - camera setup, event handling, main update loop, UI coordination |
| `src/facemesh.js` | TensorFlow.js FaceMesh integration - loads model, returns face predictions with keypoints |
| `src/three.js` | Three.js scene setup, face mesh deformation, drawing plane creation, raycasting for draw operations |
| `src/colorpicker.js` | Color picker UI wrapper around `a-color-picker` library |
| `src/triangulation.js` | Face mesh triangulation indices (from Google FaceMesh) |
| `src/refmesh.js` | Debug data - pre-computed face keypoints for testing without camera |
| `src/vendor/OBJLoader.js` | Three.js OBJ model loader |
| `static/facemesh.obj` | 468-vertex 3D face mesh model |

### Data Flow

1. **main.js** → sets up webcam via `navigator.mediaDevices.getUserMedia`
2. **main.js** → calls `facemesh.update(video)` each frame to get face keypoints
3. **main.js** → passes `scaledMesh` to `three.update(face.scaledMesh)`
4. **three.js** → deforms `baseMesh` vertices to match detected face
5. **User draws** → raycaster finds face surface intersection → creates drawing plane
6. **Drawing** → strokes rendered to 2D canvas texture applied to aligned plane

### Key Implementation Details

- **Canvas mirroring**: The Three.js canvas uses `transform: scale(-1, 1)` to correct for webcam mirroring
- **Drawing planes**: Created on-demand when user draws on detected face, aligned to face normal
- **Line smoothing**: Uses `simplify-js` library to reduce path complexity before rendering
- **Material opacity**: `baseMesh` material is transparent (`opacity: 0`) by default so only drawings are visible

### Configuration Notes

- `useCamera` flag in `main.js` controls camera vs debug data mode
- Drawing parameters (`color`, `thickness`, `smooth`, `debug`) are exposed via `three.params`
- Material Design components used for UI (slider, icon buttons)
- ESLint with Prettier-Standard for code style