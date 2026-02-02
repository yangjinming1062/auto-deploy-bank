# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

soap-ws is a lightweight Java library for handling SOAP on a purely XML level. It wraps Spring-WS and enables SOAP message generation and transmission without generating stubs. The library is organized as a multi-module Maven project.

## Build Commands

```bash
# Compile the project
mvn compile

# Build and install to local repository
mvn clean install

# Run all tests
mvn test

# Run a single test class
mvn test -Dtest=ClassName

# Run tests for specific module
mvn test -pl soap-builder

# Run integration tests only
mvn test -pl soap-it

# Skip license header check
mvn install -Dlicense.skip=true

# Run with FindBugs
mvn install -Pfindbugs

# Run with code coverage (Clover)
mvn install -Pclover

# Generate project site
mvn site
```

## Architecture

### Core Modules

- **soap-common** - Common utilities, WSDL parsing core (`Wsdl`), and `SoapContext` configuration
- **soap-legacy** - Extracted soapUI code (LGPL 2.1 license); handles low-level XML/SOAP generation
- **soap-builder** - `SoapBuilder` interface and implementation for generating SOAP XML messages from WSDL operations
- **soap-client** - `SoapClient` for HTTP(S) transmission of SOAP messages; supports SSL, basic auth, proxies
- **soap-server** - `SoapServer` for exposing SOAP endpoints; built on Jetty with Spring-WS integration
- **soap-it** - Integration tests for client-server cooperation
- **soap-examples** - Example projects: quickstart, arquillian, testing
- **soap-test** - Testing utilities and Spock test helpers

### Main Abstractions (Entry Points)

```java
// Parse WSDL and get a builder
Wsdl wsdl = Wsdl.parse("http://example.com/service?WSDL");
SoapBuilder builder = wsdl.binding().localPart("ServiceSoap").find();

// Build a SOAP message
String message = builder.buildInputMessage(operation);

// Create a client and send
SoapClient client = SoapClient.builder()
    .endpointUrl("http://example.com/service")
    .build();
String response = client.post(soapAction, message);

// Create a server
SoapServer server = SoapServer.builder()
    .httpPort(9090)
    .build();
server.registerRequestResponder("/service", new AutoResponder(builder));
```

### Key Design Patterns

- **Fluent builders** - `SoapClient.builder()...build()`, `SoapContext.builder()...build()`
- **Finder pattern** - `wsdl.binding().localPart("X").find()`, `builder.operation().name("Y").find()`
- **Factory methods** - `Wsdl.parse()`, `SoapClient.builder()`, `SoapServer.builder()`
- **Visitor pattern** - `BindingOperationVisitor` for traversing WSDL operations
- **Template method** - `AbstractResponder` handles request matching; subclasses implement `respond()`

### Thread Safety

Core classes (`SoapClient`, `SoapServer`) are annotated with `@ThreadSafe` and are safe for concurrent use.

## Dependencies

- **WSDL4J** - WSDL parsing
- **Apache HttpClient** - HTTP communication
- **Jetty 6** - Embedded server
- **Spring-WS** - SOAP message handling
- **Guava** - Preconditions and utilities
- **Apache Commons** - Lang, IO, Logging, Codec

## Testing

The project uses JUnit 4 for unit tests and Spock (Groovy) for specification-based tests in `soap-it`. Integration tests exercise client-server communication over HTTP, HTTPS, and proxies.

## Configuration

- Java 1.6 source/target compatibility
- Groovy 2.1.2 with GMaven plugin
- OSGi bundle packaging via maven-bundle-plugin

## Notes

- The `soap-legacy` module is licensed under LGPL 2.1; all other modules are Apache 2.0
- `Wsdl.parse()` recursively fetches and resolves imported WSDL/XSD files
- `SoapOperationMatcher` in soap-server handles operation matching via SOAP Action header (SOAP 1.1), RPC namespace patterns, or document type matching
- All core classes (`SoapClient`, `SoapServer`) are annotated with `@ThreadSafe`