# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZXing ("Zebra Crossing") is an open-source, multi-format 1D/2D barcode image processing library implemented in Java. **The project is in maintenance mode** - only bug fixes and minor enhancements will be considered. Feature requests are not accepted. Pull requests with bug fixes are acted on promptly.

## Build Commands

```bash
# Standard build (compiles all active modules)
mvn install

# Build without running tests
mvn package -DskipTests

# Run tests
mvn test

# Run a specific test
mvn test -Dtest=TestClassName

# Check code style (Checkstyle)
mvn checkstyle:check

# Check license headers (Apache RAT)
mvn apache-rat:check

# Check API compatibility (Clirr)
mvn clirr:check

# Build with code coverage
mvn test -Pjacoco
```

**Requirements:**
- Maven 3.6.3+
- Java 8 (1.8) for core and javase modules
- Java 17+ for zxingorg web module
- Android modules require `ANDROID_HOME` environment variable and JDK < 9

## Architecture

### Core Modules

| Module | Purpose |
|--------|---------|
| `core/` | Platform-independent barcode decoding/encoding logic |
| `javase/` | Java SE utilities (BufferedImage handling, J2SE client code) |
| `android/` | Barcode Scanner Android app (not compatible with Android 14+) |
| `android-core/` | Shared Android-specific code |
| `android-integration/` | Integration with Barcode Scanner via Intent |
| `zxingorg/` | Web application at zxing.org (requires Java 17+) |
| `zxing.appspot.com/` | Web-based barcode generator (Java < 9) |

### Key Entry Points

**Decoding:**
- `com.google.zxing.MultiFormatReader` - Main entry point; auto-detects and delegates to format-specific readers
- `com.google.zxing.BinaryBitmap` - Wraps processed image data
- `com.google.zxing.LuminanceSource` - Abstraction for image sources

**Encoding:**
- `com.google.zxing.MultiFormatWriter` - Main encoding entry point

**Format Packages:**
- `com.google.zxing.qrcode` - QR Code support
- `com.google.zxing.datamatrix` - Data Matrix support
- `com.google.zxing.oned` - 1D barcodes (UPC, EAN, Code 39, Code 128, etc.)
- `com.google.zxing.pdf417` - PDF 417 support
- `com.google.zxing.aztec` - Aztec Code support
- `com.google.zxing.maxicode` - MaxiCode support

### Design Patterns

- **Strategy Pattern**: Each barcode format is isolated in its own package (e.g., `com.google.zxing.qrcode`)
- **Interface-Driven Design**: Core logic built around `Reader` and `Writer` interfaces
- **Image Abstraction**: Input images abstracted via `LuminanceSource` and `Binarizer` to support multiple image sources

## Code Style

- Checkstyle configuration: `core/src/checkstyle/checkstyle.xml`
- All source files must include Apache License 2.0 header
- Compiler uses `-Xlint:all` with `-Xlint:-serial`

## Contributing

- Only bug fixes are accepted (no new features)
- Pull requests must include test coverage for the fix
- Bug reports without a pull request will generally be closed
- All contributions are licensed under Apache License 2.0