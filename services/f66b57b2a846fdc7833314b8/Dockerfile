FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/f66b57b2a846fdc7833314b8

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install visualization extras for Flask-based monitoring
RUN pip install --no-cache-dir Flask flask_sqlalchemy pydot networkx pandas plotly

# Copy application and install package
COPY setup.py .
COPY parsl/ ./parsl/
RUN pip install --no-cache-dir -e .

# Create directory for monitoring database
RUN mkdir -p /home/ubuntu/deploy-projects/f66b57b2a846fdc7833314b8/runinfo

# Expose the visualization port
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Default command runs the visualization server with a valid database path
CMD ["parsl-visualize", "sqlite:////home/ubuntu/deploy-projects/f66b57b2a846fdc7833314b8/runinfo/monitoring.db", "-p", "8080", "-l", "0.0.0.0"]