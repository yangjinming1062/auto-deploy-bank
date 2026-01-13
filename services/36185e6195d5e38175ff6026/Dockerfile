FROM python:3.9-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/36185e6195d5e38175ff6026

# Install Flask and other common dependencies first (for better caching)
COPY requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt

# Copy all application code including papers
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["python", "app.py"]