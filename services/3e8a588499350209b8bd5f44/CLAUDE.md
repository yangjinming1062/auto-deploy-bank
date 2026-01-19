# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tolgee is an open-source localization platform (alternative to Crowdin, Phrase, Lokalise). The codebase consists of three main components:
- **Backend**: Kotlin/Spring Boot API server (Gradle multi-module project)
- **Frontend**: React/TypeScript web application (Vite build system)
- **E2E Tests**: Cypress-based integration tests

## Common Commands

### Backend Development
```bash
# Run backend
./gradlew server-app:bootRun --args='--spring.profiles.active=dev'

# Run tests
./gradlew test

# Format Kotlin code
./gradlew ktlintFormat

# Update database migrations (after JPA changes)
./gradlew diffChangeLog
# If docker command not found, use:
./gradlew diffChangeLog --no-daemon
```

### Frontend Development
```bash
cd webapp

# Start development server
npm run start

# Build for production
npm run build

# Run tests
npm test

# Lint and format
npm run prettier
npm run eslint
npm run tsc

# Regenerate API schemas (backend must be running first)
npm run schema        # Main API
npm run billing-schema # Billing API (if applicable)
```

### E2E Testing
```bash
cd e2e

# Run tests headless
npm run cy:run

# Open Cypress UI
npm run cy:open
```

## High-Level Architecture

### Backend (Kotlin/Spring Boot)
Located in `backend/` with Gradle modules:
- **api**: Public API endpoints and DTOs
- **app**: Main application entry point and configuration
- **data**: JPA entities and database layer
- **security**: Authentication and authorization
- **development**: Development utilities and E2E data controllers
- **testing**: Test utilities and base classes
- **misc**: Shared utilities and helpers
- **ktlint**: Code style configuration

Database migrations use Liquibase (changelog in `backend/app/src/main/resources/db.changelog.xml`).

### Frontend (React/TypeScript)
Located in `webapp/` with structure:
- **src/views/**: Feature-based view components
- **src/component/**: Reusable UI components
- **src/service/**: API services and HTTP clients
- **src/hooks/**: Custom React hooks
- **src/i18n/**: Internationalization and translation keys

Uses React Query for API communication with typed hooks. Business events tracked via PostHog using `tg.hooks/useReportEvent`.

### E2E Tests
Located in `e2e/` using Cypress. Test data generated via backend E2E controllers and exposed through `e2e/cypress/common/apiCalls/testData/`.

## Development Workflow

### 1. Setting Up Local Development
1. Install prerequisites: Java 21, Docker, Node.js 18+
2. Clone repo and configure git: `git config blame.ignoreRevsFile .git-blame-ignore-revs`
3. Start backend: `./gradlew server-app:bootRun --args='--spring.profiles.active=dev'`
4. Start frontend: `cd webapp && npm ci && npm run start`
5. Open http://localhost:3000

### 2. Configuration
Create `backend/app/src/main/resources/application-dev.yaml` to override defaults:
```yaml
spring:
  jpa:
    show-sql: true
tolgee:
  front-end-url: http://localhost:3000
  file-storage-url: http://localhost:8080
```

### 3. Frontend Path Aliases
Use TypeScript path aliases instead of relative imports:
- `tg.component/*` → `component/*`
- `tg.service/*` → `service/*`
- `tg.hooks/*` → `hooks/*`
- `tg.views/*` → `views/*`

Example: `import { useUser } from 'tg.hooks/useUser'`

### 4. API Communication
Use typed React Query hooks from `useQueryApi.ts`:
```typescript
// Query
const { data, isLoading } = useApiQuery({
  url: '/v2/projects/{projectId}/languages',
  method: 'get',
  path: { projectId: project.id },
});

// Mutation
const mutation = useApiMutation({
  url: '/v2/projects/{projectId}/languages',
  method: 'post',
  invalidatePrefix: '/v2/projects',
});
```

## Critical Quirks & Conventions

### Testing

#### Backend Tests
Use TestData pattern for test setup:
```kotlin
class YourControllerTest {
  @Autowired
  lateinit var testDataService: TestDataService

  @BeforeEach
  fun setup() {
    testData = YourTestData()
    testDataService.saveTestData(testData.root)
  }

  @AfterEach
  fun cleanup() {
    testDataService.cleanTestData(testData.root)
  }
}
```

JSON response testing with `.andAssertThatJson`:
```kotlin
performProjectAuthGet("items").andAssertThatJson {
  node("_embedded.items") {
    node("[0].id").isEqualTo(1)
  }
}
```

#### E2E Tests (CRITICAL)
**STRICTLY ENFORCED**: Use `data-cy` attributes for all selectors:
- All values typed in `e2e/cypress/support/dataCyType.d.ts` (auto-generated)
- Use helpers: `gcy('...')` or `cy.gcy('...')`
- NEVER use text content for selectors
- Example:
  ```tsx
  <Alert severity="error" data-cy="signup-error-seats-spending-limit">
    <T keyName="spending_limit_dialog_title" />
  </Alert>
  // In test:
  gcy('signup-error-seats-spending-limit').should('be.visible');
  ```

E2E test data requires 3 components:
1. TestData class (`backend/data/src/main/kotlin/.../YourTestData.kt`)
2. E2E controller (`backend/development/src/main/kotlin/.../YourFeatureE2eDataController.kt`)
3. Frontend object (`e2e/cypress/common/apiCalls/testData/testData.ts`)

### Business Event Tracking
```typescript
// Event-triggered reporting
import { useReportEvent } from 'tg.hooks/useReportEvent';
const reportEvent = useReportEvent();
reportEvent('event_name', { key: 'value' });

// Component mount reporting
import { useReportOnce } from 'tg.hooks/useReportEvent';
useReportOnce('page_viewed', { pageName: 'settings' });
```

### Error Codes
Backend error codes in `Message.kt` enum are converted to **lowercase** for frontend:
```typescript
cy.intercept('POST', '/v2/projects/*/keys*', {
  statusCode: 400,
  body: {
    code: 'plan_key_limit_exceeded',  // lowercase!
    params: [1000, 1001],
  },
});
```

### Translation Keys
**NEVER** update translation files manually. Translation keys are auto-added after merging to main. Freely use nonexistent keys in code.

### API Schema Regeneration
After backend API changes:
1. Start backend: `./gradlew server-app:bootRun --args='--spring.profiles.active=dev'`
2. Run: `cd webapp && npm run schema && npm run billing-schema`

## Git Workflow

### Branch Naming
Format: `firstname-lastname/feature-description`

Generate from git config:
```bash
git config get user.name | awk '{print $1, $2}' | \
  iconv -f UTF-8 -t ASCII//TRANSLIT | \
  tr -cd '[:alpha:]' | tr '[:upper:]' '[:lower:]'
```

### Commit Message Prefixes
- `feat:` - Breaking changes or new features
- `fix:` - Non-breaking bug fixes
- `chore:` - Non-behavior changes (docs, tests, formatting)

## References

- **AGENTS.md**: Detailed Tolgee-specific guidance for AI agents
- **DEVELOPMENT.md**: Comprehensive setup and development guide
- **README.md**: Project overview and feature descriptions
- **CONTRIBUTING.md**: Contribution guidelines and resources