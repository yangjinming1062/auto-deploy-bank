# Use a base image with Python3.9 and Nodejs20 slim version
FROM nikolaik/python-nodejs:python3.9-nodejs20-slim

# Install Debian software needed by MetaGPT and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Mermaid CLI globally
RUN npm install -g @mermaid-js/mermaid-cli && npm cache clean --force

WORKDIR /app

# Set environment variables for non-secret values
ENV PYTHONUNBUFFERED=1
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Copy dependency definition files
COPY requirements.txt setup.py ./

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the application in editable mode and the specific dependencies for the web service
RUN pip install -e . && pip install "connexion[uvicorn]~=3.0.5"

# The internal port the example web service will run on
EXPOSE 8080

# Run the example OpenAPI web service to have a running service
CMD ["uvicorn", "metagpt.tools.openapi_v3_hello:app", "--host", "0.0.0.0", "--port", "8080"]
