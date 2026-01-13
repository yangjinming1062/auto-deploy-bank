# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

INCEpTION is a semantic annotation platform offering intelligent annotation assistance and knowledge management. It's a web application where multiple users can work on annotation projects with recommender systems for automated suggestions.

**Technology Stack:**
- **Backend**: Java 17, Spring Boot 3.x, Maven
- **Frontend**: TypeScript, Svelte, Vite, ESBuild
- **Database**: Hibernate with Liquibase migrations
- **UI Framework**: Apache Wicket
- **Documentation**: AsciiDoc

## Common Commands

### Building the Project

```bash
# Full build (skip tests and checkstyle for faster builds)
mvn clean install -DskipTests=true -Dcheckstyle.skip=true

# Build specific module
cd inception/inception-app-webapp && mvn clean install -DskipTests=true

# Compile without tests (useful during development)
mvn clean compile -DskipTests
```

### Running Tests

```bash
# Run all tests
mvn test

# Run tests for specific module
cd inception/inception-support && mvn test

# Run single test class
mvn test -Dtest=ClassNameTest

# Run tests with more verbose output
mvn test -X

# Run with coverage (Jacoco)
mvn clean verify -Pjacoco
```

### Running the Application

**From IDE:**
- Run the `de.tudarmstadt.ukp.inception.INCEpTION` class as a Java application

**System Properties for Development:**
- `inception.home=/home/username/inception-dev` - Application data directory
- `wicket.core.settings.general.configuration-type=development` - Enable dev mode (disables caches)

**From Command Line:**
```bash
java -Dwicket.core.settings.general.configuration-type=development \
     -Dinception.home=/path/to/dev/data \
     -jar inception-app-webapp/target/inception-app-webapp-*.jar
```

### TypeScript/JavaScript Components

Many modules include TypeScript/Svelte components with their own build process:

```bash
# Each TS module has its own package.json and build script
cd inception/inception-ui-kb
npm ci  # or npm install
npm run build

# For live development (watch mode)
npm run build -- --live
```

TS modules use:
- ESBuild for bundling
- Svelte with Svelte-preprocess
- Sass for styling
- Vitest for testing
- ESLint with neostandard for linting

## Architecture

### High-Level Structure

**3-Layer Architecture:**
1. **Presentation Layer**: Apache Wicket (UI components)
2. **Business Layer**: Spring Boot (services, configuration)
3. **Data Layer**: Hibernate (database access, JPA)

### Key Patterns

**Services (Business Logic):**
- Services encode the core logic of INCEpTION
- Injected into Wicket pages and other services
- Example: `inception-scheduling/src/main/java/.../SchedulingService.java`

**Wicket Components:**
- Wicket can only inject interfaces
- Pattern: `ExampleComponent` interface + `ExampleComponentImpl` implementation

**Database Migrations:**
- Managed by Liquibase
- Each module defines migrations in `src/main/resources/db-changelog.xml`
- Auto-discovered on application start
- Schema changes require new migrations

### Major Module Categories

**Core Application:**
- `inception-app-webapp` - Main Spring Boot application
- `inception-ui-*` - UI components (Wicket pages)
- `inception-api-*` - REST API endpoints

**Annotation Editors:**
- `inception-brat-editor` - BRAT annotation editor
- `inception-diam-editor` - DIAM annotation editor
- `inception-html-*` - HTML-based editors (Apache Annotator, Recogito)

**I/O Formats:**
- `inception-io-*` - Document import/export (CoNLL, DOCX, TEI, JSON, etc.)

**Recommender System:**
- `inception-recommendation` - ML-based annotation recommendations
- `inception-imls-*` - Individual ML services (OpenNLP, HuggingFace, LLM support, etc.)

**Knowledge Base:**
- `inception-kb` - Knowledge base integration
- `inception-concept-linking` - Entity linking

**Search:**
- `inception-search-*` - Search functionality (core, Mtas, OpenSearch, Solr)

**External Integrations:**
- `inception-external-search-*` - External document repositories (PubMed, PubAnnotation)

### Directory Structure

```
inception/
├── inception-app-webapp/          # Main web application
│   ├── src/main/java/             # Java source
│   │   └── de/tudarmstadt/ukp/inception/
│   │       └── INCEpTION.java     # Application entry point
│   ├── src/main/resources/
│   │   └── application.yml        # Spring Boot configuration
│   └── src/main/webapp/           # Web resources
├── inception-support/             # Shared utilities
├── inception-ui-*/               # Wicket UI modules
├── inception-io-*/               # Document format modules
├── inception-imls-*/             # ML service integrations
├── inception-recommendation/     # Recommender system
├── inception-kb/                 # Knowledge base
├── inception-search-*/           # Search modules
└── [100+ other modules]          # Specialized functionality
```

