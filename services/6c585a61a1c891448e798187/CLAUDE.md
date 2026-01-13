# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AIAS (AI Application Suite) is a comprehensive AI platform providing:

- **1_sdks**: Reusable SDKs for image processing, NLP, audio, video, and big data
- **2_training_platform**: Java-based training platform for custom image classification models
- **3_api_platform**: Spring Boot API platform with Vue frontend offering ready-to-use AI capabilities (OCR, translation, ASR, image enhancement, etc.)
- **4_web_app**: Domain-specific web applications (face search, image search, image generation, etc.)
- **5_desktop_app**: Desktop applications for OCR, image upscaling, and LLM

## Common Commands

### Backend (Java/Spring Boot)

All Java modules use Maven and Spring Boot 2.1.9:

```bash
# Build and package
mvn clean package -DskipTests

# Install dependencies
mvn clean install

# Run tests
mvn test

# Run a specific module (replace with actual jar name)
java -Dfile.encoding=utf-8 -jar path/to/module/target/module-name.jar

# Example for API platform
cd 3_api_platform/api-platform
mvn clean package
java -Dfile.encoding=utf-8 -jar target/api-platform-0.23.0.jar
```

### Frontend (Vue.js)

Frontend applications use Vue 2.x, Element UI, and npm:

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build:prod

# Staging build
npm run build:stage

# Lint code
npm run lint

# Run unit tests
npm run test:unit

# CI test (lint + unit tests)
npm run test:ci
```

### Model Management

Models are downloaded separately from Baidu Pan links (see individual README files). Configure model paths in `src/main/resources/application.yml`:

```yaml
# Select environment profile
spring:
  profiles:
    active: win  # win | mac | linux | online

model:
  # Non-generation models path
  modelPath: D:\\path\\to\\models\\

  # Image generation models (AIGC)
  sd:
    cpuModelPath: H:\\path\\to\\aigc\\sd_cpu\\
    gpuModelPath: H:\\path\\to\\aigc\\sd_gpu\\

  # Device type (cpu | gpu)
  device: gpu
```

**Important**: Image generation models (62GB+) use lazy loading - they load on first use. GPU requires 4GB+ VRAM per feature; CPU mode works but is significantly slower.

## Architecture

### Technology Stack

- **Backend**: Java 8+, Spring Boot 2.1.9, Maven
- **ML Framework**: DJL (Deep Java Library) 0.23.0, Deeplearning4j, ND4J
- **Model Engines**: PyTorch, ONNX Runtime
- **Frontend**: Vue 2.6, Element UI 2.13, Vue CLI 4.x
- **Image Processing**: OpenCV (via DJL)
- **Build Tools**: Maven (backend), npm (frontend)

### Key Modules

#### 1. API Platform (`3_api_platform/api-platform`)

Spring Boot REST API providing AI capabilities:

- Main class: `top.aias.platform.MainApplication`
- Controllers in: `src/main/java/top/aias/platform/controller/`
- Services in: `src/main/java/top/aias/platform/service/`
- Configuration in: `src/main/java/top/aias/platform/config/`

Key capabilities: OCR, translation, ASR, image segmentation, super-resolution, face restoration, image generation (via ControlNet).

#### 2. Training Platform (`2_training_platform/train-platform`)

Custom model training platform:

- Main class: `top.aias.training.MainApplication`
- Uses Deeplearning4j with ND4J backend
- Supports CPU/GPU via ND4J backend configuration
- Features: model training, visualization, inference, feature extraction

#### 3. SDKs (`1_sdks`)

Reusable SDKs organized by domain:
- `1_image_sdks`: OCR, classification, detection, segmentation
- `2_nlp_sdks`: Sentence encoding, translation, tokenization
- `3_audio_sdks`: ASR, TTS, voice cloning
- `4_video_sdks`: Video analysis
- `5_bigdata_sdks`: Kafka/Flink integration
- `6_aigc`: Image generation

### Configuration Files

- **Backend**: `application.yml` with profile-specific configs (`application-win.yml`, `application-linux.yml`, etc.)
- **Frontend**: `package.json` with scripts and dependencies
- **Maven**: Standard `pom.xml` with Spring Boot parent

### Port Configuration

- API Platform: `http://localhost:8089`
- Training Platform: `http://localhost:8090`
- Frontend dev servers: `http://localhost:8080` (varies by app)

## Development Notes

### Backend Development

1. All Java modules follow Spring Boot conventions
2. Model loading is managed via DJL's model zoo
3. Profile-based configuration for different environments (win/mac/linux/online)
4. CORS configuration required for frontend communication
5. Use `-Dfile.encoding=utf-8` when running JARs to avoid encoding issues

### Frontend Development

1. Vue 2.x with Element UI components
2. Axios for API communication
3. Vuex for state management
4. ESLint configuration for code quality
5. Jest for unit testing

### Model Dependencies

1. **Non-generation models**: ~8.2GB (OCR, translation, ASR, etc.)
2. **Image generation models**: ~62GB (optional, lazy-loaded)
3. Model download links provided in each module's README
4. CPU/GPU auto-detection with manual override via configuration

### Common Tasks

#### Adding a New API Endpoint

1. Create controller in `src/main/java/top/aias/platform/controller/`
2. Add service logic in service layer
3. Configure Swagger documentation if needed
4. Update frontend to consume the API

#### Running a Single Test

```bash
# Maven
mvn test -Dtest=ClassName#methodName

# Frontend (Jest)
npm run test:unit -- --testNamePattern="test name"
```

#### Building for Production

```bash
# Backend
cd module-name
mvn clean package -DskipTests
# Deploy target/module-name-version.jar

# Frontend
cd frontend-app
npm run build:prod
# Deploy dist/ directory to web server
```

## Documentation

- Main README: Root level with project overview
- Module READMEs: Individual READMEs in each module directory
- Model downloads: Baidu Pan links in each module's README
- Documentation: `0_docs/` contains tutorials and FAQ

## Dependencies and Compatibility

- **JDK**: 1.8+ (recommended: JDK 11)
- **Node.js**: >=8.9 for frontend
- **GPU**: CUDA 11.x/12.x for optimal image generation performance
- **Memory**: 8GB+ RAM for basic operation, 24GB+ VRAM for all image generation features
- **OS**: Windows x64, Linux x64, macOS x64 (CPU); Windows x64, Linux x64 (GPU)