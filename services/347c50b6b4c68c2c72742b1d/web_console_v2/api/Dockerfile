FROM python:3.7-slim

# Install curl, wget and make for healthcheck and protobuf generation
RUN apt-get update && apt-get install -y curl wget make && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# Copy requirements and install dependencies
COPY requirements.txt .
# Pin compatible versions for Flask 1.1.x and older pyOpenSSL/cryptography
RUN pip install --no-cache-dir 'jinja2<3.1' 'itsdangerous<2.1' 'werkzeug<2.1' 'pyopenssl==20.0.1' 'cryptography<38.0' -r requirements.txt

# Copy application code
COPY . .

# Generate protobuf files
RUN make protobuf

# Create log directory
RUN mkdir -p /var/log/fedlearner_webconsole

# Expose the internal port
EXPOSE 1991

# Healthcheck - check if the server is responding (404 is acceptable)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:1991/api/v2/projects 2>/dev/null || wget -q --spider http://localhost:1991/ 2>/dev/null || exit 1

# Run database migrations and start the application
CMD FLASK_APP=command:app flask db upgrade && \
    FLASK_APP=command:app flask create-initial-data && \
    gunicorn server:app --config=gunicorn_config.py --bind 0.0.0.0:1991