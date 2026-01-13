# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GROBID (GeneRation Of BIbliographic Data) is a machine learning library for extracting, parsing and re-structuring raw PDF documents into structured XML/TEI encoded documents with a focus on technical and scientific publications. It's a Java/Kotlin project using Gradle as the build system.

**Key capabilities:**
- Header extraction and parsing (title, authors, affiliations, etc.)
- References extraction and parsing (~.87-.90 F1-score)
- Citation contexts recognition and resolution
- Full text extraction and structuring from PDF articles
- PDF coordinates for extracted information
- Parsing of names, affiliations, addresses, dates
- Bibliographic reference consolidation via CrossRef or biblio-glutton

## Build System

**Requirements:**
- OpenJDK 21 (required for building)
- Gradle 9.0.0 (wrapper included)

**Main build command:**
```bash
./gradlew clean install
```
This builds all modules and publishes to Maven local. Tests are excluded by default.

**Run tests:**
```bash
./gradlew test                                    # Run all tests
./gradlew test -x test                            # Skip tests
./gradlew grobid-core:test                        # Run only grobid-core tests
./gradlew :grobid-service:test                    # Run service tests only
```

## Modules

The project is structured as 4 Gradle subprojects:

### 1. grobid-core
**Location:** `grobid-core/`

**Purpose:** Core library containing all parsing engines, document processing logic, and ML models.

**Key packages:**
- `org.grobid.core.engines` - All parser engines (HeaderParser, CitationParser, FullTextParser, etc.)
- `org.grobid.core.document` - Document structure and processing
- `org.grobid.core.layout` - Layout token management and PDF processing
- `org.grobid.core.process` - Document processing pipelines
- `org.grobid.core.data` - Data structures for bibliographical entities
- `org.grobid.core.analyzers` - Text analyzers and tokenization
- `org.grobid.core.features` - Feature extraction for ML models
- `org.grobid.core.lexicon` - Lexicon and dictionary management
- `org.grobid.core.sax` - XML/TEI parsing and serialization

**Main entry point:** `org.grobid.core.main.batch.GrobidMain` for command-line batch processing

**Output:**
- `grobid-core/build/libs/grobid-core-{version}.jar` - Standard jar
- `grobid-core/build/libs/grobid-core-{version}-onejar.jar` - Fat JAR with dependencies

### 2. grobid-service
**Location:** `grobid-service/`

**Purpose:** REST API web service built with Dropwizard framework.

**Main class:** `org.grobid.service.main.GrobidServiceApplication`

**Run service:**
```bash
./gradlew :grobid-service:runShadow              # Run with shadow JAR
./gradlew :grobid-service:distZip                # Create distribution
```

**Configuration:** `grobid-home/config/grobid.yaml`

**Ports:** Service runs on port 8080 (configurable in grobid.yaml)

### 3. grobid-trainer
**Location:** `grobid-trainer/`

**Purpose:** Training and evaluation framework for ML models.

**Training tasks:**
```bash
./gradlew :grobid-trainer:train_header           # Train header extraction model
./gradlew :grobid-trainer:train_citation         # Train citation parser
./gradlew :grobid-trainer:train_fulltext         # Train full text parser
./gradlew :grobid-trainer:train_reference_segmentation  # Train reference segmenter
./gradlew :grobid-trainer:train_affiliation_address    # Train affiliation parser
./gradlew :grobid-trainer:train_name_header      # Train person name parser (header)
./gradlew :grobid-trainer:train_name_citation    # Train person name parser (citations)
./gradlew :grobid-trainer:train_date             # Train date parser
./gradlew :grobid-trainer:train_figure           # Train figure parser
./gradlew :grobid-trainer:train_table            # Train table parser
./gradlew :grobid-trainer:train_funding_acknowledgement # Train funding parser
```

**Evaluation tasks:**
```bash
./gradlew :grobid-trainer:jatsEval -Pp2t=/path/to/goldenSet      # JATS evaluation
./gradlew :grobid-trainer:teiEval -Pp2t=/path/to/goldenSet       # TEI evaluation
./gradlew :grobid-trainer:PrepareDOIMatching -Pp2t=/path/to/PMC  # Prepare DOI matching eval
./gradlew :grobid-trainer:EvaluateDOIMatching -Pp2t=/path/to/PMC # Run DOI matching eval
```

**Key classes:**
- `org.grobid.trainer.AbstractTrainer` - Base trainer class
- `org.grobid.trainer.TrainerRunner` - Main entry point
- Individual trainers for each model type (HeaderTrainer, CitationTrainer, etc.)

### 4. grobid-home
**Location:** `grobid-home/`

**Purpose:** Contains all runtime resources, models, configuration, and native libraries.

**Contents:**
- `config/` - Configuration files (grobid.yaml, grobid.properties)
- `models/` - Trained ML models (CRF and Deep Learning models)
- `lib/` - Native libraries (JEP, pdfalto binaries)
- `pdfalto/` - PDF to XML conversion tool
- `language-detection/` - Language detection models
- `lexicon/` - Lexical resources
- `sentence-segmentation/` - Sentence segmentation models

**Package distribution:**
```bash
./gradlew :grobid-home:packageGrobidHome         # Creates grobid-home.zip
```

## Architecture & Processing Pipeline

**Core processing flow:**
1. **PDF Processing:** PDF → XML via `pdfalto` tool (grobid-home/pdfalto/)
2. **Layout Analysis:** XML → Layout tokens with coordinates and visual features
3. **Sequence Labeling:** Layout tokens → Labeled sequences using CRF or Deep Learning models
4. **Structure Construction:** Labeled sequences → XML/TEI structured output

