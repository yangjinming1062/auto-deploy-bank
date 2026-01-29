# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

COMSAT is a set of Java libraries that integrate [Quasar](http://puniverse.github.io/quasar/) (lightweight threads/fibers) with various web and enterprise technologies. It wraps standard APIs (Servlet, JDBC, HTTP clients, etc.) to make them fiber-blocking, enabling high concurrency with few threads.

## Build Commands

```bash
# Build and install to local Maven repository
gradle install

# Full build with tests
gradle build

# Run tests for a specific module
gradle :comsat-servlet:test

# Run a single test class
gradle :comsat-servlet:test --tests "*FiberHttpServletTest"

# Generate Javadoc
gradle javadoc

# Check license headers
gradle licenseMain

# Apply license headers
gradle licenseFormatMain
```

**Note:** Tests require the Quasar javaagent (`-javaagent:path-to-quasar-jar.jar`), which is automatically configured in the test task via `configurations.quasar`.

## Architecture

### Module Organization

This is a multi-module Gradle project with integration modules that wrap standard APIs:

**Web Framework Integrations:**
- `comsat-servlet` - `FiberHttpServlet` extends `HttpServlet` for fiber-per-request servlets
- `comsat-jersey-server` - Jersey `ServletContainer` for fiber-blocking JAX-RS resources
- `comsat-spring:*` - Spring Web MVC, Boot auto-configuration, and Spring Security
- `comsat-dropwizard` - Dropwizard integration with fiber-aware DB and HTTP client

**HTTP Clients:**
- `comsat-httpclient` - `FiberHttpClientBuilder` wraps Apache HttpClient
- `comsat-jax-rs-client` - `AsyncClientBuilder` wraps Jersey JAX-RS client
- `comsat-retrofit` - `FiberRestAdapterBuilder` wraps Retrofit
- `comsat-okhttp` - `FiberOkHttpClient` wraps OkHttp
- `comsat-httpkit` - Clojure Ring HTTP Kit adapter

**Database Access:**
- `comsat-jdbc` - `FiberDataSource` wraps DataSources (JDBC operations run in thread pool)
- `comsat-jdbi` - `FiberDBI` for JDBI
- `comsat-jooq` - jOOQ integration
- `comsat-mongodb-allanbank` - `FiberMongoFactory` for MongoDB

**Web Actors (new API):**
- `comsat-actors-api` - Core Web Actor API (`@WebActor`, `BasicActor`, message types)
- `comsat-actors-netty` - `WebActorHandler`/`AutoWebActorHandler` for Netty
- `comsat-actors-undertow` - `WebActorHandler`/`AutoWebActorHandler` for Undertow
- `comsat-actors-servlet` - Servlet-based deployment via `WebActorInitializer`

**Other Integrations:**
- `comsat-kafka` - `FiberKafkaProducer` for Apache Kafka
- `comsat-shiro` - Apache Shiro realm instrumentation

**Utilities:**
- `comsat-test-utils` - Embedded server helpers (Jetty, Tomcat, Undertow) and test utilities

### Key Patterns

1. **Fiber Wrapping**: Standard blocking APIs are wrapped with fiber-blocking versions (e.g., `FiberHttpServlet` extends `HttpServlet`, `FiberDataSource` wraps `DataSource`)

2. **Suspension**: Methods that use fiber-blocking APIs must be `@Suspendable` (or declare `throws SuspendExecution`)

3. **Instrumentation**: The build uses Quasar's `scanSuspendables` task to generate `META-INF/suspendables` and `META-INF/suspendable-supers` files

4. **Provided Dependencies**: `quasar-core` is listed as `provided` to avoid bundling it with each module

## Branch Strategy

- `master` - Feature improvements and new features
- `release` - Bug fixes only

## Contributing

Sign the [Contributor's Agreement](https://docs.google.com/a/paralleluniverse.co/forms/d/1U5GinUnRsYbvAP5W3-o11wmRkMmicD_WgRDS6Sy30HA/viewform) before submitting PRs.