FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/8ff2525ba39659bfb5cfc963

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest

# Copy project and install in editable mode
COPY . .
RUN pip install -e .

# Run the Flask web server
CMD ["python", "app.py"]