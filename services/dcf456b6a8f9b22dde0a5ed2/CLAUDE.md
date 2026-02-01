# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Protenix is a trainable PyTorch reproduction of AlphaFold 3 for predicting biomolecular complex structures (proteins, nucleic acids, ligands, ions, etc.). It includes diffusion-based structure generation, MSA/ESM features, and constraint-guided prediction.

## Build and Test Commands

```bash
# Install in editable mode (CPU-only)
python3 setup.py develop --cpu

# Install GPU version
python3 setup.py develop

# Run all tests
pytest tests/

# Run a specific test
pytest tests/test_attention_pair_bias.py -v

# Run tests with coverage
pytest tests/ --cov=protenix

# Development installation with pre-commit hooks
pip install pre-commit
pre-commit install
```

## Code Quality

This project uses pre-commit hooks for code quality:
- **flake8** with bugbear, pep8-naming, torchfix plugins
- **pydoclint** for docstring validation
- **ufmt** (black + usort) for formatting
- **License header** insertion for .py and .sh files

Run `pre-commit run --all-files` before committing.

## Architecture

### Core Model (`protenix/model/`)

- **protenix.py**: Main `Protenix` class implementing the AF3 algorithm (diffusion inference/training loop)
- **loss.py**: Multi-task loss computation (diffusion, distogram, confidence)
- **generator.py**: Diffusion noise schedulers and sampling
- **sample_confidence.py**: Confidence head for structure quality prediction
- **modules/**:
  - **transformer.py**: `AttentionPairBias` - core attention with pair bias (Algorithm 24 in AF3)
  - **pairformer.py**: MSA module and Pairformer stack (adapted from OpenFold)
  - **diffusion.py**: DiffusionModule for atom-level structure denoising
  - **embedders.py**: Input feature embedding (RelativePositionEncoding, InputFeatureEmbedder, ConstraintEmbedder)
  - **frames.py**: Rigid frame operations for structure representation
  - **head.py**: Output heads (DistogramHead, ConfidenceHead)
- **tri_attention/**: Optimized triangle attention implementations (Triton, cuEVariance, DeepSpeed)
- **layer_norm/**: Custom LayerNorm implementations for performance

### Data Pipeline (`protenix/data/`)

- **featurizer.py**: `Featurizer` class converting parsed structures to model inputs
- **parser.py**: Molecular structure parsing (PDB/CIF/mmCIF, ligands)
- **json_parser.py**, **json_maker.py**: JSON I/O format handling
- **msa_featurizer.py**: MSA (Multiple Sequence Alignment) processing
- **esm_featurizer.py**: ESM (Evolutionary Scale Modeling) embedding extraction
- **constraint_featurizer.py**: Constraint feature encoding (pocket, contact, substructure)
- **dataloader.py**: Training data loading with cropping and batching
- **dataset.py**: Dataset definitions for training/evaluation
- **ccd.py**: Chemical Component Dictionary handling for ligand processing

### Configuration System (`protenix/config/`)

- **config.py**: `ConfigManager` class handles hierarchical config merging from YAML/dict + CLI args
- Configs use `ml_collections.ConfigDict` with custom types:
  - `RequiredValue`: Must be provided
  - `DefaultNoneWithType`: Optional with type hint
  - `GlobalConfigValue`: References another config key
  - `ListValue`: Comma-separated CLI parsing

### Runners (`runner/`)

- **train.py**: Distributed training with torchrun, checkpointing, EMA, wandb
- **inference.py**: Single-structure inference with diffusion sampling
- **batch_inference.py**: CLI entry point (`protenix` command) for predict/msa/tojson
- **msa_search.py**: MSA search utility using external services (ColabFold-style)
- **dumper.py**: Output format conversion (PDB, CIF, mmCIF)

### Configuration Files (`configs/`)

- **configs_base.py**: Core training/inference configs (model architecture, optimization, data settings)
- **configs_data.py**: Dataset paths and data processing parameters
- **configs_inference.py**: Inference-specific settings
- **configs_model_type.py**: Model variants:
  - `protenix_base_default_v0.5.0`: Full model with MSA (368M params)
  - `protenix_base_constraint_v0.5.0`: With constraint support
  - `protenix_mini_esm_v0.5.0`: Lightweight with ESM (135M params)
  - `protenix_tiny_default_v0.5.0`: Tiny variant (109M params)

## Inference and Training

### CLI Commands

```bash
# Convert PDB/CIF to input JSON
protenix tojson --input examples/7pzb.pdb --out_dir ./output

# Run MSA search
protenix msa --input examples/example.json --out_dir ./output --msa_server_mode colabfold

# Predict structure (uses precomputed MSA by default)
protenix predict --input examples/example.json --out_dir ./output --seeds 101 --model_name "protenix_base_default_v0.5.0"

# Use ESM-only mini model (no MSA)
protenix predict --input examples/example.json --out_dir ./output --model_name "protenix_mini_esm_v0.5.0" --use_msa false
```

### Shell Scripts

```bash
# Demo inference
bash inference_demo.sh

# Demo training
bash train_demo.sh

# Fine-tuning
bash finetune_demo.sh
```

### Kernel Optimization

Set environment variables before running:
```bash
export LAYERNORM_TYPE=fast_layernorm  # fast_layernorm or torch
# Triangle attention: --triangle_attention "triattention" | "cuequivariance" | "deepspeed" | "torch"
# Triangle multiplicative: --triangle_multiplicative "cuequivariance" | "torch"
```

## Key Design Patterns

1. **Token-atom representation**: Structures use token-level (residue) and atom-level representations with broadcasting (`broadcast_token_to_atom`, `aggregate_atom_to_token`)

2. **Diffusion process**: Iterative denoising over multiple cycles (N_cycle) with fixed diffusion steps (N_step)

3. **Local rearrangement**: For efficiency, pair representations use sparse local operations (`rearrange_qk_to_dense_trunk`)

4. **Checkpointing**: Model uses gradient checkpointing for memory efficiency (`checkpoint_blocks`)

5. **Symmetric permutations**: Handles symmetric molecules (ligands) with `SymmetricPermutation` class

6. **Rigid body frames**: Protein/atom positions represented as rotation-translation matrices in `frames.py`

## Common Development Tasks

### Adding a New Model Variant

1. Add config to `configs/configs_model_type.py` following existing patterns
2. Define model architecture parameters (N_cycle, n_blocks per module)
3. Configure diffusion settings (N_step, gamma0)
4. Set `load_strict` appropriately (False for fine-tuning)

### Modifying Data Processing

- Training data flow: `dataset.py` → `dataloader.py` → model forward
- Cropping and shuffling controlled in `data_configs` (`train_crop_size`, `train_shuffle_mols`)
- MSA/ESM features optionally disabled via `data.msa.enable_*`, `esm.enable`

### Adding Custom Constraints

1. Implement constraint encoding in `protenix/model/modules/embedders.py`
2. Add constraint type to `protenix/data/constraint_featurizer.py`
3. Update `configs_model_type.py` with constraint embedder settings
4. Add constraint loss terms in `loss.py` if training with constraints