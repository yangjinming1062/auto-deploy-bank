# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Eden* Architect is an enterprise Spring Boot development framework providing one-stop solutions for distributed application development. The project is organized as a multi-module Maven project with Spring Boot 2.4.13.

**GroupId:** `io.github.shiyindaxiaojie`

**Minimum JDK:** 1.8 (CI runs on JDK 8)

## Build Commands

```bash
# Build and install to local Maven repository
./mvnw install -T 4C

# Clean build without tests
./mvnw clean package -T 4C

# Run unit tests only
./mvnw clean package -Punit-test -T 4C

# Deploy to GitHub Packages
./mvnw deploy -Pgithub -DskipTests -T 4C

# SonarCloud analysis
mvn -B verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar -Dsonar.projectKey=shiyindaxiaojie_eden-architect
```

## Project Structure

```
eden-architect/
├── eden-components/          # Core framework modules (16 modules)
│   ├── eden-dependencies/    # Centralized dependency version management
│   ├── eden-parent/          # Parent POM with plugin configurations
│   ├── eden-commons/         # Utility extensions (Apache Commons, Guava)
│   ├── eden-extensions/      # Extensibility framework (Dubbo-style SPI)
│   ├── eden-cola/            # COLA framework (DDD, state machine,、业务扩展点)
│   ├── eden-solutions/       # Solution toolkits (caching, distributed lock, ID generation)
│   ├── eden-spring-framework/# Base Spring extensions (error codes, exception handling)
│   ├── eden-spring-data/     # Data storage extensions (Mybatis, Redis, Flyway)
│   ├── eden-spring-security/ # Security extensions (OAuth2, JWT, Shiro)
│   ├── eden-spring-integration/# Third-party integrations (RocketMQ, Kafka, Netty, XxlJob)
│   ├── eden-spring-boot/     # Spring Boot extensions
│   ├── eden-spring-boot-starters/ # Auto-configuration starters (56 modules)
│   ├── eden-spring-cloud/    # Spring Cloud extensions (Nacos, Sentinel, Zookeeper)
│   ├── eden-spring-cloud-starters/# Spring Cloud starters (22 modules)
│   └── eden-spring-test/     # Testing extensions (TestContainer, embedded middleware)
├── eden-tests/               # Test suites
│   ├── eden-deployment-tests/
│   ├── eden-integration-tests/
│   ├── eden-performance-tests/
│   └── eden-smoke-tests/
├── eden-agents/              # Agent modules
├── eden-plugins/             # Maven plugins
└── examples/                 # Example applications
```

## Module Dependency Order

When making changes, build modules in this order:
1. `eden-dependencies` (version management)
2. `eden-parent` (parent configurations)
3. `eden-commons`, `eden-extensions` (foundation)
4. Core modules (`eden-spring-*`)
5. Starters (depend on core modules)
6. Tests

## Code Style

**EditorConfig** is used for formatting:
- Java/Groovy/XML files: tab indentation (4 spaces)
- Other files: 2-space indentation
- UTF-8 encoding, LF line endings
- Insert final newline, trim trailing whitespace

## Key Frameworks & Libraries

- **ORM/数据访问:** Mybatis, Flyway, Liquibase
- **消息队列:** RocketMQ, Kafka
- **缓存:** Redis (with distributed lock support)
- **任务调度:** XxlJob
- **监控:** CAT, Arthas
- **工具库:** Lombok, MapStruct, Guava, Apache Commons
- **JSON处理:** Fastjson, Fastjson2, Gson, Jackson
- **测试:** JUnit 5, Spock, Groovy, TestContainer

## Configuration Properties Pattern

Spring Boot starters follow the pattern `xxx.enabled` as the main switch:
```yaml
cat:
  enabled: true  # 默认关闭，按需开启
  trace-mode: true
```

## Testing Notes

- Unit tests use maven-surefire-plugin with JUnit 5
- Integration tests use maven-failsafe-plugin
- Gatling is used for performance tests
- Tests for starters are in `eden-spring-boot-test`

## Publishing to Maven Central

The project supports publishing to Maven Central via Sonatype OSSRH:
- Sonatype profile: `-Psonatype-ossrh`
- Requires GPG signing for releases