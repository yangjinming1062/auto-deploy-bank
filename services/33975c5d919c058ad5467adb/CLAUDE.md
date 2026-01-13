# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**vue-manage-system** is a Vue 3-based admin management system template built with TypeScript, Element Plus, Pinia, and Vite 3. It's designed for rapid development of enterprise management systems with features like authentication, dashboard, data tables, charts, rich text editing, permission management, and theme switching.

**Live Demo**: https://lin-xin.github.io/example/vue-manage-system/

## Common Commands

### Setup & Installation
```bash
# Node.js >= 14.18+ required
npm install                    # Install dependencies (Yarn is preferred based on lock file)

# Development
npm run dev                    # Start dev server with hot reload

# Production
npm run build                  # Build for production (dist/ folder generated)
npm run serve                  # Preview the production build locally
```

### Dependencies
- **Vue 3** (Composition API)
- **Element Plus** (UI components)
- **Pinia** (State management)
- **Vue Router 4** (Routing)
- **Vite 3** (Build tool)
- **TypeScript** (Type safety)
- **ECharts, Schart** (Charts)
- **WangEditor, MdEditor-v3** (Rich text & Markdown editors)
- **Axios** (HTTP client)
- **XLSX** (Excel import/export)

## Code Architecture

### Directory Structure
```
src/
├── api/            # API modules (Axios requests)
├── assets/         # Static resources (CSS, images, fonts)
├── components/     # Reusable Vue components
├── router/         # Vue Router configuration & permission guards
├── store/          # Pinia stores (permissions, themes, tabs, user auth)
├── types/          # TypeScript type definitions
├── utils/          # Utility functions
└── views/          # Page-level components
    ├── chart/      # Chart components (Schart, ECharts with word cloud)
    ├── element/    # Element Plus demo components (forms, upload, etc.)
    ├── pages/      # Auth & utility pages (login, 404, reset password)
    ├── system/     # System management (user, role, menu management)
    └── table/      # Table operations (basic, editable, import/export Excel)
```

### Key Architecture Patterns

1. **Routing**: Hash-based routing with permission-based guards
   - Configuration in `src/router/index.ts`
   - Route meta fields for permissions and titles
   - Lazy-loaded route components

2. **State Management**: Pinia stores for global state
   - Permission store (role-based access control)
   - Theme store (theme switching)
   - Tabs store (multiple tabs navigation)
   - User authentication store

3. **Theme System**: Modular CSS-based theming
   - CSS custom properties (variables)
   - Theme switching support
   - Customizable color schemes

4. **Auto-import Configuration**:
   - Vite plugins auto-import Element Plus components and APIs
   - TypeScript declarations in `auto-imports.d.ts` and `components.d.ts`

5. **Build Configuration**:
   - Base path: `./` (relative paths for deployment)
   - Path aliases: `@` → `src/`, `~` → `src/assets/`
   - Unplugin auto-import for Element Plus

## Development Notes

### Mock Data
- Static mock files located in `public/mock/`
- Mock API endpoints for development

### Excel Operations
- SheetJS (XLSX) integration for data import/export
- Excel template: `public/template.xlsx`

### Authentication Flow
- Login/Register/Reset password pages in `src/views/pages/`
- Permission-based route guards
- Role and menu management in `src/views/system/`

### Important Configuration Files
- `vite.config.ts`: Build tool configuration
- `tsconfig.json`: TypeScript compiler settings
- `package.json`: Dependencies and scripts
- `.github/FUNDING.yml`: GitHub Sponsors configuration

### No Testing Framework
This project does not include a testing setup (no Jest, Vitest, or Cypress configuration). Unit testing and E2E testing would need to be added separately if required.

## Component Usage Example

### Schart.js Integration (from README_EN.md)
```vue
<template>
    <div>
        <schart class="wrapper" canvasId="myCanvas" :options="options"></schart>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import Schart from "vue-schart";
const options = ref({
    type: "bar",
    title: {
        text: "Sales Chart",
    },
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
    datasets: [
        {
            label: "Electronics",
            data: [234, 278, 270, 190, 230],
        },
        {
            label: "Accessories",
            data: [164, 178, 190, 135, 160],
        },
    ],
})
</script>
<style>
.wrapper {
    width: 7rem;
    height: 5rem;
}
</style>
```

## Resources

- **Main Documentation**: https://lin-xin.github.io/example/vuems-doc/
- **Repository**: https://github.com/lin-xin/vue-manage-system
- **MIT License** (Copyright 2016-2023)

## Development Tips

- All dependencies are managed via `package.json`
- TypeScript is configured but strict mode is disabled in `tsconfig.json`
- Vue Router uses hash mode (no server-side routing configuration needed)
- The build output is relative-path based for easy deployment
- Component library (Element Plus) is fully integrated with auto-import