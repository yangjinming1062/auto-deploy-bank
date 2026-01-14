# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build System

This project uses Maven (Java 17).

### Building
```bash
mvn install -DskipUnitTests=false -DskipIntegrationTests=false
```

### Running Tests
Unit Tests and Integration Tests are disabled by default. Tests run automatically for PRs and commits.

- **Run all tests:**
  ```bash
  mvn install -DskipUnitTests=false -DskipIntegrationTests=false
  ```
- **Run only Unit Tests:**
  ```bash
  mvn test -DskipUnitTests=false
  ```
- **Run a specific Unit Test class:**
  ```bash
  mvn test -DskipUnitTests=false -Dtest=[full.package.testClassName] -DfailIfNoTests=false
  ```
- **Run only Integration Tests:**
  ```bash
  mvn install -DskipIntegrationTests=false
  ```
- **Run a specific Integration Test class:**
  ```bash
  mvn install -DskipIntegrationTests=false -Dit.test=[full.package.testClassName] -DfailIfNoTests=false
  ```

### Code Quality
- **Checkstyle:** Validates code style based on `checkstyle.xml` (runs automatically during build/verify).
  ```bash
  mvn checkstyle:check
  ```

## Project Architecture

DSpace is a multi-module Maven project providing a backend REST API and several machine interfaces (OAI-PMH, SWORD, RDF, etc.).

### Key Modules
- **dspace-api:** Contains the core domain models (Site, Community, Collection, Item, Bundle, Bitstream), business logic, services, and DAOs. Uses Hibernate/JPA for persistence.
- **dspace-services:** Core services and configuration.
- **dspace-server-webapp:** The REST API and main web application. Built as a WAR file.
- **dspace-oai:** OAI-PMH interface.
- **dspace-sword / dspace-swordv2:** SWORD deposit interfaces.
- **dspace-rdf:** RDF data provider.
- **dspace-iiif:** IIIF presentation API.
- **dspace-saml2:** SAML 2 authentication.

### Key Patterns & Conventions
- **Entities:** Domain classes (Item, Collection, etc.) are located in `dspace-api/src/main/java/org/dspace/content` and annotated with `@Entity`.
- **Service Layer:** Business logic is typically encapsulated in `*Service` classes (e.g., `CollectionService`). Data access objects (DAOs) handle persistence interactions.
- **REST API:** Controllers are in `dspace-server-webapp`. The API uses Spring MVC and Spring HATEOAS.
- **Configuration:** Uses Spring Boot configuration (`application.properties` / `yaml`) and DSpace-specific XML configuration.

### Tech Stack
- **Language:** Java 17
- **Framework:** Spring Boot 3 / Spring Framework 6
- **ORM:** Hibernate 6 / JPA
- **Database:** PostgreSQL (H2 for tests)
- **Search:** Apache Solr
- **Build:** Maven

### Testing
- **Unit Tests:** Run using `maven-surefire-plugin`. Located in `src/test/java`. Usually use H2 in-memory database.
- **Integration Tests:** Run using `maven-failsafe-plugin`. Typically require a running PostgreSQL and Solr instance. Can also be tested using Docker Compose.

### Documentation
- **Contribution Guidelines:** See `CONTRIBUTING.md`.
- **REST API Contract:** https://github.com/DSpace/RestContract
- **DSpace Wiki:** https://wiki.lyrasis.org/display/DSPACE/