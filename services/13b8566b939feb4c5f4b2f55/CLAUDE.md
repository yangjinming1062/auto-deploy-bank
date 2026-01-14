# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GenForce is an efficient PyTorch library for deep generative modeling, focusing on GANs (Generative Adversarial Networks). It supports PGGAN, StyleGAN, StyleGAN2, and StyleGAN2-ADA with distributed training capabilities.

## Commands

### Installation
```shell
pip install -r requirements.txt
# Requires: torch, torchvision, CUDA, and project-specific dependencies
```

### Training (Distributed)
```shell
# Local machine with multiple GPUs
GPUS=8
CONFIG=configs/stylegan_ffhq256.py
WORK_DIR=work_dirs/stylegan_ffhq256_train
./scripts/dist_train.sh ${GPUS} ${CONFIG} ${WORK_DIR}

# With Slurm cluster
GPUS=8 ./scripts/slurm_train.sh ${PARTITION} ${JOB_NAME} ${CONFIG} ${WORK_DIR}
```

### Testing/Evaluation
```shell
# Local machine
GPUS=8
CONFIG=configs/stylegan_ffhq256_val.py
WORK_DIR=work_dirs/stylegan_ffhq256_val
CHECKPOINT=checkpoints/stylegan_ffhq256.pth
./scripts/dist_test.sh ${GPUS} ${CONFIG} ${WORK_DIR} ${CHECKPOINT}

# With Slurm
GPUS=8 ./scripts/slurm_test.sh ${PARTITION} ${JOB_NAME} ${CONFIG} ${WORK_DIR} ${CHECKPOINT}
```

### Inference/Synthesis
```shell
# Generate images with pretrained model
python synthesize.py stylegan_ffhq1024

# With custom checkpoint
python synthesize.py --checkpoint checkpoints/stylegan_ffhq256.pth --config configs/stylegan_ffhq256_val.py --synthesis_num 1000 --fid_num 50000
```

### Model Conversion
Convert official TensorFlow/PyTorch models to this library's format:
```shell
python convert_model.py stylegan2 \
    --source_model_path ${SOURCE_MODEL_PATH} \
    --test_num 10 \
    --save_test_image
```

### Quick Demo
```shell
./scripts/stylegan_training_demo.sh
```

## Architecture

### Core Modules

- **`models/`** - GAN implementations with factory functions (`build_model`, `build_generator`, `build_discriminator`)
  - `pggan_*/stylegan_*/stylegan2_*/stylegan2ada_*` - Generator/discriminator pairs for each GAN type
  - `encoder.py` - Encoder network for GAN inversion
  - `perceptual_model.py` - Perceptual loss model (VGG-based)
  - `model_zoo.py` - Pre-trained model registry with download URLs

- **`runners/`** - Training/inference controllers with modular design
  - `base_runner.py` - Base class handling distributed training, checkpoint saving/loading
  - `base_gan_runner.py` - GAN-specific training logic
  - `stylegan_runner.py` - StyleGAN/StyleGAN2 training loops with progressive growing (LOD)
  - `encoder_runner.py` - Encoder training for GAN inversion

- **`datasets/`** - Data loading with LMDB support and iterative data loaders
  - `BaseDataset` - Handles zip/LMDB data formats with resolution and augmentation options
  - `IterDataLoader` - Infinite iterator with repeat capability for training

- **`runners/controllers.py`** - Training callbacks (Timer, LRScheduler, Snapshoter, FIDEvaluator, Checkpointer)

- **`metrics/`** - Evaluation metrics (FID, etc.)

### Configuration System

Configs are Python files in `configs/` defining:
- `runner_type` - Which runner class to use
- `gan_type` / `resolution` - Model architecture
- `batch_size` / `total_img` - Training settings
- `data` - Dataset paths (supports zip/LMDB with `root_dir`, `data_format`)
- `modules` - Generator/discriminator configs with `model`, `lr`, `opt`, `kwargs_train/val`
- `loss` - Loss function type and hyperparameters
- `controllers` - Callbacks with scheduling options

### Checkpoint Format

```python
checkpoint = {
    'models': {name: state_dict},
    'running_metadata': {'iter': int, 'seen_img': int},
    'optimizers': {name: state_dict},
    'learning_rates': {name: state_dict},
}
```

### Key Training Concepts

- **LOD (Level of Detail)** - Progressive growing used in PGGAN/StyleGAN for resolution increase
- **Generator smooth** - Exponential moving average of generator weights for stable evaluation
- **Style mixing** - Random mixing of latent codes during training for StyleGAN
- **Distributed** - Uses `torch.nn.parallel.DistributedDataParallel` with NCCL backend

## Model Zoo

Pre-trained models are registered in `models/model_zoo.py` with download URLs. Available models include PGGAN (celebahq, LSUN scenes), StyleGAN (FFHQ, LSUN), and StyleGAN2 (FFHQ, churches, cats, horses, cars). Download to `checkpoints/` directory.