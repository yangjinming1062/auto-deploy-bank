# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

InstanceDiffusion is a diffusion model that adds precise instance-level control to text-to-image generation. It supports multiple input types for specifying instance locations: single points, scribbles, bounding boxes, and instance segmentation masks. The model uses UniFusion blocks for instance conditioning and ScaleU blocks for improved instance-aware generation.

## High-Level Architecture

The codebase is organized as follows:

- **ldm/models/**: Core model definitions
  - `autoencoder.py`: VAE autoencoder for encoding/decoding images
  - `diffusion/`: Diffusion model implementations (LDM - Latent Diffusion Model)

- **ldm/modules/**: Neural network components
  - `diffusionmodules/openaimodel.py`: UNet architecture based on Stable Diffusion 1.5
  - `diffusionmodules/text_grounding_net.py`: UniFusion blocks for instance conditioning (core contribution)
  - `attention.py`: Attention mechanisms including gated self-attention
  - `encoders/`: Text encoders (CLIP-based)
  - `losses/`: Training loss functions
  - `ema.py`: Exponential Moving Average utilities

- **dataset/**: Data loading and preprocessing
  - `jsondataset.py`: Dataset for loading JSON-formatted training data
  - `decode_item.py`: Decodes and processes instance conditions (masks, points, scribbles, boxes)

- **configs/**: Configuration files
  - `train_sd15.yaml`: Training configuration for Stable Diffusion 1.5
  - `test_*.yaml`: Test configurations for different input types (box, mask, point, scribble)

- **utils/**: Utility functions for training, inference, and evaluation

## Common Commands

### Installation
```bash
# Create conda environment
conda create --name instdiff python=3.8 -y
conda activate instdiff

# Install dependencies
pip install -r requirements.txt
```

### Training
Training uses submitit for distributed training on SLURM clusters:

```bash
# Training with multi-GPU/multi-node setup
python run_with_submitit.py \
    --workers 8 \
    --ngpus 8 \
    --nodes 8 \
    --batch_size 8 \
    --base_learning_rate 0.00005 \
    --timeout 20000 \
    --warmup_steps 5000 \
    --partition learn \
    --name=instancediffusion \
    --wandb_name instancediffusion \
    --yaml_file="configs/train_sd15.yaml" \
    --official_ckpt_name='pretrained/v1-5-pruned-emaonly.ckpt' \
    --train_file="train.txt" \
    --random_blip 0.5 \
    --count_dup true \
    --add_inst_cap_2_global false \
    --enable_ema true \
    --re_init_opt true
```

For more training options: `python run_with_submitit.py -h`

### Inference
Generate images using pre-trained checkpoints:

```bash
python inference.py \
  --num_images 8 \
  --output OUTPUT/ \
  --input_json demos/demo_cat_dog_robin.json \
  --ckpt pretrained/instancediffusion_sd15.pth \
  --test_config configs/test_box.yaml \
  --guidance_scale 7.5 \
  --alpha 0.8 \
  --seed 0 \
  --mis 0.36 \
  --cascade_strength 0.4
```

**Key parameters:**
- `--mis` (Multi-instance Sampler): Proportion of timesteps using multi-instance sampler (≤ 0.4 recommended). Higher values reduce information leakage but slow generation.
- `--alpha`: Proportion of timesteps using instance-level conditions. Higher values improve location adherence but may reduce image quality.
- `--cascade_strength`: Set > 0 to use SDXL refiner (not used in paper evaluations).

### Evaluation on MSCOCO (Zero-shot)

Location conditions (box, point, scribble, mask):
```bash
CUDA_VISIBLE_DEVICES=0 python eval_local.py \
    --job_index 0 \
    --num_jobs 1 \
    --use_captions \
    --save_dir "eval-cocoval17" \
    --ckpt_path pretrained/instancediffusion_sd15.pth \
    --test_config configs/test_mask.yaml \
    --test_dataset cocoval17 \
    --mis 0.36 \
    --alpha 1.0
```

Attribute binding evaluation:
```bash
# For colors
CUDA_VISIBLE_DEVICES=0 python eval_local.py \
    --job_index 0 \
    --num_jobs 1 \
    --use_captions \
    --save_dir "eval-cocoval17-colors" \
    --ckpt_path pretrained/instancediffusion_sd15.pth \
    --test_config configs/test_mask.yaml \
    --test_dataset cocoval17 \
    --mis 0.36 \
    --alpha 1.0 \
    --add_random_colors

python eval/eval_attribute_binding.py --folder eval-cocoval17-colors --test_random_colors
```

Point-based image generation evaluation:
```bash
CUDA_VISIBLE_DEVICES=0 python eval_local.py \
    --job_index 0 \
    --num_jobs 1 \
    --use_captions \
    --save_dir "eval-cocoval17-point" \
    --ckpt_path pretrained/instancediffusion_sd15.pth \
    --test_config configs/test_point.yaml \
    --test_dataset cocoval17 \
    --mis 0.36 \
    --alpha 1.0

# Install YOLOv8 for evaluation
pip install ultralytics
mv datasets/coco/images/val2017 datasets/coco/images/val2017-official
ln -s generation_samples/eval-cocoval17-point datasets/coco/images/val2017
yolo val segment model=yolov8m-seg.pt data=coco.yaml device=0
python eval/eval_pim.py --pred_json /path/to/predictions.json
```

## Key Implementation Details

### Input Format
- **Bounding boxes**: `[xmin, ymin, width, height]` (normalized 0-1)
- **Masks**: RLE (Run-Length Encoding) format
- **Scribbles**: `[x1, y1, ..., x20, y20]` (can have duplicate points)
- **Points**: `[x, y]`

### Model Components

1. **UniFusion** (ldm/modules/diffusionmodules/text_grounding_net.py:UniFusion):
   - Learnable fusion blocks that integrate instance conditions with the backbone
   - Handles boxes, points, scribbles, and masks
   - Configurable with `train_add_*` and `test_drop_*` flags

2. **ScaleU blocks**:
   - Rescale skip-connection and backbone feature maps
   - Improve UNet's ability to respect instance conditioning
   - Integrated in UNet architecture

3. **Multi-instance Sampler** (ldm/models/diffusion/plms_instance.py):
   - Reduces information leakage across multiple instances
   - Controlled by `mis` parameter
   - Activated during specific timesteps

4. **Gated Self-Attention**:
   - Controlled by `alpha` parameter
   - Allows selective use of instance conditions
   - Enabled via `fuser_type: gatedSA` in config

### Attention Efficiency
The implementation supports Flash/Math/MemEfficient attention via PyTorch's `torch.backends.cuda.sdp_kernel`. Disable by setting `efficient_attention: False` in the configuration YAML file.

## Pretrained Models

Download from:
- **InstanceDiffusion**: [Hugging Face](https://huggingface.co/xudongw/InstanceDiffusion) or [Google Drive](https://drive.google.com/drive/folders/1Jm3bsBmq5sHBnaN5DemRUqNR0d4cVzqG?usp=sharing)
- **Stable Diffusion 1.5**: [Hugging Face](https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt)

Place models in `pretrained/` directory.

## Data Preparation

See `dataset-generation/README.md` for detailed instructions on preparing training datasets. Training data should be organized with instance annotations including text captions and location conditions (boxes/points/scribbles/masks).

## Configuration

All configurations use Hydra for structured configs. Key config files:
- `configs/train_sd15.yaml`: Main training configuration
- `configs/test_*.yaml`: Test configurations for different input modalities

## Development Notes

- The codebase uses **PyTorch ≥ 2.0** and **torchvision** that matches the PyTorch installation
- **OpenCV ≥ 4.6** required for demos and visualization
- Supports distributed training with submitit on SLURM clusters
- Mixed precision training with GradScaler (automatic loss scaling)
- EMA (Exponential Moving Average) for model weights during training
- Gradient checkpointing enabled via `use_checkpoint: True` in UNet config

## Important References

- Paper: [InstanceDiffusion: Instance-level Control for Image Generation](https://arxiv.org/abs/2402.03290)
- Project page: [http://people.eecs.berkeley.edu/~xdwang/projects/InstDiff/](http://people.eecs.berkeley.edu/~xdwang/projects/InstDiff/)
- Diffusers port: [https://huggingface.co/kyeongry/instancediffusion_sd15](https://huggingface.co/kyeongry/instancediffusion_sd15)

## Third-party Implementations

- [ComfyUI-InstanceDiffusion](https://github.com/logtd/ComfyUI-InstanceDiffusion): Port to ComfyUI

## License

Apache License 2.0 for the majority of InstanceDiffusion. CLIP, BLIP, Stable Diffusion, and GLIGEN have separate licenses.