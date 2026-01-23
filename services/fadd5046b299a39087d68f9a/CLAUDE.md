# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CADLab - Imaging Biomarkers and Computer-Aided Diagnosis Laboratory

This is a collection of independent medical imaging deep learning projects from NIH Clinical Center. Each subdirectory is a standalone research project.

## Project Types

- **PyTorch projects** (modern): LesaNet, MULAN, CXR-Binary-Classifier, Lung_Segmentation_XLSor, Emphysema_3D_CNN
- **Caffe/Caffe2 projects** (legacy): CNNSliceClassifier, LymphNodeRFCNNPipeline
- **TensorFlow projects** (legacy): Emphysema_3D_CNN, panreas_hnn
- **Python utilities**: SortDicomFiles, body_part_regressor, MAPLEZ_LLM_report_labeler

## Common Operations

### Install Dependencies
```bash
# Per-project dependencies in requirements.txt
pip install -r requirements.txt

# For projects with CUDA extensions (e.g., Lung_Segmentation_XLSor)
cd libs && sh build.sh && python build.py
cd ../cc_attention && sh build.sh && python build.py
```

### Training
```bash
# LesaNet (PyTorch)
python main.py --mode train

# CXR-Binary-Classifier
python train_densenet.py -a densenet121 -p True

# Lung_Segmentation_XLSor
python train.py
```

### Testing/Evaluation
```bash
# LesaNet
python main.py --mode eval

# Lung_Segmentation_XLSor
python test.py

# CXR-Binary-Classifier
python test_densenet.py
```

### Inference/Demo
```bash
# LesaNet demo mode
python main.py --mode demo

# MULAN demo
python run.py --mode demo
```

## Common Medical Imaging Formats

Projects work with:
- **DICOM** (.dcm) - standard medical imaging format
- **NIfTI** (.nii, .nii.gz) - neuroimaging and volumetric data
- **PNG/JPEG** - 2D images (CXR, screenshots)
- **HDF5** (.h5, .h5py) - large dataset storage

Key libraries: `nibabel`, `opencv-python`, `Pillow`, `h5py`, `pydicom`

## Configuration Patterns

Many projects use YAML configuration:
- `config.yml` - experiment-specific settings
- `default.yml` - default hyperparameters
- `config.py` - configuration loader (easydict pattern)

Configuration modes often controlled via `--mode` argument:
- `train` - training mode
- `eval` or `infer` - evaluation mode
- `demo` - inference on single input
- `batch` - batch inference

## Common Model Architectures

- **VGG16bn** - LesaNet
- **ResNet variants** - various projects
- **DenseNet** - CXR-Binary-Classifier
- **Custom CNNs** - LymphNodeRFCNNPipeline (Caffe)
- **Mask R-CNN derivatives** - MULAN, lesion_detector_3DCE
- **HED (Holistically-Nested Edge Detection)** - panreas_hnn

## Key Dependencies

Core stack (most projects):
- `torch` / `torchvision` - PyTorch
- `numpy` - numerical computing
- `scipy` - scientific computing
- `opencv-python` - image processing
- `nibabel` - NIfTI format support
- `sklearn` / `scikit-learn` - ML utilities
- `matplotlib` - visualization
- `pyyaml` - config files
- `easydict` - config access pattern

Specialized:
- `pycocotools` - MULAN
- `cffi`, `cython` - CUDA compilation
- `tqdm` - progress bars
- `GPUtil` - GPU monitoring

## Project Structure Patterns

```
project_name/
├── main.py / run.py           # Entry point
├── config.yml / default.yml   # Configuration
├── requirements.txt           # Dependencies
├── dataset_*.py              # Data loaders
├── network_*.py / model.py   # Model definitions
├── my_process.py             # Training loop
├── utils.py                  # Utilities
├── train.py / test.py        # Training/inference scripts
├── checkpoints/              # Saved models
└── results/                  # Output directory
```

## Running on GPU

Most projects auto-detect GPU or require setting:
```bash
export CUDA_VISIBLE_DEVICES=0
# or
python script.py --gpu_id 0
```

CUDA versions vary by project (8.0, 9.0, 10.0). Older projects may require older PyTorch/CUDA combinations.

## Checkpoint Format

- **PyTorch**: `.pth` or `.pkl` files via `torch.save()`
- **Caffe**: `.caffemodel` binary
- **Legacy**: pickle files with custom structures