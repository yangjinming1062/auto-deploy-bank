# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenPrompt is an open-source framework for **prompt-learning** with pre-trained language models (PLMs). It provides a standard, flexible, and extensible framework to deploy prompt-learning pipelines by combining PLMs with templates and verbalizers. The framework is compatible with models from [Hugging Face Transformers](https://github.com/huggingface/transformers).

## Quick Start

### Installation

**From PyPI:**
```bash
pip install openprompt
```

**From source:**
```bash
pip install -r requirements.txt
python setup.py install
```

**For development (editable install):**
```bash
pip install -r requirements.txt
python setup.py develop
```

**Note:** Requires Python 3.8+ and PyTorch 1.8.1+

### Run a Simple Tutorial

The `tutorial/` directory contains practical examples. Start with:
```bash
python tutorial/0_basic.py
```

## Common Commands

### Build Documentation
```bash
cd docs
pip install -r requirements.txt
make clean
make html
```

### Download Datasets
```bash
bash datasets/download_text_classification.sh
bash datasets/download_super_glue.sh
bash datasets/download_fewglue.sh
# See datasets/ directory for all download scripts
```

### Run Tests
```bash
python -m pytest test/test_data_processor/
# Run a specific test
python -m pytest test/test_data_processor/test_text_classification_dataset.py::test_AgnewsProcessor -v
```

## Code Architecture

OpenPrompt follows a modular architecture with these key components:

### Core Framework (`openprompt/`)

**Base Classes:**
- `pipeline_base.py:26` - **PromptDataLoader**: Wraps datasets with templates and tokenization; extends PyTorch DataLoader
- `pipeline_base.py` - **PromptModel**: Base class for prompt-based models
- `prompt_base.py:22` - **Template**: Base class for templates that modify input text with placeholders and masks
- `prompt_base.py` - **Verbalizer**: Base class mapping labels to vocabulary words

**Main Model Classes (from `__init__.py:2`):**
- `PromptForClassification`: Classification tasks
- `PromptForGeneration`: Generation tasks
- `PromptDataLoader`: Data loading with template wrapping

**PLM Support (`plms/`):**
Supports 10+ model types via Hugging Face Transformers:
- BERT, RoBERTa, ALBERT, ELECTRA (MLM)
- T5, T5-LM (Seq2Seq)
- GPT, GPT-2, OPT, GPTJ (Causal LM)

Load models using:
```python
from openprompt.plms import load_plm
plm, tokenizer, model_config, WrapperClass = load_plm("bert", "bert-base-cased")
```

**Prompt Implementations (`prompts/`):**
- **Manual templates**: `ManualTemplate` with hardcoded text
- **Soft templates**: `SoftTemplate` with learnable embeddings
- **Mixed templates**: `MixedTemplate` combining hard/soft tokens
- **Prefix tuning**: `PrefixTuningTemplate` (see `4.1_all_tasks_are_generation.py:4`)
- **Manual verbalizers**: `ManualVerbalizer` with predefined label words
- **Soft verbalizers**: `SoftVerbalizer` with learnable projections
- **Automatic verbalizers**: `AutomaticVerbalizer`, `KnowledgeableVerbalizer`

**Data Utils (`data_utils/`):**
- InputExample: Standard input format
- InputFeatures: Tokenized features
- Dataset processors for various benchmarks (text classification, NLI, generation, etc.)

**Training (`trainer.py`):**
- `ClassificationRunner`: Standard classification training loop
- `GenerationRunner`: Text generation training
- `LMBFFClassificationRunner`: LM-BFF specific training
- `ProtoVerbClassificationRunner`: Prototype-based verbalizers

### Configuration System

Configuration uses **YACS CfgNode** (`default_config.py:3`):

**Key Configuration Nodes:**
- `cfg.environment`: GPU settings, model parallelism
- `cfg.plm`: Model name, path, optimization parameters
- `cfg.train`: Training epochs, batch size, gradient accumulation
- `cfg.logging`: Log path, levels, experiment tracking
- `cfg.checkpoint`: Save best/latest checkpoints
- `cfg.classification` / `cfg.generation`: Task-specific metrics

### Experiments (`scripts/`)

Organized by task type:
- `TextClassification/`: Sentiment analysis, topic classification
- `SuperGLUE/`: NLI, QA, commonsense reasoning
- `FewGLUE/`: Few-shot learning experiments
- `RelationClassification/`: Entity relation extraction
- `CondGen/`: Conditional generation

Each directory contains dataset-specific configuration files and results.

## Key Workflows

### Standard Prompt Learning Pipeline

