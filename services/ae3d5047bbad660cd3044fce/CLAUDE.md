# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-module Maven project containing 50+ learning modules for Java/Spring technologies from Imooc (a Chinese online learning platform). The project has three main sections:

- **Root level modules** (01-spring through 50-boot) - Main learning modules
- **gradle-source-code/** - Gradle learning examples
- **teach-source-code/** - Teaching reference implementations

## Build Commands

```bash
# Build entire project from root
mvn clean install

# Build specific module (navigate to module dir first)
cd 05-boot/05-boot-simple && mvn clean package

# Skip tests during build
mvn clean install -DskipTests

# Run tests for specific module
mvn test

# Run single test class
mvn test -Dtest=HelloControllerTest

# Run single test method
mvn test -Dtest=HelloControllerTest#hello
```

## Key Dependencies

- **Java Version**: 1.8
- **Spring Framework**: 5.1.14.RELEASE
- **Spring Boot**: 2.1.13.RELEASE
- **Hibernate**: 5.3.15.Final
- **MyBatis**: 2.1.1 (Spring Boot Starter)
- **JUnit**: 4.12
- **Logging**: SLF4J 1.7.30, Log4j2 2.11.2

## Module Structure Pattern

Most modules follow this structure:
- Parent pom at module root (e.g., `05-boot/pom.xml`)
- Sub-modules with `-simple` or descriptive suffixes (e.g., `05-boot-simple/`)
- Sub-module has standard Maven layout: `src/main/java`, `src/main/resources`, `src/test/java`

Nested module example:
```
05-boot/
├── pom.xml (parent for boot modules)
├── 05-boot-simple/
│   ├── pom.xml (actual jar module)
│   └── src/main/java/.../BootSimpleGirlApplication.java
```

## Package Naming Convention

Java packages follow: `com.myimooc.{module}.{component}`

Examples:
- Controller: `com.myimooc.boot.simple.controller`
- Service: `com.myimooc.boot.simple.service`
- Repository: `com.myimooc.boot.simple.repository`
- Entity: `com.myimooc.boot.simple.model.entity`

## Test Patterns

Tests typically extend `AbstractTestSupport` and use JUnit 4 with Spring Boot Test annotations:

```java
@RunWith(SpringRunner.class)
@SpringBootTest
public class GirlControllerTest extends AbstractTestSupport {
    // tests
}
```

## Maven Mirrors

The project is configured with Chinese Maven mirrors for faster downloads:
- Aliyun: http://maven.aliyun.com/nexus/content/groups/public
- Huawei: https://mirrors.huaweicloud.com/repository/maven/

## Development Notes

- Modules prefixed with `*-java` are standalone Java applications (no Spring Boot)
- Modules prefixed with `*-boot` are Spring Boot applications
- Modules prefixed with `*-spring` or `*-mvc` are Spring Framework applications
- Some modules (15-java, 19-excel, 41-boot-small) have nested multi-module structures
- The `45-java-sms` module requires JDK9 and is commented out in the parent pom