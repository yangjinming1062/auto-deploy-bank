# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **iText Core Community** (v9.4.0), a high-performance Java library for creating, manipulating, and maintaining PDF documents. It's a multi-module Maven project with strong focus on backward compatibility and comprehensive testing.

**Key Features:**
- PDF creation, manipulation, and digital signing
- PDF/A and PDF/UA compliance
- Form creation and manipulation
- Barcode generation and SVG support
- FIPS-compliant cryptography
- Native image compilation support (GraalVM)

## Common Commands

### Build & Install
```bash
# Build without running tests (fastest)
mvn clean install -Dmaven.test.skip=true

# Build with tests (requires Ghostscript and ImageMagick)
mvn clean install -P test \
  -DITEXT_GS_EXEC="gs command" \
  -DITEXT_MAGICK_COMPARE_EXEC="magick compare command"

# Build with FIPS Bouncy Castle
mvn clean install -P test,bouncy-castle-fips-test,!bouncy-castle-test \
  -DITEXT_GS_EXEC="gs command" \
  -DITEXT_MAGICK_COMPARE_EXEC="magick compare command"

# Native build with GraalVM (requires JDK 22+)
mvn clean install -Pnative -DskipTests=false \
  -DITEXT_GS_EXEC="gs command" \
  -DITEXT_MAGICK_COMPARE_EXEC="magick compare command"
```

### Testing
```bash
# Run single test class
mvn test -Dtest=ClassNameTest

# Run specific test method
mvn test -Dtest=ClassNameTest#methodName

# Run tests in specific module
cd kernel && mvn test

# Run tests with coverage (Sonar)
mvn clean install -P test

# Mutation testing (Jenkins only)
mvn clean install -P mutationtest
```

### Code Quality
```bash
# Check backward compatibility (after build)
mvn verify --activate-profiles qa \
  -Dcheckstyle.skip=true \
  -Ddependency-check.skip=true \
  -Dpmd.skip=true \
  -Dspotbugs.skip=true \
  -Dmaven.main.skip=true \
  -Dmaven.test.skip=true \
  -Djapicmp.breakBuildOnModifications=true \
  -Djapicmp.breakBuildOnBinaryIncompatibleModifications=true \
  -Djapicmp.breakBuildOnSourceIncompatibleModifications=true

# Check Javadoc for missing documentation
mvn clean install
mvn javadoc:javadoc | grep -E "(: warning:)|(: error:)"
```

## Architecture & Module Structure

The project follows a layered architecture with clear separation of concerns:

### Dependency Hierarchy
- **commons** → Base utilities
- **io** → Low-level I/O operations (fonts, images, streams)
- **kernel** → Low-level PDF operations (reading/writing PDF structure, encryption)
- **layout** → High-level layout engine (Document, Paragraph, Table, etc.)
- **forms** → PDF forms (AcroForm support)
- **pdfa** → PDF/A compliance
- **pdfua** → PDF/UA accessibility
- **sign** → Digital signatures
- **barcodes** → Barcode generation
- **svg** → SVG rendering support
- **styled-xml-parser** → CSS/HTML parsing
- **hyph** → Hyphenation
- **font-asian** → Asian font support
- **bouncy-castle-*** → Cryptography adapters (standard and FIPS)
- **pdftest** → Test utilities

### Key Architectural Patterns
1. **Kernel → Layout separation**: Kernel handles low-level PDF objects, Layout provides high-level API
2. **Bouncy Castle abstraction**: Multiple modules isolate Bouncy Castle dependencies
3. **Multi-profile support**: Different profiles for test, FIPS, native compilation
4. **Java → .NET porting**: Uses `sharpen` tool to generate C# code

### Critical Dependencies
- **Ghostscript** and **ImageMagick**: Required for visual PDF comparison in tests
- **GraalVM**: Required for native image compilation
- **Bouncy Castle**: Cryptography (v1.81), with standard and FIPS variants

## Development Conventions

### Class Structure Ordering (CodeConventions.md)
1. Public constants
2. Protected constants
3. Private constants
4. Public fields
5. Protected fields
6. Private fields
7. Public constructors
8. Protected constructors
9. Private constructors
10. Public static methods
11. Public methods
12. Protected static methods
13. Protected methods
14. Private static methods
15. Private methods
16. Public static classes
17. Public classes
18. Protected static classes
19. Protected classes
20. Private static classes
21. Private classes

### Coding Standards (CONTRIBUTING.md)
- Follow [Oracle's Java Code Conventions](https://www.oracle.com/technetwork/java/codeconvtoc-136057.html)
- Wrap code at **100 characters**
- **All public API methods must have JavaDoc**
- **All features/bug fixes must include unit tests**
- **Java 8 compatibility** (source and target)
- Java is developed first, then ported to .NET

### Commit Message Format
```
<subject> (50 chars max, imperative mood, no period)

<body> (wrapped at 72 chars)

<footer>

Breaking Changes: ...
Closes: JIRA-123
```

## Module-Specific Notes

### kernel Module
- **Low-level PDF operations**: Direct PDF object manipulation
- **Canvas API**: Direct PDF canvas drawing
- **Parser**: PDF content extraction and analysis
- **Crypto**: Encryption/decryption support

### layout Module
- **High-level API**: Document, Paragraph, Table, Image
- **Layout engine**: Automatic pagination, hyphenation
- **Renderer**: Converts layout objects to PDF commands

### Testing Strategy
- **Unit Tests**: Using JUnit Jupiter, grouped by `@Tag`:
  - `@UnitTest` - Fast unit tests
  - `@BouncyCastleUnitTest` - BC-specific unit tests
  - `@IntegrationTest` - Slower integration tests
  - `@BouncyCastleIntegrationTest` - BC-specific integration tests
  - `@SlowTest` - Tests requiring visual comparison
  - `@PerformanceTest` - Performance benchmarks
  - `@SampleTest` - Example tests

### Profiles Reference
- **develop** (default): Standard development
- **test**: Runs all tests with coverage
- **bouncy-castle-fips-test**: FIPS-compliant tests
- **native**: GraalVM native image compilation
- **qa**: Quality assurance (japicmp, dependency check)
- **mutationtest**: Mutation testing (Jenkins)

## Build Configuration

### Maven Compiler
- **Source**: Java 1.8
- **Target**: Java 1.8
- **Max memory**: 1024m (`<argLine>-Xmx1024m</argLine>`)

### Test Configuration
- **Skip tests by default**: `skipTests=true`
- **Thread count**: 1 (for visual comparison consistency)
- **Test reports**: `${project.build.directory}/surefire-reports`

### JavaDoc Configuration
- **Source**: Java 8 API links
- **Groups**: API divided into logical groups (Barcodes, Forms, Kernel, Layout, etc.)
- **Exclusions**: Internal utilities, Brotli codec, JSoup parser, etc.

## Important Notes

1. **Visual Testing**: Many tests compare generated PDFs with reference files using ImageMagick
2. **Cryptography**: FIPS mode requires special Bouncy Castle modules
3. **Native Compilation**: GraalVM native tests need specific initialization flags
4. **Backward Compatibility**: Must pass japicmp checks in QA profile
5. **Documentation**: Missing Javadoc warnings must be addressed before release
6. **iCLA Required**: Contributors must sign iText Contributor License Agreement

## Useful Resources

- **Knowledge Base**: https://kb.itextpdf.com
- **API Documentation**: https://itextpdf.com/api
- **Examples**: https://github.com/itext/i7js-examples
- **Signing Examples**: https://github.com/itext/i7js-signing-examples
- **Support**: Stack Overflow (`itext` tag)