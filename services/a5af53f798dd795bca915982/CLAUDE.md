# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Omi is an open-source AI wearable ecosystem consisting of multiple components:
- **Mobile App** (Flutter) - iOS, Android, macOS
- **Backend** (Python/FastAPI) - AI processing, transcription, storage
- **Device Firmware** - nRF chips (Zephyr RTOS) and ESP32-S3 smart glasses
- **SDKs** - React Native, Swift, Python for device integration
- **AI Personas Web** (Next.js) - Custom AI assistant interface
- **Plugins** - Extensible integrations for apps

## Common Development Commands

### Mobile App (Flutter)
```bash
cd app

# Setup for specific platform
bash setup.sh ios      # iOS development
bash setup.sh android  # Android development
bash setup.sh macos    # macOS development

# Run app
flutter run --flavor dev

# Run tests
flutter test

# Run single test
flutter test test/file_name_test.dart

# Build release
flutter build ios --flavor prod
flutter build apk --flavor prod
```

**Prerequisites:**
- Flutter SDK v3.35.3
- iOS: Xcode v16.4+, CocoaPods v1.16.2
- Android: Android Studio, JDK v21, NDK v28.2.13676358
- macOS: Xcode v26.0, CocoaPods v1.16.2

### Backend (Python/FastAPI)
```bash
cd backend

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run with ngrok for local development
ngrok http --domain=your-domain.ngrok-free.app 8000

# Start backend
uvicorn main:app --reload --env-file .env

# Run tests (if test file exists)
pytest tests/test_filename.py
python -m pytest
```

**Key Dependencies:** FastAPI, Firebase Admin, Redis, Pinecone, Deepgram, OpenAI, LangChain

**Required APIs:** OpenAI, Deepgram, Redis (Upstash), Pinecone vector DB, Firebase

### Omi Device Firmware (nRF/Zephyr RTOS)
```bash
cd omi/firmware

# Build firmware (requires nRF Connect extension in VS Code)
# Use CMakePresets.json to select device configuration:
# - devkit (for DevKit1, DevKit2)
# - omi (for production devices)
# Overlay files in boards/ define hardware-specific configs

# Flash firmware (via nRF Connect or nrfjprog)
```

**Key Components:**
- Audio capture and encoding (Opus codec)
- Bluetooth Low Energy streaming
- SD card storage when disconnected
- LED status indicators
- See `readme.md` and `BUILD_AND_OTA_FLASH.md` for detailed instructions

### OmiGlass (ESP32-S3 Smart Glasses)
```bash
cd omiGlass

# Install dependencies
npm install

# Configure API keys
cp .env.template .env
# Add Groq/OpenAI API keys

# Start web interface (Expo)
npm start

# Install firmware
# 1. Open firmware/firmware.ino in Arduino IDE
# 2. Install ESP32 board package
# 3. Select XIAO_ESP32S3 board
# 4. Set PSRAM to "OPI PSRAM"
# 5. Upload firmware
```

### Python SDK
```bash
cd sdks/python

# Install in editable mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Run example
python examples/main.py

# Development workflow
python -m pytest tests/
```

### React Native SDK
```bash
cd sdks/react-native

# Install dependencies
npm install
# or
yarn install

# Build SDK
npm run build

# Run tests
npm test
```

## High-Level Architecture

### Mobile App Architecture (Flutter)
The Flutter app is the central hub that connects to Omi devices:

**Key Directories:**
- `lib/` - Main application code
  - Feature-based organization
  - Bluetooth connectivity via `flutter_blue_plus`
  - Audio streaming from Omi devices
  - Real-time transcription display
  - Plugin/app management system

**Audio Flow:**
1. App connects to Omi device via BLE
2. Receives Opus-encoded audio packets
3. Streams audio to backend for transcription
4. Displays real-time transcripts and summaries

**State Management:** Provider pattern with `provider` package
**Key Features:**
- Multi-platform (iOS, Android, macOS)
- Firebase authentication
- Plugin system for custom integrations
- OTA firmware updates via `nordic_dfu` and `mcumgr_flutter`

### Backend Architecture (Python/FastAPI)

**API Router Structure** (`backend/routers/`):
- `transcribe.py` - Speech-to-text endpoints (Deepgram, Speechmatic, Soniox, OpenAI)
- `conversations.py` - Conversation management
- `memories.py` - Vector storage (Pinecone/Qdrant) for embeddings
- `chat.py` - AI chat processing with LangChain
- `plugins.py` - Plugin marketplace and apps
- `integrations.py` - Third-party integrations (Slack, Notion, etc.)
- `auth.py` - Firebase authentication
- `firware.py` - OTA firmware updates
- `mcp.py` - Model Context Protocol support

