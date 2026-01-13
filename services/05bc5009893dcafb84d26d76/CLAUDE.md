# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Build

To build the project from source, use one of the following commands:

* Using Maven:
  ```bash
  mvn clean install
  ```

* Using the Maven wrapper:
  ```bash
  ./mvnw clean install
  ```

* Using Docker:
  ```bash
  ./run-in-docker.sh mvn package
  ```

## Architecture

This is a multi-module Maven project for generating API client libraries, server stubs, and documentation from OpenAPI definitions.

- The core logic for code generation resides in the `modules/openapi-generator` directory.
- The project uses a variety of configuration files (YAML) located in `bin/configs` to customize the generation for different languages and frameworks.
- The `modules/openapi-generator-cli` contains the command-line interface for the tool.
