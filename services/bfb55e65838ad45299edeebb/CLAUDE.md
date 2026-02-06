# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Complex-YOLOv4 is a PyTorch implementation of 3D object detection on point clouds, based on the paper [Complex-YOLO: Real-time 3D Object Detection on Point Clouds](https://arxiv.org/pdf/1803.06199.pdf). It processes LiDAR point clouds from the KITTI dataset and outputs 3D bounding boxes in bird's-eye view (BEV).

## Commands

### Installation
```bash
pip install -U -r requirements.txt
```
Note: `mayavi` and `shapely` require separate installation per their official docs.

### Training
Single GPU:
```bash
cd src && python train.py --gpu_idx 0 --batch_size <N> --num_workers <N>
```

Multi-GPU distributed training:
```bash
python train.py --dist-url 'tcp://127.0.0.1:29500' --dist-backend 'nccl' --multiprocessing-distributed --world-size 1 --rank 0
```

Using the shell script:
```bash
cd src && ./train.sh
```

### Evaluation (mAP computation)
```bash
python evaluate.py --gpu_idx 0 --pretrained_path <PATH> --cfgfile <CFG> --img_size <SIZE> --conf-thresh 0.5 --nms-thresh 0.5 --iou-thresh 0.5
```

### Inference with visualization
```bash
python test.py --gpu_idx 0 --pretrained_path ../checkpoints/complex_yolov4/complex_yolov4_mse_loss.pth --cfgfile ./config/cfg/complex_yolov4.cfg --show_image
```

### Visualize dataset
```bash
cd src/data_process
python kitti_dataloader.py --output-width 608
```

### View training logs in TensorBoard
```bash
cd logs/<saved_fn>/tensorboard/
tensorboard --logdir=./
```

## Architecture

### Data Pipeline
1. **KittiDataset** (`data_process/kitti_dataset.py`): PyTorch Dataset that loads LiDAR point clouds (`.bin`), camera images (`.png`), calibration files (`.txt`), and labels (`.txt`) from the KITTI format
2. **kitti_bev_utils.py**: Converts 3D point clouds to 2D bird's-eye view images
3. **transformation.py**: Data augmentations including random rotation (±20°), scaling (0.95-1.05), horizontal flip, cutout, and mosaic (composes 4 BEV images)
4. **kitti_dataloader.py**: Creates DataLoaders with appropriate collate functions for multiscale training

### Model Architecture
- **Darknet backbone** (`models/darknet2pytorch.py`): CSP (Cross-Stage Partial) darknet architecture with Mish activations, parsed from `.cfg` configuration files
- **YOLO detection heads** (`models/yolo_layer.py`): Three detection scales (52x52, 26x26, 13x13 for 608x608 input) predicting rotated 3D bounding boxes
- The model uses complex numbers (sin/cos) to encode orientation angles for rotated box detection

### Key Configuration Files
- `config/cfg/complex_yolov4.cfg`: Darknet model architecture definition
- `config/kitti_config.py`: KITTI dataset parameters (boundary ranges, discretization, class IDs)
- `config/train_config.py`: All training hyperparameters via argparse

### Training Loop
- **train.py**: Handles single/multi-GPU training with DistributedDataParallel
- Loss: Supports MSE or GIoU loss for rotated boxes
- Learning rate: Cosine or multi-step scheduler with burn-in phase
- Checkpoints saved to `checkpoints/<saved_fn>/` as `Model_*.pth` and `Utils_*.pth` (optimizer/lr state)

### Evaluation Pipeline
- **evaluate.py**: Computes mAP using rotated box IoU
- **evaluation_utils.py**: Non-max suppression (NMS), batch statistics, AP calculation
- **post_processing_v2()**: Filters detections by confidence threshold and applies NMS

### Coordinate Systems
- **Lidar coordinates**: X=right, Y=down, Z=forward (KITTI Velodyne)
- **Camera coordinates**: X=right, Y=down, Z=forward
- Transformation functions in `transformation.py` convert between camera and lidar box representations

## Dataset Structure
```
dataset/kitti/
├── ImageSets/
│   ├── train.txt
│   └── val.txt
├── training/
│   ├── image_2/
│   ├── calib/
│   ├── label_2/
│   └── velodyne/
├── testing/
│   ├── image_2/
│   ├── calib/
│   └── velodyne/
└── classes_names.txt
```

## Key Arguments
- `--mosaic`: Enable mosaic augmentation (4 images stitched)
- `--multiscale_training`: Randomly vary input size every 10 batches
- `--use_giou_loss`: Use GIoU loss instead of MSE
- `--num_samples`: Debug with subset of dataset