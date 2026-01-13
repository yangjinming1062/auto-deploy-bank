# ML Tutorial Repository - Jupyter Notebook Server
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies (using minimal set for compatibility)
COPY requirements-minimal.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire repository
COPY . .

# Expose internal port 8888 for Jupyter
EXPOSE 8888

# Start Jupyter notebook server
# Allow remote access and disable token for simplicity
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
