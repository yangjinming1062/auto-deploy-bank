# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Open-AutoGLM is an AI-powered phone automation framework that controls Android devices via ADB. The agent uses vision-language models to understand screen content and executes automated actions to complete user tasks.

**Architecture**: Agent code (Python) runs on user's computer → communicates with AI model service → generates actions → ADB executes on Android device

**Key Components**:
- **main.py**: CLI entry point and system checks
- **phone_agent/agent.py**: Core `PhoneAgent` class for orchestration
- **phone_agent/adb/**: ADB interface for device control (screenshot, input, taps, swipes)
- **phone_agent/actions/**: Action execution and parsing
- **phone_agent/model/**: OpenAI-compatible model client
- **phone_agent/config/**: System prompts, supported apps, internationalization

## Common Commands

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Development Workflow
```bash
# Run pre-commit checks on all files
pre-commit run --all-files

# Run tests
pytest tests/

# List supported apps
python main.py --list-apps

# List connected devices
python main.py --list-devices
```

### Usage
```bash
# Interactive mode
python main.py --base-url http://localhost:8000/v1 --model "autoglm-phone-9b"

# Execute single task
python main.py --base-url http://localhost:8000/v1 --model "autoglm-phone-9b" "打开微信发消息"

# With API key authentication
python main.py --base-url http://localhost:8000/v1 --model "autoglm-phone-9b" --apikey sk-xxxxx

# Use English system prompts
python main.py --lang en --base-url http://localhost:8000/v1 "Open Chrome browser"

# Specify device ID
python main.py --device-id emulator-5554 --base-url http://localhost:8000/v1 "打开抖音"
```

### ADB Device Management
```bash
# Connect to remote device via WiFi
adb connect 192.168.1.100:5555

# Disconnect device
adb disconnect 192.168.1.100:5555

# Enable TCP/IP on USB device
adb tcpip 5555

# Check connected devices
adb devices
```

## Code Architecture

### Core Flow
1. **Agent Execution Loop** (`phone_agent/agent.py:84-130`):
   - Takes screenshot via ADB
   - Sends screenshot + context to vision-language model
   - Model returns `<think>` reasoning and `<answer>` action
   - Action parsed and executed via ADB
   - Repeat until task complete or max steps reached

2. **Action System** (`phone_agent/actions/handler.py`):
   - `Launch`: Start app by package name
   - `Tap`: Click at coordinates
   - `Type`: Input text (requires ADB Keyboard)
   - `Swipe`: Scroll/drag gestures
   - `Back`: Return to previous screen
   - `Home`: Return to desktop
   - `Wait`: Pause for page loading

3. **ADB Interface** (`phone_agent/adb/`):
   - `screenshot.py`: Capture device screen
   - `input.py`: Text input via ADB Keyboard
   - `device.py`: Physical interactions (tap, swipe, back, home)
   - `connection.py`: Remote ADB over WiFi

4. **Model Configuration** (`phone_agent/model/client.py`):
   - OpenAI-compatible client
   - Supports custom base URLs and API keys
   - Sends structured messages with screenshots

5. **Prompt System** (`phone_agent/config/prompts*.py`):
   - `prompts_zh.py`: Chinese system prompt
   - `prompts_en.py`: English system prompt
   - Defines available actions and response format
   - Uses `<think>` and `<answer>` tags

### Supported Apps
View full list via `python main.py --list-apps` (50+ apps including WeChat, Taobao, Douyin, etc.)

### Configuration
Environment variables (`phone_agent/config/__init__.py`):
- `PHONE_AGENT_BASE_URL`: Model API URL (default: http://localhost:8000/v1)
- `PHONE_AGENT_MODEL`: Model name (default: autoglm-phone-9b)
- `PHONE_AGENT_API_KEY`: API key (default: EMPTY)
- `PHONE_AGENT_MAX_STEPS`: Max steps per task (default: 100)
- `PHONE_AGENT_DEVICE_ID`: ADB device ID
- `PHONE_AGENT_LANG`: Language (cn or en, default: cn)

## Key Files

### Configuration
- `phone_agent/config/apps.py`: Supported apps and package names
- `phone_agent/config/prompts_zh.py`: Chinese system prompt
- `phone_agent/config/prompts_en.py`: English system prompt

### Core Implementation
- `phone_agent/agent.py`: PhoneAgent class and execution loop
- `phone_agent/model/client.py`: Model client for OpenAI-compatible APIs
- `phone_agent/actions/handler.py`: Action parsing and execution
- `phone_agent/adb/screenshot.py`: Screenshot capture
- `phone_agent/adb/input.py`: Text input via ADB Keyboard

### CLI Entry Point
- `main.py`: Command-line interface, system requirements check, argument parsing

### Examples
- `examples/basic_usage.py`: Basic usage patterns
- `examples/demo_thinking.py`: Verbose mode demonstration

## Development Notes

### Pre-commit Hooks
The project uses pre-commit with:
- **ruff**: Linting and import sorting
- **ruff-format**: Code formatting
- **typos**: Spell checking
- **pymarkdown**: Markdown linting

Configuration: `.pre-commit-config.yaml`

### Dependencies
Core (`requirements.txt`):
- Pillow>=12.0.0 (image processing)
- openai>=2.9.0 (OpenAI-compatible client)

Optional for model deployment:
- vllm>=0.12.0 or sglang>=0.5.6.post1 (model serving)
- transformers>=5.0.0rc0 (transformers library)

Development (`setup.py` extras_require["dev"]):
- pytest>=7.0.0 (testing)
- black>=23.0.0 (code formatting)
- mypy>=1.0.0 (type checking)
- ruff>=0.1.0 (linting)

### Python API
```python
from phone_agent import PhoneAgent
from phone_agent.model import ModelConfig
from phone_agent.agent import AgentConfig

# Configure model
model_config = ModelConfig(
    base_url="http://localhost:8000/v1",
    model_name="autoglm-phone-9b",
)

# Configure agent
agent_config = AgentConfig(
    max_steps=100,
    device_id=None,  # Auto-detect
    lang="cn",
    verbose=True,
)

# Create and run agent
agent = PhoneAgent(
    model_config=model_config,
    agent_config=agent_config,
)
result = agent.run("打开淘宝搜索无线耳机")
```

### System Requirements
- Python 3.10+
- ADB (Android Debug Bridge) installed and in PATH
- Android 7.0+ device with USB debugging enabled
- ADB Keyboard APK installed and enabled on device
- Model service (local or remote) - not included in this repo

## Important Notes

### ADB Keyboard Requirement
Text input requires ADB Keyboard:
1. Install APK: https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk
2. Enable in Settings → Language & Input → Virtual Keyboard
3. Verify with `adb shell ime enable com.android.adbkeyboard/.AdbIME`

### Device Permissions
Ensure both enabled in Developer Options:
- USB Debugging
- USB Debugging (Security Settings)

### Model Integration
This repo contains only the agent code. Models are served separately via:
- **Third-party APIs**: BigModel, ModelScope
- **Self-hosted**: vLLM or SGLang (requires NVIDIA GPU, ~20GB VRAM)

Example model service URLs:
- BigModel: `https://open.bigmodel.cn/api/paas/v4`
- ModelScope: `https://api-inference.modelscope.cn/v1`
- Local vLLM: `http://localhost:8000/v1`

### Contribution Guidelines
- All naming in English (no pinyin)
- Follow PEP 8 style
- Run `pre-commit run --all-files` before PR
- Use type hints
- Update relevant prompt files for new features

### Remote Debugging
Supports ADB over WiFi:
```bash
# On device: Enable wireless debugging in Developer Options
adb connect <IP>:<PORT>
python main.py --device-id <IP>:<PORT> --base-url <MODEL_URL> "task"
```