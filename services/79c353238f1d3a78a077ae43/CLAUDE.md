# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Drools is an open-source rule engine, [DMN engine](https://kie.apache.org/docs/components/drools/drools_dmn) and complex event processing (CEP) engine for Java™ and the JVM Platform. This is a large Maven-based project with 40+ modules, containing:

- **Drools**: Forward-chaining and backward-chaining inference-based rules engine
- **KIE DMN**: Decision Model Notation (DMN) engine implementation
- **KIE PMML**: Predictive Model Markup Language support
- **Efesto**: Clean Architecture-based compilation and runtime framework

## Build System

This project uses Maven as the primary build system with a Makefile wrapper for convenience.

### Common Commands

```bash
# Full build
make build
# or
mvn clean install

# Quick build (uses -Dquickly)
make build-quickly

# Run all tests
make test
# or
mvn clean verify

# Run unit tests only
make quick-test
# or
mvn clean verify -DquickTests

# Clean project
make clean

# Deploy to repository
make deploy

# Execute specific Maven command
make mvn cmd="<your-mvn-command>"

# Show project dependencies
make tree
```

### Important Build Notes

- **Encoding**: If build fails with `UnmappableCharacterException`, set `-Dfile.encoding=UTF-8` for `MAVEN_OPTS`:
  ```bash
  export MAVEN_OPTS=-Dfile.encoding=UTF-8
  mvn clean install
  ```

- **Locale-specific tests**: Some tests require en_US locale. Use one of these profiles:
  ```bash
  make test -Ptest-en
  # or
  make test -DTestEn
  ```

- **New DRL Parser**: A new Antlr4-based DRL parser is under development. Enable with:
  ```bash
  mvn clean install -DenableNewParser
  ```

### Build Profiles

- `fullProfile`: Includes drools-distribution module
- `reproducible`: Enables reproducible build checks
- `rewrite`: OpenRewrite-based refactoring (JUnit4 to JUnit5 migration)
- `enableNewParser`: Activates the new Antlr4-based DRL parser
- `test-en`: For non-en_US locales

## Architecture

### High-Level Structure

The project follows a modular architecture with clear separation of concerns:

1. **Core Engine** (`drools-*` modules)
   - `drools-core`: Core rule engine implementation
   - `drools-drl`: DRL (Drools Rule Language) parser and compilation
   - `drools-compiler`: Rule compiler
   - `drools-kiesession`: KieSession implementation
   - `drools-mvel`: MVEL dialect support (deprecated)

2. **DMN Engine** (`kie-dmn` modules)
   - Contains the DMN (Decision Model Notation) engine
   - Includes FEEL (Friendly Enough Expression Language) implementation
   - Supports both interpreted and code-generated execution
   - See `kie-dmn/Developer_Guide.md` for detailed architecture

3. **Efesto Framework** (`efesto` modules)
   - Clean Architecture-based compilation and runtime framework
   - Plugin-style architecture with clear separation between compilation and runtime
   - See `efesto/EfestoDeveloperGuide.md` for plugin development

4. **Additional Components**
   - `kie-pmml-trusty`: PMML (Predictive Model Markup Language) support
   - `kie-drl`: KIE-specific DRL integration
   - `kie-ci`: Maven integration for KIE projects
   - `kie-maven-plugin`: Maven plugin for KIE projects

### Key Architectural Patterns

**Efesto Clean Architecture:**
- Core components (`efesto-core`) have zero knowledge of plugins
- Plugins implement `KieCompilerService` (compilation) and/or `KieRuntimeService` (runtime)
- Plugins are discovered via Java ServiceLoader (SPI)
- Results are stored in `IndexFile.{model}_json` format
- See `efesto/EfestoDeveloperGuide.md` for plugin development guidelines

**DMN Execution Modes:**
- **Interpreted**: Static interpretation of AST (Abstract Syntax Tree)
- **Code-Generated**: Dynamic code generation for better performance
- Controlled via `DoCompileFEELProfile` or `CompilerContext.setDoCompile(true)`

