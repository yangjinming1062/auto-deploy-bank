# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Cost-Effective Active Learning (CEAL) implementation for medical image segmentation using a U-Net architecture. It uses Monte Carlo Dropout at test time to model pixel-wise uncertainty for active learning sample selection and pseudo-annotation.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the main CEAL training pipeline:
```bash
python src/CEAL.py
```

## Architecture

The system consists of four main modules in `src/`:

- **CEAL.py**: Main entry point. Initializes training data, loads U-Net model, runs initial training phase, then executes active learning iterations. Configures model checkpoints and logging.

- **constants.py**: Configuration parameters including:
  - Image dimensions (`img_rows`, `img_cols`)
  - Dataset split (`nb_total`, `nb_train`, `nb_labeled`)
  - CEAL hyperparameters (`nb_iterations`, `nb_step_predictions`, `nb_no_detections`, `nb_random`, `nb_most_uncertain`, `pseudo_epoch`, `nb_pseudo_initial`, `pseudo_rate`)
  - Training parameters (`nb_initial_epochs`, `nb_active_epochs`, `batch_size`)
  - Path placeholders (`[global_path_name]`, `[initial_weights_name]`, `[output_weights_name]`) requiring configuration

- **unet.py**: U-Net encoder-decoder architecture with skip connections. Uses Keras with Theano dimension ordering (`th`). Key components:
  - `get_unet(dropout)`: Builds the model with 4 downsampling/upsampling levels
  - `dice_coef_loss`: Custom loss function for segmentation
  - Overrides `Dropout.call` to enable dropout at test time for Monte Carlo sampling

- **utils.py**: CEAL algorithm utilities:
  - `compute_uncertainty()`: Calculates uncertainty using MC Dropout predictions with optional EDT transform
  - `compute_train_sets()`: Core CEAL labeling step that selects samples for manual annotation and pseudo-labeling
  - Sample selection strategies: `no_detections_index()`, `random_index()`, `most_uncertain_index()`, `get_pseudo_index()`
  - `data_generator()`: Keras ImageDataGenerator for augmentation

- **data.py**: Data handling:
  - `create_train_data()`: Preprocesses raw images to `imgs_train.npy` and `imgs_mask_train.npy`
  - `load_train_data()`: Loads gzipped numpy arrays, resizes, and normalizes

## Data Flow

1. Load training data from `skin_database/imgs_train.npy.gz` and `skin_database/imgs_mask_train.npy.gz`
2. Preprocess images to 192x240 (64*3 x 80*3)
3. Train U-Net on initial labeled subset
4. Active loop iterations:
   - Compute predictions on unlabeled data
   - Calculate uncertainty for each sample via MC Dropout
   - Select samples for manual annotation (most uncertain + no detections + random)
   - Generate pseudo-labels for high-confidence predictions
   - Retrain on expanded labeled set

## Important Implementation Details

- Keras 1.2.2 with TensorFlow-GPU 1.1.0 (legacy versions)
- Theano dimension ordering (`K.set_image_dim_ordering('th')`) - channels first (1, img_rows, img_cols)
- Dropout is modified to be active during inference for Monte Carlo sampling
- Binary predictions use 0.5 threshold via `cv2.threshold()`
- Output directories (`models/`, `logs/`, `ranks/`, `plots/`) are created automatically
- Logs written to `logs/log_file.txt` with format: `step epoch loss val_dice_coef`