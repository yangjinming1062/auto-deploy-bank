# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NLPIA is a community-developed NLP library that accompanies the book "Natural Language Processing in Action". It provides utilities, data loaders, and example code for building NLP pipelines.

## Build and Test Commands

```bash
# Install in editable mode
pip install -e .

# Run all tests
python setup.py test

# Run tests directly with pytest
pytest

# Run a single test file
pytest tests/conftest.py

# Run with coverage
pytest --cov nlpia --cov-report xml

# Run linting
flake8 setup.py nlpia tests

# Run tox (multi-environment testing)
tox
```

## Architecture

### Core Modules

- **`loaders.py`**: Main data access module. Use `get_data(name)` to download and load datasets (word vectors, NLP corpora, etc.). Supports large downloads like word2vec (GoogleNews), GloVe, IMDB, Ubuntu dialog.
- **`constants.py`**: Path configuration. `DATA_PATH` (`src/nlpia/data`) for small datasets, `BIGDATA_PATH` (`src/nlpia/bigdata`) for large downloaded models/corpus.
- **`transcoders.py`**: Text processing utilities (tokenization, normalization).
- **`embedders.py`**: Word/sentence embedding utilities.
- **`features.py`**: Feature extraction for NLP pipelines.
- **`models.py`**: NLP model wrappers and implementations.
- **`web.py`**: HTTP utilities and web scraping helpers.

### Data Organization

- **Small data** (`src/nlpia/data/`): CSV/JSON/text files for datasets like stopwords, word lists, sentiment data.
- **Big data** (`src/nlpia/bigdata/`): Downloaded large files (word vectors, ML models, corpora). Populated at runtime via `get_data()`.

### Book Examples

`src/nlpia/book/examples/ch*.py` - Chapter-by-chapter examples from the NLP in Action book. Run these to verify examples work:

```python
from nlpia.book.examples import ch04
```

### Key Entry Points

```python
from nlpia.loaders import get_data
from nlpia.loaders import nlp  # SpaCy wrapper

# Load a dataset (auto-downloads if needed)
df = get_data('sms-spam')
wv = get_data('w2v')  # word2vec vectors

# Parse text with SpaCy
doc = nlp("Your text here")
```

## Style Conventions

From CONTRIBUTING.md:
- **Docstrings**: Google/NumPy style format (Args/Returns sections)
- **Line length**: ~120 characters max
- **Quotes**: Double quotes for natural language strings, single quotes for machine keys
- **Complexity**: McCabe threshold 12 (avoid deeply nested conditionals)
- **Doctests**: Include examples that serve as tests

## Dependencies

Core: pandas, nltk, spacy, gensim, tensorflow, keras, scikit-learn, matplotlib, seaborn

## Development Notes

- The project uses `pugnlp` for utilities like `clean_columns()` and file operations.
- `BIG_URLS` in `loaders.py` defines all downloadable datasets with URLs and metadata.
- Tests use pytest with doctests enabled (`--doctest-modules`).
- Large data files (word vectors) are downloaded to `BIGDATA_PATH` on first access.