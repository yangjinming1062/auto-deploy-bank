FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libxinerama1 \
    libxcursor1 \
    libxi6 \
    curl \
    wget \
    make \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU version first
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
# Remove torch/torchvision from requirements and install separately
RUN grep -v -E "^(torch|torchvision|torchaudio)$" requirements.txt > requirements_no_torch.txt
RUN pip install --no-cache-dir -r requirements_no_torch.txt

COPY . .

# Create model directories
RUN mkdir -p weights/icon_detect_v1_5 \
    && mkdir -p weights/icon_caption_florence

EXPOSE 8000

CMD ["uvicorn", "omni:app", "--host", "0.0.0.0", "--port", "8000"]