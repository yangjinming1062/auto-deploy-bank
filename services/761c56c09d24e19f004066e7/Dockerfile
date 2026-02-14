FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/761c56c09d24e19f004066e7

# Copy all source files first (needed for editable install)
COPY pyproject.toml .
COPY src/ ./src/
COPY README.md .
COPY LICENSE.txt .

# Install numpy with upper bound to avoid np.bool8 removal in numpy 2.0
RUN pip install --no-cache-dir "numpy<2.0"

# Install bokeh from PyPI
RUN pip install --no-cache-dir "bokeh>=3.0"

# Use CDN for resources to avoid static file issues
ENV BOKEH_RESOURCES="cdn"

# Install package in editable mode (overrides Python code, keeps static files)
RUN pip install --no-cache-dir -e .

# Expose internal port
EXPOSE 5006

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5006/ || exit 1

# Start Bokeh server
CMD ["bokeh", "serve", "--address", "0.0.0.0", "--port", "5006"]