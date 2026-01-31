FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/078757de8fa3338c182e0ffc

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 7860

# Run the application
CMD ["python", "app.py", "--server_name", "0.0.0.0", "--server_port", "7860"]