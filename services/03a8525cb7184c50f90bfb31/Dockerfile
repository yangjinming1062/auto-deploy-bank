FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_TEMP_DIR=.gradio_cache
ENV TOKENIZERS_PARALLELISM=false

# Install curl for healthcheck and protobuf for tiktoken
# Also install mesa packages for trimesh/opencv headless rendering
RUN apt-get update && apt-get install -y \
    curl \
    protobuf-compiler \
    libprotobuf-dev \
    libgl1 \
    libgl1-mesa-dri \
    libosmesa6 \
    libxkbcommon0 \
    libxmu6 \
    libxi6 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/03a8525cb7184c50f90bfb31

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY scripts/ ./scripts/
COPY aether/ ./aether/
COPY .project-root ./.project-root
# Copy assets if exists
RUN if [ -d "assets" ]; then cp -r assets/ ./assets/; fi

# Create necessary directories
RUN mkdir -p .gradio_cache outputs temp_frames_*

# Expose the Gradio port
EXPOSE 7860

# Run the Gradio application
CMD ["python", "scripts/demo_gradio.py"]