## Configuration

**Main Configuration:**
- `inception-app-webapp/src/main/resources/application.yml` - Spring Boot settings
- Environment variables: `INCEPTION_DB_URL`, `INCEPTION_DB_USERNAME`, `INCEPTION_DB_PASSWORD`, `INCEPTION_DB_DRIVER`, `INCEPTION_DB_DIALECT`

**Development Settings:**
- Default database: HSQLDB file-based in `~/.inception/`
- Wicket development mode: Set `wicket.core.settings.general.configuration-type=development`
- Logs: Configured via Log4J2

## Code Style

**Java Code:**
- DKPro code formatting profile required (Eclipse/IntelliJ available)
- Checkstyle validation runs during build
- Rules:
  - No tabs, 4 spaces for Java
  - Max 100 characters per line
  - Curly braces on next line for classes/methods, same line for logic
  - Parameter names start with `a` (e.g., `void foo(String aValue)`)
  - Line endings: UNIX (configure `core.autocrlf=input` on Windows)

**TypeScript/JavaScript:**
- ESLint with neostandard configuration
- 2 spaces indentation for TS files

## Development Workflow

1. **Create Issue**: All changes tracked in GitHub issues
2. **Create Branch**: `feature/[ISSUE-NUMBER]-[description]` or `bugfix/[ISSUE-NUMBER]-[description]`
3. **Commit Format**:
   ```
   #[ISSUE NUMBER] - [ISSUE TITLE]

   - Change 1
   - Change 2
   ```
4. **Pull Request**: Create PR for code review
5. **Merge**: After review and CI checks

## Testing

- **Java Tests**: JUnit 5, Mockito, AssertJ
- **TypeScript Tests**: Vitest
- **Test Categories**: Some tests marked as "slow" (configurable via `excludedTestCategories`)
- **Coverage**: Jacoco plugin available
- **CI**: Jenkins pipeline with Maven 3, JDK 17, parallel builds

## Build Profiles

- `jacoco` - Enable code coverage reporting
- `checkstyle` - Run code style checks (enabled by default)
- `skipTests` - Skip test execution
- `slow` - Include slow-running tests

## Database Schema

- **Migration Tool**: Liquibase
- **Schema Location**: `src/main/resources/db/changelog/db.changelog-master.xml`
- **Schema Validation**: Hibernate validates schema on startup (`hibernate.ddl-auto=validate`)
- **Module-Specific Tables**: Each module can define its own tables and migrations

## Key Technologies

- **UIMA**: Underlying text annotation framework
- **DKPro Core**: NLP toolkit integration
- **Bootstrap 5**: UI styling
- **jQuery**: Client-side interactions
- **Svelte**: Modern reactive UI components
- **STOMP**: WebSocket messaging
- **Liquibase**: Database version control
- **SpotBugs**: Static analysis (CI integration)

## Important Files

- `pom.xml` (root) - Parent POM with dependency management
- `inception/pom.xml` - Main module aggregator
- `inception-app-webapp/pom.xml` - Web application POM
- `Jenkinsfile` - CI/CD pipeline definition
- `CONTRIBUTORS.txt` - Project contributors
- `inception-doc/` - Documentation source (AsciiDoc)

## CI/CD

**Jenkins Pipeline:**
- Triggered on PR and main branch commits
- Stages: Checkout, Info, PR build (merge requests), SNAPSHOT build (main branch)
- Build: `mvn -B -Dmaven.test.failure.ignore=true -T 4 -Pjacoco clean verify javadoc:javadoc`
- Analysis: Maven Console, Java, JavaDoc, SpotBugs, TaskScanner
- JDK 17, Maven 3, parallel builds enabled

## Resources

- **Documentation**: https://inception-project.github.io/documentation/latest/
- **Developer Guide**: Available in `inception/inception-doc/src/main/resources/META-INF/asciidoc/developer-guide/`
- **User Guide**: https://inception-project.github.io/documentation/latest/user-guide
- **Demo Server**: https://morbo.ukp.informatik.tu-darmstadt.de/demo
- **GitHub**: https://github.com/inception-project/inception
- **Issues**: https://github.com/inception-project/inception/issues