# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeepPATH is a deep learning framework for classifying histopathology images (lung cancer) using the Inception v3 architecture. It processes whole slide images (SVS format) to classify cancer types (LUAD/LUSC/Normal) and predict mutations.

**Paper Reference:** Coudray et al., "Classification and mutation prediction from non-small cell lung cancer histopathology images using deep learning", Nature Medicine 2018.

## Dependencies

- Python 3.6.5 - 3.7.6
- TensorFlow-GPU 1.9.0
- openslide-python 1.1.1
- numpy, scipy, matplotlib, scikit-learn
- Bazel (for building training binaries)

Create environment using: `conda env create -f conda3_520_env_deepPath.yml`

## Key Directory Structure

- `00_preprocessing/` - Image tiling, sorting, and TFRecord conversion
- `01_training/` - Inception v3 training code (modified TensorFlow models)
- `02_testing/` - Evaluation and inference scripts
- `03_postprocessing/` - ROC curves, heatmaps, sensitivity/specificity analysis
- `example_TCGA_lung/` - Complete workflow example with commands

## Common Commands

### Preprocessing (00_preprocessing)

Tile SVS images:
```bash
python 00_preprocessing/0b_tileLoop_deepzoom6.py -s 299 -e 0 -j 32 -B 25 -o <output_dir> "path/to/images/*svs"
```

Sort tiles into train/valid/test sets:
```bash
python 00_preprocessing/0d_SortTiles.py --SourceFolder=<tiles> --JsonFile=<metadata.json> --Magnification=20 --SortingOption=3 --PercentTest=15 --PercentValid=15
```

Convert to TFRecord format:
```bash
# Training set (sharded)
python 00_preprocessing/TFRecord_2or3_Classes/build_image_data.py --directory=<sorted_dir> --output_directory=<output> --train_shards=1024 --validation_shards=128

# Test/valid set (one file per slide)
python 00_preprocessing/TFRecord_2or3_Classes/build_TF_test.py --directory=<sorted_dir> --output_directory=<output> --one_FT_per_Tile=False
```

### Training (01_training)

Build model with Bazel:
```bash
cd 01_training/xClasses
bazel build inception/imagenet_train
```

Train from scratch:
```bash
bazel-bin/inception/imagenet_train --num_gpus=1 --batch_size=30 --train_dir=<output_dir> --data_dir=<TFRecord_dir> --ClassNumber=3 --mode='0_softmax'
```

Transfer learning (pretrained Inception v3):
```bash
curl -O http://download.tensorflow.org/models/image/imagenet/inception-v3-2016-03-01.tar.gz
bazel-bin/inception/imagenet_train --num_gpus=1 --batch_size=30 --train_dir=<output_dir> --data_dir=<TFRecord_dir> --pretrained_model_checkpoint_path=path/to/model.ckpt-157585 --fine_tune=True --initial_learning_rate=0.001 --ClassNumber=3
```

### Testing/Evaluation (02_testing)

Run validation on checkpoint:
```bash
python 02_testing/xClasses/nc_imagenet_eval.py --checkpoint_dir=<checkpoint_dir> --eval_dir=<output_dir> --data_dir=<TFRecord_valid> --batch_size=30 --run_once --TVmode='test' --ClassNumber=3
```

### Postprocessing (03_postprocessing)

Generate ROC curves with bootstrap:
```bash
python 03_postprocessing/0h_ROC_MultiOutput_BootStrap_2.py --file_stats=<out_filename_Stats.txt> --output_dir=<output> --labels_names=<labels.txt>
```

Generate heatmaps:
```bash
python 03_postprocessing/0g_HeatMap_MultiChannels.py --output_dir=<output> --tiles_stats=<out_filename_Stats.txt> --Classes='3,1,2'
```

## Mode Options

- `--mode='0_softmax'`: Single-label classification (one class per tile)
- `--mode='1_sigmoid'`: Multi-output classification (multiple labels per tile, e.g., mutations)

## Data Flow

1. Download SVS slides from GDC portal
2. Tile images using `0b_tileLoop_deepzoom*.py`
3. Sort tiles into classes using `0d_SortTiles.py`
4. Convert to TFRecord format
5. Train with Inception v3 (bazel build + imagenet_train)
6. Evaluate with `nc_imagenet_eval.py`
7. Generate ROC/heatmaps with postprocessing scripts

## Important Notes

- Always use full paths, not relative paths
- Submit jobs via cluster scheduler (SGE/slurm) - see README examples
- Check output and error logs for failures
- Version 2 TFRecord format reads images as BGR (not RGB)
- For multi-threading issues, use `--num_threads=1`
- Patient tiles must stay together (same set: train/valid/test)