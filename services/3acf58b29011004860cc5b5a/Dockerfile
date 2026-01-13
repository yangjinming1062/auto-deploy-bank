FROM python:3.10-slim

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set python unbuffered
ENV PYTHONUNBUFFERED=1

# Install uv
RUN pip install uv

# Copy dependency files and install dependencies
COPY requirements.txt ./
RUN uv pip install --no-cache-dir -r requirements.txt --system

# Copy the rest of the application
COPY . .

# Expose the internal port
EXPOSE 6185

# Command to run the application
CMD ["python", "main.py"]
