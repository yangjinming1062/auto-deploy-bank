# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Rasa NLU** (version 0.12.2), a natural language understanding library for building chatbots and conversational agents. This is a fork specifically optimized for Chinese language support, extending the original RasaHQ/rasa_nlu project.

The core purpose is to parse natural language text to extract:
- **Intents**: What the user wants to do (e.g., "greet", "restaurant_search", "medical")
- **Entities**: Specific pieces of information (e.g., "disease", "location", "cuisine")

## Architecture

### Pipeline-Based Design

Rasa NLU uses a **component pipeline** architecture where processing flows through configurable stages:

```
Text Input → Tokenizer → Featurizer → NER Extractor → Intent Classifier → Output
```

All components inherit from the base `Component` class in `rasa_nlu/components.py:101-250`. Components must implement:
- `train()`, `process()`, or `train_process()` methods
- `requires`: List of context properties needed from previous components
- `provides`: List of context properties this component adds

### Core Components

**Tokenizers** (`rasa_nlu/tokenizers/`):
- Jieba tokenizer (for Chinese)
- MITIE, spaCy, whitespace tokenizers
- Each produces `tokens` for subsequent processing

**Featurizers** (`rasa_nlu/featurizers/`):
- Convert tokens into feature vectors
- Supports n-grams, regex patterns, MITIE features, count vectors

**Entity Extractors** (`rasa_nlu/extractors/`):
- MITIE, spaCy, CRF (conditional random fields)
- Duckling (for numbers, dates, amounts)
- Entity synonyms mapping

**Intent Classifiers** (`rasa_nlu/classifiers/`):
- sklearn, MITIE, embedding-based, keyword-based
- Classifies user intent with confidence score

### Key Modules

| File | Purpose |
|------|---------|
| `train.py` | Training logic and CLI entry point for `python -m rasa_nlu.train` |
| `server.py` | HTTP server for inference via `python -m rasa_nlu.server` |
| `model.py` | Model management - `Trainer`, `Interpreter`, `Metadata` classes |
| `components.py` | Component registry, base classes, validation logic |
| `config.py` | Configuration loading and validation (`RasaNLUModelConfig`) |
| `data_router.py` | Routes requests to appropriate models across projects |
| `evaluate.py` | Model evaluation and testing utilities |

## Development Commands

### Installation
```bash
# Install in development mode
pip install -e .

# Install with specific backend support (extras_require)
pip install -e .[spacy]     # spaCy backend
pip install -e .[mitie]     # MITIE backend
pip install -e .[tensorflow] # TensorFlow backend
pip install -e .[jieba]     # Chinese support (Jieba)

# Install dev dependencies
pip install -r alt_requirements/requirements_dev.txt

# Alternative dependency sets in alt_requirements/
# e.g., alt_requirements/requirements.txt, alt_requirements/requirements_dev.txt
```

**Dependencies:**
- Base requirements: `requirements.txt`
- Dev requirements: `alt_requirements/requirements_dev.txt`
- Alternative sets: `alt_requirements/` directory
- Optional backends: Extras in `setup.py` (`spacy`, `tensorflow`, `mitie`, `jieba`)
- Documentation: Sphinx (build with `make livedocs`)

### Testing
```bash
# Run all tests
make test

# Run linting (PEP8 checks - 120 char line length, ignores W503/E126)
make lint

# Run specific test file
py.test tests/base/test_config.py -v

# Run specific test category (base tests or training tests)
py.test tests/base/ -v
py.test tests/training/ -v

# Run with coverage
py.test tests --verbose --cov rasa_nlu

# Run with PEP8 style checking
py.test --pep8 -m pep8
```

**Test Structure:**
- `tests/base/` - 18 test files for components, config, server, etc.
- `tests/training/` - Training functionality tests
- `tests/conftest.py` - Shared pytest fixtures
- Coverage exclusions configured in `.coveragerc`
- PEP8 and pytest settings in `setup.cfg`

### Building & Training

