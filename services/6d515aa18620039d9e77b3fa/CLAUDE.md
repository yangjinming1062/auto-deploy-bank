# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Limdu is a machine-learning framework for Node.js supporting **multi-label classification**, **online learning**, and **real-time classification**. It's designed for natural language understanding in dialog systems and chat-bots.

## Build & Test Commands

```bash
npm test              # Run all tests with mocha (--recursive flag)
npm run test -- --grep "pattern"  # Run tests matching a pattern
```

Tests use Mocha with `should` assertions and are located in `test/` with subdirectories:
- `test/classifiersTest/` - Tests for binary and multilabel classifiers
- `test/featuresTest/` - Tests for feature extraction utilities
- `test/utilsTest/` - Tests for utility functions

## Architecture

### Module Structure

```
limdu/
├── index.js                 # Main entry point
├── classifiers/             # Binary and multilabel classifiers
│   ├── index.js            # Exports: NeuralNetwork, Bayesian, Winnow, Perceptron, SVM, kNN, DecisionTree, multilabel
│   ├── EnhancedClassifier.js # Meta-classifier wrapper with feature extraction/normalization
│   └── multilabel/         # Multi-label algorithms: BinaryRelevance, PassiveAggressive, HOMER, MetaLabeler, etc.
├── features/               # Feature extraction and normalization
│   ├── NGramsOfWords.js    # Extract word n-gram features
│   ├── NGramsOfLetters.js  # Extract character n-gram features
│   ├── FeatureLookupTable.js # Convert string features to integer indices
│   └── normalizers/        # LowerCaseNormalizer, RegexpNormalizer
├── formats/                # Data format converters (ARFF, JSON, TSV, SVM-light)
├── utils/                  # Utilities: PrecisionRecall, partitions, trainAndTest
└── test/                   # Mocha tests
```

### Key Concepts

**Classifiers** (`classifiers/index.js`):
- Support both `trainBatch(dataset)` and `trainOnline(sample, label)` methods
- Binary classifiers return single values (0/1 or string labels)
- Multi-label classifiers (in `classifiers/multilabel/`) return arrays of labels
- Some classifiers support `explain` parameter in `classify()` to return explanation objects

**EnhancedClassifier** (`classifiers/EnhancedClassifier.js`):
- Meta-classifier that wraps any classifier with preprocessing pipeline:
  - `normalizer` - Normalizes input before feature extraction
  - `featureExtractor` - Converts input to feature-value pairs
  - `featureLookupTable` - Converts features to integer indices
  - `spellChecker` - Optional spell correction for classification
- Supports `inputSplitter` for segmenting multi-sentence inputs
- Stores `pastTrainingSamples` for retraining capabilities

**Feature Extractors** (`features/index.js`):
- Functions with signature `function(input, features) { ... }` that populate a features object
- Can be chained as arrays or wrapped in `CollectionOfExtractors`
- Use `features.normalize()` helper to convert array to collection if needed

**Training Data Format**:
```javascript
// Binary classification
{input: sample, output: label}

// Multi-label classification
{input: sample, output: ["label1", "label2"]}
```

### Adding a New Classifier

1. Create the classifier file in an appropriate subdirectory of `classifiers/`
2. Implement `trainBatch(dataset)`, `trainOnline(input, output)`, and `classify(input)` methods
3. Export from `classifiers/index.js`
4. Add corresponding tests in `test/classifiersTest/`

### Release Process

Uses semantic-release with commits following Conventional Commits format. Run `npm test` successfully before committing changes.