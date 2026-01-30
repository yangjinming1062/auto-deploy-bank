FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/home/ubuntu/deploy-projects/aba058e690d69492fdde366c/hf_model

# Install system dependencies for OpenCV and other packages
RUN apt-get update && apt-get install -y \
    curl \
    libxcb1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libfontconfig1 \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/aba058e690d69492fdde366c

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install FastAPI and uvicorn for web service
RUN pip install --no-cache-dir fastapi uvicorn python-multipart

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]