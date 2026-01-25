# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GenForce is an efficient PyTorch library for deep generative modeling, supporting distributed training of GANs (Generative Adversarial Networks). It implements PGGAN, StyleGAN, StyleGAN2, and StyleGAN2-ADA architectures with a modular controller-based design.

## Build & Run Commands

### Installation
```shell
conda create -n genforce python=3.7
conda activate genforce
conda install cudatoolkit=10.0 cudnn=7.6.5  # Optional: for TF model conversion
pip install torch==1.7 torchvision==0.8
pip install -r requirements.txt
```

### Training
**Local machine (distributed):**
```shell
GPUS=8
CONFIG=configs/stylegan_ffhq256.py
WORK_DIR=work_dirs/stylegan_ffhq256_train
./scripts/dist_train.sh ${GPUS} ${CONFIG} ${WORK_DIR}
```

**SLURM cluster:**
```shell
CONFIG=configs/stylegan_ffhq256.py
WORK_DIR=work_dirs/stylegan_ffhq256_train
GPUS=8 ./scripts/slurm_train.sh ${PARTITION} ${JOB_NAME} ${CONFIG} ${WORK_DIR}
```

### Testing/Inference
```shell
GPUS=8
CONFIG=configs/stylegan_ffhq256_val.py
WORK_DIR=work_dirs/stylegan_ffhq256_val
CHECKPOINT=checkpoints/stylegan_ffhq256.pth
./scripts/dist_test.sh ${GPUS} ${CONFIG} ${WORK_DIR} ${CHECKPOINT}
```

### Quick Demo
```shell
./scripts/stylegan_training_demo.sh  # Train on toy dataset (500 animeface images)
python synthesize.py stylegan_ffhq1024  # Synthesize images with pretrained model
```

### Model Conversion
Convert official TF/PyTorch pretrained models to GenForce format:
```shell
python convert_model.py stylegan2 \
    --source_model_path ${SOURCE_MODEL_PATH} \
    --test_num 10 \
    --save_test_image
```

## Architecture

### Core Modules

**`models/`** - Generator and discriminator implementations
- `pggan_generator.py` / `pggan_discriminator.py`
- `stylegan_generator.py` / `stylegan_discriminator.py`
- `stylegan2_generator.py` / `stylegan2_discriminator.py`
- `stylegan2ada_generator.py` / `stylegan2ada_discriminator.py`
- `encoder.py` - GAN inversion encoders
- `model_zoo.py` - Pretrained model registry with download URLs

**`runners/`** - Training/evaluation logic with controller pattern
- `base_runner.py` - Base class with distributed training scaffolding
- `base_gan_runner.py` - Base GAN training loop
- `stylegan_runner.py` - StyleGAN training (lod-based progressive growth)
- `encoder_runner.py` - Encoder training for GAN inversion
- `controllers/` - Modular callbacks: Checkpointer, FIDEvaluator, Snapshoter, ProgressScheduler, RunningLogger
- `losses/` - `LogisticGANLoss`, `EncoderLoss`

**`datasets/`** - Data loading
- `datasets.py` - `BaseDataset` supporting folders and zip files
- `dataloaders.py` - `IterDataLoader` for iterative loading with repeat support
- `distributed_sampler.py` - Custom distributed sampling

**`metrics/`** - Evaluation metrics
- `fid.py` - Fréchet Inception Distance
- `inception.py` - Inception Score computation

**`converters/`** - Model weight converters from official implementations
- `pggan_converter.py`, `stylegan2_converter.py`, `stylegan2ada_pth_converter.py`
- Contains mirrored official TF/PyTorch code for pickle loading

### Configuration System

Configs are Python files (e.g., `configs/stylegan_ffhq256.py`) with attributes:
```python
runner_type = 'StyleGANRunner'  # or 'StyleGAN2Runner'
gan_type = 'stylegan'           # pggan, stylegan, stylegan2, stylegan2ada
resolution = 256                # Output resolution
batch_size = 4                  # Per-GPU batch
data = dict(
    train=dict(root_dir='data/ffhq.zip', data_format='zip', resolution=256, mirror=0.5),
    val=dict(root_dir='data/ffhq.zip', data_format='zip', resolution=256),
)
modules = dict(
    discriminator=dict(model=dict(gan_type=gan_type, resolution=resolution), ...),
    generator=dict(model=dict(gan_type=gan_type, resolution=resolution), ...),
)
controllers = dict(RunningLogger=dict(every_n_iters=10), Snapshoter=dict(...), ...)
loss = dict(type='LogisticGANLoss', d_loss_kwargs=dict(r1_gamma=10.0), ...)
```

### Key Entry Points

- `train.py` - Distributed training launcher (uses `torch.distributed.launch`)
- `test.py` - Inference and FID evaluation
- `synthesize.py` - Quick image synthesis with pretrained models
- `convert_model.py` - Convert official model weights

### Common Development Patterns

1. **Adding a new GAN type**: Register in `models/__init__.py` (`_GAN_TYPES_ALLOWED`), create generator/discriminator classes, add builder functions, update `runners/__init__.py`

2. **Adding a new controller**: Create class in `runners/controllers/`, register in `runners/controllers/__init__.py`, add to config `controllers` dict

3. **Checkpoint format**: Dict with keys `models`, `running_metadata`, `optimizers`, `learning_rates`

4. **Distributed training**: Uses `torch.distributed.launch` with ` DistributedDataParallel`, config via `init_dist()` in `utils/misc.py`