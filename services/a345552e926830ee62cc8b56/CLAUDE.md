# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Payara Platform Community Edition is a Jakarta EE 11 application server and MicroProfile 6.1 runtime, forked from Eclipse GlassFish. It comprises three main components:

- **api/** - Public APIs and Bill of Materials for dependency management
- **nucleus/** - Core kernel (minimal embeddable runtime with HK2 DI, Grizzly NIO, module system)
- **appserver/** - Full Jakarta EE application server (web, EJB, JMS, JPA, security, transactions, etc.)

## Build Commands

```bash
# Full build (skip tests)
mvn -DskipTests clean package

# Quick build (used in CI)
mvn -B -V -ff -e clean install --strict-checksums \
  -PQuickBuild,BuildEmbedded,jakarta-staging \
  -Djavac.skip -Dsource.skip

# Build with javadoc
mvn clean install -Pjavadoc

# Generate source JARs
mvn clean install -Psource
```

## Test Commands

```bash
# Quicklook integration tests
mvn -B -V -ff -e clean test --strict-checksums -Pall,jakarta-staging \
  -f appserver/tests/quicklook/pom.xml

# Payara samples tests (requires Playwright)
mvn -V -B -ff clean install --strict-checksums \
  -Ppayara-server-remote,playwright -f appserver/tests/payara-samples

# MicroProfile TCK tests
mvn -B -V -ff -e clean verify --strict-checksums \
  -Ppayara-server-remote,full -f MicroProfile-Config
```

## Development

**Distribution output paths:**
- Payara Server: `appserver/distributions/payara/target/payara.zip`
- Payara Micro: `appserver/extras/payara-micro/payara-micro-distribution/target/payara-micro.jar`

**Debugging Payara Server:**
```bash
# After building, start with debug mode
cd appserver/distributions/payara/target/stage/payara7/glassfish
./asadmin start-domain --verbose --debug
# Attach debugger on port 9009
```

**Single module development:** Build the modified module and copy the JAR to `glassfish/modules` in your staged installation, then restart the server.

**Java version:** Requires JDK 21 (update Maven compiler source/target to 21 in pom.xml if different).

## Architecture

```
nucleus/          → Core kernel (HK2 DI, Grizzly NIO, config, admin, clustering)
    admin/        → REST/CLI administration
    hk2/          → Dependency injection framework
    grizzly/      → Network I/O layer

appserver/        → Jakarta EE application server
    web/          → Servlet/JSP container
    ejb/          → Enterprise JavaBeans
    persistence/  → JPA providers (EclipseLink)
    security/     → JACC, JAAS, JASPIC providers
    transaction/  → JTA transaction manager
    admingui/     → Admin console (JSF/Mojarra)
    distributions/payara/        → Full server distribution
    extras/payara-micro/         → Microservices runtime
    payara-appserver-modules/    → MicroProfile implementations
        openapi/, health/, metrics/, config/, fault-tolerance/, jwt/, etc.
```

## Contributing Requirements

**Copyright headers:** Add to any modified file:
```
Portions Copyright [year] Payara Foundation and/or its affiliates
```

**Contributor License Agreement:** Required before code can be merged. Download and sign `PayaraCLA.pdf`, then email to cla@payara.org.

**Git workflow:**
1. Fork repository and create feature branch: `git checkout -b issue-###`
2. Make changes and commit: `git commit -m "fixes #<GithubNumber>"`
3. Rebase on upstream main: `git fetch upstream && git rebase upstream/main`
4. Push and create PR

**Build verification:** Ensure `mvn -DskipTests clean package` passes before submitting PR.

## Key Dependencies

- Jakarta EE 11 (Full Profile)
- MicroProfile 6.1
- HK2 4.0.0-M3 (dependency injection)
- Grizzly NIO framework
- Jersey 4.0.0 (JAX-RS/JAX-WS)
- EclipseLink 5.0.0 (JPA)
- Weld 6.0.3 (CDI)
- Hazelcast 5.3.8 (clustering)