**Audio Processing Pipeline:**
1. Receives audio from mobile app
2. Optional VAD (Voice Activity Detection) with Silero VAD
3. STT via multiple providers (Deepgram, OpenAI Whisper, Soniox)
4. Embeddings generation (OpenAI)
5. Vector storage (Pinecone) for semantic search
6. LLM processing for summaries, action items (OpenAI, Groq)

**Data Storage:**
- Firebase Firestore - Primary database
- Redis - Caching and sessions
- Pinecone/Qdrant - Vector embeddings
- Google Cloud Storage - File storage

### Device Firmware Architecture (nRF/Zephyr)

**Bluetooth Protocol:**
- Custom BLE service for audio streaming
- Characteristic UUID: `19B10001-E8F2-537E-4F6C-D104768A1214`
- Opus-encoded audio packets
- Automatic reconnection handling

**Storage System:**
- SD card fallback when no BLE connection
- Automatic file streaming when reconnected
- Opus format for efficient storage

**Power Management:**
- Optimized for 24h+ battery life
- Low-power Bluetooth
- Smart duty cycling

### SDKs Architecture

**Python SDK:**
- Bluetooth connection to Omi devices
- Opus audio decoding
- Real-time transcription integration
- See `sdks/python/omi/` for core library

**React Native SDK:**
- Native BLE bridge for audio streaming
- Event-based architecture
- TypeScript definitions

**Swift SDK:**
- Native iOS Bluetooth framework
- AudioKit integration
- On-device STT with SwiftWhisper

## Key Configuration Files

- `app/pubspec.yaml` - Flutter dependencies and configuration
- `app/setup.sh` - Platform-specific setup automation
- `backend/requirements.txt` - Python dependencies
- `backend/.env.template` - Environment variables template
- `codemagic.yaml` - CI/CD for mobile app releases
- `omi/firmware/CMakePresets.json` - Device-specific build configs
- `omi/firmware/boards/` - Hardware overlay files

## Testing Strategy

**Flutter App:**
- Unit tests: `flutter test`
- Integration tests: `integration_test/`
- Widget tests in `test/` directory

**Backend:**
- Tests in `backend/tests/`
- Use `pytest` for Python tests
- Mock external services in tests

**SDKs:**
- Python SDK: `pytest` in `sdks/python/`
- React Native SDK: Jest tests in `sdks/react-native/jest/`

## Development Environment Setup

**Mobile App:**
1. Install Flutter SDK v3.35.3
2. Run `bash setup.sh <platform>` in `app/`
3. Configure Firebase with `flutterfire config`
4. Set up platform-specific tooling (Xcode/Android Studio)

**Backend:**
1. Python 3.10+ with `venv`
2. Install `requirements.txt`
3. Configure `.env` with API keys
4. Set up ngrok for webhook testing
5. Enable required Google Cloud APIs

**Device Firmware:**
1. VS Code with nRF Connect extension
2. Install nRF SDK
3. CMake build system
4. J-Link debugger (for debugging)

## Plugin Development

See `plugins/` directory for examples:
- `plugins/example/` - Basic plugin template
- `plugins/instructions/` - Plugin instructions
- `plugins/composio/` - Composio integration
- `plugins/hume-ai/` - Hume AI emotion detection

Plugins extend the mobile app's capabilities through webhook integrations.

## Documentation

- Main docs: https://docs.omi.me/
- Backend setup: https://docs.omi.me/doc/developer/backend/Backend_Setup
- App setup: https://docs.omi.me/doc/developer/AppSetup
- Firmware: https://docs.omi.me/doc/developer/firmware/Compile_firmware
- Plugin development: https://docs.omi.me/doc/developer/apps/Introduction
- Community Discord: http://discord.omi.me

## Important Notes

- **Firebase Setup:** Required composite indexes for `dev_api_keys` and `mcp_api_keys` collections in Firestore
- **API Keys:** Multiple STT providers supported (Deepgram, OpenAI, Speechmatic, Soniox)
- **Vector DB:** Pinecone index must be created with correct dimensions (1536 for OpenAI embeddings)
- **CI/CD:** Mobile app releases managed via Codemagic (see `codemagic.yaml`)
- **Hardware Variants:** Different overlay files for V1/V2 devices
- **Firmware Versions:** Separate builds for DevKit vs production devices