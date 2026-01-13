# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

dcm4che is a comprehensive DICOM (Digital Imaging and Communications in Medicine) toolkit written in Java. This is version 3.x, a complete rewrite focused on minimizing the memory footprint of DICOM datasets. The project implements DICOM standards and provides a complete set of libraries and command-line utilities for handling medical imaging data.

**Key URLs:**
- Sources: https://github.com/dcm4che/dcm4che
- Issue Tracker: https://github.com/dcm4che/dcm4che/issues
- Build Status: GitHub Actions workflow at `.github/workflows/build.yml`

## Build Commands

This is a Maven-based multi-module project using the Maven Wrapper (`mvnw`).

### Prerequisites
- Java 17 (JDK) or newer required

### Common Commands

```bash
# Build all modules
./mvnw install

# Run tests without coverage
./mvnw test

# Run tests with coverage report
./mvnw -B -P test-coverage verify

# Build a specific module
./mvnw install -pl dcm4che-core -am

# Run tests for a specific module
./mvnw test -pl dcm4che-core

# Run a single test class
./mvnw test -pl dcm4che-core -Dtest=AttributesTest

# Skip tests
./mvnw install -DskipTests

# Clean build
./mvnw clean install

# Analyze with SonarCloud (used in CI)
./mvnw -B org.sonarsource.scanner.maven:sonar-maven-plugin:sonar
```

**Note:** Use `./mvnw` (Linux/Mac) or `.\mvnw.cmd` (Windows) instead of `mvn` directly.

## Architecture

### Project Structure

The project is organized as a multi-module Maven build with the following major module groups:

#### Core Libraries

- **dcm4che-core** - The foundational library containing:
  - `org.dcm4che3.data` - DICOM data structures (Attributes, VR, Value types, Sequences, etc.)
  - `org.dcm4che3.io` - DICOM file I/O operations
  - `org.dcm4che3.media` - Media handling and processing
  - `org.dcm4che3.util` - Utility classes
  - Central classes: `Attributes.java`, `VR.java`, `Value.java`, `ElementDictionary.java`

- **dcm4che-net** - Network layer implementing DICOM communication protocols:
  - `org.dcm4che3.net` - DICOM associations, connections, application entities
  - Manages DICOM network sessions, PDU encoding/decoding, DIMSE operations
  - Central classes: `Association.java`, `ApplicationEntity.java`, `Device.java`, `Connection.java`

- **dcm4che-image** - Image processing and manipulation
- **dcm4che-imageio** - Image I/O with codec support (OpenCV, RLE)
- **dcm4che-imageio-test** - Test utilities for image I/O
- **dcm4che-dcmr** - DICOM definitions and references
- **dcm4che-hl7** - HL7 v2.x messaging support
- **dcm4che-json** - JSON serialization for DICOM data
- **dcm4che-dict** - DICOM standard dictionary
- **dcm4che-dict-priv** - Private DICOM dictionaries
- **dcm4che-mime** - MIME type handling

#### Configuration Management

- **dcm4che-conf** - LDAP-based configuration management (DICOM Application Configuration Management Profile - PS 3.15 Annex H)
  - Includes: conf-api, conf-api-hl7, conf-json, conf-ldap, conf-ldap-audit, etc.
  - `dcm4che-conf-ldap-schema` - LDAP schema definitions

#### Command-Line Tools

- **dcm4che-tool** - Parent module for ~40 command-line utilities:
  - **Network tools**: `storescp`, `storescu`, `findscu`, `getscu`, `movescu`, `dcmqrscp`
  - **DICOM conversion**: `dcm2xml`, `xml2dcm`, `dcm2json`, `json2dcm`, `dcm2jpg`, `jpg2dcm`
  - **DICOM manipulation**: `dcmdump`, `deidentify`, `dcm2dcm`, `dcmvalidate`, `dcmdir`
  - **HL7 tools**: `hl7snd`, `hl7rcv`, `hl72xml`, `xml2hl7`, `hl7pdq`, `hl7pix`
  - **Web services**: `stowrs`, `stowrsd`, `wadors`, `wadows`
  - **Specialized tools**: `pdf2dcm`, `dcm2pdf`, `planarconfig`, `syslog`, `syslogd`
  - Each tool is a separate Maven module in the dcm4che-tool directory

