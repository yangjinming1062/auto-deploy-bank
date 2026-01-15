# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Keras implementation of **CSP (Center and Scale Prediction)** for pedestrian and face detection, accepted at CVPR 2019. The detection pipeline reformulates object detection as predicting the center location and scale of objects, rather than traditional anchor-based approaches.

## Dependencies

```bash
pip install -r requirements.txt
```

Note: This project requires Python 2.7, TensorFlow 1.4.1, Keras 2.0.6, and OpenCV 3.4.1.15 specifically (different OpenCV versions may produce slightly different results).

## Common Commands

```bash
# Train on Caltech dataset (pedestrian detection)
python train_caltech.py

# Train on CityPersons dataset
python train_city.py

# Train on WiderFace dataset (face detection)
python train_wider.py

# Test on Caltech
python test_caltech.py

# Test on CityPersons
python test_city.py

# Test on WiderFace (multi-scale)
python test_wider_ms.py

# Generate cache files (if datasets change)
python generate_cache_caltech.py
python generate_cache_city.py
python generate_cache_wider.py
```

## Architecture

### Network Structure (resnet50.py)

The backbone is ResNet-50 (or MobileNet). The key architecture uses feature pyramid levels P3, P4, P5:

1. **Backbone**: ResNet-50 stages 2-5 extract features
2. **Feature Fusion**: Each stage is upsampled via deconvolution and concatenated
3. **Prediction Heads** (3 outputs from `nn_p3p4p5`):
   - `center_cls`: Sigmoid classification for center detection
   - `height_regr`: Log-scale height prediction (or height+width for 'hw' mode)
   - `offset_regr`: Center offset from feature pixel (optional)

### Ground Truth Generation (data_generators.py)

For each image, the `calc_gt_center` function creates 3 maps:
- **Semantic map**: Gaussian-weighted object presence at center
- **Scale map**: Log height (and optionally width) at center
- **Offset map**: Sub-pixel center offset (optional)

### Loss Functions (losses.py)

- **cls_center**: Focal loss with `(1-p)^2` weighting for hard examples
- **regr_h / regr_hw**: Smooth L1 loss on normalized height/width
- **regr_offset**: Smooth L1 loss on offset with 0.1 weight

### Key Configuration (config.py)

```python
C.scale = 'h'       # 'h', 'w', or 'hw' (height, width, or both)
C.offset = True     # Include offset prediction
C.down = 4          # Feature map downsampling rate
C.num_scale = 1     # 1 for height-only, 2 for height+width
C.network = 'resnet50'  # or 'mobilenet'
```

## Data Directory Structure

```
data/
├── caltech/              # Caltech dataset
│   ├── train_3/images/
│   ├── train_3/annotations_new/
│   └── test/images/
│   └── test/annotations_new/
├── citypersons/          # CityPersons dataset
│   ├── annotations/
│   └── images/
├── WiderFace/            # WiderFace dataset
├── cache/
│   └── caltech/train_gt, train_nogt, test
│   └── citypersons/train, val
│   └── widerface/...
└── models/
    └── resnet50_weights_*.h5
```

Cache files are pickle files containing image paths and annotation data. Training uses hybrid data (images with and without pedestrians in 50/50 ratio).

## Training Pipeline

1. Load pre-trained backbone weights from `data/models/`
2. Initialize teacher model with same weights
3. Train with Adam optimizer (lr=1e-4), iterating `iter_per_epoch` times per epoch
4. After each batch, update teacher weights: `w_tea = alpha * w_tea + (1-alpha) * w_stu` (alpha=0.999)
5. Save model on epoch end at `output/valmodels/{dataset}/{scale}/off2` or `nooff`

## Evaluation

Results are saved to `output/valresults/{dataset}/{scale}/off` or `nooff`. Final metrics are computed using MATLAB scripts in `eval_caltech/` and `eval_city/` directories. The CityPersons evaluation uses Python scripts in `eval_city/eval_script/`.