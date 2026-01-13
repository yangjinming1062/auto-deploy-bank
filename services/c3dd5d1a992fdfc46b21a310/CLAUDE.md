# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lucida is a speech and vision-based intelligent personal assistant with a microservices architecture. Multiple services communicate via Thrift RPC, orchestrated by a central Command Center that uses query classification to determine which services to invoke based on user input.

## Architecture

### High-Level Structure

- **lucida/**: Backend services and Command Center (CMD)
  - **commandcenter/**: Main orchestrator (Python/Flask)
  - Service implementations (C++, Java, Python)
    - IMM (Image Matching) - OpenCV C++
    - QA (Question Answering) - Java/OpenEphyra
    - CA (Calendar Assistant) - Java
    - IMC (Image Classification) - C++
    - FACE (Facial Recognition) - C++
    - DIG (Digit Recognition) - C++
    - WE (Weather) - Python
    - MS (Music Service) - Python
- **tools/**: Shared dependencies (OpenCV, Thrift, MongoDB, etc.)

### Service Communication

Services communicate using Apache Thrift (Python/Java) and Facebook Thrift (C++):

- **Core Thrift Interface** (`lucida/lucidaservice.thrift`):
  ```thrift
  service LucidaService {
     void create(1:string LUCID, 2:lucidatypes.QuerySpec spec);
     void learn(1:string LUCID, 2:lucidatypes.QuerySpec knowledge);
     string infer(1:string LUCID, 2:lucidatypes.QuerySpec query);
  }
  ```

- **Data Types** (`lucida/lucidatypes.thrift`):
  - QuerySpec: Contains service graph configuration
  - QueryInput: Individual node with type/data/tags

### Service Graph System

The Command Center uses a query classifier to determine service workflows:
- Each service is defined in `lucida/commandcenter/controllers/Config.py`
- Service graphs are DAGs (Directed Acyclic Graphs) of service nodes
- Example: Image query → IMM → QA
- Ports configured in `lucida/config.properties`

## Common Commands

### Development Setup

```bash
# Install all dependencies and build services
make local

# Start all services in tmux windows
make start_all

# Start in secure mode (HTTPS/WSS)
make start_all_secure

# Start test services only
make start_test_all

# Clean build artifacts
make clean_all_tools
make clean_all_service
```

### Individual Service Control

```bash
# Build all services
cd lucida && make all

# Start specific service (from its directory)
cd lucida/imagematching/opencv_imm && make start_server
cd lucida/commandcenter && make start_server
cd lucida/calendar && make start_server
```

### Docker Deployment

```bash
# Build Docker image
docker build -t lucida:latest .

# Deploy to Kubernetes (follow tools/deploy/ instructions)
cd tools/deploy
```

## Service Implementation Guide

### Adding a New Service

1. **Implement Thrift Interface**:
   - Define handlers in `lucida/<service>/` following existing patterns
   - Use C++ (Facebook Thrift):参照 `lucida/imagematching/opencv_imm/`
   - Use Java (Apache Thrift):参照 `lucida/calendar/`
   - Use Python:参照 existing Python services

2. **Update Configuration** (`lucida/commandcenter/controllers/Config.py`):
   ```python
   SERVICES = {
     'NEW_SERVICE': Service('NEW_SERVICE', <PORT>, 'text', 'text')
   }

   CLASSIFIER_DESCRIPTIONS = {
     'text': {
       'class_NEW': Graph([Node('NEW_SERVICE')])
     }
   }
   ```

3. **Update Build Files**:
   - Add to `lucida/Makefile` SUBDIRS
   - Add start commands to `tools/start_all_tmux.sh`

4. **Add Training Data** (optional):
   - Create `lucida/commandcenter/data/class_<NAME>.txt`

### Service Port Configuration

Edit `lucida/config.properties`:
```
CMD_PORT=8081
QA_PORT=8082
IMM_PORT=8083
CA_PORT=8084
IMC_PORT=8085
FACE_PORT=8086
DIG_PORT=8087
WE_PORT=8088
MS_PORT=8089
```

## Key Files and Directories

### Core Configuration
- `lucida/commandcenter/controllers/Config.py` - Service orchestration config
- `lucida/config.properties` - Port mappings
- `lucida/lucidaservice.thrift` - Core service interface
- `lucida/lucidatypes.thrift` - Data structures

### Build System
- `Makefile` - Top-level build commands
- `Makefile.common` - Shared build configuration
- `tools/Makefile` - Dependencies installation
- Individual service `Makefile`s - Service-specific builds

### Services (lucida/)
- `commandcenter/` - Flask web app, query classifier, workflow orchestration
- `imagematching/opencv_imm/` - Image matching with OpenCV
- `questionanswering/OpenEphyra/` - QA with OpenEphyra
- `calendar/` - Calendar service
- `djinntonic/` - Image classification, face/digit recognition (C++)

### Dependencies (tools/)
- `install_python.sh` - Python 2.7.9 + packages
- `install_opencv.sh` - OpenCV
- `install_thrift.sh` - Apache Thrift 0.9.3
- `install_fbthrift.sh` - Facebook Thrift
- `install_mongodb.sh` - MongoDB + C++ driver

## Testing and Development

- Each service has test clients (e.g., `lucida/imagematching/opencv_imm/test/IMMClient.cpp`)
- Web interface: http://localhost:3000/
- Access tmux session: `tmux a -t lucida`
- Test data: `lucida/commandcenter/data/`

## Environment Requirements

- Ubuntu 14.04/16.04 (gcc 4.8.4 required)
- Python 2.7.9 (virtualenv)
- Java 8
- MongoDB
- LD_LIBRARY_PATH=/usr/local/lib

## Important Notes

1. **Thrift Order**: Install Apache Thrift before Facebook Thrift
2. **GCC Version**: Use gcc 4.8.4 (MongoDB C++ driver fails on newer versions)
3. **Ubuntu 16.04**: Modify `tools/python_requirements.txt` (set pyOpenSSL==0.14)
4. **ASR Service**: Uses kaldi gstreamer server (not in standard SERVICES config)
5. **Workflow System**: Command center supports stateful workflows via workFlow classes