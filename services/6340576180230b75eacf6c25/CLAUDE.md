# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

This is the **Google Cloud Platform Java Samples** repository containing 70+ modules demonstrating various Google Cloud services. Each module is a standalone sample project with Maven build configuration.

**Java Versions:** Java 8, 11, 17, 21 (Java 11/17 enforced for CI, Java 8/21 tested periodically)
**License:** Apache License 2.0
**Primary Build System:** Maven

## Common Development Commands

### Prerequisites
```bash
# Set your GCP project (required for most tests)
export GOOGLE_CLOUD_PROJECT=your-project-id
# or
export GOOGLE_SAMPLES_PROJECT=your-project-id

# Set up authentication (Application Default Credentials)
gcloud auth application-default login
```

### Build, Lint, and Test

**Via Makefile (recommended):**
```bash
make build                    # Compile code
make test                     # Run all tests (requires project ID + ADC)
make lint                     # Run Checkstyle linting
make check-env               # Verify environment variables

# Run in specific directory
make lint build dir=translate/snippets
make test dir=bigquery/bigqueryconnection/snippets
```

**Via Maven (module-specific):**
```bash
cd module-name
mvn compile                   # Compile code
mvn test                      # Run unit tests
mvn verify                    # Run integration tests
mvn -P lint checkstyle:check  # Run linting
mvn clean verify              # Full clean build and test

# Run single test class
mvn test -Dtest=ClassNameIT

# Run single test method
mvn test -Dtest=ClassNameIT#methodName
```

**Special cases:**
- **Functions module:** `cd functions && find */pom.xml | xargs -I {} dirname {} | xargs -I {} sh -c "cd {} && mvn clean verify"`

### Testing Requirements

**Environment Variables:**
- `GOOGLE_CLOUD_PROJECT` or `GOOGLE_SAMPLES_PROJECT` (required)
- `GOOGLE_APPLICATION_CREDENTIALS` (optional, for service account auth)

**Test Framework:**
- JUnit 4 + Google Truth
- Integration tests (suffix `IT`) using Maven Failsafe
- Unit tests using Maven Surefire

**Test Best Practices (enforced in SAMPLE_FORMAT.md):**
- Use **UUIDs** for resource names to enable parallel execution
- Clean up resources in `finally` blocks or `@After`/`@AfterClass`
- Pass infrastructure via environment variables
- **No mocks** for external services (tests verify sample logic, not API correctness)
- Use `MultipleAttemptsRule` for flaky tests

## Repository Structure

### Core Directories

The repository contains **70+ independent service modules**:

**Major Service Modules:**
- `aiplatform/` - Vertex AI and machine learning
- `bigquery/` - Data warehouse queries and ETL
- `bigtable/` - NoSQL wide-column database
- `compute/` - Compute Engine instances and networking
- `dataflow/` - Stream/batch data processing
- `dlp/` - Data loss prevention
- `functions/` - Cloud Functions serverless
- `kms/` - Key management and encryption
- `language/` - Natural language processing
- `pubsub/` - Message queuing and pub/sub
- `run/` - Cloud Run serverless containers
- `spanner/` - Global SQL database
- `storage/` - Object storage and file management
- `translate/` - Language translation
- `vision/` - Image analysis and OCR

**Infrastructure:**
- `.github/` - GitHub Actions workflows (auto-approve, label, snippet-bot)
- `.kokoro/` - Internal Google CI/CD configs for Java 8/11/17/21
- `unittests/` - Shared test utilities
- `pom.xml` (parent) - Shared dependency management

### Standard Module Structure

```
service-name/
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/google/samples/
│   │           ├── Quickstart.java         # Minimal working example
│   │           ├── Create操作.java         # CRUD operation examples
│   │           ├── List操作.java
│   │           └── Update操作.java
│   └── test/
│       └── java/
│           └── com/google/samples/
│               ├── QuickstartTest.java     # Unit tests
│               ├── Create操作IT.java       # Integration tests
│               └── List操作IT.java
├── pom.xml
└── README.md                                # Module-specific docs
```

**Sample Types:**
- **Quickstart** - Minimal example demonstrating basic usage
- **Operation samples** - CRUD operations (Create, Read, Update, Delete, List)
- **Snippets** - Focused code examples for specific features

## Code Architecture Patterns

### Dependency Management
- **Google Cloud Libraries BOM** (Bill of Materials) for consistent versioning
- Parent POM: `com.google.cloud.samples:shared-configuration:1.2.0`
- Service-specific client libraries per module

