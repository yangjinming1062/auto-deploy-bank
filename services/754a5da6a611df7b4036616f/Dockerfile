FROM python:3.7-slim

# Install curl and git for healthcheck and pip git dependencies
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    JUPYTER_BASE_URL=/ \
    JUPYTER_ALLOW_INSECURE_WRITERS=true

WORKDIR /home/ubuntu/deploy-projects/754a5da6a611df7b4036616f

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose JupyterLab port
EXPOSE 8888

# Start JupyterLab
CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--allow-root", "--no-browser"]