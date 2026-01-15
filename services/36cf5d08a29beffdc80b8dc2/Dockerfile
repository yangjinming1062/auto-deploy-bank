FROM python:3.12-slim

# Install GEOS library and build tools (required for basemap)
RUN apt-get update && apt-get install -y \
    libgeos-c1t64 \
    libgeos-dev \
    gcc \
    g++ \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GEOS_DIR=/usr
ENV MPLBACKEND=Agg

# Copy requirements first for better caching
COPY dep/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Flask for web service
RUN pip install --no-cache-dir flask

# Copy the rest of the application
COPY . .

# Build and install basemap from source
RUN python -m pip install .

# Expose port
EXPOSE 8000

CMD ["python", "app.py"]