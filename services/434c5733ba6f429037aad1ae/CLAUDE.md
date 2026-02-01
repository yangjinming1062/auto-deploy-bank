# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
npm start          # Start development server (port 3000)
npm run build      # Build for production
npm test           # Run tests
npm run deploy     # Build and deploy to GitHub Pages
```

## Technology Stack

- **React 18** + **TypeScript** (Create React App)
- **@jscad/modeling** + **@jscad/regl-renderer** for 3D geometry and rendering
- **@hookstate/core** for centralized state
- **OpenJSCAD.org** submodules (local packages in `OpenJSCAD.org/packages/`)

## Architecture

### State Management (`src/lib/params.ts`)

Centralized state using Hookstate. The `Params` type defines all enclosure parameters (dimensions, holes, mounts, screws, waterproof seal). Access via `useParams()` hook.

### 3D Rendering (`src/ui/Renderer.tsx`)

Uses `@jscad/regl-renderer` for WebGL rendering with orbit controls. Implements selective re-rendering:
- Tracks param changes with `diffParams()` and `checkDeps()`
- Only regenerates model components that depend on changed params
- Three render positions: lid, base, and waterproof seal (side-by-side)

### Enclosure Generation (`src/lib/enclosure/`)

| File | Purpose |
|------|---------|
| `base.ts` | Base body with floor, walls, holes, wall flanges |
| `lid.ts` | Lid with optional waterproof seal groove |
| `holes.ts` | Circular/square/rectangular cutouts on surfaces |
| `pcbmount.ts` | Internal PCB standoffs |
| `screws.ts` | Corner lid screws |
| `wallmount.ts` | Wall/flange mounts |
| `waterproofseal.ts` | TPU gasket for waterproof versions |
| `utils.ts` | `roundedCube`, `hollowRoundCube`, `clover` primitives |

### UI Components (`src/ui/`)

| Component | Purpose |
|-----------|---------|
| `App.tsx` | Layout container |
| `Renderer.tsx` | 3D viewport with orbit controls |
| `ParamForm.tsx` | Configuration form |
| `Tools.tsx` | Export (STL) and save/load settings |
| `LoadingIndicator.tsx` | Loading overlay during renders |

## Important Notes

- **All measurements in millimeters**
- **Holes require support material** for 3D printing
- X/Y coordinates relative to base center
- Surfaces: 'top', 'bottom', 'left', 'right', 'front', 'back'
- Overall height = Base Height + wall thickness