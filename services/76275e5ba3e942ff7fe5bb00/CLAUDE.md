# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyTorch implementation of 3 GAN (Generative Adversarial Network) models using the same convolutional architecture base. Supports training on MNIST, Fashion-MNIST, CIFAR-10, and STL10 datasets.

## Common Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Train a model:**
```bash
python main.py --model DCGAN \
               --is_train True \
               --download True \
               --dataroot datasets/fashion-mnist \
               --dataset fashion-mnist \
               --epochs 30 \
               --cuda True \
               --batch_size 64
```

**Evaluate/generate images:**
```bash
python main.py --model DCGAN \
               --is_train False \
               --dataroot datasets/fashion-mnist \
               --dataset fashion-mnist \
               --cuda True \
               --batch_size 64 \
               --load_D discriminator.pkl \
               --load_G generator.pkl
```

**View training progress with TensorBoard:**
```bash
tensorboard --logdir ./logs/
```

## Architecture

**Entry Point (`main.py`):**
- Parses command-line arguments via `utils/config.py`
- Routes to appropriate model class based on `--model` flag
- Handles data loading and calls model train/evaluate methods

**Model Hierarchy:**
- All models inherit training infrastructure patterns from the base `GAN` class
- `models/gan.py` - Base GAN with fully-connected Generator (100→256→512→1024) and Discriminator (1024→512→256→1)
- `models/dcgan.py` - DCGAN with convolutional/transpose-conv architecture; Generator uses ConvTranspose2d (100→1024→512→256→channels), Discriminator uses Conv2d (channels→256→512→1024)
- `models/wgan_clipping.py` - WGAN with weight clipping enforcement
- `models/wgan_gradient_penalty.py` - WGAN-GP with gradient penalty loss

**Utilities (`utils/`):**
- `config.py` - Argument parsing (model type, dataset, epochs, batch size, cuda, etc.)
- `data_loader.py` - Dataset loading (MNIST, Fashion-MNIST, CIFAR-10, STL10) with transforms
- `tensorboard_logger.py` - TensorBoard logging via TensorFlow summary writers
- `fashion_mnist.py` - Custom MNIST/Fashion-MNIST dataset implementations
- `inception_score.py` - Inception score calculation for generated images

**Key Patterns:**
- All models define `G` (Generator) and `D` (Discriminator) as `nn.Module` attributes
- Training loop follows standard GAN pattern: train D on real/fake, then train G
- Models save checkpoints as `generator.pkl` and `discriminator.pkl`
- Generated images saved to `training_result_images/` and `interpolated_images/`
- DCGAN includes `generate_latent_walk()` for interpolating between random latent vectors

## Supported Model Arguments

| Flag | Options | Description |
|------|---------|-------------|
| `--model` | GAN, DCGAN, WGAN-CP, WGAN-GP | Model architecture |
| `--dataset` | mnist, fashion-mnist, cifar, stl10 | Dataset name |
| `--is_train` | True, False | Train or evaluate |
| `--cuda` | True, False | Enable GPU training |
| `--generator_iters` | integer | Iterations for WGAN generator (default: 10000) |