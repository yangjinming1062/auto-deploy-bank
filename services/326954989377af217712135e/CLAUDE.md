# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **MindSpore Model Zoo** - a collection of AI/ML models implemented using the [MindSpore](https://www.mindspore.cn/) deep learning framework. Models span computer vision (CV), natural language processing (NLP), audio, recommendation systems, and graph neural networks.

### Directory Structure

- `official/` - Officially maintained SOTA models maintained by the MindSpore team
- `research/` - Research models contributed by institutions and researchers
- `community/` - External community models and toolkit links
- `utils/` - Shared utilities for distributed training, data conversion, and inference
- `benchmark/` - Benchmark scripts for Ascend hardware

## Model Contribution Standards

When contributing new models, follow the standard directory structure:

```
model_zoo/
├── official or research/
│   └── MODEL_NAME/
│       ├── README.md                    # Required model documentation
│       ├── requirements.txt             # Python dependencies
│       ├── train.py                     # Training script
│       ├── eval.py                      # Evaluation script
│       ├── export.py                    # Model export script
│       ├── scripts/                     # Shell scripts
│       │   ├── run_distribute_train.sh  # Distributed training
│       │   ├── run_standalone_train.sh  # Single machine training
│       │   └── run_eval.sh              # Evaluation
│       ├── src/                         # Model source code
│       │   ├── ModelNet.py              # Model architecture
│       │   ├── config.py                # Configuration parameters
│       │   ├── dataset.py               # Data loading
│       │   └── callback.py              # Training callbacks
│       └── config/                      # YAML config files
```

## Common Operations

### Generate HCCL Config for Ascend Distributed Training

```bash
cd utils/hccl_tools
python hccl_tools.py --device_num="[0,8)" --visible_devices="0,1,2,3,4,5,6,7"
```

The generated `hccl_8p_0-7_xxx.json` file is required for distributed training on Ascend hardware.

### Run Distributed Training (Ascend)

```bash
bash scripts/run_distribute_train.sh RANK_TABLE_FILE DATASET_PATH CONFIG_PATH
```

### Run Single Machine Training (GPU/Ascend)

```bash
# Ascend
bash scripts/run_standalone_train.sh DEVICE_ID DATASET_PATH CONFIG_PATH

# GPU
bash scripts/run_standalone_train_gpu.sh DEVICE_ID DATASET_PATH CONFIG_PATH
```

### Run Evaluation

```bash
bash scripts/run_eval.sh DATASET_PATH CONFIG_PATH CHECKPOINT_PATH
```

### Training with MindSpore

Most models use this pattern:

```bash
python train.py --config_path=/path/to/config.yaml --data_path=/path/to/dataset
```

### Configuration Pattern

Models use YAML config files combined with argparse. Config files can contain:
1. Configuration parameters
2. Parameter descriptions (second YAML doc)
3. Parameter choices (third YAML doc)

Example config parsing in `src/model_utils/config.py` handles merging CLI args with YAML configs.

## Code Style

- **Python**: Follow [PEP 8](https://pep8.org/). Use pylint for linting.
- **C++**: Follow [Google C++ Style Guide](http://google.github.io/styleguide/cppguide.html). Use cpplint and cppcheck.
- **Shell**: Use shellcheck for shell scripts.
- **Markdown**: Use markdownlint (MD007: indent=4 spaces, MD009: 0 or 2 trailing spaces).

All code should pass linting checks before submission.

## Model References for Implementation

Use these well-structured models as references:
- [ResNet](official/cv/ResNet) - Standard training/eval pattern with distributed support
- [YOLOv5](official/cv/YOLOv5) - Object detection with YOLO toolbox integration
- [Transformer](official/nlp/Transformer) - NLP model reference

## MindSpore Integration

- Import: `import mindspore as ms`
- Neural network: `import mindspore.nn as nn`
- For Ascend distributed training, use `mindspore.communication.management.init()`
- Models are typically wrapped with `ms.Model(net, loss_fn=loss, optimizer=opt)`
- Use `model.train()` for training and `model.eval()` for evaluation

## Environment Notes

- Models target MindSpore framework with support for Ascend, GPU, and CPU backends
- Check `requirements.txt` for model-specific dependencies
- Some models require specific dataset paths or preprocessing
- Use `modelarts/` directory for ModelArts cloud platform compatibility

## Contributing

Before contributing:
1. Sign the [MindSpore CLA](https://www.mindspore.cn/icla)
2. Review [CONTRIBUTING.md](CONTRIBUTING.md) for code style and workflow
3. Use [how_to_contribute/README_TEMPLATE.md](how_to_contribute/README_TEMPLATE.md) for model documentation