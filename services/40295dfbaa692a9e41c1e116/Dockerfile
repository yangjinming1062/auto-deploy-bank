FROM python:3.9-slim

# Install curl for healthcheck and build tools for C++ extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        g++ \
        gcc \
        && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/40295dfbaa692a9e41c1e116

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install setuptools < 60.0 for numpy.distutils compatibility
RUN pip install --no-cache-dir 'setuptools<60.0'

# Install skmultiflow from local source
COPY setup.py README.md MANIFEST.in ./
COPY src/ src/
RUN python setup.py install

# Copy application code
COPY app.py .

# Expose internal port
EXPOSE 8080

# Start Flask application
CMD ["python", "app.py"]