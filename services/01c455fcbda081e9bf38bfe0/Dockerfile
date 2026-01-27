FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install curl, build tools, and SuiteSparse for scikit-sparse
RUN apt-get update && apt-get install -y curl gcc g++ build-essential libsuitesparse-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/01c455fcbda081e9bf38bfe0

# Copy requirements
COPY requirements.txt .

# Install torch and torchvision first (theseus-ai requires torch)
RUN pip install --no-cache-dir torch torchvision

# Install pytorch3d from official wheels
RUN pip install --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt210/download.html

# Install remaining dependencies (excluding torch/torchvision to avoid conflicts)
RUN sed '/^torch\d*==/d; /^torchvision==/d; /^pytorch3d$/d' requirements.txt > requirements_no_torch.txt && \
    pip install --no-cache-dir -r requirements_no_torch.txt

# Copy application code
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Expose the web server port
EXPOSE 8080

# Default command - run the web server
CMD ["python", "web_server.py"]