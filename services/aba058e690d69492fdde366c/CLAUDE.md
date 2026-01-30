# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dolphin-v2 is a document image parsing model using Qwen2.5-VL (Vision-Language Model) for parsing diverse document types (digital-born or photographed). It employs a two-stage architecture:
- **Stage 1**: Document type classification + layout analysis with reading order prediction
- **Stage 2**: Parallel element-wise parsing for different element types

## Commands

### Installation
```bash
pip install -r requirements.txt
```

### Download Model
```bash
git clone https://huggingface.co/ByteDance/Dolphin-v2 ./hf_model
# Or: huggingface-cli download ByteDance/Dolphin-v2 --local-dir ./hf_model
```

### Inference
```bash
# Page-level parsing (entire document to JSON/Markdown)
python demo_page.py --model_path ./hf_model --save_dir ./results --input_path ./demo/page_imgs

# Element-level parsing (single element type: text, table, formula, code)
python demo_element.py --model_path ./hf_model --input_path <image> --element_type [table|formula|text|code]

# Layout detection only
python demo_layout.py --model_path ./hf_model --save_dir ./results --input_path ./demo/page_imgs

# With custom batch size for parallel element decoding
python demo_page.py --model_path ./hf_model --max_batch_size 8 ...
```

### Code Quality
```bash
# Install pre-commit hooks
pre-commit install

# Run all formatters/linters
pre-commit run --all-files
```

## Architecture

### Entry Points
- `demo_page.py`: Full document parsing pipeline (layout → elements → JSON/Markdown)
- `demo_element.py`: Single element extraction (text, table, formula, code)
- `demo_layout.py`: Layout analysis only, visualizes bounding boxes

### Core Classes and Functions

**DOLPHIN class** (`demo_*.py`):
- Wrapper around `Qwen2_5_VLForConditionalGeneration` with `AutoProcessor`
- `chat(prompt, image)`: Single/batch inference with vision-language model
- Device: CUDA with bfloat16 (or CPU with float32)

**Key processing functions** (`utils/utils.py`):
- `process_single_image()`: Stage 1 (layout) → Stage 2 (element parsing)
- `process_elements()`: Groups elements by type, calls `process_element_batch()`
- `process_element_batch()`: Parallel inference for same-type elements
- `parse_layout_string()`: Parses LLM output `[bbox][label][tags][PAIR_SEP]...`
- `process_coordinates()`: Maps model coordinates back to original image space
- `check_bbox_overlap()`: Detects photographed documents (high IoU = distorted page)

**Markdown conversion** (`utils/markdown_utils.py`):
- `MarkdownConverter`: Converts structured results to Markdown format
- Handles sections (`sec_0-5` → headings), tables (HTML→Markdown), formulas (→`$$`), code (→code blocks)

### Output Structure
```
<save_dir>/
├── output_json/           # Structured results with bboxes and labels
├── markdown/              # Rendered Markdown files
│   └── figures/           # Extracted figure images
└── layout_visualization/  # Bounding box overlays
```

### Element Labels
- `para`, `sec_0-5`: Text/sections (nested heading levels)
- `tab`: Tables (HTML format in output)
- `equ`: Formulas (LaTeX in `$$...$$`)
- `fig`: Figures (saved to figures/, referenced as markdown image)
- `code`: Code blocks
- `list`: List items
- `distorted_page`: Fallback for photographed documents
- `fnote`, `watermark`, `meta_num`: Metadata elements

### Model Prompts
- Layout: "Parse the reading order of this document."
- Table: "Parse the table in the image."
- Formula: "Read formula in the image."
- Code: "Read code in the image."
- Text: "Read text in the image."