# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DMD2 (Improved Distribution Matching Distillation) is a research project for distilling large-scale diffusion models (SDXL, SDv1.5, ImageNet) into efficient one-step or few-step generators. It uses a teacher-student distillation approach with distribution matching and GAN losses.

## Environment Setup

```bash
conda create -n dmd2 python=3.8 -y
conda activate dmd2
pip install --upgrade anyio
pip install -r requirements.txt
python setup.py develop
```

## Common Commands

### SDXL Inference (Demo)
```bash
# 4-step generation (higher quality)
python -m demo.text_to_image_sdxl --checkpoint_path SDXL_CKPT_PATH --precision float16

# 1-step generation
python -m demo.text_to_image_sdxl --num_step 1 --checkpoint_path SDXL_CKPT_PATH --precision float16 --conditioning_timestep 399
```

### ImageNet Inference
```bash
python -m demo.imagenet_example --checkpoint_path IMAGENET_CKPT_PATH
```

### SDXL Training (8-node FSDP)
```bash
# Generate FSDP configs first
python main/sdxl/create_sdxl_fsdp_configs.py --folder fsdp_configs/EXP_NAME --master_ip $MASTER_IP --num_machines 8 --sharding_strategy 4

# Start training on all nodes (NODE_RANK 0-7)
bash experiments/sdxl/sdxl_cond999_8node_lr5e-7_denoising4step_diffusion1000_gan5e-3_guidance8_noinit_noode_backsim_scratch.sh $CHECKPOINT_PATH $WANDB_ENTITY $WANDB_PROJECT fsdp_configs/EXP_NAME NODE_RANK
```

### ImageNet Training
```bash
bash experiments/imagenet/imagenet_gan_classifier_genloss3e-3_diffusion1000_lr2e-6_scratch.sh $CHECKPOINT_PATH $WANDB_ENTITY $WANDB_PROJECT
```

### Evaluation (SDXL)
```bash
python main/sdxl/test_folder_sdxl.py \
    --folder $CHECKPOINT_PATH/sdxl_cond999_8node_lr5e-7_denoising4step_diffusion1000_gan5e-3_guidance8_noinit_noode_backsim_scratch/TIMESTAMP/ \
    --conditioning_timestep 999 --num_step 4 --wandb_entity $WANDB_ENTITY \
    --wandb_project $WANDB_PROJECT --eval_res 512 --ref_dir $CHECKPOINT_PATH/coco10k/subset \
    --anno_path $CHECKPOINT_PATH/coco10k/all_prompts.pkl --total_eval_samples 10000 --clip_score
```

## Architecture

### Core Components

**SDUniModel** (`main/sd_unified_model.py`): Unified wrapper containing:
- `feedforward_model`: The student/generator UNet being trained
- `guidance_model`: Contains both frozen teacher (real_unet) and trainable critic (fake_unet)
- Text encoders (CLIP for SDv1.5, SDXLTextEncoder for SDXL)
- VAE decoder (AutoencoderKL or AutoencoderTiny for fast decoding)

**SDGuidance** (`main/sd_guidance.py`): Manages score estimation and losses:
- `real_unet`: Frozen teacher model for score estimation
- `fake_unet`: Trainable critic that learns to estimate distribution of student samples
- `cls_pred_branch`: GAN discriminator head for distinguishing real vs generated images

**Trainer** (`main/train_sd.py`): Coordinates training loop:
- Two-time-scale update: Generator and guidance model updated at different rates (`dfake_gen_update_ratio`)
- Supports FSDP for distributed training
- Weights & Biases logging with visual grids

### Training Data Flow

1. Generate noise latents
2. Forward pass through student generator
3. Compute distribution matching loss (matches student output distribution to teacher)
4. Compute GAN loss (if enabled) comparing generated images to real training images
5. Update guidance model first, then generator (or based on update ratio)

### Key Loss Components

- **Distribution Matching Loss** (`loss_dm`): Matches generated image distribution to teacher's distribution
- **GAN Loss** (`loss_fake_mean`): Trains fake_unet to predict noise for generated images
- **Classifier Loss** (`gen_cls_loss`, `guidance_cls_loss`): Realism discrimination on clean images

## Critical Training Arguments

| Flag | Description |
|------|-------------|
| `--sdxl` | Use SDXL model architecture (required for text-to-image) |
| `--use_fp16` | Use BF16 precision (FP16 causes divergence on ImageNet) |
| `--tiny_vae` | Use Tiny VAE for faster decoding and lower memory |
| `--denoising` | Enable multi-step denoising training (SDXL only) |
| `--backward_simulation` | Simulate inference-time sampling during training |
| `--cls_on_clean_image` | Enable GAN discriminator loss on real images |
| `--gen_cls_loss` | Enable generator classifier loss |
| `--dfake_gen_update_ratio` | Guidance updates per generator update (default 5) |
| `--conditioning_timestep` | Timestep for single-step generation (999 for 4-step, 399 for 1-step) |

## Known Issues

- **FSDP for SDXL training is slow** - help appreciated
- **LoRA training is slower than full finetuning** and uses same memory - help appreciated
- ImageNet training requires BF16; FP16 causes divergence without loss scaling

## Key Files

- `main/train_sd.py`: Main training script with Trainer class
- `main/sd_unified_model.py`: SDUniModel architecture
- `main/sd_guidance.py`: SDGuidance with loss computations
- `main/sd_unet_forward.py`: Custom forward passes including classify_forward
- `main/utils.py`: Utility functions (get_x0_from_noise, data loaders)
- `experiments/*/`: Experiment scripts for each model variant
- `fsdp_configs/`: Accelerate FSDP configuration files