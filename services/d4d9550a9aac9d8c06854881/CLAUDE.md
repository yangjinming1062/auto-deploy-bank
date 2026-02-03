# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UNet implementation for the Kaggle TGS Salt Identification Challenge. Segments salt deposits from seismic images using a UNet architecture with SENet encoder and object context modules.

## Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Training
```bash
python train.py --vtf --pretrained imagenet --loss-on-center --batch-size 32 --optim adamw \
  --learning-rate 5e-4 --lr-scheduler noam --basenet senet154 --max-epochs 250 \
  --data-fold fold0 --log-dir runs/fold0
```

Key arguments:
- `--data-fold`: Choose fold (fold0-fold9 or fold01-fold10)
- `--vtf`: Enable validation time flip augmentation (doubles validation set)
- `--loss-on-center`: Loss computed only on original 101x101 region (before padding)
- `--resize`: Resize to 128x128 instead of reflective padding
- `--debug`: Write debug images to tensorboard
- `--resume`: Resume from checkpoint

### Stochastic Weight Averaging
```bash
python swa.py --input runs/fold0/models --output fold0_swa.pth
```

### Testing/Inference
```bash
python test.py --tta fold0_swa.pth --output-prefix fold0
```

### Tensorboard
```bash
tensorboard --logdir runs
```

## Architecture

### UNet with Deep Supervision
The model returns three outputs:
- `logit`: Main pixel-level mask (1x101x101)
- `logit_pixel`: Tuple of 5 multi-scale predictions at different decoder levels
- `logit_image`: Image-level classification (whether salt exists in image)

### Loss Function
```python
deep_supervised_criterion(logit, logit_pixel, logit_image, truth_pixel, truth_image)
# Returns: 0.05 * loss_image + 0.1 * loss_pixel + 1.0 * loss
```
- **Image loss**: BCE with logits on image-level classification
- **Pixel loss**: Symmetric Lovasz loss on 5 multi-scale outputs
- **Main loss**: Symmetric Lovasz hinge loss on main output

### Key Modules
- `models/unet.py`: UNet with configurable encoder backbone
- `models/basenet.py`: Encoder backbones (senet154, resnet34, vgg11, etc.)
- `models/oc_net.py`: Object Context (BaseOC) modules
- `models/inplace_abn.py`: ActivatedBatchNorm for memory efficiency
- `losses/lovasz_losses.py`: Lovasz hinge loss variants
- `transforms/unet_transforms.py`: Data augmentations (geometric, brightness, Cutout)

### Data Format
- Train images: `datasets/train/images/{id}.png` (101x101 RGB)
- Train masks: `datasets/train/masks/{id}.png` (101x101 grayscale)
- Test images: `datasets/test/images/{id}.png`
- Fold splits: `datasets/folds/list_train{fold_id}_{n}.csv`, `list_valid{fold_id}_{n}.csv`

### Output
- Checkpoints: `runs/{log_dir}/checkpoints/`
- Model files: `runs/{log_dir}/models/`
- Submission: `{prefix}-submission.csv` (RLE-encoded masks)
- Probabilities: `{prefix}-probabilities.pkl.gz`