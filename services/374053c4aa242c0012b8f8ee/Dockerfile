FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install docsify-cli globally
RUN npm install -g docsify-cli@latest

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN grep -E -v "^(pywin32|pywinpty|torch|torchvision|torchaudio)" requirements.txt > requirements_linux.txt && \
    pip install --no-cache-dir -r requirements_linux.txt && \
    pip install --no-cache-dir torch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1

# Copy source code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=40323

# Expose port
EXPOSE 40323

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:40323 || exit 1

# Start docsify server
CMD ["docsify", "serve", "docs", "--port", "40323"]
