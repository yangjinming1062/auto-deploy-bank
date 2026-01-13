# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

### Building the Project

```bash
# Build without tests (fastest)
./mvnw clean install -DskipTests -Dmaven.javadoc.skip=true

# Full build with tests
./mvnw clean install

# Run tests only
./mvnw test

# Run specific test
./mvnw test -Dtest=JavaClientCodegenTest

# Run integration tests for a specific language
mvn integration-test -f samples/client/petstore/python/pom.xml
```

### Running the CLI

```bash
# After building, run the CLI
java -jar modules/openapi-generator-cli/target/openapi-generator-cli.jar help

# Generate code from OpenAPI spec
java -jar modules/openapi-generator-cli/target/openapi-generator-cli.jar \
  generate -g java -i <spec-url> -o /path/to/output

# List all generators
java -jar modules/openapi-generator-cli/target/openapi-generator-cli.jar list

# Generate metadata for creating a new generator
./bin/meta-codegen.sh
```

### Testing & CI

```bash
# Regenerate Petstore samples (used for integration tests)
./bin/generate-samples.sh ./bin/configs/python*
./bin/generate-samples.sh ./bin/configs/java*

# Run CI tests including all samples
mvn verify -Psamples

# Test a specific generator
cd samples/client/petstore/java && mvn test
```

## Project Structure

OpenAPI Generator is organized as a Maven multi-module project:

- **modules/openapi-generator** - Core generation engine and all language generators
- **modules/openapi-generator-cli** - Command-line interface (entry point: OpenAPIGenerator.java)
- **modules/openapi-generator-core** - Shared core utilities
- **modules/openapi-generator-gradle-plugin** - Gradle plugin
- **modules/openapi-generator-maven-plugin** - Maven plugin
- **modules/openapi-generator-online** - Web-based generator UI
- **samples/** - Integration test samples for each language

## Architecture Overview

### Core Components

The code generation pipeline follows this flow:

1. **OpenAPIGenerator** (modules/openapi-generator-cli/src/main/java/org/openapitools/codegen/OpenAPIGenerator.java)
   - CLI entry point using Airlift Airline
   - Commands: list, generate, meta, validate, version, completion, batch-generate

2. **DefaultGenerator** (modules/openapi-generator/src/main/java/org/openapitools/codegen/DefaultGenerator.java)
   - Main generation engine that orchestrates the entire process
   - Reads OpenAPI spec, loads generator config, processes templates

3. **CodegenConfig** (modules/openapi-generator/src/main/java/org/openapitools/codegen/CodegenConfig.java)
   - Interface that each language generator implements
   - Defines generator capabilities, options, and behavior

4. **DefaultCodegen** (modules/openapi-generator/src/main/java/org/openapitools/codegen/DefaultCodegen.java)
   - Base implementation with common code generation logic
   - Handles model, operation, and parameter processing

5. **Template Engine**
   - Uses Mustache templating (see modules/openapi-generator/src/main/resources/)
   - Each language has its own template directory

### Language Generators

Each language generator is in `modules/openapi-generator/src/main/java/org/openapitools/codegen/languages/` and typically extends an Abstract base class:

- **Java**: JavaClientCodegen extends AbstractJavaCodegen
- **Python**: PythonClientCodegen extends AbstractPythonCodegen
- **JavaScript**: JavaScriptClientCodegen extends AbstractTypeScriptClientCodegen
- **C#**: CSharpClientCodegen extends AbstractCSharpCodegen
- And many more...

Key files to understand when modifying generators:
- Generator class: `languages/{Language}ClientCodegen.java` or `languages/{Language}ServerCodegen.java`
- Templates: `src/main/resources/{language}/`
- Tests: `src/test/java/org/openapitools/codegen/`

### Templates

All templates use Mustache and are located in `modules/openapi-generator/src/main/resources/`:
- Each language has its own subdirectory
- Common templates in `src/main/resources/_common/`
- Template variables documented at: https://github.com/openapitools/openapi-generator/wiki/Mustache-Template-Variables

### Configuration Loading

See `modules/openapi-generator/src/main/java/org/openapitools/codegen/CodegenConfigLoader.java` for how generator configs are discovered and loaded dynamically.

## Key Development Workflows

### Adding a New Generator

1. Create new generator class extending appropriate Abstract class
2. Add templates in `src/main/resources/{language}/`
3. Register in `CodegenConfigLoader`
4. Test with `./bin/meta-codegen.sh`
5. Update Petstore samples in `bin/configs/`
6. Add integration tests in `samples/`

### Modifying an Existing Generator

1. Find the generator class in `languages/`
2. Update the generator Java code and/or templates
3. Regenerate samples: `./bin/generate-samples.sh ./bin/configs/{language}*`
4. Run integration tests: `mvn integration-test -f samples/client/petstore/{language}/pom.xml`
5. Review generated changes and commit

### Testing

- **Unit tests**: `modules/openapi-generator/src/test/java/org/openapitools/codegen/`
- **Template tests**: Regenerate and commit sample changes
- **Integration tests**: `samples/` directory with language-specific tests
- **CI**: `mvn verify -Psamples` (requires all language tools installed)

## Code Style & Conventions

- Java: Follows [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- Checkstyle: Configuration in `google_checkstyle.xml`
- SpotBugs: Configuration in `spotbugs-exclude.xml`
- Each language should follow its own community style guide (see CONTRIBUTING.md for links)

## Important Resources

- [Contributing Guidelines](CONTRIBUTING.md)
- [OpenAPI Generator Wiki](https://github.com/openapitools/openapi-generator/wiki)
- [Migration from Swagger Codegen](docs/migration-from-swagger-codegen.md)
- [New Generator Guide](https://openapi-generator.tech/docs/new-generator)
- [Integration Tests Wiki](https://github.com/OpenAPITools/openapi-generator/wiki/Integration-Tests)

## Security Note

⚠️ When generating code from untrusted sources, review inputs carefully to avoid potential code injection vulnerabilities. Report security issues to team@openapitools.org.
