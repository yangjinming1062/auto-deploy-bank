# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FINN is an open-source framework for fast, scalable quantized neural network inference on FPGAs. It transforms quantized ONNX models into dataflow-style FPGA accelerators that generate highly efficient, high-throughput, low-latency implementations.

**Key Architecture**: The toolflow uses a series of model transformations and analysis passes to progressively transform an ONNX model into FPGA-ready hardware. The build process is orchestrated by `build_dataflow_steps.py` which defines a sequence of transformation steps.

## Development Environment

FINN requires complex tool dependencies (Vivado, Vitis, XRT) and is **designed to run in Docker only**. See `run-docker.sh` for the standard development environment setup.

Required environment variables for full functionality:
- `FINN_XILINX_PATH`: Path to Xilinx tools installation (e.g., `/opt/Xilinx`)
- `FINN_XILINX_VERSION`: Xilinx tools version (e.g., `2022.2`)
- `PLATFORM_REPO_PATHS`: Path to Vitis platform files for Alveo cards

## Build and Test Commands

```bash
# Install development dependencies
pip install -e ".[testing]"

# Run all tests (primary method - Docker-based)
./run-docker.sh quicktest

# Run pytest directly
pytest tests/

# Run a single test file
pytest tests/transformation/test_qonnx_to_finn.py

# Run tests by marker (see setup.cfg for full list)
pytest -m "util" tests/           # Utility function tests
pytest -m "transform" tests/      # Transformation tests
pytest -m "fpgadataflow" tests/   # FPGA dataflow tests
pytest -m "end2end" tests/        # End-to-end flow tests
pytest -m "brevitas_export" tests/# Brevitas export tests
pytest -m "not slow" tests/       # Exclude slow tests

# Run pre-commit hooks
pre-commit run --all-files

# Install pre-commit hooks
pre-commit install
```

## Code Style

FINN uses:
- **black** with line length 100
- **isort** for import sorting
- **flake8** with E203 ignored

All Python code must pass pre-commit hooks before committing.

## Repository Structure

```
src/finn/
├── builder/           # Build orchestration (build_dataflow.py, steps)
├── transformation/    # Model transformation passes
│   ├── fpgadataflow/ # FPGA-specific transformations
│   ├── qonnx/        # QONNX-to-FINN dialect conversion
│   └── streamline/   # Model streamlining passes
├── custom_op/        # Custom ONNX operations
│   └── fpgadataflow/ # HLS/RTL implementations (matrixvectoractivation, thresholding, etc.)
├── analysis/         # Model analysis (resource/cycle estimation)
├── core/             # Execution engines (rtlsim_exec, onnx_exec)
└── util/             # Utilities

finn-rtllib/          # Verilog RTL IP library components
docker/               # Docker build environment
tests/
├── transformation/
├── fpgadataflow/
├── brevitas/         # Brevitas export tests
└── end2end/
```

## Key Architectural Concepts

### Transformation Pattern
All transformations inherit from `qonnx.transformation.base.Transformation` and implement an `apply(self, model)` method that returns the transformed model. Examples in `src/finn/transformation/qonnx/`.

### Dependency Chain
The toolflow supports two input paths:
1. **QONNX-based flow**: Brevitas → ONNX → QONNX transformations → FINN transformations
2. **Standard flow**: ONNX → Streamlining → FPGA dataflow → HLS → Bitstream

### Custom Op Implementation
FPGA dataflow custom ops inherit from `HWCustomOp` (extends `qonnx.custom_op.base.CustomOp`) and define:
- `get_nodeattr_types()`: Declares attributes (FIFO depths, folding factors, etc.)
- `code_gen_*()` methods: Generate HLS/Verilog code
- `execute_*()` methods: Simulation execution

**Key hardware layer implementations** (`src/finn/custom_op/fpgadataflow/`):
- `VectorVectorActivation`: Matrix-vector/matrix-matrix multiplication
- `Thresholding`: Binarized/thresholded activation layers
- `ConvolutionInputGenerator`: Sliding window generation for convolutions
- `StreamingDataFlowPartition`: Model partitioning across IPs
- `StreamingFIFO`: Data buffering between layers
- `AddStreams`: Element-wise addition
- `StreamingMaxPool`/`Pool`: Max/average pooling
- `GlobalAccPool`: Global pooling accumulator

### Build Steps
The standard build flow (see `default_build_dataflow_steps` in `build_dataflow_config.py`):
1. `step_qonnx_to_finn`: Convert QONNX dialect to FINN dialect
2. `step_tidy_up`: Clean up model structure
3. `step_streamline`: Optimize and fuse operations
4. `step_convert_to_hw`: Convert to hardware nodes
5. `step_create_dataflow_partition`: Partition for FPGA
6. `step_specialize_layers`: Hardware specialization
7. `step_target_fps_parallelization`: Set folding/parallelization
8. `step_apply_folding_config`: Configure implementation
9. `step_generate_estimate_reports`: Resource estimation
10. `step_hw_codegen`: Generate HLS/Verilog code
11. `step_set_fifo_depths`: Size FIFOs for timing
12. `step_create_stitched_ip`: Integrate IPs with Vivado/Vitis
13. `step_synthesize_bitfile`: Generate bitstream (optional)

## Docker Configuration

FINN uses Docker as its primary development environment. Key images:
- Base image: Ubuntu 22.04 with Verilator 4.224 and XRT
- Published as `maltanar/finn:dev_latest` on DockerHub
- Build scripts: `docker/Dockerfile.finn`, `run-docker.sh`

## Contribution Guidelines

- Pull requests: target `dev` branch, not `main`
- All commits require a Signed-off-by line (DCO)
- New functionality requires unit tests
- Use pre-commit hooks before submitting