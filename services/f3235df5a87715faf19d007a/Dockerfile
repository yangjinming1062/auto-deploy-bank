FROM python:3.10-slim

# Install curl, git, and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/f3235df5a87715faf19d007a

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 8080

# Run the Gradio application
CMD ["python", "app.py", "--port", "8080"]