FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/c26b5406a66c2f84b5788b4d

# Create logs directory
RUN mkdir -p logs

# Copy requirements and necessary files for installation
COPY requirements.txt setup.py ./
COPY flaskbb/ ./flaskbb/
COPY wsgi.py wsgi-wrapper.py celery_worker.py create_admin_user.py entrypoint.sh ./
# Install FlaskBB in editable mode to enable CLI commands
RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir -r requirements.txt

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose internal port
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "wsgi:flaskbb"]