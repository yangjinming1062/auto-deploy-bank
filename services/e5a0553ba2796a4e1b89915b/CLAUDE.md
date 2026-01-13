# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **code generator sharing platform** (鱼籽 - 代码生成器共享平台) built as a progressive 3-project learning series:

1. **yuzi-generator-basic** - Local CLI code generator (Picocli + FreeMarker)
2. **yuzi-generator-maker** - Tool for creating custom code generators (with JAR packaging)
3. **yuzi-generator-web-frontend + yuzi-generator-web-backend** - Online sharing platform (React + Spring Boot)

The platform allows developers to create, publish, search, download, and use code generators online.

## Development Commands

### Backend (yuzi-generator-web-backend)

```bash
cd yuzi-generator-web-backend

# Run the application
mvn spring-boot:run

# Build JAR
mvn clean package

# Run tests
mvn test

# Run specific test class
mvn test -Dtest=GeneratorServiceTest

# Package with dependencies (for production)
mvn clean package -DskipTests
```

**Database Setup** (required before running):
- Import `/yuzi-generator-web-backend/sql/create_table.sql` into MySQL
- Update `src/main/resources/application.yml` with your database credentials
- Update Redis, Elasticsearch configurations in `application.yml` if using those features

**API Documentation**: http://localhost:8101/api/doc.html (after starting the application)

### Frontend (yuzi-generator-web-frontend)

```bash
cd yuzi-generator-web-frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Fix linting issues
npm run lint:fix

# Type check
npm run tsc
```

### Maker Tool (yuzi-generator-maker)

```bash
cd yuzi-generator-maker

# Build executable JAR with dependencies
mvn clean package

# Run the generator maker
java -jar target/yuzi-generator-maker-1.0-jar-with-dependencies.jar
```

### Basic Generator (yuzi-generator-basic)

```bash
cd yuzi-generator-basic

# Build executable JAR
mvn clean package

# Run the basic generator
java -jar target/yuzi-generator-basic-1.0-SNAPSHOT-jar-with-dependencies.jar
```

## High-Level Architecture

### Backend Architecture (Spring Boot)

```
yuzi-generator-web-backend/
├── src/main/java/com/yupi/web/
│   ├── annotation/          # Custom annotations (e.g., @AuthCheck)
│   ├── aop/                 # AOP interceptors and filters
│   ├── config/              # Configuration classes
│   │   ├── MyBatisPlusConfig.java    # MyBatis Plus pagination
│   │   ├── CorsConfig.java           # CORS settings
│   │   ├── XxlJobConfig.java         # XXL-JOB scheduling
│   │   ├── CosClientConfig.java      # Tencent Cloud COS
│   │   └── JsonConfig.java           # JSON serialization
│   ├── constant/            # Constants
│   ├── controller/          # REST controllers
│   │   ├── UserController.java
│   │   ├── GeneratorController.java
│   │   └── FileController.java
│   ├── service/             # Business logic layer
│   │   └── impl/            # Service implementations
│   ├── mapper/              # MyBatis data access layer
│   ├── model/               # Data models
│   │   ├── entity/          # Database entities
│   │   ├── dto/             # Data transfer objects
│   │   ├── vo/              # View objects
│   │   └── enums/           # Enums
│   ├── manager/             # Business managers (Redis, COS, etc.)
│   ├── job/                 # XXL-JOB scheduled tasks
│   ├── vertx/               # Vert.x reactive handlers
│   ├── utils/               # Utility classes
│   └── exception/           # Exception handling
```

**Key Technologies**:
- **Database**: MySQL + MyBatis-Plus
- **Cache**: Caffeine (local) + Redis (distributed)
- **Search**: Elasticsearch for full-text search
- **Storage**: Tencent Cloud COS for file storage
- **Scheduling**: XXL-JOB for distributed tasks
- **Reactive**: Vert.x for high-performance request handling
- **Templates**: FreeMarker engine (also used by yuzi-generator-maker)

### Frontend Architecture (React + Ant Design Pro)

```
yuzi-generator-web-frontend/src/
├── pages/
│   ├── Index/               # Homepage with generator search/list
│   ├── Generator/
│   │   ├── Add/             # Create generator page
│   │   │   ├── components/
│   │   │   │   ├── FileConfigForm.tsx    # File configuration
│   │   │   │   ├── ModelConfigForm.tsx   # Model configuration
│   │   │   │   └── GeneratorMaker.tsx     # Generator creation wizard
│   │   │   └── index.tsx
│   │   ├── Detail/          # Generator detail page
│   │   │   └── components/
│   │   │       ├── AuthorInfo.tsx
│   │   │       ├── FileConfig.tsx
│   │   │       └── ModelConfig.tsx
│   │   └── Use/             # Online generator usage page
│   ├── Admin/               # Admin management pages
│   ├── User/
│   │   ├── Login/           # User login
│   │   └── Register/        # User registration
│   └── Test/                # Test pages
├── components/              # Reusable components
│   ├── FileUploader/        # File upload component
│   ├── PictureUploader/     # Image upload component
│   └── RightContent/        # Header components
├── services/
│   └── backend/             # API service layer
└── constants/               # Frontend constants
```

