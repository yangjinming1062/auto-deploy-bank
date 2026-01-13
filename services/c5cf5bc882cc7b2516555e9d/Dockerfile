FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml /app/
RUN pip install --no-cache-dir \
    "gradio>=4.0,<6.0" \
    "aiortc" \
    "aioice>=0.10.1" \
    "librosa" \
    "numpy" \
    "numba>=0.60.0" \
    "fastapi" \
    "uvicorn[standard]" \
    "python-dotenv" \
    "elevenlabs" \
    "groq" \
    "onnxruntime>=1.20.1" \
    "fastrtc-moonshine-onnx"

# Copy application code
COPY . /app/

# Install fastrtc package in development mode with STT support
RUN pip install -e .[stt]

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SSR_MODE=false
ENV MODE=UI

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start command
CMD ["uvicorn", "demo.llm_voice_chat.app:app", "--host", "0.0.0.0", "--port", "8000"]