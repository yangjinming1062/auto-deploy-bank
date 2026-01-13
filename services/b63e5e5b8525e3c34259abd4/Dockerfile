# Use python:3.12-slim base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install curl for healthcheck and mysql client dependencies
RUN apt-get update && apt-get install -y curl default-libmysqlclient-dev pkg-config build-essential --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Cache deps
COPY requirements.txt .
COPY requirements.development.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements.development.txt mysqlclient


# Copy application code
COPY . .

# Copy config file
COPY bugsink/conf_templates/docker.py.template bugsink_conf.py

# Copy and set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Set default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers=10", "--access-logfile", "-", "bugsink.wsgi"]