**Key Features**:
- Ant Design Pro components for enterprise UI
- ProComponents for advanced components
- Dynamic form generation based on modelConfig
- File upload/download integration with backend COS
- Code editor for template customization

### Code Generator Maker (yuzi-generator-maker)

```
yuzi-generator-maker/
├── generator/               # Core generation logic
│   ├── file/
│   │   ├── StaticFileGenerator.java      # Static file copying
│   │   ├── DynamicFileGenerator.java     # FreeMarker template generation
│   │   └── FileGenerator.java            # Unified file generator
│   ├── JarGenerator.java                 # JAR packaging
│   ├── ScriptGenerator.java              # Shell script generation
│   └── main/
│       ├── MainGenerator.java            # Main generator orchestrator
│       ├── GenerateTemplate.java         # Template generation
│       └── ZipGenerator.java             # ZIP packaging
├── meta/                    # Metadata management
│   ├── Meta.java            # Meta information model
│   ├── MetaManager.java     # Meta file loader
│   └── MetaValidator.java   # Meta validation
├── template/                # Template maker utilities
│   ├── TemplateMaker.java   # Core template creation logic
│   ├── TemplateMakerUtils.java
│   ├── model/               # Configuration models
│   └── FileFilter.java      # File filtering logic
└── Main.java                # CLI entry point (Picocli)
```

**Key Design Patterns**:
- **Command Pattern**: CLI commands using Picocli
- **Template Method Pattern**: File generation workflow
- **Builder Pattern**: Meta configuration building
- **Strategy Pattern**: Different file generation strategies (static/dynamic)

## Core Concepts

### 1. Metadata (Meta)

Code generators are defined by metadata in JSON format:
```json
{
  "name": "generator-name",
  "description": "description",
  "version": "1.0",
  "author": "author",
  "basePackage": "com.example",
  "models": [...],
  "files": [...]
}
```

### 2. File Configuration

Defines which files to include in the generator:
- Static files (copied directly)
- Dynamic files (processed by FreeMarker templates)

### 3. Model Configuration

Defines user input parameters:
- Model types: String, Boolean, File
- Validation rules
- Default values

### 4. Template Making Process

The maker tool converts an existing project into a generator by:
1. Scanning project files
2. Identifying template variables
3. Creating meta configuration
4. Packaging into distributable generator

## Database Schema

Main entities in `yuzi-generator-web-backend/sql/create_table.sql`:

- **user**: User accounts (admin/user roles)
- **generator**: Code generator definitions
  - `fileConfig`: JSON for file structure
  - `modelConfig`: JSON for user input models
  - `distPath`: Storage location of generated artifacts
  - `status`: Generator status (0=offline, 1=online)

## Key Integration Points

1. **Backend uses yuzi-generator-maker**: The web backend depends on `yuzi-generator-maker` as a library to generate code at runtime
2. **FreeMarker Templates**: Shared across CLI tools and web backend
3. **COS Object Storage**: All generated files and generator artifacts stored in Tencent Cloud COS
4. **Redis Sessions**: Spring Session + Redis for distributed authentication
5. **Elasticsearch Search**: Generators indexed for full-text search capabilities

## Important Configuration Files

- `yuzi-generator-web-backend/src/main/resources/application.yml` - Main configuration
- `yuzi-generator-web-backend/src/main/resources/application-prod.yml` - Production overrides
- `yuzi-generator-web-frontend/src/requestConfig.ts` - API endpoint configuration
- `yuzi-generator-web-frontend/src/constants/index.ts` - Frontend constants

## Development Tips

1. **Database Changes**: After modifying MySQL schema, update corresponding MyBatis-Plus entity classes
2. **Adding New APIs**: Update `GeneratorController.java` and ensure frontend API calls in `services/backend/` are synchronized
3. **FreeMarker Templates**: Place templates in backend resources or use maker tool to generate them
4. **Redis Cache**: Cache keys are defined in constants; be mindful of cache invalidation
5. **XXL-JOB Tasks**: Register new jobs in `job/` directory and configure in `XxlJobConfig.java`
6. **Vert.x Handlers**: For high-performance endpoints, implement in `vertx/` directory

## Testing

- Backend: JUnit 5 tests in `src/test/java/`
- Frontend: Testing Library React (configured but test files not included)
- Run backend tests: `mvn test` in backend directory
- Run specific test: `mvn test -Dtest=ClassName`

## Deployment

1. **Backend**: Build JAR with `mvn clean package`, deploy to server with MySQL/Redis/ES
2. **Frontend**: Build with `npm run build`, serve via Nginx
3. **Database**: Import `sql/create_table.sql`
4. **Dependencies**: Ensure MySQL, Redis, Elasticsearch, XXL-JOB, COS credentials are configured

## Performance Optimizations Implemented

- Caffeine + Redis multi-level caching
- Vert.x reactive programming for hot paths
- Elasticsearch for fast generator search
- XXL-JOB distributed task scheduling
- COS pre-signed URLs for direct client uploads