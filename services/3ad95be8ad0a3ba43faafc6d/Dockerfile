FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install curl, Tkinter, and OpenGL dependencies for GUI automation
RUN apt-get update && apt-get install -y curl tk libtk8.6 libglx-mesa0 libglib2.0-0 mesa-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/3ad95be8ad0a3ba43faafc6d

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY lackey/ ./lackey/
COPY setup.py .
COPY web_server.py .

# Install the package
RUN pip install --no-cache-dir -e .

# Default command - run the web server
CMD ["python", "/home/ubuntu/deploy-projects/3ad95be8ad0a3ba43faafc6d/web_server.py"]