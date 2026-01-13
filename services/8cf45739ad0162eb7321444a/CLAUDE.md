# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Google Cloud Java Client Libraries** monorepo, containing Java idiomatic client libraries for Google Cloud Platform services. The repository contains:

- **200+ individual client libraries** (e.g., `java-translate`, `java-storage`, `java-bigquery`)
- Each library is a Maven module with its own `pom.xml`
- Generated client libraries following GAPIC (gRPC API Client) architecture
- Code generation infrastructure using OwlBot

## High-Level Architecture

### Repository Structure

```
google-cloud-java/
├── pom.xml                                    # Root aggregator POM (not released)
├── google-cloud-pom-parent/                  # Parent for parent POMs
├── google-cloud-jar-parent/                  # Root parent for all client modules
├── gapic-libraries-bom/                      # BOM for non-preview libraries
├── generation/                               # Code generation scripts and configs
│   ├── generation_config.yaml               # Master config for all libraries
│   ├── apply_versions.sh                    # Updates versions across modules
│   └── ...
├── java-*/                                  # Individual client libraries (200+)
│   ├── google-cloud-{service}/              # Main client library
│   ├── proto-google-{service}/              # Generated protobuf classes
│   ├── grpc-google-{service}/               # Generated gRPC stubs
│   ├── samples/                             # Usage examples
│   └── owlbot.py                            # Library-specific generation rules
└── .github/workflows/                       # CI/CD pipelines
```

### POM Hierarchy

1. **Root POM** (`/pom.xml`): Aggregates all modules, not released
2. **google-cloud-pom-parent**: Parent for parent POMs, minimal configuration
3. **google-cloud-jar-parent**: Root parent for all client modules
   - Contains common build configuration
   - Manages non-annotated dependency versions
4. **Individual library POMs**: Each service has its own module POM

### Code Generation Flow

Libraries are generated using **OwlBot**:
- **owlbot.py**: Python script per library that moves generated files and applies fixes
- **generation_config.yaml**: Defines which APIs to generate and their metadata
- **.OwlBot-hermetic.yaml**: Configuration for hermetic (isolated) builds
- **Staging dirs**: Generated code is placed in staging directories before being moved

The generation process:
1. Protobuf definitions → proto-google-cloud-{service}
2. gRPC stubs → grpc-google-cloud-{service}
3. Client library → google-cloud-{service}
4. Post-processing via owlbot.py

## Development Commands

### Prerequisites

**Required**: Application Default Credentials (ADC) for running tests
```bash
# Generate a service account key in GCP console and set:
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

### Build & Test

**Build the entire monorepo:**
```bash
mvn install -B -ntp -T 1C
```

**Run unit tests (skip integration tests):**
```bash
mvn test -B -ntp -DskipITs
```

**Run tests for a specific library:**
```bash
cd java-translate
mvn test -B -ntp
```

**Run integration tests:**
```bash
# Integration tests require credentials and take significant time
mvn verify -B -ntp
```

**Format code:**
```bash
mvn com.spotify.fmt:fmt-maven-plugin:format
```

**Run linter (Checkstyle):**
```bash
mvn checkstyle:check@checkstyle
```

**Run enforcer (dependency rules):**
```bash
mvn enforcer:enforce@enforce
```

### Testing Different Java Versions

Tests run on multiple Java versions (8, 11, 17, 21, 25) via CI:
```bash
# Test with specific Java version
export JAVA_HOME=/path/to/java11
mvn test -B -ntp
```

### Release Management

**Update versions across all modules:**
```bash
# Uses versions.txt to track released vs current versions
cd generation
./apply_versions.sh
```

**Check for existing release versions:**
```bash
cd generation
./check_existing_release_versions.sh
```

## Library Structure

Each client library follows a standard structure:

```
java-translate/
├── google-cloud-translate/          # Main client library
│   ├── src/main/java/
│   │   └── com/google/cloud/translate/
│   │       ├── v3/                  # v3 API
│   │       └── v3beta1/             # beta API
│   └── pom.xml                      # Library-specific POM
├── proto-google-cloud-translate-v3/ # Generated protobuf classes
├── grpc-google-cloud-translate-v3/  # Generated gRPC stubs
├── samples/                         # Usage examples
├── owlbot.py                        # Generation post-processing
└── pom.xml                          # Module POM (aggregates submodules)
```

### Key Library Components

- **ServiceClient**: Main entry point for each service
- **Settings**: Configuration for the client (timeouts, retries, etc.)
- **Paged APIs**: For list operations with pagination
- **Request/Response classes**: Protobuf-based messages
- **Callable interfaces**: For custom RPC operations

## CI/CD Pipeline

### GitHub Actions (`.github/workflows/ci.yaml`)

**Unit Tests**: Runs on Java 8, 11, 17, 21, 25
**Windows Tests**: Separate job for Windows compatibility
**Linting**: Code format and Checkstyle validation
**Enforcer**: Dependency rule validation
**BOM Validation**: Validates gapic-libraries-bom

### Kokoro CI (`.kokoro/build.sh`)

Internal Google CI system that runs:
- Unit tests
- Integration tests
- GraalVM tests (native image compatibility)
- Lint checks

JOB_TYPE options:
- `test`: Unit tests
- `integration`: Integration tests
- `graalvm`/`graalvm-presubmit`: Native image tests
- `lint`: Code formatting and style checks

## Common Development Tasks

### Making Changes to Multiple Libraries

Use generation scripts in `/generation/`:
- **`readme_update.sh`**: Updates README files across modules
- **`set_owlbot_config.sh`**: Updates OwlBot configuration
- **`update_owlbot_postprocessor_config.sh`**: Updates post-processor configs

### Working with Generated Code

**DO NOT edit generated files directly:**
- `proto-google-*`: Protobuf generated code (DO NOT MODIFY)
- `grpc-google-*`: gRPC stubs (DO NOT MODIFY)
- Client code in `google-cloud-*/src/main/java/com/google/cloud/{service}/` (mostly generated)

**DO edit:**
- `owlbot.py`: Post-processing rules
- Manual additions in `google-cloud-*/src/main/java/` with `// [START] custom` markers
- `samples/`: Example code
- Tests and documentation

