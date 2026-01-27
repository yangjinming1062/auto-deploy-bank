FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TOKENIZERS_PARALLELISM=false

# Install torch first (CPU version for compatibility)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy requirements and install remaining Python dependencies
COPY requirements.txt .

# Remove torch-related lines from requirements.txt (already installed)
RUN sed -i '/^torch\b/d' /app/requirements.txt
RUN sed -i '/^torchvision\b/d' /app/requirements.txt
RUN sed -i '/^pytorch_lightning\b/d' /app/requirements.txt

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pytorch-lightning separately with version compatible with torch
RUN pip install --no-cache-dir pytorch-lightning

# Copy project files
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]