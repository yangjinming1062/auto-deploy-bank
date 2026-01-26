# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Car Recognition using deep learning - fine-tuning ResNet-152 on the Stanford Cars Dataset (196 car classes, ~16,000 images). Achieves ~88% test accuracy.

## Commands

```bash
# Install dependencies
pip install -r Requirements.txt

# Data preprocessing - extracts and organizes dataset
python pre_process.py

# Train model with transfer learning
python train.py

# Monitor training with TensorBoard
tensorboard --logdir logs

# Analyze validation accuracy and confusion matrix
python analyze.py

# Generate predictions on test set
python test.py

# Run demo on a single image (default uses sample image)
python demo.py --i [image_path]
```

## Architecture

**Model**: ResNet-152 with ImageNet pre-trained weights (transfer learning)
- Original FC1000 layer replaced with FC196 for 196 car classes
- Input: 224x224 RGB images
- Uses custom `Scale` layer from `custom_layers/scale_layer.py`

**Data Pipeline**:
- `pre_process.py`: Extracts tar.gz files, crops images using bounding boxes from devkit MAT files, resizes to 224x224, splits train/valid 80:20
- Training uses `ImageDataGenerator` for augmentation (rotation, shifts, zoom, flip)

**Key Files**:
- `resnet_152.py`: Model architecture (identity_block, conv_block, resnet152_model)
- `utils.py`: `load_model()` function loads weights from `models/model.96-0.89.hdf5`
- `train.py`: Training with callbacks (TensorBoard, ModelCheckpoint, EarlyStopping, ReduceLROnPlateau)

**Directory Structure**:
- `data/{train,valid,test}` - Processed image directories
- `devkit/` - MAT files with annotations (cars_train_annos, cars_test_annos, cars_meta)
- `models/` - Pre-trained ResNet weights and trained model checkpoints
- `logs/` - TensorBoard training logs
- `custom_layers/` - Custom Keras Scale layer for ResNet