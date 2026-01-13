# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

### Installation
```bash
npm install
```
This automatically runs `bower install` via the postinstall script.

### Development Server
```bash
gulp serve
```
Runs development server with live reload at http://localhost:3000

### Build for Production
```bash
gulp build
```
Outputs optimized files to `release/` directory

### Build for Development
```bash
gulp dev-release
```
Outputs development build to `dev-release/` directory with unminified dependencies

## Project Architecture

### Module Structure
This is an AngularJS-based admin panel framework with a modular architecture:

- **BlurAdmin** (src/app/app.js:3): Main application module
- **BlurAdmin.theme** (src/app/theme/theme.module.js): Core theme system with components, directives, filters, inputs, services
- **BlurAdmin.pages** (src/app/pages/pages.module.js): Feature modules organized under pages/

### Directory Structure
```
src/
├── app/                    # Application code
│   ├── pages/             # Feature modules
│   │   ├── charts/        # Chart components
│   │   ├── components/    # Reusable UI components
│   │   ├── dashboard/     # Dashboard views
│   │   ├── form/          # Form-related features
│   │   ├── maps/          # Map components
│   │   ├── profile/       # User profile
│   │   ├── tables/        # Data tables
│   │   └── ui/            # UI elements
│   ├── theme/             # Theme system
│   │   ├── components/    # Theme components
│   │   ├── directives/    # Custom directives
│   │   ├── filters/       # Custom filters
│   │   ├── inputs/        # Form input components
│   │   └── services/      # Theme services
│   └── assets/            # Static assets
├── sass/                  # SCSS stylesheets
│   ├── main.scss         # Main stylesheet with injector comments
│   ├── auth.scss         # Authentication page styles
│   ├── 404.scss          # 404 page styles
│   └── theme/            # Theme SCSS files
├── index.html            # Main HTML template
├── auth.html             # Authentication template
├── reg.html              # Registration template
└── 404.html              # 404 error template
```

## Available Gulp Tasks

### Core Tasks
- `gulp` or `gulp default` - Clean and build production release
- `gulp build` - Build production release (html, fonts, other assets)
- `gulp serve` - Start dev server with live reload
- `gulp serve:dist` - Build and serve production release
- `gulp watch` - Watch files and rebuild on changes
- `gulp inject` - Inject CSS/JS dependencies into HTML templates
- `gulp clean` - Clean temporary and output directories

### Scripts & Styles
- `gulp scripts` - Lint and validate JavaScript
- `gulp scripts-reload` - Rebuild scripts and trigger browser reload
- `gulp styles` - Compile SCSS to CSS
- `gulp styles-reload` - Rebuild styles and trigger browser reload

### Specialized Builds
- `gulp fonts` - Extract and copy fonts from bower components
- `gulp other` - Copy non-code assets (images, etc.)
- `gulp partials` - Minify HTML and cache in Angular template cache
- `gulp dev-fonts` - Copy fonts for dev release
- `gulp dev-release` - Build development release

### Documentation & Deployment
- `gulp deploy-docs` - Generate and deploy documentation to gh-pages
- `gulp marketplace-release` - Create distributable release zip

## Build System Details

### Paths Configuration (gulp/conf.js:14-20)
- `src`: 'src'
- `dist`: 'release' (production build)
- `devDist`: 'dev-release' (development build)
- `tmp`: '.tmp' (temporary build files)
- `e2e`: 'e2e'

### Key Dependencies
- **Frontend**: AngularJS 1.5.8, Bootstrap 3.3.5, jQuery 3.1.1
- **Charts**: Chart.js, amCharts, Chartist, Morris.js
- **Maps**: Leaflet, amMap
- **UI**: Angular UI Router, Angular UI Bootstrap, Font Awesome, Ionicons
- **Build**: Gulp 3.9.0, Sass, ESLint, BrowserSync

### Wiredep Configuration (gulp/conf.js:27-30)
Bower dependencies are automatically injected into HTML with these exclusions:
- bootstrap.js
- bootstrap-sass/*.js
- require.js

## CI/CD

Travis CI (configured in .travis.yml) runs on Node.js 8:
- Installs gulp globally
- Runs `npm install`
- Executes `gulp build`

## Template Injection

SCSS files in `src/sass/**/_*.scss` are automatically injected into main.scss via injector comments (gulp/styles.js:47-49). Custom theme files in `src/sass/theme/conf/**/*.scss` are excluded from this injection.

## Important Notes

- The build process generates source maps for both JS and CSS
- HTML templates are minified and cached in Angular's template cache
- Bower dependencies are automatically injected into HTML files via wiredep
- The dev release includes all bower dependencies in a `lib/` directory
- Custom fonts from bower are copied to dist/fonts/
- ESLint runs on all JS files with Angular plugin rules

## Common Development Workflow

1. Start development server: `gulp serve`
2. Edit files in `src/app/` or `src/sass/`
3. BrowserSync automatically reloads on changes
4. Run `gulp build` to create production build
5. Run `gulp serve:dist` to test production build locally