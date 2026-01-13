# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🏗️ Project Overview

**Paper2Poster** is a multimodal poster automation system that generates editable academic posters from scientific papers. It uses a multi-agent system with the CAMEL framework to parse papers, plan layouts, and render PowerPoint posters.

## 📦 Project Structure

- **PosterAgent/** - Core poster generation pipeline
  - `new_pipeline.py` - Main entry point (PosterAgent.new_pipeline)
  - `parse_raw.py` - Paper parsing using Docling
  - `gen_outline_layout.py` - Layout planning
  - `tree_split_layout.py` - Binary tree layout optimization
  - `gen_pptx_code.py` - PowerPoint code generation
  - `gen_poster_content.py` - Content generation

- **Paper2Poster-eval/** - Evaluation framework
  - `eval_poster_pipeline.py` - Poster evaluation
  - `create_paper_questions.py` - PaperQuiz creation

- **utils/** - Utilities and configuration
  - `wei_utils.py` - Model configurations, agent setups, code execution utilities
  - `config_utils.py` - YAML config loading
  - `logo_utils.py` - Logo search and management
  - `style_utils.py` - Poster styling
  - `theme_utils.py` - Theme management

- **config/poster.yaml** - Global poster styling configuration

## 🚀 Common Commands

### Installation
```bash
pip install -r requirements.txt

# Install system dependencies
sudo apt install libreoffice
conda install -c conda-forge poppler
```

### Environment Setup
Create `.env` file with API keys:
```bash
OPENAI_API_KEY=<your_openai_api_key>
# Optional: Google Search API for logo search
GOOGLE_SEARCH_API_KEY=<your_google_search_api_key>
GOOGLE_SEARCH_ENGINE_ID=<your_search_engine_id>
```

### Generate a Poster
```bash
# High Performance (GPT-4o)
python -m PosterAgent.new_pipeline \
    --poster_path="${dataset_dir}/${paper_name}/paper.pdf" \
    --model_name_t="4o" \
    --model_name_v="4o" \
    --poster_width_inches=48 \
    --poster_height_inches=36

# Economic (Qwen-2.5-7B + GPT-4o)
python -m PosterAgent.new_pipeline \
    --poster_path="${dataset_dir}/${paper_name}/paper.pdf" \
    --model_name_t="vllm_qwen" \
    --model_name_v="4o" \
    --poster_width_inches=48 \
    --poster_height_inches=36

# Local (Qwen-2.5-7B-Instruct)
python -m PosterAgent.new_pipeline \
    --poster_path="${dataset_dir}/${paper_name}/paper.pdf" \
    --model_name_t="vllm_qwen" \
    --model_name_v="vllm_qwen_vl" \
    --poster_width_inches=48 \
    --poster_height_inches=36
```

**Key Arguments:**
- `--max_workers` - Parallel section generation (default: 10)
- `--conference_venue` - Auto-search for conference logo (e.g., "NeurIPS")
- `--institution_logo_path` - Custom institution logo
- `--conference_logo_path` - Custom conference logo
- `--use_google_search` - Use Google Custom Search API for logos
- `--no_blank_detection` - Disable overflow detection
- `--ablation_no_tree_layout` - Disable binary tree layout
- `--ablation_no_commenter` - Disable visual feedback loop
- `--ablation_no_example` - Disable example prompting

### Docker Deployment
```bash
docker build -t paper2poster .
docker run --rm \
  -e OPENAI_API_KEY=<your_key> \
  -v "$(pwd)/Paper2Poster-data:/Paper2Poster-data" \
  -v "$(pwd)/generated_posters:/app/generated_posters" \
  paper2poster \
  python -m PosterAgent.new_pipeline \
    --poster_path="/Paper2Poster-data/${paper_name}/paper.pdf" \
    --model_name_t="4o" \
    --model_name_v="4o"
```

### Download Evaluation Dataset
```bash
python -m PosterAgent.create_dataset
```

### Evaluate Posters
```bash
# PaperQuiz evaluation
python -m Paper2Poster-eval.eval_poster_pipeline \
    --paper_name="${paper_name}" \
    --poster_method="${model_t}_${model_v}_generated_posters" \
    --metric=qa

# VLM-as-Judge evaluation
python -m Paper2Poster-eval.eval_poster_pipeline \
    --paper_name="${paper_name}" \
    --poster_method="${model_t}_${model_v}_generated_posters" \
    --metric=judge

# Statistical metrics
python -m Paper2Poster-eval.eval_poster_pipeline \
    --paper_name="${paper_name}" \
    --poster_method="${model_t}_${model_v}_generated_posters" \
    --metric=stats
```

### Create Custom PaperQuiz
```bash
python -m Paper2Poster-eval.create_paper_questions \
    --paper_folder="Paper2Poster-data/${paper_name}"
```

## 🔧 Architecture

### Multi-Agent Pipeline
1. **Parser** - Uses Docling to extract content and structure from paper.pdf
2. **Planner** - Aligns text-visual pairs into binary-tree layout preserving reading order
3. **Painter-Commenter Loop** - Renders panels with VLM feedback for overflow detection

### Model Configuration
All models configured in `utils/wei_utils.py:26-196` with `get_agent_config()`:
- **OpenAI**: 4o, 4o-mini, o1, o3, GPT-4.1, GPT-5
- **OpenRouter**: Qwen-2.5 models (7B, 72B, VL variants)
- **VLLM**: Qwen-2.5-7B-Instruct, Qwen2-VL-7B, Phi-4, LLaVA
- **DeepInfra**: Qwen-2.5-72B, Gemini-2-Flash

For vLLM models, ensure server is running on specified ports:
- `vllm_qwen` - http://localhost:8000/v1
- `vllm_qwen_vl` - http://localhost:7000/v1
- `llava`, `molmo-o`, `qwen-2-vl-7b`, `vllm_phi4` - http://localhost:8000/v1

### Style Customization
Global defaults in `config/poster.yaml`:
- Font sizes (main: 60pt, titles: 80pt, poster title: 85pt)
- Colors (RGB tuples)
- Vertical alignment
- Section title symbols

Per-poster override: Place `poster.yaml` next to `paper.pdf`

### Logo System
Auto-detects and adds logos to posters:
1. Local search in `logo_store/institutes/` and `logo_store/conferences/`
2. Web search (DuckDuckGo by default, Google with API keys)

## 🧪 Ablation Studies
Three ablation flags in `new_pipeline.py:41-43`:
- `--ablation_no_tree_layout` - Disables binary tree layout optimization
- `--ablation_no_commenter` - Disables painter-commenter feedback loop
- `--ablation_no_example` - Disables example-based prompting

## 📊 Data Directory Structure
```
Paper2Poster-data/
└── {paper_name}/
    ├── paper.pdf
    ├── meta.json (optional - contains poster dimensions)
    └── poster.yaml (optional - per-poster styling)
```

Generated posters saved in `{model_t}_{model_v}_generated_posters/{paper_name}/poster.pptx`

## 🎨 Dependencies
Key system dependencies (not Python):
- **LibreOffice** - PowerPoint file generation
- **Poppler** - PDF processing
- **Docker** (optional) - Containerized deployment

Python packages managed via `requirements.txt` (includes CAMEL, Docling, python-pptx, vLLM)

## 📝 Configuration Files

- `.env` - API keys and environment variables
- `config/poster.yaml` - Global poster styling
- `poster.yaml` (optional) - Per-poster styling override
- `logo_store/` - Local logo repository

## 🐛 Common Issues

- **Permission denied with Docker**: Use `sudo docker build` and `sudo docker run`
- **No sudo access**: Download LibreOffice soffice manually and add to PATH
- **API errors**: Check `.env` file has required API keys
- **Overflow issues**: Try `--no_blank_detection` flag
- **Logo not found**: Use `--use_google_search` with Google API keys or specify custom paths