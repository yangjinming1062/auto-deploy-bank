# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache OpenNLP is a machine learning-based toolkit for processing natural language text. It provides support for common NLP tasks such as tokenization, sentence segmentation, part-of-speech tagging, named entity extraction, chunking, parsing, coreference resolution, and language detection.

## Build Commands

```bash
# Full build with tests
mvn install

# Run only unit tests (excludes integration tests)
mvn test

# Run integration tests (*IT.java files)
mvn verify

# Run a single test class
mvn test -Dtest=TokenizerMETest

# Run tests with code coverage (JaCoCo)
mvn -Pjacoco clean verify

# CI profile (uses local download directory, nightlies for v1.5 models)
mvn -Pci clean install

# High-memory evaluation tests (4GB heap)
mvn -Peval-tests install

# High-memory tests (>20GB heap, tagged with @Tag(HighMemoryUsage))
mvn -Phigh-memory-tests install

# Skip checkstyle validation
mvn install -Dcheckstyle.skip=true

# Skip forbidden APIs checks
mvn install -Dforbiddenapis.skip=true
```

**Requirements:** JDK 17+, Maven 3.3.9+

## Code Standards

- **Checkstyle:** Max line length 110 characters, ASF license header required, no tabs, LF line endings
- **License headers:** All source files must include the ASF license header (enforced by checkstyle)
- **Tests:** JUnit 5 (Jupiter) with naming convention `*Test.java` for unit tests and `*IT.java` for integration tests
- **Logging:** SLF4J API with Simple logger for tests

## Module Architecture

```
opennlp/
├── opennlp-api/          # Core interfaces and APIs
├── opennlp-core/         # ML implementations
│   ├── opennlp-ml-commons/   # Shared ML infrastructure
│   ├── opennlp-ml-maxent/    # Maximum Entropy classifiers
│   ├── opennlp-ml-perceptron/ # Perceptron classifiers
│   ├── opennlp-ml-bayes/     # Naive Bayes classifiers
│   ├── opennlp-ml-*/opennlp-dl*  # ONNX deep learning models
│   ├── opennlp-runtime/      # Shared runtime utilities
│   ├── opennlp-models/       # Model loading utilities
│   ├── opennlp-formats/      # Data format handlers
│   └── opennlp-cli/          # Command-line interface
├── opennlp-tools/        # Main NLP toolkit (tokenize, parser, etc.)
├── opennlp-extensions/   # UIMA annotators, Morfologik addon
├── opennlp-distr/        # Distribution packaging
└── opennlp-docs/         # Documentation
```

**Key package in opennlp-tools:** `opennlp.tools.util` contains shared utilities; domain-specific packages like `opennlp.tools.tokenize`, `opennlp.tools.parser` follow.

## Dependency Injection Pattern

ML implementations (maxent, perceptron, bayes) are discovered via Java Service Provider Interface (SPI). Add your provider configuration to `META-INF/services/` to register new implementations.

## Contribution Guidelines

PRs must:
1. Reference a JIRA ticket (OPENNLP-XXXX)
2. Have PR title starting with the JIRA ticket number
3. Be rebased against the latest `main` branch
4. Pass `mvn clean install` locally before submitting
5. Include/update unit tests for changes
6. Have ASF-compatible licenses for any new dependencies (update LICENSE/NOTICE files if needed)

Check GitHub Actions after submission for any build issues.