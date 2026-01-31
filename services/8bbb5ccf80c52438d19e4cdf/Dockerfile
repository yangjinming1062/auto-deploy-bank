FROM python:3.11-slim

# Install system dependencies including build tools for insightface and OpenCV
RUN apt-get update && apt-get install -y curl build-essential libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/8bbb5ccf80c52438d19e4cdf

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create models directory
RUN mkdir -p ./models

# Expose the Gradio port
EXPOSE 7860

# Start the application
CMD ["python", "app.py"]