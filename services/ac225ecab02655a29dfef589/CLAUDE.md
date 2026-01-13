# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

## Repository Overview

This is a multi-project repository containing a family of GUI automation agents developed by Tongyi Lab, Alibaba Group. The repository contains several independent agent projects, each with its own documentation and requirements.

### Project Structure

- **Mobile-Agent-v3** - Latest multi-modal, multi-platform GUI agent framework with GUI-Owl foundation model (Recommended)
- **UI-S1** - Semi-online Reinforcement Learning approach for GUI automation with training/evaluation code
- **PC-Agent** - Hierarchical multi-agent collaboration for PC tasks (Windows/Mac)
- **GUI-Critic-R1** - Pre-operative error diagnosis model for GUI automation
- **Mobile-Agent-E** - Self-evolving mobile agent
- **Mobile-Agent-v2** - Previous version (NeurIPS 2024)
- **Mobile-Agent-v1** - Original version (ICLR 2024 Workshop)

## Common Commands by Project

### Mobile-Agent-v3

**Setup:**
```bash
pip install qwen_agent qwen_vl_utils numpy
# Install Android Debug Bridge and set up device
```

**Run on Android:**
```bash
cd Mobile-Agent-v3/mobile_v3
python run_mobileagentv3.py \
    --adb_path "Your ADB path" \
    --api_key "Your vllm api key" \
    --base_url "Your vllm base url" \
    --model "Your model name" \
    --instruction "Your instruction" \
    --add_info "Supplementary knowledge (optional)" \
    --coor_type "qwen-vl"  # If using models with 0-1000 coordinates
    --notetaker True        # Enable memory
```

**Run on HarmonyOS:**
```bash
cd Mobile-Agent-v3/mobile_v3
python run_mobileagentv3.py \
    --hdc_path "Your HDC path" \
    --api_key "Your vllm api key" \
    --base_url "Your vllm base url" \
    --model "Your model name" \
    --instruction "Your instruction"
```

**Evaluate on OSWorld:**
```bash
cd Mobile-Agent-v3/os_world_v3
# Edit run_guiowl.sh or run_ma3.sh with your vllm service info
sh run_guiowl.sh    # GUI-Owl evaluation
sh run_ma3.sh       # Mobile-Agent-v3 evaluation
```

**Evaluate on AndroidWorld:**
```bash
cd Mobile-Agent-v3/android_world_v3
# Install AndroidWorld dependencies first
sh run_guiowl.sh    # GUI-Owl evaluation
sh run_ma3.sh       # Mobile-Agent-v3 evaluation
```

### UI-S1

**Setup:**
```bash
conda create -n ui-s1 python=3.11
conda activate ui-s1
cd UI-S1
pip install -e .
pip install vllm==0.8.2
pip install flash-attn==2.7.4.post1 --no-build-isolation
```

**Train:**
```bash
# Download data to datasets/AndroidControl/
cd UI-S1
bash scripts/train_example.sh
python scripts/model_merger.py merge --local_dir checkpoints/XXX
```

**Inference and Evaluation:**
```bash
# Launch vLLM server
vllm serve /checkpoints-7B --served-model-name UI-S1-7B \
    --tensor_parallel_size 1 --trust-remote-code --limit-mm-per-prompt image=2

# Evaluate on SOP metric
python evaluation/eval_qwenvl.py --model_name UI-S1-7B

# Evaluate other models
python evaluation/eval_qwenvl.py --model_name Qwen2.5-VL-7B
python evaluation/eval_agentcpm.py --model_name AgentCPM-GUI-8B
python evaluation/eval_os-atlas-7b.py --model_name OS-Atlas-7B
```

### PC-Agent

**Setup:**
```bash
conda create --name pcagent python=3.10
source activate pcagent

# Windows
pip install -r requirements.txt

# Mac
pip install -r requirements_mac.txt
pip install openocr-python

# Install OpenOCR
git clone https://github.com/Topdu/OpenOCR.git
pip install openocr-python
```

**Configure:**
Edit `config.json` to add your API keys:
```json
{
  "vl_model_name": "gpt-4o",
  "llm_model_name": "gpt-4o",
  "token": "sk-...",
  "url": "https://api.openai.com/v1"
}
```

**Run:**
```bash
# Windows
python run.py --instruction="Your instruction" --mac 0

# Mac
python run.py --instruction="Your instruction" --mac 1

# Additional options:
--add_info "Specific operational knowledge"
--disable_reflection  # Skip reflection for efficiency
--simple 1           # Skip task decomposition for simple tasks
```

