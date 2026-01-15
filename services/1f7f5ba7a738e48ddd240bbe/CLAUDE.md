# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenBoxes is an open-source inventory and supply chain management system built as a hybrid Grails/React application. The backend is Grails 3.3.16 (Groovy/Java) with GORM 6.1.12 and Hibernate 5.2.18. The frontend is React 16 with Redux, bundled via Webpack. Data is stored in MySQL/MariaDB with Liquibase migrations.

## Commands

### Frontend Development
```bash
npm run watch        # Watch mode for development (bundles as you edit)
npm run bundle       # Production bundle
npm test             # Run Jest unit tests
npm run styleguide   # Start React Styleguidist dev server
npm run eslint       # Lint with auto-fix
```

### Backend Development
```bash
./gradlew bootRun                                    # Run application with dev config (port 8080)
./gradlew test                                       # Unit tests only
./gradlew integrationTest                            # Integration tests only
./gradlew jacocoTestReport                           # All tests with code coverage report
./gradlew war                                        # Build WAR for deployment
TEST_DATABASE=mysql:8.0.36 ./gradlew jacocoTestReport   # Test against specific database
```

## Architecture

### Backend Structure (Grails)

The Grails application uses the standard structure with domain models, controllers, and services organized under `org.pih.warehouse`:

- **Controllers**: `grails-app/controllers/org/pih/warehouse/` - API endpoints organized by domain:
  - `api/` - REST API controllers
  - `inventory/` - Inventory management
  - `order/` - Order processing
  - `product/` - Product catalog
  - `receiving/` - Inbound shipments
  - `shipping/` - Outbound shipments
  - `reporting/` - Report endpoints

- **Domain**: `grails-app/domain/org/pih/warehouse/` - GORM entities:
  - `core/` - User, Location, Party, etc.
  - `inventory/` - InventoryItem, Stock, etc.
  - `order/` - Order, OrderItem, etc.
  - `product/` - Product, Category, etc.
  - `requisition/` - Requisition, RequisitionItem
  - `shipping/` - Shipment, ShipmentItem

- **Services**: `grails-app/services/org/pih/warehouse/` - Business logic layer

- **Migrations**: `grails-app/migrations/` - Liquibase changelogs for database schema

- **Configuration**: `grails-app/conf/application.yml` - Main config; additional config files can be placed in `~/.grails/` or `${catalina.base}/.grails/`

### Frontend Structure (React)

The React frontend is in `src/js/` with module aliases defined in webpack.config.js:

- `components/` - React components organized by feature
- `actions/` - Redux action creators
- `reducers/` - Redux reducers
- `selectors/` - Redux selectors
- `api/` - API client functions (axios-based)
- `hooks/` - Custom React hooks
- `utils/` - Utility functions
- `consts/` - Constants
- `store.jsx` - Redux store configuration
- `MainRouter.jsx` - React Router setup

### Frontend/Backend Integration

The frontend is bundled by Webpack into `src/main/webapp/webpack/`, then rendered within Grails GSP pages. The webpack output is included via `grails-app/views/common/react.gsp`. API calls go to Grails controllers, which return JSON.

## Testing

### Frontend Tests (Jest)
- Location: `src/js/**/*.spec.js`
- Run with: `npm test`
- Config: Jest config in package.json

### Backend Tests
- **Unit tests**: `test/unit/` - Spock specs using `mockFor*` utilities
- **Integration tests**: `test/integration/` - Full Spring context with Testcontainers
- **Functional tests**: `spec/` - Geb functional tests for API/UI

Run all tests with: `./gradlew jacocoTestReport`

## Key Configuration

### Environment Variables (Frontend)
- `REACT_APP_WEB_SENTRY_DSN` - Sentry DSN for error tracking
- `REACT_APP_SENTRY_ENVIRONMENT` - Sentry environment
- `REACT_APP_WEB_SENTRY_TRACES_SAMPLE_RATE` - Tracing sample rate

### Database
- MySQL 8.0 or MariaDB 10.3+ required
- Connection configured in `grails-app/conf/application.yml`
- Schema managed via Liquibase migrations in `grails-app/migrations/`

### Development Notes
- Java 8 required (sourceCompatibility = 1.8)
- Node 14 and npm 6/7 for frontend build
- Default context path: `/openboxes`
- Grails profile: `react-webpack`