**Train a model:**
```bash
python -m rasa_nlu.train \
  -c sample_configs/config_jieba_mitie_sklearn.yml \
  --data data/examples/rasa/demo-rasa_zh.json \
  --path models
```

**Start server:**
```bash
python -m rasa_nlu.server \
  -c sample_configs/config_jieba_mitie_sklearn.yml \
  --path models
```

**Evaluate model:**
```bash
python -m rasa_nlu.evaluate \
  -c sample_configs/config_jieba_mitie_sklearn.yml \
  --data data/examples/rasa/demo-rasa_zh.json \
  --path models
```

### Maintenance
```bash
make clean          # Remove build artifacts
make livedocs       # Build live-reloading docs (Sphinx)
make check-readme   # Validate README for PyPI
```

### Docker
**Dockerfiles available in `docker/`:**
- `Dockerfile` - Bare minimum
- `Dockerfile_full` - Full installation with all backends
- `Dockerfile_mitie` - MITIE backend only
- `Dockerfile_spacy_sklearn` - spaCy + sklearn backend
- `Dockerfile_test` - Testing environment

**Build and run:**
```bash
# Build image
docker build -f docker/Dockerfile_full -t rasa-nlu .

# Run server
docker run -p 5000:5000 -v $(pwd)/models:/app/models rasa-nlu \
  python -m rasa_nlu.server -c config.yml --path /app/models
```

Google Cloud Build configuration in `cloudbuild.yaml`.

## Configuration

**Pipeline Configuration:** YAML files define the processing pipeline. See `sample_configs/` for examples.

**Common Chinese Configuration** (`sample_configs/config_jieba_mitie_sklearn.yml`):
```yaml
language: "zh"
pipeline:
- name: "nlp_mitie"
  model: "data/total_word_feature_extractor_zh.dat"
- name: "tokenizer_jieba"
- name: "ner_mitie"
- name: "ner_synonyms"
- name: "intent_entity_featurizer_regex"
- name: "intent_featurizer_mitie"
- name: "intent_classifier_sklearn"
```

**Training Data Format:** JSON (see `data/examples/rasa/demo-rasa_zh.json`) or Markdown format.

## CI/CD

- **Travis CI** configuration in `.travis.yml`
- **Python versions:** 2.7, 3.5, 3.6
- **Testing stages:**
  - Lint check (`py.test --pep8`)
  - Unit tests with coverage (base, training)
  - Downloads spaCy models
  - Installs MITIE from GitHub
  - Documentation deployment
  - PyPI deployment on tags (automatic on master branch tags)
- **Google Cloud Build** - `cloudbuild.yaml` for Docker image building
- **GitHub templates** - PR template, issue templates, and funding config in `.github/`

## Important Notes

1. **Component Dependencies:** Components have `requires`/`provides` contracts. When adding/modifying components, ensure dependencies are satisfied (see `components.py:66-88`).

2. **Model Persistence:** Models are saved in timestamped directories (e.g., `models/default/model_20170921-170911/`). The `Metadata` class in `model.py` handles model metadata.

3. **Training Data Loading:** Use `load_data()` from `rasa_nlu.training_data` - supports JSON files, directories, or URLs (see `training_data/loading.py`).

4. **Server Protocol:** The server exposes `/parse` endpoint for inference with JSON payload: `{"q": "query text", "project": "project_name", "model": "model_name"}`.

5. **Chinese Language Support:**
   - Requires `jieba` tokenizer
   - Needs MITIE Chinese word feature extractor: `data/total_word_feature_extractor_zh.dat`
   - Can use custom Jieba dictionary via `user_dicts` parameter

## Adding New Components

1. Create component class inheriting from `Component`
2. Implement required methods (`train`, `process`, etc.)
3. Register in `rasa_nlu/registry.py`
4. Update component imports in `rasa_nlu/__init__.py`
5. Add tests in `tests/` directory
6. Update documentation

See existing components in `rasa_nlu/{classifiers,extractors,featurizers,tokenizers}/` for examples.