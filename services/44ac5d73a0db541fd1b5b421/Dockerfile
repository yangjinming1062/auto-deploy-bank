FROM python:3.10-slim

# Install system dependencies including ADB
RUN apt-get update && apt-get install -y \
    android-tools-adb \
    android-tools-fastboot \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PHONE_AGENT_BASE_URL=http://localhost:8000/v1
ENV PHONE_AGENT_MODEL=autoglm-phone-9b
ENV PHONE_AGENT_API_KEY=EMPTY
ENV PHONE_AGENT_MAX_STEPS=100
ENV PHONE_AGENT_LANG=cn

# Default command - shows help/usage
CMD ["python", "main.py", "--help"]