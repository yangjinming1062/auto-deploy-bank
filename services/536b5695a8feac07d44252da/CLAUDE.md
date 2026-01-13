# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Booking.js v3** by Timekit - an embeddable booking widget that integrates with the Timekit API. The widget allows users to create beautiful booking interfaces for scheduling appointments.

## Common Commands

### Development
- `yarn dev` - Start development server at http://localhost:8081
- `yarn test` - Run test suite with Karma
- `yarn test:watch` - Run tests in watch mode

### Building
- `yarn build` - Build production bundle using webpack

### Deployment & Releases
The project uses [Flux](https://github.com/getflux/flux) for deployment automation:
- `yarn deploy:prod` - Deploy to production CDN
- `yarn deploy:hosted` - Deploy to hosted environment
- `yarn release:patch` - Release patch version (x.x.X)
- `yarn release:minor` - Release minor version (x.X.0)
- `yarn release:major` - Release major version (X.0.0)

### Testing Individual Specs
Karma runs all `*.spec.js` files in the `/test` directory. To test specific functionality, run the full suite with `yarn test` (single run mode enabled in karma.conf.js).

## Architecture

The codebase follows a dual-module pattern with two main entry points:

### 1. `/src/booking/` - Primary Booking Widget
The main booking interface using FullCalendar for calendar rendering.
- **Entry point**: `src/booking/index.js` - Exports the BookingWidget class
- **Core class**: `src/booking/widget.js` - Main BookingWidget orchestrator
- **Helpers** (src/booking/helpers/):
  - `config.js` - Configuration management with default configs and presets
  - `util.js` - Utility functions and callbacks
  - `template.js` - Template rendering and DOM manipulation
  - `base.js` - Base class for common functionality
- **Pages** (src/booking/pages/):
  - `booking.js` - Main booking flow
  - `reschedule.js` - Reschedule flow
- **Services** (src/booking/services/):
  - `timezones.js` - Timezone handling
- **Templates** (src/booking/templates/): HTML templates for widget components
- **Styles** (src/booking/styles/): SCSS styles using FullCalendar and custom styles

### 2. `/src/services/` - Service Selection Module
Alternative/additional UI module for service selection (locations, services, calendar).
- **Entry point**: `src/services/index.js` - Re-exports widget.js
- **Core classes** (src/services/classes/): Similar pattern to booking module
  - `config.js`, `util.js`, `template.js`, `base.js`
- **Pages** (src/services/pages/):
  - `calendar.js`, `locations.js`, `services.js`

### Configuration
- `src/booking/configs.js` - Default configuration settings
- `src/services/configs.js` - Service module configurations

### SDK Integration
The widget integrates with the Timekit API via `timekit-sdk` (v1.19.3). The SDK instance is available through `widget.getSdk()` and is configured in `widget.render()` with authentication and API settings.

### Dependency Flow
```
BookingWidget (widget.js)
├── Config class (manages settings, defaults, remote config loading)
├── Util class (logging, callbacks, validation)
├── Template class (DOM rendering, FullCalendar integration)
└── timekit-sdk (API communication)
```

## Key Dependencies
- **FullCalendar** - Calendar rendering (@fullcalendar/core, daygrid, timegrid, interaction, etc.)
- **moment/moment-timezone** - Date/time manipulation
- **lodash** - Utility functions
- **timekit-sdk** - Timekit API client
- **webpack** - Module bundling
- **Jasmine/Karma** - Testing framework
- **Puppeteer** - Chrome Headless for testing

## Development Workflow

1. **Local Development**: Use `yarn dev` for hot-reload development
2. **Testing**: Write Jasmine specs in `/test` directory following the pattern in existing tests (initialization.spec.js, availabilityListView.spec.js, etc.)
3. **Build**: Run `yarn build` to create production bundle in `/public/build`
4. **Release**: Update version in package.json, ensure tests pass, merge to master, then use release scripts

## Testing Setup
- **Test framework**: Jasmine with Karma test runner
- **Browser**: Chrome Headless (via Puppeteer)
- **Test files**: Located in `/test` directory as `*.spec.js`
- **Fixtures**: HTML fixtures in `/test/fixtures/`
- **Utilities**: Test utilities in `/test/utils/` (mockAjax, defaultConfig, createWidget, commonInteractions)

## CI/CD
- **CI**: CircleCI configuration in `.circleci/config.yml`
- **Deployment**: Flux-managed deployments to AWS CDN (see flux.json)
- **Production CDN**: `timekit-cdn/booking-js/v3`
- **Staging CDN**: `timekit-cdn-staging/booking-js/v3`

## Important Notes
- The widget auto-initializes if `window.timekitBookingConfig` exists and `autoload !== false`
- Supports both singleton pattern (auto-init) and instance pattern (manual init)
- Remote configuration can be loaded for embedded projects
- The widget has a render/destroy lifecycle for proper cleanup