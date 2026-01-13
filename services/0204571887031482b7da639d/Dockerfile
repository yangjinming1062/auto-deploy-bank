FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# Install necessary packages including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the files from the host to the container
COPY . .

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["gunicorn", "-w", "2", "-b", ":8000", "app:app"]
