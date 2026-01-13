# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Java educational/reference project** containing "Hello World" examples for various Java libraries and frameworks. The main project is in the `helloworlds/` directory, which is a multi-module Maven project. The repository also includes comprehensive Java resource documentation in `link-rus/` (Russian language).

**Purpose**: Help developers learn and compare different Java technologies through simple, consistent examples.

## Common Development Commands

### Building and Compilation

```bash
# Build entire project (all modules)
mvn clean install

# Build a specific module (example: JSON libraries)
cd helloworlds/3.8-json/jackson
mvn clean compile

# Build without running tests
mvn clean compile

# Package as JAR
mvn package

# Clean build artifacts
mvn clean
```

### Running Tests

```bash
# Run all tests in a module
cd helloworlds/4.1-testing/mockito
mvn test

# Run specific test class
mvn test -Dtest=LibraryTest

# Run tests with verbose output
mvn test -X
```

### IDE Compatibility

Works with:
- IntelliJ IDEA Community Edition
- Eclipse
- NetBeans

Open the `helloworlds/` directory in your IDE as a Maven project.

## Project Structure

### Root Directory Layout

```
/home/ubuntu/deploy-projects/184e5fb6b140854df1591638/
├── helloworlds/              # Main project - Hello World examples
│   ├── 1.1-common-frameworks-and-lib/    # Common frameworks (Spring, Guava, etc.)
│   ├── 1.6-usefull-libraries/            # Useful libraries by category
│   ├── 2.8-machine-learning/             # ML libraries (Smile, DL4j)
│   ├── 2.8-natural-language-processing/  # NLP libraries (OpenNLP, Stanford CoreNLP)
│   ├── 3.7-web-crawling-and-html-parser/ # Web scraping (Jsoup)
│   ├── 3.8-json/                         # 14+ JSON libraries comparison
│   ├── 4.1-testing/                      # Testing frameworks (Mockito, Cucumber)
│   ├── 5.0-other-examples/               # Performance benchmarks
│   └── 9.9-template/                     # Template for new libraries
├── link-rus/                  # Russian-language Java resources (222KB)
├── img/                       # License indicator images
├── readme.md                  # Main documentation (362KB)
├── contributing.md            # Contribution guidelines
└── license.md                 # CC-BY-SA-4.0 license
```

### Maven Module Structure

Each library follows this pattern:

```
library_name/
├── pom.xml                    # Maven configuration with dependencies
└── src/
    ├── main/
    │   ├── java/
    │   │   └── package_name/
    │   │       ├── LibraryHelloWorld.java    # Main "Hello World" example
    │   │       └── advanced/
    │   │           ├── AdvancedFeature1.java
    │   │           └── AdvancedFeature2.java
    │   └── resources/          # Config files, if needed
    └── test/
        └── java/
            └── package_name/
                └── LibraryTest.java    # JUnit tests
```

## Architecture and Code Organization

### Multi-Module Maven Project

The `helloworlds/` directory is the parent POM that manages all library examples. Key characteristics:

- **GroupId**: `com.github.vedenin`
- **Version**: `0.01`
- **Java Version**: 1.8 (source/target)
- **Build Tool**: Apache Maven (not Gradle)
- **Packaging**: `pom` (parent), `jar` (individual modules)

### Code Patterns

1. **Simple Examples First**: Each library has a primary `LibraryHelloWorld.java` class demonstrating basic usage
2. **Advanced Features**: Located in `src/main/java/package_name/advanced/` directory
3. **Inner Classes**: Used for simple data structures (e.g., `Human`, `Place` classes in Jackson examples)
4. **Self-Contained**: All classes often in one file for simple examples
5. **Consistent Style**: Uniform code style across all examples

### Major Library Categories

#### JSON Libraries (3.8-json/)
Contains **14 different JSON libraries** with comparison:
- Jackson, Gson, Fastjson, Moshi, LoganSquare
- JSON-java, Genson, JsonPath, Ig-json-parser
- JsonSchema2Pojo, Json Schema Validator, and others

See `helloworlds/3.8-json/readme.md` for detailed comparison table.

#### Collections (1.6-usefull-libraries/collections/)
- Apache Commons Collections
- Guava
- Eclipse Collections (formerly GS Collections)

#### Dependency Injection (1.6-usefull-libraries/dependency_injection/)
- Spring
- Guice
- Dagger

#### Bean Mapping (1.6-usefull-libraries/bean_mapping/)
- Dozer, MapStruct, ModelMapper, Orika, Selma

#### Testing (4.1-testing/)
- Mockito (mocking framework)
- Cucumber (BDD testing)
- Image Comparison (visual testing)

#### Machine Learning (2.8-machine-learning/)
- Smile
- DeepLearning4j

## Testing Framework

- **Testing Framework**: JUnit 4.13.1
- **Mocking**: Mockito 1.9.5
- **Assertions**: Hamcrest matchers
- **Structure**: Tests in `src/test/java/` following Maven conventions

Example test structure:
```java
@Test
public void testGetBalance() throws Exception {
    assertThat(client.getBalance(), is(100));
}
```

## Adding New Library Examples

Use the **template** in `helloworlds/9.9-template/` to add new examples:

1. Copy the template directory structure
2. Update `pom.xml` with library dependencies
3. Create `LibraryHelloWorld.java` with basic example
4. Add `advanced/` examples for complex features
5. Write tests in `src/test/java/`
6. Build with `mvn clean compile` to verify

Requirements for new examples:
- Follow Maven directory structure
- Keep examples simple and focused
- Include both basic and advanced usage
- Add comprehensive JavaDoc
- Compatible with Java 1.8

## Documentation Structure

### Main Documentation Files

1. **`readme.md`** (root, 362KB) - Comprehensive categorized list of Java resources
2. **`helloworlds/readme.md`** - Index of all Hello World examples
3. **`link-rus/readme.md`** (222KB) - Russian version of resources
4. **Category-specific READMEs**:
   - `3.8-json/readme.md` - JSON library comparison with features table
   - Individual module READMEs with links and descriptions

### License Information

- **License**: Creative Commons Attribution-ShareAlike 4.0 International (CC-BY-SA-4.0)
- Visual indicators in `img/` directory show business-friendly licenses
- Allows sharing and adaptation with attribution and share-alike

## Key Build Configuration

The parent POM (`helloworlds/pom.xml`) defines:
- Maven compiler plugin (version 3.1)
- Java 1.8 source/target
- Module declarations for all examples
- Common build configuration

Individual module POMs include:
- Library-specific dependencies
- JUnit test dependencies
- Consistent with parent POM

## Statistics

- **161 Java source files** (main code)
- **67 test Java files**
- **48 Maven POM files** (including nested modules)
- **20+ library categories** covered
- **14 JSON libraries** compared side-by-side
- Extensive cross-references between documentation and code

## Development Notes

- This is an educational/reference project, not a production application
- Focus is on demonstrating library usage, not production-ready code
- Examples should be simple, self-contained, and easy to understand
- No complex business logic or architecture patterns
- Prioritizes clarity and learning over sophistication