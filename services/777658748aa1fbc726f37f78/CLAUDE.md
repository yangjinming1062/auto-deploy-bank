# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

INCEpTION is a semantic annotation platform providing intelligent annotation assistance and knowledge management. It is a multi-module Maven project (~150 modules) built on:

- **Java 17** (Spring Boot 3.5.8)
- **Apache Wicket** for web UI
- **Apache UIMA** for text processing
- **Hibernate/JPA** for data persistence
- **Svelte** for frontend components

## Build Commands

```bash
# Full build (skip tests for speed)
mvn clean install -DskipTests

# Build WAR file for deployment
mvn clean package -pl inception/inception-app-webapp -am

# Run all tests
mvn test

# Run specific test class
mvn test -Dtest=DocumentServiceImplTest

# Run test method
mvn test -Dtest=DocumentServiceImplTest#testDocumentNameValidationErrorMessages

# Build with jacoco coverage
mvn clean verify -Pjacoco

# Run tests in specific module
mvn test -pl inception/inception-documents
```

## Architecture

### Core Modules (inception/)
- **inception-model** - Domain models and DTOs
- **inception-project** - Project management and settings
- **inception-documents** - Document handling and storage
- **inception-security** - Authentication and authorization
- **inception-scheduling** - Task scheduling

### Annotation System
- **inception-ui-annotation** - Main annotation editor UI (Wicket-based)
- **inception-api-render** - Annotation rendering API
- **inception-api-annotation** - Annotation service API
- **inception-layer-*** - Layer type implementations (span, relation, chain, etc.)
- **inception-feature-*** - Feature type implementations (string, number, link, lookup)

### Recommender System (ML/AI)
- **inception-recommendation** - Core recommendation engine
- **inception-active-learning** - Active learning support
- **inception-imls-*** - Machine learning module implementations:
  - **inception-imls-llm-support** - LLM-based recommendations
  - **inception-imls-chatgpt** - OpenAI ChatGPT integration
  - **inception-imls-ollama** - Ollama integration
  - **inception-imls-opennlp** - OpenNLP-based recommendations
  - **inception-imls-stringmatch** - String matching recommender
  - **inception-imls-external** - External ML service support

### Import/Export (IO)
- **inception-io-*** modules support various formats: XMI, JSON, CoNLL, TEI, BIO, BRAT, RDF, Docx, HTML, etc.
- Located in `inception/inception-io-*` directories

### Knowledge Base
- **inception-kb** - Knowledge base core
- **inception-kb-lucene-sail** - Lucene-based KB storage
- **inception-ui-kb** - KB management UI
- **inception-concept-linking** - Entity linking to knowledge bases

### Search
- **inception-search-core** - Internal search API
- **inception-search-mtas** - Mtas/Lucene-based search
- **inception-external-search-*** - External document search (OpenSearch, Solr, PubMed, etc.)

### UI Components
- **inception-ui-*** - Various UI modules using Apache Wicket
- **inception-brat-editor** - BRAT annotation editor
- **inception-diam-*** - DIAM annotation editor
- **inception-pdf-editor2** - PDF document editor
- **inception-websocket** - Real-time collaboration support

### Application Entry Point
- **inception/inception-app-webapp/src/main/java/de/tudarmstadt/ukp/inception/INCEpTION.java** - Main Spring Boot application class
- Configuration: `inception-app-webapp/src/main/resources/application.yml`

## Development Patterns

### Service Layer
Services are located in feature modules and typically:
- Use `@Transactional` annotations
- Have corresponding repository interfaces for data access
- Inject via constructor

### Wicket Pages
- Extend `org.apache.wicket.markup.html.WebPage`
- Located in `src/main/java` alongside HTML templates
- Use `wicket:id` in HTML for component binding

### Spring Configuration
- Auto-configuration classes use `@AutoConfiguration`
- Feature configurations are discovered via `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`

### Testing
- Uses **JUnit 6** (`org.junit.jupiter.api`)
- **AssertJ** for assertions (`assertThat`)
- **Mockito** for mocking
- Integration tests use embedded databases (HSQLDB)

## Project Structure

```
inception/
  inception-*                    # ~150 modules organized by feature
  pom.xml                        # Root POM
inception/inception-app/
  inception-app-webapp/          # Main WAR module
  pom.xml                        # App module POM with all submodule declarations
pom.xml                          # Parent POM (inception root)
```

## Key Dependencies (from pom.xml)

- Spring Boot 3.5.8, Spring Security 6.5.7
- Apache Wicket 10.7.0
- Apache UIMA 3.6.1
- Hibernate 6.6.37
- Elasticsearch/OpenSearch 2.x
- Jena 5.6.0, RDF4J 5.1.3
- Node.js 22.21.1 (for frontend builds)