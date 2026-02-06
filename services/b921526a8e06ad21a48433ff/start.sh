#!/bin/bash
# Startup script for Deep Snake training container

echo "================================================"
echo "Deep Snake Training Container"
echo "================================================"
echo "CUDA_HOME: ${CUDA_HOME:-not set}"
echo "FORCE_CUDA: ${FORCE_CUDA:-0}"
echo ""

# Check for CUDA/GPU support
echo "Checking system requirements..."
CUDA_AVAILABLE=false
if python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')" 2>&1 | grep -q "CUDA available: True"; then
    CUDA_AVAILABLE=true
    echo "GPU support: AVAILABLE"
else
    echo "GPU support: NOT AVAILABLE"
fi

# Check if DCN extensions can be imported
echo ""
echo "Checking CUDA extensions..."
DCN_AVAILABLE=false
if python -c "from lib.csrc.dcn_v2 import _ext; print('DCN v2 extension: OK')" 2>&1; then
    DCN_AVAILABLE=true
else
    echo "DCN v2 extension: NOT AVAILABLE (requires GPU compilation)"
fi

echo ""
echo "================================================"

# Start web server in background
echo "Starting web server on port 8080..."
python web_server.py &
WEB_SERVER_PID=$!

if [ "$CUDA_AVAILABLE" = false ] || [ "$DCN_AVAILABLE" = false ]; then
    echo "WARNING: GPU support is required for this application."
    echo ""
    echo "The Deep Snake training application requires:"
    echo "  1. A GPU with CUDA support"
    echo "  2. CUDA toolkit installed and configured"
    echo "  3. DCNv2 extensions compiled for your GPU"
    echo ""
    echo "Current environment is running in CPU-only mode."
    echo "Web server is running. Training cannot proceed without GPU."
    echo ""
    echo "To enable GPU support:"
    echo "  - Use a GPU-enabled host or container runtime (nvidia-docker)"
    echo "  - Install CUDA toolkit in the container"
    echo "  - Compile the DCNv2 extensions"
    echo ""
    echo "Web server running at http://0.0.0.0:8080"
    echo "================================================"

    # Wait for web server process
    wait $WEB_SERVER_PID
else
    echo "All requirements met. Starting training..."
    echo "================================================"
    exec python train_net.py "$@"
fi