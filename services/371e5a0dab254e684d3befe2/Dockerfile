FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install system dependencies including ttfautohint and build tools
RUN apt-get update && apt-get install -y \
    ttfautohint \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Default command runs entrypoint script
CMD ["./entrypoint.sh"]