FROM python:3.11-slim

WORKDIR /home/ubuntu/deploy-projects/0d22562c88b4e00a2ad3aaef

# Install curl for healthcheck and adb for Android device control
RUN apt-get update && apt-get install -y curl android-sdk-platform-tools wget unzip && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose internal port
EXPOSE 7860

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["python", "demo.py"]