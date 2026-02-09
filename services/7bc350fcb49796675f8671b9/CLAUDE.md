# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ReVerb is an Open Information Extraction (OpenIE) system that automatically extracts binary relationships from English text. Given a sentence like "Bananas are an excellent source of potassium," ReVerb extracts the triple (bananas, be source of, potassium). The system is designed for Web-scale extraction where target relations are not specified in advance.

## Build Commands

```bash
# Build the project and create executable jar with dependencies
cd core && mvn clean compile assembly:single

# The output jar will be at:
# core/target/reverb-core-*-jar-with-dependencies.jar

# Run tests
mvn test

# Run tests for a specific test class
mvn test -Dtest=ReVerbExtractorTest
```

## Architecture

### Maven Modules

- **core/** - Main Java source code and tests
- **models/** - Trained ML models (POS tagger, chunker, tokenizer, sentence detector, confidence classifier)

### Extraction Pipeline

The system follows a **relation-first** extraction approach:

1. **Sentence Processing** (`nlp/` package)
   - `ChunkedSentence` is the core data structure representing a sentence with token, POS tag, and NP chunk layers (BIO format)
   - Uses OpenNLP models for sentence detection, tokenization, POS tagging, and shallow parsing
   - Loaded via `DefaultObjects` which provides singleton access to NLP tools

2. **Relation Extraction** (`extractor/` package)
   - `ReVerbRelationExtractor` applies regex patterns to find relation phrases matching V(W*P)*
   - `RegexExtractor` applies POS-pattern-based extraction
   - Patterns defined in `ReVerbRelationExtractor.VERB`, `WORD`, and `PREP` constants

3. **Argument Extraction**
   - `RelationFirstNpChunkExtractor` orchestrates extraction: first finds relations, then extracts arguments on left and right
   - `ChunkedArgumentExtractor` extracts NP chunks as arguments
   - Mappers (`mapper/` package) filter and transform extractions (e.g., `PronounArgumentFilter`)

4. **Confidence Scoring** (`extractor/conf/` package)
   - `ReVerbOpenNlpConfFunction` uses a logistic regression classifier to score extraction confidence
   - Trained on labeled binary extractions stored in binary format

5. **Normalization** (`normalization/` package)
   - `BinaryExtractionNormalizer` produces normalized forms of arguments and relations
   - Extracts head nouns, lemmatizes verbs

### Key Data Structures

- `ChunkedSentence` extends `BIOLayeredSequence` - immutable tokenized sentence with multiple annotation layers
- `ChunkedBinaryExtraction` - Represents (arg1, relation, arg2) with sentence reference and confidence
- `ChunkedExtraction` - Base class for extractions from a sentence
- `Extractor<T, U>` - Generic interface for extraction components; implementations include `ExtractorUnion`, `RegexExtractor`, `ChunkedArgumentExtractor`

### Main Entry Points

- **CLI**: `CommandLineReVerb` (main class) - Run with `-h` for options
- **Library**: `ReVerbExample` in `examples/` package shows usage as a library

### Experimental Features

- **R2A2** (`R2A2` class) - Enhanced extractor using arg1/substructure classifiers (`ArgLearner`, `ArgLocationClassifier`, `ArgSubstructureClassifier`) for improved accuracy at the cost of speed