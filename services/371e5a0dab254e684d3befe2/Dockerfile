FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/371e5a0dab254e684d3befe2

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# No additional dependencies needed - this is a simple HTTP server
# The font build dependencies (requirements.txt) are not needed for the web service

# Copy application code
COPY app.py .

# Expose the internal port
EXPOSE 8080

# Run the HTTP server
CMD ["python", "app.py"]