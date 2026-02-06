# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DMD2 (Improved Distribution Matching Distillation) - A research project for distilling diffusion models into efficient one-step generators. Published at NeurIPS 2024. Supports SDv1.5, SDXL, and ImageNet-64x64 models.

## Environment Setup

```bash
conda create -n dmd2 python=3.8 -y
conda activate dmd2
pip install --upgrade anyio
pip install -r requirements.txt
python setup.py develop
```

## Common Commands

### Running Demos
```bash
# ImageNet generation
python -m demo.imagenet_example --checkpoint_path IMAGENET_CKPT_PATH

# SDXL text-to-image (4-step, higher quality)
python -m demo.text_to_image_sdxl --checkpoint_path SDXL_CKPT_PATH --precision float16

# SDXL 1-step generation
python -m demo.text_to_image_sdxl --num_step 1 --checkpoint_path SDXL_CKPT_PATH --precision float16 --conditioning_timestep 399
```

### Training
Training uses `accelerate` for distributed training. FSDP is used for multi-node training (8 nodes with 8 GPUs each for SDXL).

**ImageNet-64x64:**
```bash
bash experiments/imagenet/imagenet_gan_classifier_genloss3e-3_diffusion1000_lr2e-6_scratch.sh $CHECKPOINT_PATH $WANDB_ENTITY $WANDB_PROJECT
```

**SDXL (4-step):**
```bash
# First create FSDP config
python main/sdxl/create_sdxl_fsdp_configs.py --folder fsdp_configs/EXP_NAME --master_ip $MASTER_IP --num_machines 8 --sharding_strategy 4

# Then run on all 8 nodes
bash experiments/sdxl/sdxl_cond999_8node_lr5e-7_denoising4step_diffusion1000_gan5e-3_guidance8_noinit_noode_backsim_scratch.sh $CHECKPOINT_PATH $WANDB_ENTITY $WANDB_PROJECT fsdp_configs/EXP_NAME NODE_RANK_ID
```

**SDv1.5:**
```bash
bash experiments/sdv1.5/laion6.25_sd_baseline_8node_guidance1.75_lr1e-5_seed10_dfake10_from_scratch.sh $CHECKPOINT_PATH $WANDB_ENTITY $WANDB_PROJECT $MASTER_IP
```

### Evaluation
Evaluate checkpoints continuously during training:

**ImageNet:**
```bash
python main/edm/test_folder_edm.py --folder $CHECKPOINT_PATH/... --wandb_name test_... --wandb_entity $WANDB_ENTITY --wandb_project $WANDB_PROJECT --resolution 64 --label_dim 1000 --ref_path $CHECKPOINT_PATH/imagenet_fid_refs_edm.npz --detector_url $CHECKPOINT_PATH/inception-2015-12-05.pkl
```

**SDXL:**
```bash
python main/sdxl/test_folder_sdxl.py --folder $CHECKPOINT_PATH/... --conditioning_timestep 999 --num_step 4 --wandb_entity $WANDB_ENTITY --wandb_project $WANDB_PROJECT --eval_res 512 --ref_dir $CHECKPOINT_PATH/coco10k/subset --anno_path $CHECKPOINT_PATH/coco10k/all_prompts.pkl --total_eval_samples 10000 --clip_score
```

**SDv1.5:**
```bash
python main/test_folder_sd.py --folder $CHECKPOINT_PATH/... --wandb_name test_... --wandb_entity $WANDB_ENTITY --wandb_project $WANDB_PROJECT --image_resolution 512 --latent_resolution 64 --num_train_timesteps 1000 --eval_res 256 --ref_dir $CHECKPOINT_PATH/val2014 --total_eval_samples 30000 --model_id "runwayml/stable-diffusion-v1-5" --pred_eps
```

### Downloading Checkpoints
```bash
bash scripts/download_hf_checkpoint.sh model/path/name OUTPUT_PATH
```

## Architecture

### Core Components

**`main/sd_unified_model.py` - SDUniModel**: Unified model wrapping both generator and discriminator. Contains:
- `feedforward_model`: Student UNet generator (trained)
- `guidance_model`: SDGuidance instance containing frozen teacher + fake critic
- `text_encoder`: CLIP (SDv1.5) or SDXL dual text encoders
- `vae`: AutoencoderKL or AutoencoderTiny for image encoding/decoding

**`main/sd_guidance.py` - SDGuidance**: Guidance module with two UNets:
- `real_unet`: Frozen teacher diffusion model
- `fake_unet`: Trainable student that acts as a "fake critic"
- Optional `cls_pred_branch`: Classifier for realism discrimination
- Computes distribution matching loss and GAN loss

**`main/train_sd.py` - Trainer**: Main training loop with two time-scale update rule:
- `dfake_gen_update_ratio`: Controls generator update frequency (e.g., 5 means generator updates every 5th step)
- Separate optimizers for generator and guidance model
- Supports FSDP for large-scale training
- LMDB datasets for efficient data loading

**`main/utils.py`**: Utilities including:
- `get_x0_from_noise()`: Derive x0 from noise prediction using DDIM scheduler alpha values
- `SDTextDataset`: Text prompt dataset
- `SDImageDatasetLMDB`: LMDB-based image dataset
- Visualization helpers

### Key Training Techniques

1. **Two Time-Scale Update Rule**: Generator and guidance model update at different paces via `dfake_gen_update_ratio`
2. **Distribution Matching Loss**: Generator trains to match teacher's distribution without one-to-one trajectory correspondence
3. **GAN Loss with Classifier**: Optional discriminator using `cls_on_clean_image` flag
4. **Denoising Training**: Multi-step sampling support with `denoising` flag and `backward_simulation`
5. **LoRA Support**: Generator can use LoRA adapters via `generator_lora` flag

### Supported Configurations

| Model | Resolution | Key Flags |
|-------|------------|-----------|
| ImageNet | 64x64 | `--gan_classifier`, `--diffusion_gan` |
| SDXL | 1024x1024 | `--sdxl`, `--denoising`, `--backward_simulation` |
| SDv1.5 | 512x512 | Default single-step |

### Third-Party Code

- `dnnlib/`, `torch_utils/`: Adapted from [NVlabs/edm](https://github.com/NVlabs/edm) for training infrastructure
- Uses `diffusers` library for UNet, VAE, and scheduler components
- Uses `accelerate` for distributed training and FSDP

## Code Patterns

- Precision: BF16 recommended for ImageNet, FP16 for SDXL/SDv1.5
- DDIM scheduler with 1000 timesteps for guidance computation
- Checkpoints saved to `output_path` and `cache_dir` (temporary storage)
- FSDP requires saving/resuming checkpoint at step 0 to sync parameters across nodes
- For FSDP training, model parameters initialized on different nodes may differ; always save checkpoint 0 and reload