# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Elasticsearch Ingest Plugin for OpenNLP Named Entity Recognition (NER). Extracts entities (persons, locations, dates, etc.) from text fields during document ingestion and stores results in the document before indexing.

## Build Commands

```bash
./gradlew clean check         # Build and run all tests (unit + integration)
./gradlew test                # Run unit tests only (excludes 'slow' tagged tests)
./gradlew integrationTest     # Run integration tests only (requires Docker for testcontainers)
./gradlew packageDistribution # Build distribution zip in build/distributions/
./gradlew downloadModels      # Download NLP models to test resources
```

**Note**: `test` and `check` tasks automatically run `downloadModels` first.

## Architecture

### Core Components

**IngestOpenNlpPlugin.java** - Plugin entry point:
- Registers `ingest.opennlp.model.file.*` settings for model configuration
- Creates `OpenNlpService` instance at plugin initialization
- Provides `OpenNlpProcessor.Factory` to create processor instances

**OpenNlpService.java** - Model management and entity finding:
- Loads `TokenNameFinderModel` from configured model files at startup
- Uses `ThreadLocal<TokenNameFinderModel>` to handle OpenNLP's non-thread-safe finders
- `find(content, field)` method performs NER on text using specified model
- `createAnnotatedText()` generates annotated text format for elasticsearch mapper-annotated-text plugin

**OpenNlpProcessor.java** - Ingest processor:
- Extends `AbstractProcessor` implementing the ingest pipeline interface
- Configuration: `field` (source), `target_field` (output, default "entities"), `fields` (optional filter), `annotated_text_field` (optional)
- Merges extracted entities with existing field values, avoiding duplicates

### Configuration

Models are configured in `elasticsearch.yml`:
```
ingest.opennlp.model.file.<name>:
```

For example:
```yaml
ingest.opennlp.model.file.persons: en-ner-persons.bin
ingest.opennlp.model.file.locations: en-ner-locations.bin
ingest.opennlp.model.file.dates: en-ner-dates.bin
```

## Thread Safety Implementation

OpenNLP's `NameFinderME` is not thread-safe. The implementation uses `ThreadLocal<TokenNameFinderModel>` in `OpenNlpService`:
- Each thread stores its own model reference
- Models are loaded once at startup into `ConcurrentHashMap<String, TokenNameFinderModel>`
- ThreadLocal ensures thread safety without synchronization overhead during execution

## Testing Patterns

- Unit tests: Use local model files, no external dependencies
- Integration tests: Use `testcontainers` with real Elasticsearch instance
- Test tags: 'slow' tag distinguishes integration tests from unit tests