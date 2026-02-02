# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MajsoulAI is an AI system that plays Mahjong in the game "Majsoul" (雀魂). It bridges the Majsoul game client with JianYangAI, an open-source Tenhou-format Mahjong AI. The AI uses image recognition to detect game state and simulates mouse clicks to perform actions.

## Setup Commands

**Initialize git submodules** (required before running):
```bash
git submodule update --init --recursive
```

**Install dependencies**:
```bash
pip install -r requirements.txt
```

**Install PyTorch** (version varies by system, see [pytorch.org](https://pytorch.org/get-started/locally/)):
```bash
pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/torch_stable.html
```

## Running the AI

**Start the proxy server** (required first, launches a Chrome browser with mitmproxy):
```bash
python -m majsoul_wrapper
```

**Local AI mode**:
```bash
python main.py
```

**Remote AI mode** (run on server first):
```bash
python remote.py  # On server - listens on port 14782
python main.py --remote_ip SERVER_IP  # On client
```

**Auto-match mode** (continuous ranked play):
```bash
python main.py --level L  # L = 0-4 for Copper/Silver/Gold/Jade/ throne ranks
```

## Architecture

**main.py**: Main entry point containing:
- `State` enum: AI state machine (WaitingForStart, Playing)
- `CardRecorder`: Converts tile notation between Majsoul (`'0s'`) and Tenhou format (`tile136`/`tile34`)
- `AIWrapper` class: Protocol bridge between Majsoul websocket and Tenhou AI
  - Majsoul → Tenhou: Translates game events into Tenhou protocol messages
  - Tenhou → Majsoul: Translates AI decisions into mouse click actions
- `MainLoop()`: Orchestrates browser calibration, AI subprocess management, and event loop

**remote.py**: Reverse proxy for remote AI deployment. Listens on port 14782 and proxies data between client and local JianYangAI instance.

**Key port references**:
- `37247`: Majsoul RPC server (majsoul_wrapper)
- `7479`: Local AI server
- `14782`: Remote AI server

## Submodules

- **JianYangAI/**: Mahjong AI subprocess (Tenhou-compatible protocol)
- **majsoul_wrapper/**: Browser automation and game state extraction via mitmproxy

These are git submodules that must be initialized before running.