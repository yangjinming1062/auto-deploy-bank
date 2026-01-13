# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

H5-Dooring is a powerful, open-source, free H5 visual page configuration solution. It's a drag-and-drop H5 page builder that allows users to create H5 landing pages without coding. The project is built with React 16 + UmiJS on the frontend and Koa.js on the backend.

**Technology Stack:**
- Frontend: React 16, UmiJS 3, TypeScript, Ant Design 4
- State Management: DVA (Redux-based)
- Backend: Koa.js (Node.js)
- Build Tools: Webpack, Babel, ESLint
- Testing: umi-test
- Drag & Drop: react-dnd with HTML5 backend

## Common Development Commands

### Installation
```bash
yarn install
# or
npm install
```

### Development
```bash
# Start development server (editor)
yarn start

# Start on Windows
yarn start:win

# Start backend server separately
yarn server

# Preview built version with http-server
yarn dev
```

### Building & Production
```bash
# Build for production
yarn build

# Build on Windows
yarn build:win

# Build without compression
yarn nocompress
```

### Code Quality
```bash
# Format code with Prettier
yarn prettier

# Run tests
yarn test

# Run tests with coverage
yarn test:coverage
```

### Documentation
```bash
# Start documentation dev server
yarn docs:dev

# Build documentation
yarn docs:build
```

### Testing the Built App
```bash
# Serve the dist folder locally
yarn test-demo
```

## High-Level Architecture

### Component System (`/src/materials/`)

The project uses a **component-based architecture** where each component is organized into three files:

1. **`index.tsx`** - The component implementation
2. **`schema.ts`** - DSL (Domain Specific Language) configuration defining component properties
3. **`template.ts`** - Component metadata (type, category, appearance, relationships)

Components are categorized into four main material types:

- **`/materials/base/`** - Basic components (Text, Image, Button, Icon, Header, Tab, Form, etc.)
- **`/materials/visual/`** - Chart and visualization components (Pie, Line, Area, Chart, XProgress)
- **`/materials/shop/`** - E-commerce components (CardLabel, ZhuanLan, Coupons, etc.)
- **`/materials/media/`** - Media components (Video, Audio, Map, Calendar)

### Editor Core (`/src/pages/editor/`)

The main editor interface with several key parts:

- **`Container.tsx`** - Main editor canvas container
- **`TargetBox.tsx`** - Drop target for drag-and-drop
- **`SourceBox.tsx`** - Component library panel
- **`preview.tsx`** - Preview mode renderer
- **`/models/`** - DVA models for state management (editorPcModel.ts, editorModal.js)
- **`/components/`** - Editor-specific components
- **`/services/`** - API service layer

The editor uses react-dnd with HTML5Backend for drag-and-drop functionality (configured in `/src/pages/editor/index.js`).

### Core Rendering Engine (`/src/core/`)

- **`DynamicEngine.tsx`** - Dynamic component rendering engine
- **`/renderer/`** - Component renderer utilities

### UI Components (`/src/components/`)

Reusable UI components organized by functionality:

- **`/FormComponents/`** - Form controls used in editor panels (Upload, Color, DataList, Table, etc.)
- **`/ErrorBundaries/`** - Error boundary components
- **`/LoadingCp/`** - Loading components
- **`/Calibration/`** - Alignment and calibration tools

### State Management

The project uses **DVA** (Redux + Redux-Saga) for state management. Models are located in:
- `/src/pages/editor/models/editorPcModel.ts` - Main editor state
- `/src/pages/editor/models/editorModal.js` - Editor modals state

State is configured in `.umirc.ts` with DVA plugin enabled.

### Routing

Routes are configured in `.umirc.ts`:
- `/` - Home page
- `/editor` - Main editor
- `/ide` - IDE interface
- `/help` - Help page
- `/login` - Login page
- `/preview` - Preview page

## Configuration Files

- **`.umirc.ts`** - Main UmiJS configuration (routes, plugins, theme)
- **`tsconfig.json`** - TypeScript configuration
- **`webpack.config.js`** - Webpack configuration
- **`package.json`** - Dependencies and scripts

## Component Development Pattern

When creating new components, follow this structure in `/src/materials/<category>/<ComponentName>/`:

```typescript
// index.tsx - Component implementation
interface ComponentProps {
  // ... props from schema
  isTpl: boolean; // Template mode flag
}

const Component = memo((props: ComponentProps) => {
  return props.isTpl ? (
    // Template preview
    <div>...</div>
  ) : (
    // Component preview
    <div>...</div>
  );
});
```

```typescript
// schema.ts - Component DSL definition
export default {
  // Component configuration schema
  // Defines properties, defaults, and validations
};
```

```typescript
// template.ts - Component metadata
export default {
  componentName: 'ComponentName',
  title: 'Display Title',
  icon: 'icon-name',
  // ... other metadata
};
```

## Key APIs

### Utility Functions
- **`/src/utils/tool.ts`** - Common utility functions
- **`/src/utils/req.ts`** - HTTP request utilities

### Backend API

The project includes a Koa.js backend server (`server.js`) running on port 3000 with:
- Static file serving
- CORS support
- Body parsing
- Logger middleware
- HTML rendering endpoint (`/dooring/render`, `/html`)

## Development Workflow

1. **Start development**: `yarn start` (starts Umi dev server)
2. **Make changes** to components in `/src/materials/` or editor logic
3. **Build for production**: `yarn build`
4. **Test locally**: `yarn dev` (serves the dist folder)

## Path Aliases

The project uses several path aliases configured in `.umirc.ts` and `tsconfig.json`:
- `@/*` - `src/*`
- `components/*` - `src/components/*`
- `utils/*` - `src/utils/*`
- `assets/*` - `src/assets/*`

## Important Notes

- **Node Version**: Requires Node.js with OpenSSL legacy provider (NODE_OPTIONS is pre-configured in scripts)
- **Build System**: Uses UmiJS 3 which integrates Webpack, Babel, and other build tools
- **Component Library**: Material components use dynamic imports with `@/components/LoadingCp` as loading fallback
- **Theme**: Primary color is `#2F54EB` (configured in `.umirc.ts`)
- **Pre-commit Hooks**: Lint-staged is configured to format code automatically before commits

## Additional Resources

- Documentation: `/doc/` directory (VuePress format)
- Chinese Guide: `/zh.md`
- Change Log: `/CHANGELOG.md`
- Security: `/SECURITY.md`

## Troubleshooting

- **Windows Issues**: Use `start:win` and `build:win` scripts
- **Component Drag Errors**: Try using `yarn dev` instead of `yarn start` if drag-and-drop encounters issues
- **SSL Legacy Provider**: Required for Node 17+ due to OpenSSL changes (already configured in scripts)