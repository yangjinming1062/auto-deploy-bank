FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy and build svelte app
COPY svelte-app/package.json svelte-app/package-lock.json* /tmp/svelte-app/
WORKDIR /tmp/svelte-app
RUN npm install --include=dev

COPY svelte-app/src /tmp/svelte-app/src
COPY svelte-app/public /tmp/svelte-app/public
COPY svelte-app/rollup.config.js /tmp/svelte-app/
RUN /tmp/svelte-app/node_modules/.bin/rollup -c && mkdir -p /home/ubuntu/deploy-projects/67be57818b87a6a48a1e1b47/svelte-app/public/build && cp -r /tmp/svelte-app/public/* /home/ubuntu/deploy-projects/67be57818b87a6a48a1e1b47/svelte-app/public/

# Return to app directory
WORKDIR /home/ubuntu/deploy-projects/67be57818b87a6a48a1e1b47

# Copy application code
COPY . .

# Create directories for runtime
RUN mkdir -p projects VectorStore sessions

# Expose the port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "qa_pilot_run.py"]