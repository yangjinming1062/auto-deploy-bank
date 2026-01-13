FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["python", "-m", "g4f", "api", "--port", "8080"]