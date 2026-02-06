# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Zemberek-NLP is a Natural Language Processing library for Turkish. It provides morphological analysis, tokenization, spell checking, normalization, named entity recognition, text classification, and language identification.

## Build Commands

```bash
# Build entire project
mvn clean install

# Run all tests
mvn test

# Run a single test class
mvn test -Dtest=TurkishMorphologyFunctionalTests

# Run a specific test method
mvn test -Dtest=TurkishMorphologyFunctionalTests#testSimpleAnalysis

# Build without running tests
mvn clean install -DskipTests

# Build fat JAR with all dependencies
cd all && mvn clean package
java -jar all/target/zemberek-all-*.jar
```

## Architecture

This is a multi-module Maven project with the following key modules:

### Core Dependencies
- **core** - Specialized collections (Trie, IntMap, Histogram, etc.), hash functions, I/O utilities, Turkish alphabet helpers
- **morphology** - Main module using: RuleBasedAnalyzer, WordGenerator, PerceptronAmbiguityResolver

### NLP Processing Pipeline
1. **tokenization** (`TurkishSentenceExtractor`, `TurkishTokenizer`) - Sentence boundary detection and tokenization first
2. **morphology** (`TurkishMorphology`) - Accepts tokens from tokenizer, returns `WordAnalysis`
3. **normalization** (`TurkishSpellChecker`, `TurkishSentenceNormalizer`) - Uses morphology output for spell check/normalization
4. **ner** - Named entity recognition using morphological analysis
5. **classification** - FastText-based text classification
6. **lang-id** - Language identification

### Module Integration
- `morphology` depends on `tokenization` and `core`
- `normalization` depends on `morphology`
- `ner` and `classification` depend on `morphology` and `tokenization`

## Key Classes and Patterns

### TurkishMorphology (morphology module)
- Use `TurkishMorphology.createWithDefaults()` or builder pattern
- **Important**: Create only one instance per application (initialization is expensive)
- Returns `WordAnalysis` containing `SingleAnalysis` results
- Supports caching via `AnalysisCache` for performance
- Builder options: `setLexicon()`, `useInformalAnalysis()`, `ignoreDiacriticsInAnalysis()`, `disableCache()`

### Dictionary Loading
- Default lexicon: `RootLexicon.getDefault()` or `RootLexicon.getDefault()`
- Custom dictionaries: `RootLexicon.builder().addTextDictionaries(path).build()`
- Dictionary format: one word per line, with optional POS tags (e.g., `kelime [Noun]`, `gitmek [Verb]`)

### Common Workflow
```java
TurkishMorphology morphology = TurkishMorphology.createWithDefaults();
WordAnalysis analysis = morphology.analyze("kelime");
SentenceAnalysis disambiguated = morphology.analyzeAndDisambiguate("Cümle.");
```

### Data Files Location
Resources are in module `src/main/resources/tr/` directories (dictionary files, ambiguity models, lookup tables).

## Test Organization
- Tests follow naming pattern: `*Test.java`
- Functional tests: `morphology/src/test/java/zemberek/morphology/TurkishMorphologyFunctionalTests.java`
- Base test class: `morphology/src/test/java/zemberek/morphology/analysis/AnalyzerTestBase.java`