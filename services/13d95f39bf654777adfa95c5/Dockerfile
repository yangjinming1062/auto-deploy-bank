FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl ffmpeg && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OPENCV_IO_ENABLE_OPENEXR=1

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/13d95f39bf654777adfa95c5

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir streamlit

# Copy application code
COPY . .

# Create required directories
RUN mkdir -p character_sheet results poses weights

# Expose port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start command
CMD ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.headless=true"]