### GUI-Critic-R1

**Setup:**
```bash
pip install -r requirement.txt
```

**Run Evaluation:**
```bash
python test.py \
    --model_dir <model_directory> \
    --test_file <test_file_path> \
    --save_dir <output_directory> \
    --data_dir <dataset_directory>
```

**Test Files:**
- `test_files/gui_i.jsonl` - GUI-I dataset
- `test_files/gui_s.jsonl` - GUI-S dataset
- `test_files/gui_web.jsonl` - GUI-W dataset

### Mobile-Agent-v1

**Setup:**
```bash
pip install -r requirements.txt
```

**Run:**
```bash
python run.py
# or for API mode
python run_api.py
```

### Mobile-Agent-E

**Setup:**
```bash
pip install -r requirements.txt
```

**Run:**
```bash
python run.py
```

## Architecture Overview

### Mobile-Agent-v3 Architecture

Based on `run_mobileagentv3.py:9-16`, uses a multi-agent architecture with:
- **InfoPool** - Manages knowledge and context
- **Manager** - Task planning and coordination
- **Executor** - Action execution
- **Notetaker** - Memory and information recording
- **ActionReflector** - Error handling and reflection
- **GUIOwlWrapper** - Vision-language model interface
- **AndroidController/HarmonyOSController** - Device interaction

The framework supports:
- Dynamic task decomposition and planning
- Progress management across steps
- Exception handling and reflection
- Cross-application task memory
- Active perception for dense interactive elements

### UI-S1 Architecture

Built on the **verl** (Volcano Engine Reinforcement Learning) framework:
- **verl/** - Core RL training framework
- **examples/** - Training examples and configs
- **evaluation/** - Evaluation scripts
- **uis1/** - UI-S1 specific implementation
- Uses **DAPO** (Decoding Advantage Actor-Critic) algorithm with trajectory GRPO
- Supports FSDP for large model training
- Integrates with vLLM for inference

### GUI-Owl Models

Base vision-language models used across projects:
- **GUI-Owl-7B** - 7B parameter model
- **GUI-Owl-32B** - 32B parameter model
- Support both relative (0-1000) and absolute coordinates
- Cross-platform GUI perception and grounding

## Key Dependencies

**Common:**
- `qwen_agent` - Qwen agent framework
- `qwen_vl_utils` - Vision-language utilities
- `numpy` - Numerical computing

**UI-S1:**
- `verl` - RL training framework
- `vllm==0.8.2` - Inference engine
- `flash-attn` - Attention optimization
- `transformers==4.51.1` - Model loading
- `accelerate` - Distributed training

**PC-Agent:**
- `pyautogui` - GUI automation
- `pywin32` - Windows API
- `pywinauto` - Windows UI automation
- `openocr-python` - OCR capabilities

**Mobile (ADB):**
- Android Debug Bridge (adb)
- ADB Keyboard APK for input

## Development Notes

1. **Each project is independent** - They don't share dependencies or build systems
2. **Mobile-Agent-v3 is the flagship** - Most actively developed and feature-complete
3. **vLLM integration** - Most projects use vLLM for model inference
4. **Device setup required** - Mobile/PC agents need physical devices or emulators
5. **API keys needed** - All projects require LLM API keys (OpenAI, vLLM, etc.)

## Testing

- **UI-S1**: Uses `pytest` for unit tests, see `evaluation/` scripts
- **AndroidWorld**: Built-in test suite in `android_world_v3/`
- **OSWorld**: Integrated benchmark evaluation
- **GUI-Critic-R1**: `test.py` script for evaluation

## Common Issues

1. **Coordinate systems**: GUI-Owl uses absolute coordinates; Qwen-VL uses relative (0-1000). Set `--coor_type "qwen-vl"` when using relative coordinates.

2. **ADB permissions**: On Mac/Linux, run `sudo chmod +x /path/to/adb`

3. **Input method**: Install ADB Keyboard APK and set as default on Android devices

4. **Flash attention**: May need pre-built wheel for specific CUDA/PyTorch versions

5. **Environment variables**:
   - Set `MASTER_ADDR`, `MASTER_PORT` for distributed training
   - Set `VLLM_USE_V1=1` for vLLM compatibility
   - Configure WANDB/SwanLab keys in `verl/utils/tracking.py`

## Documentation References

- Main README.md - Overview and paper links
- Individual project README.md files - Detailed usage instructions
- Paper links in each README for technical details
- HuggingFace model cards for GUI-Owl, UI-S1, GUI-Critic-R1 models