### Adding a New Library

See `generation/SUPPORTING_NEW_SERVICES.md` for full guidelines. Quick overview:

1. Add entry to `generation_config.yaml`
2. Create directory `java-{service}/`
3. Add `owlbot.py` for post-processing
4. Run generation pipeline
5. Update documentation and tests

### Version Management

**versions.txt** tracks released vs current versions:
```
module:released-version:current-version
google-cloud-storage:2.1.0:2.2.0-SNAPSHOT
```

## Coding Standards

- **Style**: Follow [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- **Code formatting**: Use `fmt-maven-plugin` (configured in POMs)
- **API Stability**:
  - `@BetaApi`/`@Experimental`: Can change between minor releases
  - `@InternalApi`: Technically public, treat as private
  - `@InternalExtensionOnly`: Public interface, internal implementation only
- **Versioning**: Follow Semantic Versioning with additional qualifications (see README.md)

## Testing Requirements

**Unit Tests**: Fast, no external dependencies
**Integration Tests**: Real service calls, slow, require:
- `GOOGLE_APPLICATION_CREDENTIALS` set
- Enabled GCP APIs
- Test project with billing

**Test locations:**
- Library-specific: `java-{service}/google-cloud-{service}/src/test/java/`
- Common test utilities in `google-cloud-jar-parent`

## Release Process

Libraries are released using **Release Please**:
- Automated changelog generation
- Version bumps based on conventional commits
- Published to Maven Central via Sonatype

## Authentication for Development

Required for integration tests and some unit tests:

1. Create service account in GCP Console
2. Download JSON key
3. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
   ```

**DO NOT use production projects for testing**

## Key Configuration Files

- **`generation_config.yaml`**: Defines all libraries, APIs, and release levels
- **`versions.txt`**: Tracks version history across modules
- **`owlbot.py`**: Per-library code generation rules
- **`.OwlBot-hermetic.yaml`**: Hermetic build configuration
- **`.repo-metadata.json`**: Repository metadata for each library
- **`gapic-libraries-bom/pom.xml`**: BOM for dependency management

## Important Notes

- Libraries are **auto-generated** from API definitions
- Most code in client libraries is **generated**, not hand-written
- Changes to generated code should be made via OwlBot post-processing
- Each library is released **independently** with its own version
- The root POM is **never released**
- Integration tests are **expensive** (real API calls) - skip with `-DskipITs`
- Tests require **active GCP project** with appropriate APIs enabled