- **dcm4che-tool-common** - Shared code for command-line tools (command-line parsing, common utilities)

#### Integration Modules

- **dcm4che-audit** - Audit trail support
- **dcm4che-audit-keycloak** - Keycloak integration for audit logging
- **dcm4che-net-audit**, **dcm4che-net-hl7**, **dcm4che-net-imageio** - Network audit/HL7/imageio extensions
- **dcm4che-soundex** - Soundex algorithm implementation
- **dcm4che-emf** - Enhanced Multi-Frame image handling
- **dcm4che-ws-rs** - RESTful web services
- **dcm4che-xdsi** - XDS-I (Cross-Enterprise Document Sharing for Imaging) integration
- **dcm4che-xroad** - X-Road (Estonian national health registry) integration
- **dcm4che-qstar** - QStar storage system integration

#### Assembly and Distribution

- **dcm4che-assembly** - Distribution assembly
- **dcm4che-jboss-modules** - JBoss Modules packaging
- **dcm4che-camel** - Apache Camel integration
- **dcm4che-test-data** - Test data fixtures

### Key Architectural Patterns

1. **Multi-layered design**: Clear separation between data layer (dcm4che-core), network layer (dcm4che-net), and application layer (tools)

2. **Memory-efficient DICOM data structures**: Version 3.x focuses on minimizing memory footprint compared to version 2.x

3. **Native library dependencies**: Uses native libraries for image compression/decompression across multiple platforms (Linux x86_64, ARM, Windows, macOS)

4. **LDAP configuration**: Enterprise deployments can use LDAP for centralized configuration management

5. **Modular utilities**: Each command-line tool is a separate, self-contained module with minimal dependencies

6. **DICOM standards compliance**: Implementation follows DICOM PS 3.15 Application Configuration Management Profile and other relevant standards

### Dependency Highlights

- **SLF4J 2.0.17 + Logback 1.5.19** - Logging
- **JaCoCo 0.8.10** - Test coverage (activated via `test-coverage` profile)
- **JUnit 4.13.2** - Testing framework
- **Weasis Core Image 4.12.2** - Image processing
- **Apache CXF 4.0.9** - Web services
- **Jakarta EE APIs** - Modern Java EE/Jakarta EE specifications
- **OpenCV** - Image I/O codec support (via dcm4che-imageio-opencv)

## Development Notes

### Native Libraries
dcm4che uses native libraries for image compression/decompression. If you encounter native library loading errors, ensure your system matches one of the supported platforms listed in the README.

### Testing
- JUnit 4 is used for testing
- Test coverage is measured with JaCoCo (see `test-coverage` Maven profile)
- Some modules have extensive integration tests that may require additional setup

### Code Style
- Java 8 source/target compatibility (despite requiring Java 17+ for build)
- OSGi bundles (using maven-bundle-plugin)
- MPL 1.1 / GPL 2.0 / LGPL 2.1 tri-license

### CI/CD
- GitHub Actions build workflow triggers on pushes to `master` and `generic-config` branches and on pull requests
- Build includes SonarCloud code quality analysis (requires SONAR_TOKEN)
- Build script: `.github/workflows/build-with-sonar.sh`

## Important Files

- `pom.xml` - Root POM with module definitions and dependency management
- `dcm4che-core/src/main/java/org/dcm4che3/data/Attributes.java` - Core DICOM data structure (150KB+ file)
- `dcm4che-core/src/main/java/org/dcm4che3/data/VR.java` - Value Representation definitions
- `dcm4che-net/src/main/java/org/dcm4che3/net/Association.java` - DICOM association management
- `README.md` - User-facing documentation and utility list
- `.github/workflows/build.yml` - CI/CD configuration