**DRL Parser (Active Development):**
- **Old Parser**: Antlr3-based, hard to maintain (under `drools-drl-parser/lang/`)
- **New Parser**: Antlr4-based, cleaner architecture (under `drools-drl-parser/antlr4/`)
- Toggle via system property: `drools.drl.antlr4.parser.enabled`
- See `drools-drl/drools-drl-parser/Developer_Notes.md`

## Development Workflow

### Testing

```bash
# Test a specific module
cd drools-core
mvn test

# Test with coverage
mvn clean verify -Djacoco.skip=false

# Run specific test class
mvn test -Dtest=ClassName

# Run specific test method
mvn test -Dtest=ClassName#methodName
```

### Code Quality

```bash
# Check for split package violations
./check-split-packages.sh

# Run OpenRewrite refactoring
mvn rewrite:run
```

### CI/CD

The project uses:
- **GitHub Actions**: Pull request validation (`/.github/workflows/`)
- **Jenkins**: Downstream build validation
- Build chain configured in `/.ci/pull-request-config.yaml`

## Module Guide

### Core Drools Modules

- **`drools-core`**: Core engine, working memory, rule execution
- **`drools-drl-parser`**: DRL language parser (both old and new)
- **`drools-compiler`**: Knowledge builder, compilation of DRL to executable models
- **`drools-kiesession`**: Stateful and stateless session implementations
- **`drools-model`**: Executable model representation

### DMN Modules

- **`kie-dmn-model`**: DMN model definitions
- **`kie-dmn-feel`**: FEEL language implementation
- **`kie-dmn-core`**: DMN engine core
- **`kie-dmn-validation`**: DMN model validation

### Other Notable Modules

- **`kie-pmml-trusty`**: PMML model compilation and execution
- **`drools-quarkus-extension`**: Quarkus integration
- **`drools-test-coverage`**: Test coverage framework
- **`drools-examples`**: Example applications

## Important Resources

- **Project Website**: https://kie.apache.org/docs/components/drools/
- **Documentation**: https://kie.apache.org/docs/documentation/
- **Developer Mailing List**: dev@kie.apache.org
- **GitHub Issues**: https://github.com/apache/incubator-kie-issues/issues

## Development Tips

1. **PlantUML Diagrams**: Architectural diagrams use PlantUML (`.puml` files)
   - IntelliJ IDEA: PlantUML Integration plugin
   - Eclipse: PlantUML plugin
   - VSCode: PlantUML extension

2. **IDE Setup**:
   - Enable annotation processing for Lombok
   - Configure UTF-8 encoding
   - Set up Maven wrapper or use system Maven 3.9.6+

3. **Parser Development**:
   - Use IntelliJ's ANTLR4 plugin for grammar debugging
   - The `dev-new-parser` branch contains the new Antlr4-based parser work
   - See `drools-drl/drools-drl-parser/Developer_Notes.md` for contribution guidelines

4. **DMN Development**:
   - DMN models are XML-based (`.dmn` files)
   - Test files are in `kie-dmn/kie-dmn-test-resources/`
   - See `kie-dmn/Developer_Guide.md` for detailed execution flow

## Common Pitfalls

1. **Test Failures on Non-en_US Systems**: Use `-Ptest-en` or `-DTestEn` profile
2. **Encoding Issues**: Always set `MAVEN_OPTS=-Dfile.encoding=UTF-8`
3. **Parser Tests**: The new parser is incomplete; expect failures in `dev-new-parser` branch
4. **Module Dependencies**: Check `Makefile` targets for common build chains
5. **Maven Memory**: Increase heap if build fails with OOM: `MAVEN_OPTS="-Xmx4g"`

## Troubleshooting

```bash
# Clean build with fresh dependencies
make clean
rm -rf ~/.m2/repository/org/kie/
make build

# Check dependency tree for conflicts
make tree

# Show git changes
make show-diff

# Update Quarkus version
make update-quarkus quarkus_version=<version>

# Prepare environment for specific tool
make prepare-env environment=<name>
```