```python
from openprompt import PromptDataLoader, PromptForClassification
from openprompt.data_utils import InputExample
from openprompt.plms import load_plm
from openprompt.prompts import ManualTemplate, ManualVerbalizer

# 1. Define task
classes = ["negative", "positive"]
dataset = [InputExample(guid=0, text_a="Example text", label=0)]

# 2. Load PLM
plm, tokenizer, model_config, WrapperClass = load_plm("bert", "bert-base-cased")

# 3. Create template
template = ManualTemplate(text='{"placeholder":"text_a"} It was {"mask"}', tokenizer=tokenizer)

# 4. Create verbalizer
verbalizer = ManualVerbalizer(classes=classes, label_words={"negative": ["bad"], "positive": ["good"]}, tokenizer=tokenizer)

# 5. Combine into model
model = PromptForClassification(template=template, plm=plm, verbalizer=verbalizer)

# 6. Create dataloader
dataloader = PromptDataLoader(dataset=dataset, template=template, tokenizer=tokenizer, tokenizer_wrapper_class=WrapperClass)

# 7. Train/inference
for batch in dataloader:
    logits = model(batch)
```

### Soft Template/Verbalizer Training

See `tutorial/1.4_soft_template.py` for learnable templates or `tutorial/1.2_soft_verbalizers.py` for learnable verbalizers.

### Generation Tasks

For generation, use `PromptForGeneration`:
```python
from openprompt import PromptForGeneration
model = PromptForGeneration(template=template, plm=plm)
```

See `tutorial/2.1_conditional_generation.py:1` and `tutorial/4.1_all_tasks_are_generation.py:1`.

## Supported Model Types

The framework distinguishes between three model architectures:

1. **MLM (Masked Language Models)**: BERT, RoBERTa, ALBERT, ELECTRA
   - Wrapper: `MLMTokenizerWrapper`
   - Use for classification, NLI, etc.

2. **LM (Causal Language Models)**: GPT, GPT-2, OPT, GPTJ
   - Wrapper: `LMTokenizerWrapper`
   - Use for generation, classification via prompting

3. **Seq2Seq**: T5, T5-LM
   - Wrapper: `T5TokenizerWrapper`, `T5LMTokenizerWrapper`
   - Use for conditional generation tasks

## Tutorial Scripts

Located in `tutorial/`:
- `0_basic.py`: Basic prompt learning pipeline
- `1.1_mixed_template.py`: Mixed hard/soft token templates
- `1.2_soft_verbalizers.py`: Learnable verbalizers
- `1.3_calibration.py`: Calibration techniques
- `1.4_soft_template.py`: Learnable templates
- `2.1_conditional_generation.py`: Generation tasks
- `3.1_LMBFF.py`: LM-BFF method
- `4.1_all_tasks_are_generation.py`: Unified generation paradigm
- `5.1_BMInf_CPM.py`: Chinese language models
- `6.1_chinese_dataset_uer_t5.py`: Custom tokenizer wrapper example
- `7_ernie_paddlepaddle/`: ERNIE support
- `8_CoT.py`: Chain-of-thought prompting
- `9_UltraChat.py`: Supervised instruction tuning

## Testing

Tests are in `test/test_data_processor/`:
- Test dataset processors (text classification, NLI, generation, etc.)
- Use standard pytest: `python -m pytest`
- Tests validate data loading, preprocessing, and processor correctness

## Documentation Build System

Documentation uses **Sphinx** (`docs/source/`):
```bash
cd docs
pip install -r requirements.txt
make clean
make html
```
GitHub Actions (`.github/workflows/main.yml:9`) automatically builds and deploys docs to gh-pages on push.

## Important Notes

- **Python version**: Requires Python 3.8+ (not 3.6+ as stated in some docs)
- **Manual installation**: PyTorch and scikit-learn are **not** auto-installed (see `setup.py:59-74`)
- **Model caching**: Models downloaded from Hugging Face are cached locally
- **Multi-GPU**: Configure via `cfg.environment` in default_config.py
- **CUDA devices**: Set `cfg.environment.cuda_visible_devices`
- **Template language**: Uses JSON-like syntax with placeholders like `{"placeholder":"text_a"}` and special tokens like `{"mask"}`

## Dependencies

Key dependencies from `requirements.txt`:
- `transformers>=4.19.0`: Hugging Face model zoo
- `torch`: Deep learning framework
- `datasets`: Hugging Face dataset utilities
- `sentencepiece`: Tokenization for some models
- `tensorboardX`: Logging
- `yacs`: Configuration system
- `dill`: Serialization
- `tqdm`: Progress bars