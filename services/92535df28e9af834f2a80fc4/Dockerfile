FROM python:3.9-slim
LABEL GeoNode development team

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=geonode.settings
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV ALLOWED_HOSTS=*

RUN mkdir -p /usr/src/geonode

# Install git first (needed for cloning repos)
RUN apt-get update -y && apt-get install -y git

# This section is borrowed from the official Django image but adds GDAL and others
RUN apt-get update -y && apt-get upgrade -y

# Preparing dependencies - include all required system libraries
RUN apt-get install -y \
    libgdal-dev \
    libpq-dev \
    libxml2-dev \
    libxml2 \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libmemcached-dev \
    libldap2-dev \
    libsasl2-dev \
    libffi-dev \
    curl \
    git \
    # Additional libraries for Python packages
    libssl-dev \
    libcrypto++-dev

RUN apt-get install -y --no-install-recommends \
    gcc \
    zip \
    gettext \
    geoip-bin \
    cron \
    postgresql-client \
    sqlite3 \
    spatialite-bin \
    libsqlite3-mod-spatialite \
    python3-dev \
    python3-psycopg2 \
    python3-ldap \
    python3-pip \
    python3-pil \
    python3-lxml \
    python3-pylibmc \
    uwsgi \
    uwsgi-plugin-python3 \
    firefox-esr \
    memcached \
    netcat-openbsd

RUN apt-get install -y devscripts build-essential debhelper pkg-kde-tools sharutils

# Fix setuptools version issue early - use 60.x which has convert_path for old packages
RUN pip install --no-cache-dir "setuptools==60.9.0" --force-reinstall

# Install core pip packages first
RUN pip install --no-cache-dir \
    pip==22.2.2 \
    invoke==1.5.0 \
    docker==4.4.4 \
    dj-database-url \
    schema \
    pyyaml

# Copy requirements first for better layer caching
COPY requirements.txt /tmp/requirements.txt

# Install main requirements
RUN pip install --no-cache-dir --src /usr/src \
    -r /tmp/requirements.txt || pip install --no-cache-dir -r /tmp/requirements.txt

# Copy project files
COPY . /usr/src/geonode/
WORKDIR /usr/src/geonode

# Copy and configure supporting files
COPY monitoring-cron /etc/cron.d/monitoring-cron
RUN chmod 0644 /etc/cron.d/monitoring-cron
RUN crontab /etc/cron.d/monitoring-cron
RUN touch /var/log/cron.log

COPY wait-for-databases.sh /usr/bin/wait-for-databases
RUN chmod +x /usr/bin/wait-for-databases

RUN chmod +x /usr/src/geonode/tasks.py
RUN chmod +x /usr/src/geonode/entrypoint.sh

COPY celery.sh /usr/bin/celery-commands
RUN chmod +x /usr/bin/celery-commands

COPY celery-cmd /usr/bin/celery-cmd
RUN chmod +x /usr/bin/celery-cmd

# Ensure log directory exists
RUN mkdir -p /var/log && touch /var/log/geonode.log

# Cleanup apt update lists
RUN rm -rf /var/lib/apt/lists/*

# Export ports
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Set entrypoint
ENTRYPOINT ["/usr/src/geonode/entrypoint.sh"]