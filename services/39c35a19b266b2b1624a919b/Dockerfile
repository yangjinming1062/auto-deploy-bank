FROM python:3.8-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=testshop.settings
ENV PYTHONPATH=/home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy all necessary files for package installation
COPY setup.py /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/
COPY README.md /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/
COPY LICENSE.txt /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/
COPY MANIFEST.in /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/
COPY tests/requirements.txt /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/requirements.txt
COPY tests/manage.py /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/manage.py
COPY shop/ /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/shop/
COPY email_auth/ /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/email_auth/
COPY tests/testshop/ /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/testshop/

# Install Python dependencies
RUN pip install --no-cache-dir setuptools && \
    pip install --no-cache-dir psycopg2-binary && \
    pip install --no-cache-dir -r /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/requirements.txt && \
    pip install --no-cache-dir -e .

# Copy remaining project files
COPY tests/ /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/tests/

# Create necessary directories
RUN mkdir -p /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/staticfiles /home/ubuntu/deploy-projects/39c35a19b266b2b1624a919b/media

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Expose port
EXPOSE 8000

# Start command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]