# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a tutorial project demonstrating mutual TLS (mTLS) authentication in Java. It contains a Spring Boot server and a client module that tests 40+ HTTP clients (Java, Kotlin, Scala, Groovy) with various SSL/TLS configurations.

## Build Commands

```bash
# Build all modules
mvn clean install

# Run single module
cd server/ && mvn spring-boot:run
cd client/ && mvn exec:java

# Run with Maven wrapper (Java 21 not required locally)
./mvnw clean install
./mvnw spring-boot:run

# Skip tests
mvn clean install -DskipTests

# Run specific test class
mvn test -Dtest=ShouldReturnHello
mvn test -Dtest=ClientRunnerIT
```

## Authentication Profiles

This project uses Maven profiles to configure different TLS authentication modes:

```bash
# No encryption
mvn clean install -Pwithout-authentication

# Server validates client certificate (one-way TLS)
mvn clean install -Pwith-one-way-authentication

# Mutual TLS with CA-signed certificates
mvn clean install -Pwith-two-way-authentication-by-trusting-root-ca

# Mutual TLS with direct certificate trust
mvn clean install -Pwith-two-way-authentication-by-trusting-each-other
```

## Architecture

### Multi-Module Maven Project

- **server/** - Spring Boot application exposing `/api/hello` endpoint on port 8080 (HTTP) or 8443 (HTTPS)
- **client/** - Integration tests demonstrating SSL/TLS configuration for 40+ HTTP clients

### Key Concepts

- **SSLFactory** (from `ayza` library) - Central SSL configuration builder; all clients derive their SSL context from this
- **KeyStore** - Contains private key and certificate (identity)
- **TrustStore** - Contains trusted certificates (used to verify counterparties)
- **One-way TLS** - Only server presents a certificate; client validates it
- **Two-way TLS (mTLS)** - Both server and client present certificates; mutual validation

### Key Files

- `client/src/main/java/nl/altindag/client/SSLConfig.java` - Creates SSLFactory bean based on application.yml
- `client/src/main/java/nl/altindag/client/ClientConfig.java` - Configures 40+ HTTP client instances with SSL
- `client/src/main/java/nl/altindag/client/service/` - Individual HTTP client implementations (Apache, JDK, OkHttp, Retrofit, etc.)

## Dependencies

- **Spring Boot 3.5.3** - Server framework
- **ayza (SSLContext Kickstart)** - SSL/TLS configuration abstraction
- **Cucumber 7.23.0** - BDD integration tests
- **JaCoCo** - Code coverage (run with `-Pjacoco`)

## Configuration

Server and client SSL properties are in their respective `application.yml` files. Key properties include:

```yaml
server.ssl.enabled: true/false
server.ssl.key-store: classpath:identity.jks
server.ssl.client-auth: need/want/none
client.ssl.two-way-authentication-enabled: true/false
client.ssl.trust-store: truststore.jks
```

## Testing

Integration tests are Cucumber-based (`.feature` files). Run the full integration test suite:

```bash
mvn verify
```

This starts the server, runs client tests against it, and generates Cucumber reports in `target/test-report/`.