### Java Standards
- **Source Structure:** Maven standard layout (`src/main/java`, `src/test/java`)
- **Package Naming:** `com.google.samples.{service-name}`
- **Class Structure:** Each sample is a standalone class with `main()` method
- **Java 11+ features:** Avoid `var` keyword in API/client library samples (reviewer discretion)

### Key Design Principles (from SAMPLE_FORMAT.md)

**Copy-paste-runnable:** Samples should run with minimal modifications
**Teach through code:** Demonstrate best practices and proper usage
**Idiomatic:** Follow Java best practices and Google Cloud conventions

**Code Structure:**
- **Arrange-Act-Assert** pattern in tests
- Clear exception handling with meaningful messages
- Client initialization patterns documented in samples
- Modern Java features (lambdas, streams) encouraged where appropriate

## Testing Architecture

### Integration Test Structure
Most samples use **integration tests** (`*IT.java`) which verify:
1. Code compiles successfully
2. Sample runs without errors
3. Correct interaction with Google Cloud service
4. Resource cleanup

**Example test pattern:**
```java
@RunWith(JUnit4.class)
public class CreateResourceIT {
  @Rule
  public final MultipleAttemptsRule multipleAttemptsRule = new MultipleAttemptsRule(5);

  @Test
  public void createResource_shouldCreateSuccessfully() throws Exception {
    // Test logic using UUID for resource names
    // Clean up in finally block or @After
  }
}
```

### Test Execution Pipeline (Kokoro CI)
- **Internal CI:** `.kokoro/tests/run_tests.sh`
- **Java versions:** 8, 11, 17, 21 (11/17 required for merge)
- **Tool:** `btlr` (Build Tool Lint Runner)
- **Environment:** Application Default Credentials required

## Documentation Hierarchy

1. **Root README.md** - Project overview and setup
2. **SAMPLE_FORMAT.md** - Comprehensive Java coding standards (20KB guide)
3. **CONTRIBUTING.md** - Contribution guidelines
4. **Module README.md** - Service-specific instructions (API enablement, IAM, resources)
5. **Inline code comments** - Implementation details and rationale

**Critical Documentation Sections:**

**SAMPLE_FORMAT.md covers:**
- Java version requirements (8, 11+)
- Code structure (Arrange-Act-Assert)
- Exception handling best practices
- Client initialization patterns
- Modern Java features (lambdas, streams)
- Testing requirements and patterns
- Package naming conventions

## Common Workflows

### Adding a New Sample
1. Create module directory structure (`src/main/java`, `src/test/java`)
2. Write sample following SAMPLE_FORMAT.md guidelines
3. Add integration test with proper cleanup
4. Update module README.md with requirements
5. Ensure Apache 2.0 license header in all files
6. Test locally with `make test dir=module-path`

### Running Specific Tests
```bash
# All tests in a module
make test dir=module-name

# Single test class
cd module-name && mvn test -Dtest=ClassNameIT

# Multiple test classes
mvn test -Dtest='*IT'

# With specific log level
mvn test -Dorg.slf4j.simpleLogger.defaultLogLevel=info
```

### CI/CD Process
1. **PR triggers:** Kokoro CI runs on Java 11/17
2. **Required checks:** Build, test, lint (Checkstyle)
3. **Auto-merge:** RenovateBot updates dependencies
4. **Code review:** Requires both product stakeholder and `java-samples-reviewers`

## Important Notes

- **No Cursor/Claude-specific rules** exist - standard GitHub workflow
- **Multi-version support:** Each module tested across Java 8, 11, 17, 21
- **Resource management:** Always clean up cloud resources in tests
- **Parallel execution:** Tests must support concurrent execution
- **No hardcoded credentials:** Use environment variables or ADC
- **UUID usage:** Required for all resource names to prevent conflicts

## Service-Specific Patterns

**BigQuery:**
- Uses `bigtable.projectID` and `bigtable.instanceID` system properties
- Datasets created/deleted per test with UUID naming

**Cloud SQL:**
- Requires additional environment variables (documented in module README)
- Connection tests use embedded databases or test containers

**Pub/Sub:**
- Topics/subscriptions created with UUIDs
- Clean up in `@AfterClass` to ensure deletion even on test failure

**Storage:**
- Buckets created per test with random UUIDs
- Objects uploaded/deleted with proper cleanup

**Functions:**
- Multiple deployment targets (gen1, gen2)
- Integration tests deploy actual functions