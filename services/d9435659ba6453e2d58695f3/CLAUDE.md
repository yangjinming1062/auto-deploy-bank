# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of sample applications demonstrating how to use the [ClipDrop API](https://clipdrop.co/apis) across multiple platforms (web, iOS, Android). Each sample is self-contained in its own directory.

## Build Commands

### Web Samples (Next.js-based)
Most web samples use Next.js with TailwindCSS:
```bash
cd web/<sample-name>
yarn install  # or npm install
yarn dev      # development server
yarn build    # production build
yarn start    # start production server
```

### Web Sample (React SPA)
The `remove-background-bulk` sample uses create-react-app:
```bash
cd web/remove-background-bulk
yarn install
yarn start              # dev server
yarn build              # production build
yarn test               # run tests (Jest/React Testing Library)
```

### iOS Samples
Open the `.xcodeproj` file in Xcode:
```bash
open iOS/clip-demo/SampleClip.xcodeproj
```
Requires an API key set in `local.properties`:
```properties
apiKey="YOUR_API_KEY"
```

### Android Samples
Open the project in Android Studio. Requires an API key in `local.properties`:
```properties
apiKey="YOUR_API_KEY"
```

## Architecture

### Web Applications
- **Framework**: React with Next.js (pages router) or create-react-app
- **Styling**: TailwindCSS with `tailwind-merge` for class handling
- **Language**: TypeScript (mostly) and JavaScript
- **Component Pattern**:
  - `components/` - UI components (Landing, Result, DropZone, etc.)
  - Feature-specific modules (e.g., `cars/cars/index.ts`, `decompose-layers/decompose/index.ts`)
  - `utils.ts` - Shared utilities (blob/canvas conversions, file handling)
- **API Calls**: Use FormData to send images; responses are typically base64 or blob data

### ClipDrop API Pattern
Most web samples follow this pattern:
```typescript
const payload = new FormData()
payload.append('image_file', file)
const response = await fetch(ENDPOINT, {
  method: 'POST',
  headers: { 'x-api-key': apiKey },
  body: payload
})
```

### Mobile Applications
- **iOS**: SwiftUI with CameraX for image capture
- **Android**: Kotlin with CameraX and OkHttp for API requests

## Key API Endpoints Used
- `https://clipdrop-api.co/remove-background/v1`
- `https://clipdrop-api.co/cleanup/v1`
- `https://clipdrop-api.co/replace-background/v1`