# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LexNLP is a Python library for information retrieval and extraction from unstructured legal text (contracts, policies, procedures, etc.). It provides NLP functionality for legal documents including sentence segmentation, entity extraction, dates/money/percentages/citations detection, and ML-based classification.

## Build and Test Commands

```bash
# Install dependencies
pip install -r python-requirements.txt
pip install -r python-requirements-dev.txt

# Install the package
pip install -e .

# Download required NLTK data
python -m nltk.downloader punkt wordnet averaged_perceptron_tagger maxent_ne_chunker words

# Run all tests
py.test lexnlp

# Run tests with coverage and pylint
py.test --cov lexnlp --pylint --pylint-rcfile=.pylintrc lexnlp

# Run a single test file
py.test lexnlp/extract/en/tests/test_copyright.py

# Run a single test
py.test lexnlp/extract/en/tests/test_copyright.py::test_copyright
```

## Code Architecture

### Core Module Structure

- **`lexnlp/extract/`** - Main extraction functionality organized by language
  - `common/` - Shared base classes and utilities (detectors, annotations, parsers)
  - `en/` - English language extractors (dates, money, citations, courts, etc.)
  - `de/` - German language extractors
  - Each extractor follows a consistent pattern with `get_<entity>()`, `get_<entity>_list()`, and `get_<entity>_annotations()` functions

- **`lexnlp/nlp/`** - NLP preprocessing and tokenization
  - `en/` - English-specific NLP utilities
  - `train/` - Training utilities

- **`lexnlp/ml/`** - Machine learning utilities
  - `catalog/` - Pre-trained models
  - `gensim_utils.py` - Word embedding utilities
  - `sklearn_transformers.py` - ML transformers
  - `vectorizers.py` - Feature vectorization

- **`lexnlp/utils/`** - Common utilities for parsing, text processing, and Unicode handling

- **`lexnlp/tests/`** - Testing utilities and test data infrastructure

### Common Patterns

1. **Extractor functions** follow this signature:
   - `get_<entity>(text, **kwargs)` - Generator yielding tuples/annotations
   - `get_<entity>_list(text, **kwargs)` - Returns list of results
   - `get_<entity>_annotations(text, **kwargs)` - Yields annotation objects with coords

2. **Test data** is stored in `test_data/` directory following pattern:
   - `test_data/<module>/<path>/<test_function>.csv`
   - Tests use `lexnlp_tests.iter_test_data_text_and_tuple()` to load test cases

3. **Annotation objects** have `coords` property for text position and `get_cite()` method for serialization

### Configuration

- `LEXNLP_USE_STANFORD=true` - Enable Stanford NLP integration (requires Stanford CoreNLP jars in `libs/`)
- `.pylintrc` - Max line length 120, ignores FIXME/TODO notes
- All source files include standard copyright header (AGPL-3.0 licensed)

### Dependencies

- Core: numpy, pandas, nltk, scikit-learn, scipy, gensim, regex
- Date handling: dateparser
- Text processing: beautifulsoup4, lxml
- License: AGPL-3.0 (dual-licensing available)
