# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Building
```bash
# Build everything and run all tests
mvn clean test

# Build without tests (faster iteration)
mvn clean compile

# Build a specific module
./build.sh languagetool-standalone clean package
./build.sh languagetool-standalone clean package -DskipTests

# Build standalone distribution
./build.sh languagetool-standalone package -DskipTests
# Result: languagetool-standalone/target/LanguageTool-{version}.zip

# Build Wikipedia module
./build.sh languagetool-wikipedia package -DskipTests
# Result: languagetool-wikipedia/target/

# Build a specific language module
./build.sh en clean test
./build.sh de clean package -DskipTests
```

### Testing
```bash
# Run all tests
mvn clean test

# Run tests for specific modules (also builds dependencies)
mvn clean --projects languagetool-core,languagetool-standalone -am test

# Run a single test class
mvn test -Dtest=EnglishTest

# Run tests with more verbose output
mvn clean test -fae

# Run only fast unit tests (skip integration tests)
mvn clean test -Dtest='*Test,!*IntegrationTest'
```

### Development Utilities
```bash
# Check for OWASP security vulnerabilities (fails on CVSS >= 8)
mvn org.owasp:dependency-check-maven:check

# Generate third-party license report
mvn license:third-party-report
# Result: languagetool-standalone/target/site/third-party-report.html

# Sort pom.xml dependencies
mvn sortpom:sort

# Generate Javadoc
mvn javadoc:javadoc
```

## High-Level Architecture

LanguageTool is a multi-module Maven project implementing a grammar/style checker for 20+ languages.

### Core Architecture
The system follows a language-agnostic core with language-specific modules:

1. **Core Pipeline** (`languagetool-core`):
   - `JLanguageTool` - Main entry point for checking text
   - `Language` - Abstract base class for all languages
   - `AnalyzedSentence` - Represents a tokenized and analyzed sentence
   - Rules system: Pattern-based (XML) and Java-based rules
   - Tokenization, POS tagging, disambiguation, and synthesis

2. **Language Modules** (`languagetool-language-modules/<lang>`):
   Each language (en, de, fr, es, etc.) contains:
   - `org.languagetool.language.<LanguageName>` - Language implementation
   - `org.languagetool.rules` - Language-specific rules
   - `org.languagetool.tagging` - POS tagger and disambiguator
   - `org.languagetool.tokenizers` - Language-specific tokenizers
   - `org.languagetool.synthesis` - Word form synthesis
   - `org.languagetool.chunking` - Syntactic chunking
   - `resources/` - Dictionaries, word lists, and grammar XML files

### Major Modules

**languagetool-core**
- Language-agnostic rule engine and checking logic
- Abstract rule classes and pattern matching
- Tokenizers, taggers, synthesizers (base implementations)
- Resource loading and caching

**languagetool-language-modules/**
- Individual modules for each supported language (en, de, fr, es, pt, nl, etc.)
- Each module provides language-specific implementations of:
  - Tagger (adds grammatical information)
  - Disambiguator (resolves POS ambiguities)
  - Synthesizer (generates word forms)
  - Chunker (identifies syntactic chunks)
  - Rules (grammar, style, and spelling rules)

**languagetool-standalone**
- Desktop GUI application
- Standalone JAR with bundled dependencies
- Entry point: `org.languagetool.gui.Main`

**languagetool-commandline**
- Command-line interface tool
- Entry point: `org.languagetool.commandline.Main`

**languagetool-server**
- HTTP server for API access
- REST API for remote grammar checking
- Production deployment package

**languagetool-http-client**
- Java client library for the HTTP API

**languagetool-wikipedia**
- Wikipedia integration tool for checking articles

**languagetool-tools**
- Utility tools for rule development and testing

### Key Technologies
- **Java 17+** - Core language
- **Maven** - Build system and dependency management
- **Morfologik** - Spelling dictionary support (Polish)
- **Apache Lucene** - Text indexing and search
- **OpenNLP** - POS tagging and chunking models
- **JFlex** - Lexical analyzer generation
- **gRPC** - Server communication (server module)
- **Prometheus & OpenTelemetry** - Observability

### Critical Files

**Root pom.xml**
- Defines all 30+ modules
- Central dependency management
- Build plugin configurations
- Version: 6.8-SNAPSHOT

**build.sh**
- Helper script for building specific modules
- Usage: `./build.sh <module> <goals...>`

**test-modules.sh**
- CI test script that detects changed modules and runs selective tests
- Runs full test suite for core/pom changes
- Otherwise, tests only affected language modules

## Module Structure

Each language module follows this pattern:
```
languagetool-language-modules/<lang>/
├── pom.xml
└── src/
    └── main/
        ├── java/org/languagetool/
        │   ├── language/<Lang>.java           # Language implementation
        │   ├── rules/<Lang>/                  # Language-specific rules
        │   ├── tagging/                       # Tagger, disambiguator
        │   ├── tokenizers/                    # Tokenizer implementations
        │   ├── synthesis/                     # Synthesizer
        │   └── chunking/                      # Chunker (if needed)
        └── resources/
            └── org/languagetool/
                └── resource/<lang>/
                    ├── <lang>.dict            # Main dictionary
                    ├── grammar.xml             # Pattern rules
                    └── hunspell/              # Hunspell dictionaries
```

## Important Notes

**Thread Safety**: `JLanguageTool` is not thread-safe. Use `MultiThreadedJLanguageTool` for concurrent access or create one instance per thread.

**Resource Loading**: Language-specific resources (dictionaries, rules) are loaded via `ResourceDataBroker` and cached for performance.

**Rule Types**:
- PatternRule - Loaded from XML grammar files
- AbstractRule - Java-based rules
- SpellingCheckRule - Spell checking (Hunspell/Morfologik)

**Version**: Current development version is 6.8-SNAPSHOT

**Testing**: Tests use JUnit 4. Integration tests may require `-Xmx3372m` heap space.

## Contributing

To add a new language:
1. Create new module under `languagetool-language-modules/<lang>/`
2. Implement `Language` subclass
3. Add POS tagging resources (OpenNLP models or Morfologik)
4. Add grammar rules (XML files or Java rules)
5. Include in root `pom.xml` modules list
6. Add tests following existing patterns

See [Development Overview](https://dev.languagetool.org/development-overview) for detailed contribution guidelines.