**Key architectural concepts:**
- **Layout Tokens:** Not plain text, but tokens with layout information (font, position, size, etc.)
- **Cascade Processing:** Document parsed through multiple specialized models in sequence
- **Model Types:** CRF-based (default, fast) and Deep Learning models (more accurate, requires GPU)
- **Consolidation:** Extracted metadata can be validated/resolved via CrossRef API or biblio-glutton

**Engine coordination:**
- `Engine.java` - Main engine orchestrating the parsing process
- `ProcessEngine.java` - Manages processing pipelines
- `EngineParsers.java` - Registry of available parsers
- Each parser extends `AbstractParser` and implements specific labeling logic

## Configuration

**Main config file:** `grobid-home/config/grobid.yaml`

**Key settings:**
- `grobidHome` - Path to grobid-home directory (default: "grobid-home")
- `temp` - Temporary directory for processing (default: "tmp")
- `pdf.pdfalto` - PDF processing limits and timeout
- `consolidation.service` - Choose "crossref" or "glutton" for metadata resolution
- `consolidation.crossref.mailto` - Email for polite CrossRef API usage
- CORS settings for web API

**Model Selection:**
Deep Learning models are disabled by default. To enable them, edit `grobid-home/config/grobid.yaml` and set models to use DL variants (e.g., change `header` to `header-BidLSTM_ChainCRF-with_ELMo`).

## Testing

**Test structure:**
- JUnit 5 tests in `src/test/java/`
- Integration tests for engines and parsers
- Tests require native libraries (JEP) to be properly loaded

**Running tests:**
```bash
./gradlew test                          # All tests
./gradlew :grobid-core:test             # Core library tests only
./gradlew :grobid-service:test          # Service tests only
./gradlew :grobid-trainer:test          # Trainer tests only
```

**Code coverage:**
```bash
./gradlew codeCoverageReport            # Generate JaCoCo coverage report
```

## Development Workflow

**Common tasks:**

1. **Build and install:**
```bash
./gradlew clean install                 # Build all modules
```

2. **Run web service:**
```bash
./gradlew :grobid-service:runShadow
# Access at http://localhost:8080
```

3. **Batch process PDFs:**
```bash
java -jar grobid-core/build/libs/grobid-core-{version}-onejar.jar \
  -gH /path/to/grobid-home \
  -dIn /path/to/input/pdfs \
  -dOut /path/to/output \
  -exe processFulltextDocument
```

4. **Train a specific model:**
```bash
./gradlew :grobid-trainer:train_header -Ptrainer CorporaPath
```

5. **Evaluate models:**
```bash
./gradlew :grobid-trainer:teiEval -Pp2t=/path/to/test/corpus
```

## Native Libraries & Dependencies

**Platform-specific native libraries in grobid-home/lib/:**
- `lin-64/` - Linux x86_64
- `mac-64/` - macOS Intel
- `mac_arm-64/` - macOS ARM (Apple Silicon)

**Contains:**
- JEP (Java Embedded Python) - For Deep Learning model integration
- pdfalto - PDF to XML converter
- CRF++ / Wapiti - CRF implementations

**Java Library Path:**
Gradle automatically configures `java.library.path` to include native libraries based on OS and architecture.

## Deep Learning Models

**Powered by DeLFT library via JEP (Java Embedded Python)**

**Requirements:**
- Python 3.8+
- NVIDIA GPU with CUDA (optional, for faster inference)
- Deep Learning models stored in grobid-home/models/

**Model types:**
- BidLSTM_CRF - Bidirectional LSTM with CRF
- BidLSTM_ChainCRF - Enhanced version with chain CRF
- _with_ELMo - Models using ELMo embeddings (better accuracy, slower)

**To enable DL models:**
Edit `grobid-home/config/grobid.yaml` and specify DL model names instead of CRF models.

## Key Files to Understand

**Core processing:**
- `grobid-core/src/main/java/org/grobid/core/engines/Engine.java` - Main orchestration
- `grobid-core/src/main/java/org/grobid/core/engines/ProcessEngine.java` - Processing pipeline
- `grobid-core/src/main/java/org/grobid/core/document/Document.java` - Document representation
- `grobid-core/src/main/java/org/grobid/core/layout/LayoutToken.java` - Token with layout info

**Parsers:**
- `grobid-core/src/main/java/org/grobid/core/engines/HeaderParser.java` - Header/metadata extraction
- `grobid-core/src/main/java/org/grobid/core/engines/CitationParser.java` - Reference parsing
- `grobid-core/src/main/java/org/grobid/core/engines/FullTextParser.java` - Full text structuring
- `grobid-core/src/main/java/org/grobid/core/engines/Segmentation.java` - Document segmentation

**Training:**
- `grobid-trainer/src/main/java/org/grobid/trainer/AbstractTrainer.java` - Base trainer logic
- `grobid-trainer/src/main/java/org/grobid/trainer/TrainerRunner.java` - Training entry point

**Service:**
- `grobid-service/src/main/java/org/grobid/service/main/GrobidServiceApplication.java` - REST API
- `grobid-service/src/main/java/org/grobid/service/GrobidRestService.java` - API endpoints

## Performance & Scaling

- Designed for high-throughput batch processing
- Multi-threaded client libraries available (Python, Java, Node.js, Go)
- Can process ~10.6 PDF/second on 16 CPU machine (920K PDF/day)
- Memory requirements: 1-3GB per processing thread
- For large-scale processing, use client libraries, not command-line batch mode

## Documentation

- Full documentation: https://grobid.readthedocs.io/
- API documentation: Web service endpoints available at http://localhost:8080/api
- Training docs: https://grobid.readthedocs.io/en/latest/Training-the-models-of-Grobid/
- Docker guide: https://grobid.readthedocs.io/en/latest/Grobid-docker/