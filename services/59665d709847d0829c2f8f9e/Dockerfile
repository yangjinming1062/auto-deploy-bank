FROM python:3.11-slim

LABEL name="httpbin"
LABEL version="0.9.2"
LABEL description="A simple HTTP service."
LABEL org.kennethreitz.vendor="Kenneth Reitz"

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /httpbin

# Copy setup.py first for better caching
COPY setup.py .

# Copy application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir gunicorn gevent && \
    pip install --no-cache-dir .

# Expose port 80
EXPOSE 80

# Start the application
CMD ["gunicorn", "-b", "0.0.0.0:80", "httpbin:app", "-k", "gevent"]