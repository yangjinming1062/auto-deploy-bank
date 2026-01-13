FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    wget \
    libgmp-dev \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    libbz2-dev \
    libncurses5-dev \
    libgdbm-dev \
    liblzma-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir fastapi uvicorn

# Copy source code
COPY . .

# Install MindSpore from pip (official package)
# Note: For production builds from source, use the development Dockerfile in scripts/docker/
RUN pip install --no-cache-dir mindspore==2.0.0

# Downgrade Pillow to avoid compatibility issues with MindSpore
RUN pip uninstall -y pillow && pip install --no-cache-dir pillow==9.5.0

# Create a simple FastAPI app to demonstrate MindSpore
RUN echo 'from fastapi import FastAPI\n\
import mindspore as ms\n\
import numpy as np\n\
\n\
app = FastAPI()\n\
\n\
@app.get("/")\n\
async def root():\n\
    return {"message": "MindSpore API", "version": ms.__version__}\n\
\n\
@app.get("/health")\n\
async def health_check():\n\
    return {"status": "healthy"}\n\
\n\
@app.get("/test")\n\
async def test_mindspore():\n\
    try:\n\
        # Initialize MindSpore context\n\
        ms.context.set_context(device_target="CPU")\n\
        # Create a simple tensor\n\
        x = ms.Tensor(np.array([1, 2, 3], dtype=np.float32))\n\
        return {"result": x.asnumpy().tolist()}\n\
    except Exception as e:\n\
        return {"error": str(e)}\n\
\n\
if __name__ == "__main__":\n\
    import uvicorn\n\
    uvicorn.run(app, host="0.0.0.0", port=8080)\n\
' > /app/api_server.py

# Expose internal port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start the service
CMD ["python", "api_server.py"]