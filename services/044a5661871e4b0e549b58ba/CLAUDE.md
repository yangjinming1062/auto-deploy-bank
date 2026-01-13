# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level overview

`keycloak-config-cli` is a command-line tool for managing Keycloak realm configurations in a declarative way using JSON or YAML files. It is a Java application built with Maven and Spring Boot, and it uses the Keycloak Admin Client to interact with the Keycloak API. The configuration files are based on the Keycloak realm export format, allowing you to manage your Keycloak configuration as code.

The tool can be run as a standalone JAR, as a Docker container, or as a Helm chart dependency.

## Code Architecture

The project is structured as a standard Maven project:
- `src/main/java`: Contains the main application source code.
- `src/test/java`: Contains the test source code.
- `pom.xml`: Defines the project's dependencies, build process, and plugins.
- `src/main/resources`: Contains application properties and other resources.
- `src/test/resources`: Contains test-specific resources and configuration files for integration tests.

The application uses the Spring Boot framework, and its configuration is managed through `application.properties` files and command-line arguments.

Integration tests are a key part of this project and are written using [TestContainers](https://www.testcontainers.org/), which allows for running tests against a real Keycloak instance in a Docker container.

## Common Commands

### Building the project

The project uses the Maven wrapper (`mvnw`), so you don't need to have Maven installed on your system. To build the project, run:

```shell
./mvnw verify
```

On Windows, use:

```shell
mvnw.cmd verify
```

### Running the application

To run the application, you need to provide the Keycloak server URL, credentials, and the location of the configuration files.

```shell
java -jar ./target/keycloak-config-cli.jar \
    --keycloak.url=http://localhost:8080 \
    --keycloak.user=admin \
    --keycloak.password=admin123 \
    --import.files.locations=./contrib/example-config/moped.json
```

### Running with Docker

A Docker image is available on [DockerHub](https://hub.docker.com/r/adorsys/keycloak-config-cli). You can run it like this:

```shell
docker run \
    -e KEYCLOAK_URL="http://<your keycloak host>:8080/" \
    -e KEYCLOAK_USER="<keycloak admin username>" \
    -e KEYCLOAK_PASSWORD="<keycloak admin password>" \
    -v <your config path>:/config \
    adorsys/keycloak-config-cli:latest
```

### Running Integration Tests

To run the integration tests, which use TestContainers, a configured Docker environment is required.

```shell
./mvnw verify
```

## Configuration

Configuration can be provided via command-line arguments or environment variables. For a full list of available options, see the `README.md` file.

A key configuration property is `import.files.locations`, which specifies the path to the realm configuration files. This can be a single file, a URL, or an Ant-style pattern to include multiple files.

## Development Notes

- **Variable Substitution**: The tool supports variable substitution in the configuration files, which is disabled by default and can be enabled with `import.var-substitution.enabled=true`. This allows for dynamic configuration using environment variables or other sources.

- **Resource Management**: `keycloak-config-cli` can manage resources in two ways:
    - **Remote State (default)**: It tracks the resources it creates and will only delete resources it manages.
    - **Full Management**: If remote state is disabled, it will delete any resource not present in the configuration files.

    The `import.managed.*` properties can be used to customize this behavior for different resource types. For more details, see `docs/MANAGED.md`.
