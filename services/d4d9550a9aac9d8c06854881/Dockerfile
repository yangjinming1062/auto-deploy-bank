FROM python:3.9-slim

# Install curl, coreutils and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    curl \
    coreutils \
    libglx-mesa0 \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Use entrypoint for data validation
ENTRYPOINT ["/app/entrypoint.sh"]